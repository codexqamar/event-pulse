import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { BellRing, Send } from "lucide-react";
import { showTestNotification, setupPushNotifications } from "@/lib/pwa";

export function SettingsPanel() {
  const [interval, setInterval] = useState([4]);
  const [sound, setSound] = useState(true);
  const [push, setPush] = useState(true);
  const [pushStatus, setPushStatus] = useState("Service worker registers automatically.");
  const [isPushBusy, setIsPushBusy] = useState(false);

  async function runPushAction(action: "setup" | "test") {
    setIsPushBusy(true);
    try {
      const result =
        action === "setup" ? await setupPushNotifications() : await showTestNotification();
      setPushStatus(result.message);
      setPush(result.status === "ready");
    } catch (error) {
      setPushStatus(error instanceof Error ? error.message : "Push setup failed.");
    } finally {
      setIsPushBusy(false);
    }
  }

  return (
    <section className="panel space-y-4 p-4">
      <h2 className="font-display text-sm font-bold uppercase tracking-wide">
        Global Controls &amp; Settings
      </h2>

      <div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-muted-foreground">Global Refresh Interval</span>
          <span className="font-mono text-primary">{interval[0]}s</span>
        </div>
        <Slider
          className="mt-3"
          min={1}
          max={30}
          step={1}
          value={interval}
          onValueChange={setInterval}
        />
        <div className="mt-1 flex justify-between font-mono text-[10px] text-muted-foreground">
          <span>1s</span>
          <span>30s</span>
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <label className="flex items-center justify-between gap-3 rounded-md bg-secondary/60 px-3 py-2.5 text-xs">
          Sound Alerts
          <Switch checked={sound} onCheckedChange={setSound} />
        </label>
        <label className="flex items-center justify-between gap-3 rounded-md bg-secondary/60 px-3 py-2.5 text-xs">
          Desktop / Mobile Push
          <Switch checked={push} onCheckedChange={setPush} />
        </label>
      </div>

      <div className="space-y-2 rounded-md bg-secondary/60 px-3 py-3">
        <div className="flex flex-wrap gap-2">
          <Button
            type="button"
            size="sm"
            disabled={isPushBusy}
            onClick={() => void runPushAction("setup")}
          >
            <BellRing className="h-3.5 w-3.5" />
            Enable Push
          </Button>
          <Button
            type="button"
            size="sm"
            variant="secondary"
            disabled={isPushBusy}
            onClick={() => void runPushAction("test")}
          >
            <Send className="h-3.5 w-3.5" />
            Test Notification
          </Button>
        </div>
        <p className="text-xs leading-relaxed text-muted-foreground">{pushStatus}</p>
      </div>

      <div className="space-y-1.5">
        <label htmlFor="ml-port" className="text-xs text-muted-foreground">
          MultiLogin Local REST Endpoint
        </label>
        <Input id="ml-port" defaultValue="http://localhost:35462" className="font-mono text-xs" />
      </div>

      <div className="space-y-1.5">
        <label htmlFor="ml-key" className="text-xs text-muted-foreground">
          MultiLogin API Key
        </label>
        <Input
          id="ml-key"
          type="password"
          defaultValue="ml_live_8f31d0c4a7"
          className="font-mono text-xs"
        />
      </div>
    </section>
  );
}
