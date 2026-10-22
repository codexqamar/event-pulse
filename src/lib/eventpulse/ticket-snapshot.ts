export type TicketPageSnapshot = {
  status: "available" | "monitoring" | "captcha" | "limited";
  summary: string;
};

type SnapshotInput = {
  html: string;
  statusCode: number;
  responseOk: boolean;
  sectionFilters: string[];
  maxPrice: number | null;
  normalTicketsOnly: boolean;
};

const SIGNALS = [
  ["low availability", "low availability"],
  ["limited availability", "limited availability"],
  ["on sale", "on sale"],
  ["presale", "presale"],
  ["resale", "resale"],
  ["standard ticket", "standard"],
  ["general admission", "general admission"],
  ["official platinum", "official platinum"],
  ["hospitality", "hospitality"],
  ["standing", "standing"],
  ["seated", "seated"],
  ["restricted view", "restricted view"],
  ["face value", "face value"],
  ["fees included", "fees included"],
  ["accessible", "accessible"],
  ["vip", "VIP"],
] as const;

const POSITIVE_SIGNALS = [
  "tickets available",
  "buy tickets",
  "resale ticket",
  "select seats",
  "available now",
  "on sale",
];

const NEGATIVE_SIGNALS = [
  "sold out",
  "no tickets available",
  "currently unavailable",
  "not currently available",
  "tickets are not available",
];

export function extractTicketPageSnapshot(input: SnapshotInput): TicketPageSnapshot {
  const text = decodeHtml(input.html)
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  const lower = text.toLowerCase();
  const pageTitle = extractPageTitle(input.html);
  const prices = extractPrices(text);
  const matchedSections = input.sectionFilters.filter((section) =>
    lower.includes(section.trim().toLowerCase()),
  );
  const sections = extractSections(lower, matchedSections);
  const signals = SIGNALS.filter(([needle]) => lower.includes(needle)).map(([, label]) => label);
  const quantities = extractQuantities(lower);
  const captcha = lower.includes("captcha") || lower.includes("verify you are human");
  const blocked = input.statusCode === 403 || input.statusCode === 429;
  const positive = POSITIVE_SIGNALS.some((needle) => lower.includes(needle));
  const negative = NEGATIVE_SIGNALS.some((needle) => lower.includes(needle));
  const sectionMatch = input.sectionFilters.length === 0 || matchedSections.length > 0;
  const priceMatch =
    input.maxPrice == null ||
    (prices.length > 0 && prices.some((price) => price.value <= input.maxPrice!));
  const normalTicketMatch =
    !input.normalTicketsOnly || !signals.includes("resale") || signals.includes("standard");
  const filterMatch = sectionMatch && priceMatch && normalTicketMatch;

  let status: TicketPageSnapshot["status"] = "monitoring";
  let state = "No matching inventory";
  if (blocked) {
    status = "limited";
    state = input.statusCode === 429 ? "Rate limited" : "Access blocked";
  } else if (captcha) {
    status = "captcha";
    state = "Captcha challenge";
  } else if (input.responseOk && positive && !negative && filterMatch) {
    status = "available";
    state = "Tickets available";
  } else if (negative) {
    state = "Sold out or unavailable";
  } else if (positive && !filterMatch) {
    state = "Inventory found outside filters";
  }

  const facts = [
    state,
    `prices: ${prices.length ? prices.map(formatPrice).join(", ") : "not exposed"}`,
    `sections: ${sections.length ? sections.join(", ") : "not exposed"}`,
    `ticket types: ${signals.length ? signals.join(", ") : "not exposed"}`,
    `quantities: ${quantities.length ? quantities.join(", ") : "not exposed"}`,
    `filter: ${filterMatch ? "matched" : "not matched"}`,
    `HTTP ${input.statusCode}`,
  ];
  if (pageTitle) facts.push(`page: ${pageTitle}`);

  return { status, summary: facts.join("; ").slice(0, 1200) };
}

export function buildTicketAlertMessage(
  eventName: string,
  previousSummary: string,
  currentSummary: string,
  firstObservation: boolean,
) {
  if (firstObservation) {
    return `${eventName}\nInitial ticket snapshot\nCurrent: ${currentSummary}`.slice(0, 1800);
  }

  const changes: string[] = [];
  const previousState = previousSummary.split(";")[0]?.trim();
  const currentState = currentSummary.split(";")[0]?.trim();
  if (previousState && currentState && previousState !== currentState) {
    changes.push(`State changed: ${previousState} -> ${currentState}`);
  }

  const previousPrice = extractFirstSummaryPrice(previousSummary);
  const currentPrice = extractFirstSummaryPrice(currentSummary);
  if (
    previousPrice &&
    currentPrice &&
    previousPrice.currency === currentPrice.currency &&
    previousPrice.value !== currentPrice.value
  ) {
    const direction = currentPrice.value < previousPrice.value ? "dropped" : "increased";
    changes.push(
      `Lowest price ${direction}: ${formatPrice(previousPrice)} -> ${formatPrice(currentPrice)}`,
    );
  }

  if (changes.length === 0) changes.push("Ticket details changed");
  return [eventName, ...changes, `Previous: ${previousSummary}`, `Current: ${currentSummary}`]
    .join("\n")
    .slice(0, 1800);
}

export function buildScheduledTicketSnapshotMessage(
  eventName: string,
  currentSummary: string,
  checkedAt: string,
) {
  return [
    eventName,
    "Scheduled monitor check complete",
    `Checked: ${checkedAt}`,
    `Current: ${currentSummary}`,
  ]
    .join("\n")
    .slice(0, 1800);
}

function extractPageTitle(html: string) {
  const match = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  return match?.[1] ? decodeHtml(match[1]).replace(/\s+/g, " ").trim().slice(0, 140) : "";
}

function extractPrices(text: string) {
  const prices = new Map<string, { currency: string; value: number }>();
  const prefix = /(?:^|\s)(£|€|\$)\s*([0-9]{1,5}(?:[.,][0-9]{2})?)(?=\s|<|$)/g;
  const suffix = /(?:^|\s)([0-9]{1,5}(?:[.,][0-9]{2})?)\s*(GBP|EUR|USD)(?=\s|<|$)/gi;

  for (const match of text.matchAll(prefix)) {
    addPrice(prices, symbolCurrency(match[1]!), match[2]!);
  }
  for (const match of text.matchAll(suffix)) {
    addPrice(prices, match[2]!.toUpperCase(), match[1]!);
  }

  return [...prices.values()]
    .sort((left, right) => left.currency.localeCompare(right.currency) || left.value - right.value)
    .slice(0, 12);
}

function addPrice(
  prices: Map<string, { currency: string; value: number }>,
  currency: string,
  rawValue: string,
) {
  const value = Number(rawValue.replace(",", "."));
  if (!Number.isFinite(value) || value <= 0 || value > 100_000) return;
  prices.set(`${currency}:${value.toFixed(2)}`, { currency, value });
}

function symbolCurrency(symbol: string) {
  if (symbol === "£") return "GBP";
  if (symbol === "€") return "EUR";
  return "USD";
}

function formatPrice(price: { currency: string; value: number }) {
  return `${price.currency} ${price.value.toFixed(2)}`;
}

function extractFirstSummaryPrice(summary: string) {
  const match = summary.match(/prices:\s*(GBP|EUR|USD)\s+([0-9]+(?:\.[0-9]{2})?)/i);
  if (!match) return null;
  return { currency: match[1]!.toUpperCase(), value: Number(match[2]) };
}

function extractQuantities(lower: string) {
  const quantities = new Set<string>();
  const pattern = /\b([1-9][0-9]?)\s+tickets?\s+(?:available|remaining)\b/g;
  for (const match of lower.matchAll(pattern)) quantities.add(`${match[1]} tickets`);
  return [...quantities].slice(0, 8);
}

function extractSections(lower: string, configuredMatches: string[]) {
  const sections = new Set(configuredMatches);
  const pattern = /\b(section|block|tier|area)\s+([a-z0-9][a-z0-9-]{0,11})\b/g;
  for (const match of lower.matchAll(pattern)) {
    sections.add(`${titleCase(match[1]!)} ${match[2]!.toUpperCase()}`);
  }
  return [...sections].slice(0, 12);
}

function titleCase(value: string) {
  return `${value.charAt(0).toUpperCase()}${value.slice(1)}`;
}

function decodeHtml(value: string) {
  return value
    .replace(/&pound;/gi, "£")
    .replace(/&euro;/gi, "€")
    .replace(/&dollar;/gi, "$")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">");
}
