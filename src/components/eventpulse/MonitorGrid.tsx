import { useState } from "react";
import { Pause, Play, ScrollText, Link2, RefreshCw, UserRound } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { PLATFORM_FILTERS, STATUS_META, TARGETS } from "@/lib/eventpulse-data";

export function MonitorGrid() {
  const [filter, setFilter] = useState<string>("All Sites");
  const rows = TARGETS.filter((t) => filter === "All Sites" || t.platform === filter);

  return (
    <section className="space-y-3">
      <div className="flex items-center justify-between gap-3">
        <h2 className="font-display text-sm font-bold uppercase tracking-wide">
          Live Event Ticket Monitoring
        </h2>
        <span className="font-mono text-[11px] text-muted-foreground">
          {rows.length} targets shown
        </span>
      </div>

      <div className="scrollbar-hidden -mx-4 flex gap-2 overflow-x-auto px-4 pb-1 lg:mx-0 lg:flex-wrap lg:px-0">
        {PLATFORM_FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={cn(
              "shrink-0 rounded-full border px-3 py-1.5 text-xs font-medium transition-colors",
              filter === f
                ? "border-primary/40 bg-primary/15 text-primary"
                : "border-border bg-card text-muted-foreground hover:text-foreground",
            )}
          >
            {f}
          </button>
        ))}
      </div>

      <div className="grid gap-3 2xl:grid-cols-2">
        {rows.map((t) => {
          const status = STATUS_META[t.status];
          return (
            <article key={t.id} className="panel p-4">
              <div className="grid grid-cols-[minmax(0,1fr)_auto] items-start gap-3">
                <div className="min-w-0">
                  <span className="inline-block rounded bg-secondary px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                    {t.platform}
                  </span>
                  <h3 className="mt-1.5 truncate font-display text-base font-semibold">
                    {t.event}
                  </h3>
                  <p className="truncate text-xs text-muted-foreground">{t.venue}</p>
                </div>
                <span
                  className={cn(
                    "shrink-0 rounded-full px-2.5 py-1 text-[11px] font-semibold ring-1",
                    status.className,
                  )}
                >
                  {status.label}
                </span>
              </div>

              <p className="mt-3 rounded-md bg-secondary/60 px-3 py-2 font-mono text-xs text-foreground">
                {t.availability}
              </p>

              <dl className="mt-3 grid gap-1.5 text-[11px] text-muted-foreground">
                <div className="flex min-w-0 items-center gap-1.5">
                  <Link2 className="h-3.5 w-3.5 shrink-0" />
                  <span className="truncate font-mono">{t.url}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <RefreshCw className="h-3.5 w-3.5 shrink-0 text-info" />
                  Refreshing every {t.refresh.toFixed(1)}s
                </div>
                <div className="flex min-w-0 items-center gap-1.5">
                  <UserRound className="h-3.5 w-3.5 shrink-0 text-online" />
                  <span className="truncate">
                    {t.profile} ({t.proxy})
                  </span>
                </div>
              </dl>

              <div className="mt-4 flex flex-wrap gap-2">
                <Button size="sm" className="font-semibold">
                  <Play className="h-3.5 w-3.5" />
                  Launch Session
                </Button>
                <Button size="sm" variant="secondary">
                  <Pause className="h-3.5 w-3.5" />
                  Pause Monitor
                </Button>
                <Button size="sm" variant="ghost">
                  <ScrollText className="h-3.5 w-3.5" />
                  View Logs
                </Button>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
