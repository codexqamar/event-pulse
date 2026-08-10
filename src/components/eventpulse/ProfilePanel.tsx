import { useState } from "react";
import { Switch } from "@/components/ui/switch";
import { PROFILES } from "@/lib/eventpulse-data";

export function ProfilePanel() {
  const [autoRotate, setAutoRotate] = useState(true);
  const [stickyMobile, setStickyMobile] = useState(false);

  return (
    <section className="panel p-4">
      <div className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3">
        <h2 className="truncate font-display text-sm font-bold uppercase tracking-wide">
          MultiLogin &amp; Proxy Profiles
        </h2>
        <span className="shrink-0 rounded-full bg-online/10 px-2 py-0.5 font-mono text-[11px] text-online ring-1 ring-online/25">
          10 Active
        </span>
      </div>

      <div className="mt-3 -mx-4 overflow-x-auto px-4">
        <table className="w-full min-w-[720px] border-collapse text-left text-xs">
          <thead>
            <tr className="text-[10px] uppercase tracking-wider text-muted-foreground">
              <th className="py-2 pr-3 font-medium">Profile</th>
              <th className="py-2 pr-3 font-medium">Assigned IP / Region</th>
              <th className="py-2 pr-3 font-medium">Cookies</th>
              <th className="py-2 pr-3 font-medium">TM Session</th>
              <th className="py-2 font-medium">Fingerprint Health</th>
            </tr>
          </thead>
          <tbody>
            {PROFILES.map((p) => (
              <tr key={p.name} className="border-t border-border">
                <td className="py-2.5 pr-3 font-mono font-semibold">{p.name}</td>
                <td className="py-2.5 pr-3 text-muted-foreground">{p.region}</td>
                <td className="py-2.5 pr-3 text-online">{p.cookies}</td>
                <td className="py-2.5 pr-3">
                  <span
                    className={
                      p.session === "Authenticated" ? "text-online" : "text-warn"
                    }
                  >
                    {p.session}
                  </span>
                </td>
                <td className="py-2.5">
                  <span
                    className={
                      p.health.startsWith("Clean") ? "text-online" : "text-warn"
                    }
                  >
                    {p.health}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <label className="flex items-center justify-between gap-3 rounded-md bg-secondary/60 px-3 py-2.5 text-xs">
          Auto-Rotate Proxy on Rate Limit
          <Switch checked={autoRotate} onCheckedChange={setAutoRotate} />
        </label>
        <label className="flex items-center justify-between gap-3 rounded-md bg-secondary/60 px-3 py-2.5 text-xs">
          Maintain Sticky Mobile IP
          <Switch checked={stickyMobile} onCheckedChange={setStickyMobile} />
        </label>
      </div>
    </section>
  );
}
