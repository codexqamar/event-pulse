export type MonitorStatus = "available" | "monitoring" | "captcha" | "limited";

export type Platform =
  | "Ticketmaster UK/WW"
  | "AXS"
  | "SeeTickets"
  | "Gigs & Tours"
  | "Royal Albert Hall";

export interface MonitorTarget {
  id: string;
  platform: Platform;
  event: string;
  venue: string;
  status: MonitorStatus;
  availability: string;
  url: string;
  refresh: number;
  profile: string;
  proxy: string;
}

export const PLATFORM_FILTERS: Array<"All Sites" | Platform> = [
  "All Sites",
  "Ticketmaster UK/WW",
  "AXS",
  "SeeTickets",
  "Gigs & Tours",
  "Royal Albert Hall",
];

export const STATUS_META: Record<
  MonitorStatus,
  { label: string; className: string }
> = {
  available: { label: "Tickets Available", className: "bg-online/15 text-online ring-online/30" },
  monitoring: { label: "Monitoring", className: "bg-info/15 text-info ring-info/30" },
  captcha: { label: "Captcha Challenge", className: "bg-warn/15 text-warn ring-warn/30" },
  limited: { label: "Rate Limited", className: "bg-alert/15 text-alert ring-alert/30" },
};

export const TARGETS: MonitorTarget[] = [
  {
    id: "8841",
    platform: "Ticketmaster UK/WW",
    event: "Coldplay — Music of the Spheres",
    venue: "Wembley Stadium, London",
    status: "available",
    availability: "Section 102 • 4 Seats Detected",
    url: "ticketmaster.co.uk/coldplay/event/8841",
    refresh: 3.5,
    profile: "Profile #04",
    proxy: "UK Residential Sticky IP",
  },
  {
    id: "9102",
    platform: "AXS",
    event: "Oasis — Live '26 Reunion",
    venue: "Royal Albert Hall, London",
    status: "monitoring",
    availability: "General Admission In Stock",
    url: "axs.com/events/9102/oasis",
    refresh: 2.0,
    profile: "Profile #07",
    proxy: "Manchester Mobile 5G",
  },
  {
    id: "7730",
    platform: "SeeTickets",
    event: "Fred again.. — Boiler Room Tour",
    venue: "O2 Arena, London",
    status: "captcha",
    availability: "Queue holding • 1,204 ahead",
    url: "seetickets.com/event/7730",
    refresh: 5.0,
    profile: "Profile #02",
    proxy: "London Residential",
  },
  {
    id: "6612",
    platform: "Gigs & Tours",
    event: "Arctic Monkeys — UK Arena Run",
    venue: "Utilita Arena, Birmingham",
    status: "limited",
    availability: "429 throttle • retry in 12s",
    url: "gigsandtours.com/event/6612",
    refresh: 8.0,
    profile: "Profile #09",
    proxy: "Leeds Datacenter",
  },
  {
    id: "5521",
    platform: "Royal Albert Hall",
    event: "Hans Zimmer — Live Orchestral",
    venue: "Royal Albert Hall, London",
    status: "available",
    availability: "Circle K • 2 Seats Detected",
    url: "royalalberthall.com/tickets/5521",
    refresh: 3.0,
    profile: "Profile #01",
    proxy: "UK Residential Sticky IP",
  },
  {
    id: "4408",
    platform: "Ticketmaster UK/WW",
    event: "Billie Eilish — Hit Me Hard World",
    venue: "Co-op Live, Manchester",
    status: "monitoring",
    availability: "Presale opens 10:00 BST",
    url: "ticketmaster.co.uk/billie/event/4408",
    refresh: 1.5,
    profile: "Profile #06",
    proxy: "Manchester Mobile 5G",
  },
];

export interface ProfileRow {
  name: string;
  region: string;
  cookies: string;
  session: string;
  health: string;
}

export const PROFILES: ProfileRow[] = [
  ["Profile 01", "London Residential", "100% Persisted", "Authenticated", "Clean / No Leaks"],
  ["Profile 02", "London Residential", "100% Persisted", "Authenticated", "Clean / No Leaks"],
  ["Profile 03", "Manchester Mobile 5G", "98% Persisted", "Authenticated", "Clean / No Leaks"],
  ["Profile 04", "UK Residential Sticky", "100% Persisted", "Authenticated", "Clean / No Leaks"],
  ["Profile 05", "Birmingham Residential", "100% Persisted", "Session Expiring", "Clean / No Leaks"],
  ["Profile 06", "Manchester Mobile 5G", "100% Persisted", "Authenticated", "Clean / No Leaks"],
  ["Profile 07", "Glasgow Residential", "96% Persisted", "Authenticated", "Minor WebGL Drift"],
  ["Profile 08", "Leeds Datacenter", "100% Persisted", "Authenticated", "Clean / No Leaks"],
  ["Profile 09", "Bristol Residential", "100% Persisted", "Re-auth Queued", "Clean / No Leaks"],
  ["Profile 10", "Dublin Mobile LTE", "100% Persisted", "Authenticated", "Clean / No Leaks"],
].map(([name, region, cookies, session, health]) => ({
  name,
  region,
  cookies,
  session,
  health,
}));

export const ALERT_LOG = [
  {
    time: "19:42:01",
    tone: "online" as const,
    text: "Ticketmaster UK: 2x Standing Tickets detected for Event ID #8841. Profile #02 notified.",
  },
  {
    time: "19:40:15",
    tone: "info" as const,
    text: "AXS: Queue opened for Event ID #9102. Auto-routing via Profile #07.",
  },
  {
    time: "19:38:44",
    tone: "warn" as const,
    text: "SeeTickets: Captcha challenge served on Event ID #7730. Solver engaged.",
  },
  {
    time: "19:36:02",
    tone: "alert" as const,
    text: "Gigs & Tours: Rate limit (HTTP 429) on Event ID #6612. Rotating Profile #09.",
  },
  {
    time: "19:33:57",
    tone: "online" as const,
    text: "Royal Albert Hall: Circle K inventory refreshed — 2 seats held by Profile #01.",
  },
  {
    time: "19:31:12",
    tone: "info" as const,
    text: "MultiLogin: Fingerprint sync completed across 10 profiles (0 leaks).",
  },
];
