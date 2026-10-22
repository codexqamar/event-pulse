// Rate-aware delivery queues for chat channels (Telegram, Discord).
//
// Every due ticket check produces an alert, so with several targets on a short refresh interval
// the alert rate exceeds Telegram's group limit (20 messages/minute) and Discord's webhook limit
// (~30 messages/minute). Each destination therefore gets one queue that paces requests below the
// provider limit, honours 429 retry_after, and packs everything that queued up while it waited
// into as few messages as the provider's length limit allows. Alerts are never dropped for being
// over the rate limit; they arrive in the next allowed message instead.

const MAX_RATE_LIMIT_RETRIES = 5;
const MAX_OUTAGE_RETRIES = 1;
const MAX_RETRY_AFTER_MS = 60_000;
const ITEM_SEPARATOR = "\n\n━━━━━━━━━━\n\n";

export type ChannelSendResult = {
  ok: boolean;
  status: number;
  retryAfterMs: number | null;
  detail: string;
};

type ChannelQueueOptions = {
  label: string;
  minIntervalMs: number;
  maxLength: number;
  header?: string;
  send: (text: string) => Promise<ChannelSendResult>;
};

type QueueItem = {
  text: string;
  resolve: (sent: boolean) => void;
  errors: string[];
};

export class ChannelQueue {
  private readonly items: QueueItem[] = [];
  private nextAllowedAt = 0;
  private pumping = false;
  private readonly options: ChannelQueueOptions;

  constructor(options: ChannelQueueOptions) {
    this.options = options;
  }

  // Resolves true once the text is delivered inside some message, false if delivery failed.
  enqueue(text: string, errors: string[]) {
    return new Promise<boolean>((resolve) => {
      this.items.push({ text: this.fitItem(text), resolve, errors });
      void this.pump();
    });
  }

  private async pump() {
    if (this.pumping) return;
    this.pumping = true;
    try {
      while (this.items.length > 0) {
        const wait = this.nextAllowedAt - Date.now();
        if (wait > 0) await sleep(wait);

        const batch = this.takeBatch();
        await this.sendBatch(batch);
      }
    } finally {
      this.pumping = false;
    }
  }

  private async sendBatch(batch: QueueItem[]) {
    const text = (this.options.header ?? "") + batch.map((item) => item.text).join(ITEM_SEPARATOR);

    for (let attempt = 0; ; attempt += 1) {
      let result: ChannelSendResult;
      try {
        result = await this.options.send(text);
      } catch (error) {
        result = {
          ok: false,
          status: 0,
          retryAfterMs: null,
          detail: error instanceof Error ? error.message : "Request failed.",
        };
      }
      this.nextAllowedAt = Date.now() + this.options.minIntervalMs;

      if (result.ok) {
        for (const item of batch) item.resolve(true);
        return;
      }

      // Rate limits are expected under load and always clear; outages get a short retry only, so
      // a provider being down cannot hold the monitor pass open.
      const retryLimit =
        result.status === 429
          ? MAX_RATE_LIMIT_RETRIES
          : result.status === 0 || result.status >= 500
            ? MAX_OUTAGE_RETRIES
            : 0;
      if (attempt < retryLimit) {
        const backoff = result.retryAfterMs ?? this.options.minIntervalMs * (attempt + 1);
        this.nextAllowedAt = Date.now() + Math.min(backoff, MAX_RETRY_AFTER_MS);
        await sleep(this.nextAllowedAt - Date.now());
        continue;
      }

      const message = `${this.options.label} failed (${result.status || "network"}): ${result.detail}`;
      console.error(message);
      for (const item of batch) {
        item.errors.push(message);
        item.resolve(false);
      }
      return;
    }
  }

  private takeBatch() {
    const budget = this.options.maxLength - (this.options.header?.length ?? 0);
    const batch: QueueItem[] = [this.items.shift()!];
    let length = batch[0]!.text.length;
    while (this.items.length > 0) {
      const nextLength = length + ITEM_SEPARATOR.length + this.items[0]!.text.length;
      if (nextLength > budget) break;
      batch.push(this.items.shift()!);
      length = nextLength;
    }
    return batch;
  }

  private fitItem(text: string) {
    const budget = this.options.maxLength - (this.options.header?.length ?? 0);
    return text.length <= budget ? text : `${text.slice(0, budget - 1)}…`;
  }
}

export function parseRetryAfterMs(response: Response, body: unknown) {
  const fromBody = readRetryAfterSeconds(body);
  if (fromBody != null) return Math.ceil(fromBody * 1000);
  const header = Number(response.headers.get("retry-after"));
  return Number.isFinite(header) && header > 0 ? Math.ceil(header * 1000) : null;
}

function readRetryAfterSeconds(body: unknown): number | null {
  if (!body || typeof body !== "object") return null;
  const record = body as { retry_after?: unknown; parameters?: { retry_after?: unknown } };
  // Telegram: { parameters: { retry_after } }, Discord: { retry_after } (seconds, may be float).
  const value = record.parameters?.retry_after ?? record.retry_after;
  return typeof value === "number" && Number.isFinite(value) && value > 0 ? value : null;
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, Math.max(ms, 0)));
}
