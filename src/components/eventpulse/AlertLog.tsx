import { ALERT_LOG } from "@/lib/eventpulse-data";
import { cn } from "@/lib/utils";

const TONE: Record<string, string> = {
  online: "bg-online",
  info: "bg-info",
  warn: "bg-warn",
  alert: "bg-alert",
};

export function AlertLog({ className }: { className?: string }) {
  return (
    <section className={cn("panel flex flex-col p-4", className)}>
      <div className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3">
        <h2 className="truncate font-display text-sm font-bold uppercase tracking-wide">
          Real-Time Alert Log
        </h2>
        <span className="shrink-0 font-mono text-[11px] text-muted-foreground">live</span>
      </div>
      <ul className="scrollbar-hidden mt-3 space-y-2 overflow-y-auto">
        {ALERT_LOG.map((log) => (
          <li
            key={log.time}
            className="flex gap-2.5 rounded-md bg-secondary/50 px-3 py-2 text-xs"
          >
            <span
              className={cn("mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full", TONE[log.tone])}
            />
            <p className="min-w-0 leading-relaxed text-muted-foreground">
              <span className="font-mono text-foreground">{log.time}</span> — {log.text}
            </p>
          </li>
        ))}
      </ul>
    </section>
  );
}
