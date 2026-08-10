import { Activity, BellRing, Globe2, Timer } from "lucide-react";
import type { LucideIcon } from "lucide-react";

const CARDS: Array<{
  label: string;
  value: string;
  sub: string;
  icon: LucideIcon;
  tone: string;
}> = [
  {
    label: "Active Monitors",
    value: "18",
    sub: "Live Streams • +2 Today",
    icon: Activity,
    tone: "text-online",
  },
  {
    label: "Ticket Alerts Detected",
    value: "142",
    sub: "Drops Today",
    icon: BellRing,
    tone: "text-warn",
  },
  {
    label: "Connected Proxy Profiles",
    value: "10 / 10",
    sub: "Isolated IPs Active",
    icon: Globe2,
    tone: "text-info",
  },
  {
    label: "Avg Response Time",
    value: "142ms",
    sub: "Across all targets",
    icon: Timer,
    tone: "text-alert",
  },
];

export function SummaryBar() {
  return (
    <section className="grid grid-cols-2 gap-3 xl:grid-cols-4">
      {CARDS.map((card) => (
        <div key={card.label} className="panel p-3 sm:p-4">
          <div className="flex items-start justify-between gap-2">
            <p className="min-w-0 text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
              {card.label}
            </p>
            <card.icon className={`h-4 w-4 shrink-0 ${card.tone}`} />
          </div>
          <p className="mt-2 font-display text-2xl font-bold tabular-nums sm:text-3xl">
            {card.value}
          </p>
          <p className="mt-0.5 truncate text-xs text-muted-foreground">{card.sub}</p>
        </div>
      ))}
    </section>
  );
}
