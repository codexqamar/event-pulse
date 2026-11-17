# HD-1 Drop Monitor - Complete Project Context

Last consolidated: 17 November 2026 (Asia/Karachi)

This document is the consolidated technical and operational context for the HD-1 Drop Monitor project. It combines the current repository state, implemented behaviour, decisions made with the client, deployment requirements, completed testing, known limitations, and remaining handover responsibilities.

No passwords, API tokens, service-role keys, webhook URLs, proxy credentials, private chat IDs, or other reusable secrets are included here. Those values must remain in Coolify or another approved secret manager.

## 1. Project summary

HD-1 Drop Monitor is a responsive Progressive Web Application for monitoring ticket-event URLs and reporting ticket availability to the client.

The main production flow is:

1. The client adds a ticket target URL and its filters in the dashboard.
2. The production scheduler decides when the target is due.
3. The backend opens the target through an approved Multilogin profile or a temporary rotating scraper profile.
4. The browser captures rendered HTML and ticket-inventory API responses.
5. The backend applies the target's section, quantity, price, and ticket-type rules.
6. A genuine new or increased stock result creates an alert.
7. The same alert is delivered through each enabled channel, including browser push, Telegram and Discord.
8. Supabase stores targets, settings, profiles, push subscriptions and alert delivery results.

The application is a monitor and alerting system. It does not complete checkout or payment.

## 2. Current repository state

- Repository directory: `D:\projects\event-pulse`
- Current branch: `main`
- Latest visible commit at the time of this consolidation: `8a34d47`
- Application package name: `tanstack_start_ts`
- Runtime target: Node.js 22
- Production application port: `3000`
- Current production URL documented by the project: `https://event-pulse.web-testlink.com/`

The working tree contains untracked generated client artifacts under `output/` and temporary authoring files under `tmp/`. They are not part of the committed application source unless deliberately added later.

Generated client artifacts currently include:

- `output/pdf/HD1-Drop-Monitor-Handover.pdf`
- `output/pdf/HD1_Drop_Monitor_Client_Testing_Guide.pdf`
- `output/pdf/HD1_Monitoring_Operations_and_Preflight_Guide.pdf`
- `output/video/HD1_Drop_Monitor_Complete_Client_Demo.mp4`
- `output/video/HD1_Real_Live_Ticket_Drop_Test.mp4`

The original client notes file is intentionally ignored by Git because it contains private client context.

## 3. Technology stack

### Frontend and full-stack framework

- React 19
- TanStack Start and TanStack Router
- Vite 8
- TypeScript 5
- Tailwind CSS 4
- Radix UI primitives
- Lucide icons
- TanStack Query

### Backend and automation

- TanStack server functions
- Node/Nitro server output
- Supabase REST API using the service-role key
- Puppeteer Core for rendered browser access
- Multilogin launcher and Multilogin automation token
- Web Push using VAPID
- Telegram Bot API
- Discord webhooks
- Optional Twilio SMS and WhatsApp

### Deployment

- Multi-stage Node 22 Alpine Docker image
- Coolify-compatible environment configuration
- Optional production Docker Compose stack containing the application and Multilogin launcher
- Docker health check against `/api/eventpulse/health`

## 4. Main application modules

### Dashboard header and summary

The header shows:

- Supabase/backend connection state.
- Active target count.
- Active Multilogin profile count.
- An Add New Target URL action.

The summary cards show:

- Active monitors.
- Alerts detected today.
- Connected proxy profiles.
- Average target response time.

### Monitor targets

The target form supports:

- Platform.
- Event name.
- Venue.
- Target URL.
- Section or area filters.
- Minimum ticket quantity.
- Maximum ticket price.
- Normal/standard tickets only.
- Even ticket quantities only.
- Start-monitoring date and time.
- Stop-monitoring date and time.
- Assigned Multilogin profile.
- Sticky proxy/IP label.

Target actions include:

- Open Ticket Page.
- Check now.
- Check and send alert.
- Pause or resume monitoring.
- Change the assigned profile.
- Delete the target.

The target status can be:

- Tickets Available.
- Monitoring.
- Captcha Challenge.
- Check Failed.
- Paused.

### Profiles

The Profiles module supports:

- Saving profile metadata and Multilogin profile/folder IDs.
- Launching a Multilogin profile through the configured launcher.
- Recording restore metadata in Supabase.
- Manually pausing a profile for 15 minutes, one hour, six hours, or until resumed.
- Resuming a profile.
- Deleting saved profile metadata.
- Showing cookie, session, fingerprint, region and sticky-IP labels.

The application currently contains an explicit allowlist of four client profile identifiers. Monitoring refuses any profile that is not in that allowlist. Exact account identifiers are intentionally not reproduced in this document.

### Alerts

The alert log displays ticket and operational events stored in Supabase.

A ticket alert can include:

- Event name and event ID.
- Venue, date and location.
- Total stock.
- Inventory type, for example resale or standard.
- Area and section.
- Row and seat examples when exposed.
- Quantity and price.
- A Buy Tickets/Open Ticket link.

### Global Controls and Settings

The Settings module supports:

- Global refresh interval from 1 to 30 seconds.
- Sound alerts.
- Desktop/mobile browser push.
- SMS alerts.
- WhatsApp alerts.
- Telegram alerts.
- Discord alerts.
- Multilogin local REST endpoint.
- Saving settings to Supabase.
- Enabling browser push and saving a device subscription.
- Sending a local test notification.
- Sending one Test All Channels alert through every enabled provider.

### Responsive navigation and modals

- Desktop uses a left navigation rail and responsive module modals.
- Mobile uses bottom navigation and shows one section at a time.
- Monitor, Profiles, Alerts and Settings each open their corresponding responsive content.

### PWA installation

- The application includes a manifest and service worker.
- Chrome can show the custom installation prompt at the lower-right of the website.
- The prompt disappears after installation or dismissal.
- The service worker caches the application shell and handles push notification clicks.

## 5. Monitoring behaviour

### Scheduler

Persistent monitoring runs inside the Node server when:

```text
EVENTPULSE_SCHEDULER_ENABLED=true
```

The scheduler:

- Starts approximately one second after the server starts.
- Evaluates due targets on the configured scheduler tick.
- Prevents two monitor passes from running simultaneously inside one process.
- Loads up to 25 non-paused targets ordered by oldest check first.
- Reloads Global Controls and Settings from Supabase on every pass.
- Respects target start and stop windows.
- Respects profile pauses and the per-profile safety interval.

Exactly one production replica must have the scheduler enabled. Extra web replicas must use `EVENTPULSE_SCHEDULER_ENABLED=false` or duplicate checks and alerts can occur.

The external monitor-run endpoint is:

```text
POST /api/eventpulse/monitor-run
```

It accepts the configured cron secret through `x-eventpulse-cron-secret` or a Bearer token. Production refuses this route when no cron secret is configured.

### Global interval and profile safety interval

The saved dashboard interval controls when a target is due. Changing the interval does not require a container restart.

The same regular Multilogin profile is also protected by `EVENTPULSE_PROFILE_MIN_INTERVAL_SECONDS`, which defaults to 60 seconds. Therefore, selecting a 10-second global interval does not force the same profile to open a ticket page every 10 seconds. Targets assigned to that profile wait their turn.

When a configured rotating scraper-proxy pool is active, each check uses a separate temporary profile and the regular-profile delay is not applied in the same way.

### Manual checks

`Check now` runs the same real browser check used by the scheduler but does not force an alert.

`Check and send alert` runs the real check and, when matching stock exists, sends the current ticket-specific result even when the same stock was previously reported.

Repeated clicks are protected by the per-profile safety interval. A manual check is refused while the assigned profile is paused or has loaded a ticket page too recently.

### Ticket change detection

For structured inventory:

- The application stores a stock snapshot per target.
- Normal scheduler alerts are created for new listing areas or increased stock.
- A small change that does not represent new or increased matched stock does not create another drop alert.
- A forced manual Check and send alert can send the current stock for controlled testing.

For pages without captured structured inventory:

- Non-Ticketmaster sites can use rendered page-text signals as a fallback.
- Ticketmaster page text alone is never treated as proof of stock because Ticketmaster pages can contain generic Buy Tickets wording even with no usable inventory.

### Captcha, blocking and failure behaviour

- Captcha is shown as a target status but does not create ticket alerts.
- Captcha does not send push, Telegram, Discord, SMS or WhatsApp notifications.
- HTTP 403 or 429 on a regular profile triggers an automatic profile pause.
- Automatic block cooldowns escalate through approximately 5, 10, 20, 40 and 60 minutes.
- A successful later check clears the automatic block state.
- Three consecutive equivalent failures create one operational warning in the dashboard.
- Equivalent operational warnings repeat no more than once every two hours.
- A removed event page (HTTP 404/410) pauses the target.
- Failed or blocked checks do not overwrite the last known real stock summary.

Profile pause state is held in server-process memory. A server restart clears the in-memory pause map and allows profiles to be checked again.

### Operational notices versus ticket alerts

By default, operational notices such as profile pauses, monitor failure/recovery and token expiry are stored in the dashboard alert log only.

Telegram, Discord, push, SMS and WhatsApp are reserved for real ticket alerts unless this advanced variable is explicitly enabled:

```text
EVENTPULSE_SYSTEM_NOTICES_TO_CHANNELS=true
```

This prevents operational noise from flooding client ticket channels.

## 6. Ticket extraction

### Ticketmaster

Ticketmaster is the strongest implemented extraction path.

The browser capture:

- Opens the real rendered page.
- Waits for Ticketmaster identification when required.
- Records matching JSON inventory responses requested by the page.
- Parses facets, offers and quick-pick inventory.
- Extracts areas, sections, rows, seat examples, ticket type, quantity and price when exposed.
- Reads event details from JSON-LD and the event URL.
- Applies section, price, quantity, even-quantity and normal-ticket filters.

Ticketmaster inventory is not reported as available when no structured inventory response was captured.

### Other listed platforms

The user interface currently lists:

- Ticketmaster UK/Worldwide.
- AXS.
- See Tickets.
- Gigs & Tours.
- Royal Albert Hall.

These other platforms currently rely mainly on generic rendered HTML and page-text interpretation unless their page responses match the implemented structured parser. They do not yet have the same platform-specific structured inventory coverage as Ticketmaster.

## 7. Multilogin and proxy design

### Regular approved profiles

The regular path:

1. Validates that the assigned profile is allowlisted.
2. Uses the Multilogin automation token.
3. Reuses or starts the selected Multilogin profile through the launcher.
4. Connects Puppeteer to its CDP port.
5. Applies stored proxy authentication where required.
6. Opens one new page for the target check.
7. Closes only the temporary page and disconnects Puppeteer.

The implementation does not intentionally edit the approved profile's proxy, cookies, fingerprint or sticky-IP assignment.

### Client decisions already established

- Client-assigned sticky residential proxies must remain unchanged.
- Auto-rotation must remain off for live checkout profiles.
- Only approved existing profiles may be used.
- Monitoring tests must not explore or modify live client accounts beyond the approved event-page check.
- No checkout or payment is permitted.

### Rotating scraper proxies

The client later requested a way to use multiple IPs for scraping while leaving the user's own click-through connection unchanged.

This is implemented through `MULTILOGIN_SCRAPER_PROXIES`:

- The value is a JSON array of HTTP or SOCKS5 proxy URLs.
- The pool rotates sequentially and wraps to the first proxy.
- Each due check creates a temporary Multilogin quick profile.
- The quick profile uses the selected scraper proxy.
- The quick profile is stopped and deleted after the check.
- Existing approved profile proxies, cookies and sticky-IP settings are not modified.
- An empty array disables this mode and returns to approved-profile monitoring.
- Up to 100 scraper proxy entries are accepted.

Proxy URLs are secrets and must never be committed.

### Token health

`GET /api/eventpulse/health` returns application health and a sanitised Multilogin token status without exposing the token.

Possible token states include:

- Missing.
- Unknown.
- Valid.
- Expiring.
- Expired.
- Non-expiring.

The warning window defaults to 72 hours. Even a requested non-expiring automation token may contain provider-managed technical expiry metadata, so production must follow the status reported by the health endpoint. Changing the Multilogin master password can invalidate active tokens.

The automation token authenticates the workspace. It does not replace the launcher. Production still needs a reachable Multilogin launcher.

## 8. Notifications

### Browser push

Browser push requires:

- A production HTTPS origin.
- `VITE_VAPID_PUBLIC_KEY` at application build time.
- Matching `VAPID_PRIVATE_KEY` and `VAPID_SUBJECT` at runtime.
- Browser notification permission.
- A saved push subscription for each device/browser.

Push notifications are persistent and include vibration and an Open HD-1 action when the device supports those features.

### Telegram

Telegram supports:

- One bot token.
- One or more comma-separated chat IDs.
- Rich HTML formatting.
- Event images when Telegram can fetch the image.
- A Buy Tickets link button.
- Fallback from image to HTML text, then to plain text if Telegram rejects rich formatting.
- Per-chat queues, provider rate-limit handling and retry-after support.

Group/channel destinations are paced more slowly to stay below Telegram's practical message limits.

### Discord

Discord supports:

- One or more comma-separated webhook URLs.
- Rich embeds containing event and ticket details.
- A link-button component when supported by the webhook.
- An embed-link fallback when Discord rejects the component format.
- Per-webhook queues and rate-limit handling.

### SMS and WhatsApp

Optional Twilio support is present for:

- Multiple SMS recipients.
- Multiple WhatsApp recipients.
- Comma-separated destination lists.

These channels remain optional and require valid Twilio sender and recipient configuration.

### Delivery audit

Each stored alert can record:

- `delivered_push`
- `delivered_sms`
- `delivered_whatsapp`
- `delivered_telegram`
- `delivered_discord`

The Test All Channels action uses the same provider delivery path but sends a sample ticket-format alert. A real preflight additionally proves that a real target page can create a ticket-specific alert.

## 9. Supabase data model

The backend currently accesses these tables:

- `eventpulse_targets`
- `eventpulse_profiles`
- `eventpulse_profile_sessions`
- `eventpulse_settings`
- `eventpulse_alerts`
- `eventpulse_push_subscriptions`

Supabase is accessed server-side through REST using the service-role key. The service-role key must never be exposed to the browser.

The code contains backward-compatibility handling for deployments that may be missing newer columns, including profile settings, folder IDs, Telegram/Discord settings, and target scheduling columns. Production should nevertheless use the complete current schema.

The SQL migration used to add current Telegram, Discord, scheduling and alert-delivery columns has previously been run by the project operator. The repository does not currently contain a dedicated versioned `supabase/migrations` directory, so the live database schema and any manually applied SQL must be preserved during handover.

## 10. Production environment variables

### Required core variables

```text
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
EVENTPULSE_CRON_SECRET
EVENTPULSE_PUBLIC_URL
EVENTPULSE_SCHEDULER_ENABLED
EVENTPULSE_SCHEDULER_TICK_MS
EVENTPULSE_PROFILE_MIN_INTERVAL_SECONDS
```

### Browser push

```text
VITE_VAPID_PUBLIC_KEY
VAPID_PRIVATE_KEY
VAPID_SUBJECT
```

`VITE_VAPID_PUBLIC_KEY` is a build-time value in the Dockerfile. Changing it requires rebuilding the application image.

### Telegram and Discord

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_IDS
DISCORD_WEBHOOK_URLS
```

### Multilogin

```text
MULTILOGIN_API_TOKEN
MULTILOGIN_TOKEN_EXPIRY_WARNING_HOURS
MULTILOGIN_LAUNCHER_ENDPOINT
MULTILOGIN_CDP_HOST
MULTILOGIN_HEADLESS
MULTILOGIN_PROXY_CREDENTIALS
MULTILOGIN_SCRAPER_PROXIES
```

### Optional Twilio

```text
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_SMS_FROM
TWILIO_SMS_TO
TWILIO_WHATSAPP_FROM
TWILIO_WHATSAPP_TO
```

### Advanced/test-only controls implemented in code

```text
EVENTPULSE_SYSTEM_NOTICES_TO_CHANNELS
EVENTPULSE_ONLY_CHANNELS
EVENTPULSE_LOCAL_BROWSER
CHROME_PATH
TELEGRAM_API_BASE_URL
```

These advanced variables are not all listed in `.env.example`. They should be used only for controlled operations or test environments.

Legacy/alternate Supabase variable names are also recognised for compatibility, but production should prefer `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`.

## 11. Docker and production topology

### Dockerfile

The Dockerfile:

- Installs dependencies with `npm ci`.
- Builds the application with Node 22 Alpine.
- Copies only the generated `.output` directory into the runtime image.
- Exposes port 3000.
- Uses `/api/eventpulse/health` as the container health check.

### Production Compose model

`docker-compose.production.yml` defines:

- `launcher`: the Multilogin launcher image.
- `app`: the HD-1 application image.

The application shares the launcher's network namespace in the supplied Compose model. The launcher exposes its required internal ports, and the application connects to the launcher on its private endpoint/CDP host.

When deploying through Coolify, the equivalent requirements are:

- Application and launcher must be able to reach each other privately.
- The production domain must route to application port 3000.
- The launcher API and CDP ports must not be unnecessarily exposed to the public Internet.
- Exactly one application instance must run the scheduler.
- Secrets must be configured in the deployment platform, not in committed files.

## 12. Completed client-driven changes

The project has been updated to cover these client requests:

- Product renamed to HD-1 Drop Monitor.
- Flexible target creation with event, venue, URL, section, quantity, price, type and time-window controls.
- Approved Multilogin profile selection.
- Sticky residential profile behaviour retained.
- Auto-rotation disabled by default for approved profiles.
- Manual profile pause/resume controls.
- Optional separate rotating scraper proxy pool.
- Browser push integration.
- Telegram bot integration.
- Discord webhook integration.
- Optional SMS and WhatsApp integration.
- Provider delivery flags stored in Supabase.
- Global interval controls connected to the production scheduler.
- Captcha notification suppression.
- Ticket-specific Telegram and Discord formatting.
- Provider queues and rate-limit handling.
- PWA install prompt at the lower-right.
- Responsive left-navigation modals and mobile navigation.
- Docker production build and health endpoint.
- Client handover, testing and operating guides.
- Real live-drop demonstration video with UK English narration.

## 13. Real preflight evidence

A controlled real preflight was completed on 16 November 2026.

The test:

- Used an official Ticketmaster UK event page for An Intimate Evening with First Aid Kit.
- Used one of the client-approved Multilogin profiles.
- Did not change the profile's proxy or enable auto-rotation.
- Used Check and send alert once.
- Detected one resale Front Stalls ticket.
- Detected section STALLS, row L and a price of GBP 77.59.
- Created a real ticket-specific alert.
- Recorded successful push, Telegram and Discord delivery flags.
- Displayed the real Discord webhook message in the configured channel.
- Used the stored Telegram delivery result because the Telegram destination is controlled by the client.
- Did not add a ticket to a basket, attempt checkout, change an account, or change a proxy.
- Removed the temporary test target after evidence was captured.
- Kept the alert audit record for verification.

This preflight was an operational test, not a source-code change.

## 14. Current verification status

Verification run on 17 November 2026:

- TypeScript check: passed (`npx tsc --noEmit`).
- Production build: passed (`npm run build`).
- Unit tests: 11 passed, 0 failed (`npm test`).
- Docker-based end-to-end test: not executed because Docker Desktop's Linux engine was not running during this consolidation. The failure occurred before the E2E application test began.

The passing unit coverage includes:

- Ticketmaster inventory URL recognition.
- Event details from JSON-LD and URL.
- Real facet and quick-pick conversion.
- Sold-out handling.
- No-inventory safety.
- Premium, section, price and quantity filters.
- Client alert formatting and channel limits.
- New-stock/drop detection.
- Protection against treating blocks, removed pages, captchas or errors as stock.
- Avoiding false captcha detection from normal reCAPTCHA scripts.

The production build emitted a non-blocking Vite notice that native tsconfig path resolution could replace the current `vite-tsconfig-paths` plugin.

## 15. Known limitations and risks

### No automatic basket or checkout

The application does not safely select tickets, add them to a basket, or continue checkout. The Open Ticket Page link opens the target URL and appends useful filter query parameters, but ticket sites are not guaranteed to interpret those parameters as cart instructions.

Site-specific basket automation remains high-risk because it can affect live client accounts, sessions, anti-bot checks and checkout state.

### Platform coverage is uneven

Ticketmaster has structured browser-visible inventory parsing. AXS, See Tickets, Gigs & Tours and Royal Albert Hall do not yet have equivalent dedicated extractors and may rely on generic page-text signals.

### Third-party dependencies can change

Monitoring depends on:

- Ticket websites and their internal APIs.
- Multilogin launcher behaviour.
- Proxy quality and authentication.
- Supabase availability.
- Telegram, Discord, Web Push and optional Twilio.

A successful preflight proves the complete chain at that moment; it does not guarantee that third-party systems will never change.

### In-memory operational state

Profile pause levels, recent profile load times, failure streaks, delivery queues and some stock comparison state are held in the running Node process. A restart clears those in-memory structures. Persistent target and alert data remains in Supabase.

### Database migration history

The repository does not contain a formal versioned Supabase migration directory. The production schema must be documented/exported before final handover so a new environment can be recreated reliably.

### Docker E2E dependency

The E2E suite starts a Dockerised headless Chrome container. Docker Desktop must be running before `npm run test:e2e` can pass.

## 16. Remaining production and client responsibilities

Before final acceptance, the following must be confirmed or maintained:

- Final production domain and DNS ownership.
- HTTPS/SSL working on the final production domain.
- Production Supabase availability and schema backup.
- Exactly one scheduler-enabled application replica.
- Running and privately reachable production Multilogin launcher.
- Valid Multilogin automation token and expiry monitoring.
- Approved profiles, profile IDs and folder IDs.
- Working profile sessions and sticky proxy subscriptions.
- Telegram bot membership/permissions in the final destination.
- Valid Discord webhook ownership.
- VAPID keys and browser subscriptions for every device that needs push.
- Optional Twilio credentials and final recipients if SMS/WhatsApp are required.
- Final target event URLs and filters.
- Client acceptance of the monitoring interval and profile safety interval.
- Client-run acceptance test and formal issue reporting.
- Rotation of any credential previously shared in ordinary chat.

For each final target, the client should supply or approve:

- Event URL and platform.
- Event and venue name.
- Sections/areas.
- Minimum quantity.
- Even-quantity rule.
- Maximum price.
- Allowed/excluded ticket types.
- Start and stop times.
- Assigned approved profile or scraper-pool use.

## 17. Recommended client acceptance test

1. Open the production dashboard over HTTPS.
2. Confirm Supabase is connected.
3. Confirm the Multilogin health endpoint reports a usable token and reachable launcher.
4. Save a sensible global refresh interval.
5. Enable the required alert channels.
6. Enable push on each client device that needs browser notifications.
7. Run Test All Channels and record the per-channel counts.
8. Add one approved safe target URL with a future automatic start time.
9. Run Check and send alert once.
10. Confirm the target's inventory result.
11. Confirm push, Telegram and Discord receive matching ticket-specific information.
12. Confirm a captcha state does not create repeated external messages.
13. Confirm the production scheduler checks an approved live target at the saved interval, subject to the profile safety interval.
14. Remove temporary test targets.
15. Report any failure with time, timezone, target, profile, status, provider flags and a screenshot/log excerpt that contains no secrets.

## 18. Important source files

### Application entry and routes

- `src/server.ts` - server entry, health endpoint, scheduler and secured monitor-run endpoint.
- `src/routes/index.tsx` - dashboard layout and responsive module navigation.
- `src/routes/__root.tsx` - root shell, metadata and error handling.

### Monitoring backend

- `src/lib/eventpulse/supabase.server.ts` - Supabase data access, scheduler pass, manual checks, alert creation and provider delivery.
- `src/lib/eventpulse/multilogin-browser.server.ts` - approved profile enforcement, launcher connection, token health and rotating quick profiles.
- `src/lib/eventpulse/page-capture.server.ts` - rendered page and inventory response capture.
- `src/lib/eventpulse/ticket-inventory.ts` - structured inventory parsing, filters, reports and rich ticket alerts.
- `src/lib/eventpulse/ticket-snapshot.ts` - page interpretation and safe fallback signals.
- `src/lib/eventpulse/profile-pause.server.ts` - automatic and manual profile pause logic.
- `src/lib/eventpulse/channel-queue.server.ts` - provider queues, pacing, retries and batching.
- `src/lib/eventpulse/types.ts` - shared dashboard and backend types.

### Frontend modules

- `src/components/eventpulse/MonitorGrid.tsx`
- `src/components/eventpulse/ProfilePanel.tsx`
- `src/components/eventpulse/SettingsPanel.tsx`
- `src/components/eventpulse/AlertLog.tsx`
- `src/components/eventpulse/SectionModal.tsx`
- `src/components/eventpulse/PwaInstallPrompt.tsx`
- `src/components/eventpulse/Nav.tsx`

### PWA and deployment

- `src/lib/pwa.ts`
- `public/sw.js`
- `public/manifest.webmanifest`
- `Dockerfile`
- `docker-compose.production.yml`
- `.env.example`

### Tests

- `tests/ticket-alerts.test.mjs`
- `tests/e2e/run.mjs`
- `tests/fixtures/`

### Handover documentation

- `CLIENT_HANDOVER.md`
- `CLIENT_INPUT_NEEDED_HD1.md`
- `HD1_DROP_MONITOR_HANDOFF.md`
- `output/pdf/HD1_Drop_Monitor_Client_Testing_Guide.pdf`
- `output/pdf/HD1_Monitoring_Operations_and_Preflight_Guide.pdf`

Some older handover documents describe requirements that have since been implemented, particularly Telegram, Discord and Multilogin access. This `PROJECT_CONTEXT.md` should be treated as the current consolidated overview, while the source code and live deployment remain the final technical source of truth.

## 19. Useful commands

Install and run locally:

```powershell
npm ci
npm run dev
```

Validate source:

```powershell
npx tsc --noEmit
npm test
npm run build
```

Run Docker-dependent E2E tests after Docker Desktop is ready:

```powershell
npm run test:e2e
```

Build and start the production Compose stack after all required secrets are configured:

```powershell
docker compose -f docker-compose.production.yml up -d --build
```

Check application/token health:

```text
GET /api/eventpulse/health
```

## 20. Operational definition of complete

The project is operationally complete when:

- Production services remain online.
- The application can reach Supabase and the Multilogin launcher.
- One scheduler instance checks approved targets on the saved schedule.
- A genuine ticket result is detected safely.
- Push, Telegram and Discord receive the same ticket-specific alert.
- Captcha and transient failures do not flood client channels.
- Approved profile cookies, proxies, sticky IPs and account state remain unchanged.
- The client completes acceptance testing and controls all production accounts and secrets.

