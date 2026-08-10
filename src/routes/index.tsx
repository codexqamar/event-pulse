import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Header } from "@/components/eventpulse/Header";
import { SideRail, BottomNav, type NavId } from "@/components/eventpulse/Nav";
import { SummaryBar } from "@/components/eventpulse/SummaryBar";
import { MonitorGrid } from "@/components/eventpulse/MonitorGrid";
import { ProfilePanel } from "@/components/eventpulse/ProfilePanel";
import { AlertLog } from "@/components/eventpulse/AlertLog";
import { SettingsPanel } from "@/components/eventpulse/SettingsPanel";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "EventPulse | Multi-Site Ticket Monitor Dashboard" },
      {
        name: "description",
        content:
          "Real-time ticketing analytics across Ticketmaster, AXS and SeeTickets with MultiLogin proxy profile management.",
      },
      { property: "og:title", content: "EventPulse | Multi-Site Ticket Monitor" },
      {
        property: "og:description",
        content:
          "Monitor worldwide ticket drops, proxy profiles and fingerprint health from one dark-mode command center.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Dashboard,
});

function Dashboard() {
  const [tab, setTab] = useState<NavId>("monitors");

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <SideRail active={tab} onSelect={setTab} />

      <div className="flex min-w-0 flex-1 flex-col">
        <Header />

        <main className="flex-1 space-y-5 px-4 pb-24 pt-4 lg:px-6 lg:pb-8">
          <SummaryBar />

          {/* Mobile: one section at a time via bottom nav */}
          <div className="space-y-5 lg:hidden">
            {tab === "monitors" && <MonitorGrid />}
            {tab === "profiles" && <ProfilePanel />}
            {tab === "alerts" && <AlertLog className="max-h-[70vh]" />}
            {tab === "settings" && <SettingsPanel />}
          </div>

          {/* Desktop: full command center */}
          <div className="hidden gap-5 lg:grid lg:grid-cols-[minmax(0,1fr)_340px]">
            <div className="space-y-5">
              <MonitorGrid />
              <ProfilePanel />
            </div>
            <aside className="space-y-5">
              <AlertLog className="max-h-[420px]" />
              <SettingsPanel />
            </aside>
          </div>
        </main>
      </div>

      <BottomNav active={tab} onSelect={setTab} />
    </div>
  );
}
