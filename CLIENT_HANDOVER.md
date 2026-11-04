# HD-1 Drop Monitor Handover

## Application access

- Production application: https://event-pulse.web-testlink.com/

## Current monitoring behavior

- Target URLs are checked at the interval saved under Global Controls & Settings.
- Ticket snapshots and changes are sent through enabled push, Telegram, Discord, SMS, and WhatsApp
  channels when their production credentials are configured.
- Captcha challenge status remains visible on the dashboard, but captcha notifications are disabled
  across every channel to prevent repeated pings.
- Optional rotating scraper proxies use temporary Multilogin quick profiles. They do not modify the
  existing approved profiles, cookies, or sticky proxy assignments.
- Clicking a ticket link opens the target URL on the user's own browser and network connection.

## Rotating proxy setup

Add `MULTILOGIN_SCRAPER_PROXIES` in Coolify as a JSON array. Example format:

```text
[
  "http://username:password@proxy-one.example:8000",
  "socks5://username:password@proxy-two.example:1080"
]
```

Use working residential or mobile scraping proxies supplied by the client or proxy provider. Keep
this value secret. The application rotates sequentially, one proxy per due target check, and starts
again at the first proxy after reaching the end. Use `[]` to disable this mode and return to regular
approved-profile monitoring.

## Production requirements

Production needs these services and secrets:

- Deployed HD-1 Drop Monitor application container.
- Multilogin launcher container on the same private network.
- Supabase URL and service-role key.
- Scheduler enabled on exactly one application replica.
- Multilogin automation token and launcher connection settings.
- VAPID public/private keys and subject for browser push.
- Telegram bot token and chat IDs.
- Discord webhook URL list.
- Optional Twilio settings for SMS and WhatsApp.
- Optional rotating scraper proxy pool.

Real credentials must remain in Coolify or another secret manager and must not be included in this
handover document or shared through unsecured messages.

## Acceptance test

1. Open production and save a refresh interval under Global Controls & Settings.
2. Enable the required alert channels and run Test All Channels.
3. Add one safe target URL and confirm its dashboard status updates at the saved interval.
4. Confirm push, Telegram, and Discord receive the same non-captcha monitor message.
5. Confirm a captcha page changes dashboard status without sending a captcha notification.
6. With a proxy pool configured, run several due checks and confirm no approved profile proxy or
   sticky-IP setting changes in Multilogin.
7. Open the ticket link and confirm it uses the user's normal browser/network connection.

## Credential handover

Account owners should provide or transfer access directly through each provider rather than placing
passwords in this document. Required ownership includes Coolify, Supabase, Multilogin, Telegram,
Discord, domain/DNS, and Twilio if used. Rotate any credential previously sent through chat after
handover.
