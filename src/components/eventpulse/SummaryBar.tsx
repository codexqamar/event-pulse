import { Activity, BellRing, Globe2, Timer } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import type { DashboardStats } from "@/lib/eventpulse/types";

const CARD_META: Array<{
  key: keyof DashboardStats;
  label: string;
  sub: (stats: DashboardStats) => string;
  icon: LucideIcon;
  tone: string;
}> = [
  {
    key: "activeMonitors",
    label: "Active Monitors",
    sub: () => "Live Streams",
    icon: Activity,
    tone: "text-online",
  },
  {
    key: "alertsToday",
    label: "Ticket Alerts Detected",
    sub: () => "Drops Today",
    icon: BellRing,
    tone: "text-warn",
  },
  {
    key: "connectedProfiles",
    label: "Connected Proxy Profiles",
    sub: (stats) => `${stats.connectedProfiles} Isolated IPs Active`,
    icon: Globe2,
    tone: "text-info",
  },
  {
    key: "avgResponseMs",
    label: "Avg Response Time",
    sub: () => "Across all targets",
    icon: Timer,
    tone: "text-alert",
  },
];

export function SummaryBar({ stats }: { stats: DashboardStats }) {
  return (
    <section className="grid grid-cols-2 gap-3 xl:grid-cols-4">
      {CARD_META.map((card) => (
        <div key={card.label} className="panel p-3 sm:p-4">
          <div className="flex items-start justify-between gap-2">
            <p className="min-w-0 text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
              {card.label}
            </p>
            <card.icon className={`h-4 w-4 shrink-0 ${card.tone}`} />
          </div>
          <p className="mt-2 font-display text-2xl font-bold tabular-nums sm:text-3xl">
            {card.key === "avgResponseMs" ? `${stats[card.key]}ms` : stats[card.key]}
          </p>
          <p className="mt-0.5 truncate text-xs text-muted-foreground">{card.sub(stats)}</p>
        </div>
      ))}
    </section>
  );
}
