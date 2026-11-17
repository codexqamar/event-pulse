from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "HD1_Monitoring_Operations_and_Preflight_Guide.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#07111F")
NAVY_2 = colors.HexColor("#0F1E33")
SLATE = colors.HexColor("#26364D")
CYAN = colors.HexColor("#08B9D6")
GREEN = colors.HexColor("#19C58B")
AMBER = colors.HexColor("#F5B942")
ROSE = colors.HexColor("#F15B77")
INK = colors.HexColor("#182233")
MUTED = colors.HexColor("#59687B")
PALE = colors.HexColor("#F3F7FB")
LINE = colors.HexColor("#D8E1EA")
WHITE = colors.white


def register_fonts():
    regular = Path("C:/Windows/Fonts/segoeui.ttf")
    bold = Path("C:/Windows/Fonts/segoeuib.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("UI", str(regular)))
        pdfmetrics.registerFont(TTFont("UI-Bold", str(bold)))
        return "UI", "UI-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverKicker", fontName=FONT_BOLD, fontSize=10, leading=13,
    textColor=CYAN, tracking=1.4, alignment=TA_CENTER, spaceAfter=9,
))
styles.add(ParagraphStyle(
    name="CoverTitle", fontName=FONT_BOLD, fontSize=28, leading=33,
    textColor=WHITE, alignment=TA_CENTER, spaceAfter=14,
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName=FONT, fontSize=12.5, leading=18,
    textColor=colors.HexColor("#C7D4E5"), alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    name="H1x", fontName=FONT_BOLD, fontSize=20, leading=24,
    textColor=NAVY, spaceAfter=10, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="H2x", fontName=FONT_BOLD, fontSize=13, leading=17,
    textColor=SLATE, spaceBefore=10, spaceAfter=5, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="Bodyx", fontName=FONT, fontSize=9.2, leading=13.2,
    textColor=INK, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Smallx", fontName=FONT, fontSize=7.8, leading=10.5,
    textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="Bulletx", fontName=FONT, fontSize=9.1, leading=13.2,
    textColor=INK, leftIndent=13, firstLineIndent=-8, bulletIndent=3,
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="TableHead", fontName=FONT_BOLD, fontSize=7.7, leading=10,
    textColor=WHITE,
))
styles.add(ParagraphStyle(
    name="TableCell", fontName=FONT, fontSize=7.4, leading=10,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="TableCellBold", fontName=FONT_BOLD, fontSize=7.4, leading=10,
    textColor=INK,
))


def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def bullet(text):
    return Paragraph(f"- {text}", styles["Bulletx"])


def callout(title, text, accent=CYAN, background=PALE):
    data = [[
        Table([[""]], colWidths=[3 * mm], rowHeights=[20 * mm], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), accent),
        ])),
        Paragraph(f"<b>{title}</b><br/>{text}", ParagraphStyle(
            "Callout", parent=styles["Bodyx"], fontSize=8.6, leading=12,
            leftIndent=2, spaceAfter=0,
        )),
    ]]
    table = Table(data, colWidths=[5 * mm, 162 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 5),
        ("LEFTPADDING", (1, 0), (1, 0), 8),
        ("RIGHTPADDING", (1, 0), (1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def checklist(rows):
    data = [[P("STEP", "TableHead"), P("ACTION", "TableHead"), P("SUCCESS CONDITION", "TableHead")]]
    for idx, action, success in rows:
        data.append([P(str(idx), "TableCellBold"), P(action, "TableCell"), P(success, "TableCell")])
    table = Table(data, colWidths=[13 * mm, 78 * mm, 76 * mm], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_2),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def requirement_table(rows):
    data = [[P("REQUIREMENT", "TableHead"), P("WHAT MUST BE READY", "TableHead"), P("WHY IT MATTERS", "TableHead")]]
    for name, ready, why in rows:
        data.append([P(name, "TableCellBold"), P(ready, "TableCell"), P(why, "TableCell")])
    table = Table(data, colWidths=[40 * mm, 68 * mm, 59 * mm], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_2),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(20 * mm, PAGE_H - 17 * mm, PAGE_W - 20 * mm, PAGE_H - 17 * mm)
        canvas.setFont(FONT_BOLD, 8)
        canvas.setFillColor(SLATE)
        canvas.drawString(20 * mm, PAGE_H - 13 * mm, "HD-1 DROP MONITOR")
        canvas.setFont(FONT, 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - 20 * mm, PAGE_H - 13 * mm, "Monitoring Operations and Preflight Guide")
        canvas.line(20 * mm, 16 * mm, PAGE_W - 20 * mm, 16 * mm)
        canvas.setFont(FONT, 7.3)
        canvas.drawString(20 * mm, 11 * mm, "Operational guidance - no passwords or secret values included")
        canvas.drawRightString(PAGE_W - 20 * mm, 11 * mm, f"Page {doc.page}")
    canvas.restoreState()


class GuideDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=23 * mm,
            bottomMargin=20 * mm,
            title="HD-1 Drop Monitor - Monitoring Operations and Preflight Guide",
            author="HD-1 Drop Monitor Project",
            subject="Operational requirements for reliable monitoring and alert delivery",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(PageTemplate(id="guide", frames=frame, onPage=header_footer))


story = []

# Cover
cover = Table([["HD-1"]], colWidths=[34 * mm], rowHeights=[34 * mm], hAlign="CENTER")
cover.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), CYAN),
    ("TEXTCOLOR", (0, 0), (-1, -1), NAVY),
    ("FONTNAME", (0, 0), (-1, -1), FONT_BOLD),
    ("FONTSIZE", (0, 0), (-1, -1), 17),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor("#50D8EA")),
]))

cover_panel = Table([[
    [
        Spacer(1, 12 * mm),
        cover,
        Spacer(1, 12 * mm),
        P("OPERATIONS GUIDE", "CoverKicker"),
        P("Monitoring Setup,<br/>Live Preflight and Production Readiness", "CoverTitle"),
        P("What must be running, configured and verified so HD-1 Drop Monitor can continuously check target URLs and deliver reliable ticket alerts.", "CoverSub"),
        Spacer(1, 12 * mm),
        Table([
            [P("SCOPE", "TableHead"), P("ONE-TIME SETUP", "TableHead"), P("DAILY OPERATION", "TableHead")],
            [P("Production and controlled testing", "TableCell"), P("Services, credentials, networking", "TableCell"), P("Targets, intervals, alerts, recovery", "TableCell")],
        ], colWidths=[50 * mm, 50 * mm, 50 * mm], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), SLATE),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#EAF1F8")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#60748C")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ])),
        Spacer(1, 19 * mm),
        P("Prepared for operational handover and client acceptance testing", "CoverSub"),
    ]
]], colWidths=[177 * mm], rowHeights=[257 * mm])
cover_panel.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), NAVY),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 13 * mm),
    ("RIGHTPADDING", (0, 0), (-1, -1), 13 * mm),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
story.extend([Spacer(1, -12 * mm), cover_panel, PageBreak()])

# Purpose
story += [
    P("1. What this document is for", "H1x"),
    P("A successful preflight proves that the complete operational chain works at that moment. It is not a code change. It is a controlled run that checks the real services, credentials, browser profile, ticket page and notification providers together."),
    callout(
        "The monitoring chain",
        "Dashboard target -> scheduler or manual check -> Multilogin launcher -> ticket website -> inventory result -> Supabase audit record -> push, Telegram and Discord delivery.",
        GREEN,
        colors.HexColor("#ECFAF5"),
    ),
    Spacer(1, 6 * mm),
    P("Two separate outcomes must be proven", "H2x"),
    requirement_table([
        ("Monitoring works", "The target is due, the launcher can start the assigned browser route, and the event page returns usable inventory.", "Without this, there is no reliable ticket result to alert on."),
        ("Notifications work", "The enabled channel credentials are valid and each provider accepts the same alert payload.", "A successful scrape is not useful if the client never receives it."),
        ("Continuous operation works", "Exactly one scheduler instance remains online and reloads the saved global interval.", "Manual checks alone do not provide unattended monitoring."),
    ]),
    Spacer(1, 6 * mm),
    callout(
        "Important distinction",
        "Test All Channels proves provider configuration. A real preflight additionally proves that a ticket URL can be checked and that a real inventory result can create a ticket-specific alert.",
        AMBER,
        colors.HexColor("#FFF7E5"),
    ),
    Spacer(1, 7 * mm),
    P("Safe operating boundaries", "H2x"),
    bullet("Do not change a client's approved profile proxy, cookies, login state or sticky-IP assignment during a monitoring test."),
    bullet("Do not enable auto-rotation on approved checkout profiles."),
    bullet("Do not attempt checkout or payment. Monitoring and alert delivery are the scope of this guide."),
    bullet("Use only approved profiles and an approved event URL for any real preflight."),
    bullet("Remove temporary test targets after recording or acceptance testing, unless the client wants them to remain live."),
]
story.append(PageBreak())

# Prereqs
story += [
    P("2. What must be ready before monitoring", "H1x"),
    requirement_table([
        ("Application", "The HD-1 application container is healthy and the production URL loads.", "The dashboard and API must remain available."),
        ("Supabase", "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are stored as deployment secrets and the database is reachable.", "Targets, settings, profiles, alert records and subscriptions are stored here."),
        ("Scheduler", "EVENTPULSE_SCHEDULER_ENABLED=true on exactly one application replica. Other replicas use false.", "Two enabled replicas can create duplicate checks and alerts."),
        ("Public URL", "EVENTPULSE_PUBLIC_URL contains the final HTTPS production address.", "Push links and server callbacks must resolve to the deployed application."),
        ("Multilogin token", "MULTILOGIN_API_TOKEN is a valid automation token. Token status is checked through /api/eventpulse/health.", "The application needs workspace access to launch monitoring profiles."),
        ("Launcher", "A Multilogin launcher is online and reachable from the application container using MULTILOGIN_LAUNCHER_ENDPOINT and MULTILOGIN_CDP_HOST.", "A token alone cannot run browser profiles."),
        ("Profiles", "Approved profiles exist, are logged in where required, and keep their client-assigned sticky residential IPs.", "Authenticated inventory may only be visible inside the real profile session."),
        ("Push", "VITE_VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY and VAPID_SUBJECT are configured. The user's browser has granted notification permission.", "Both server credentials and a browser subscription are required."),
        ("Telegram", "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_IDS are correct. The bot can post to the destination.", "Telegram delivery fails if the bot lacks permission or the chat ID is wrong."),
        ("Discord", "DISCORD_WEBHOOK_URLS contains the intended webhook URL or URLs.", "The webhook must still exist and allow posting to the channel."),
        ("Optional proxies", "MULTILOGIN_SCRAPER_PROXIES contains valid secret proxy URLs, or [] when disabled.", "The separate scraper pool may rotate without changing approved sticky profiles."),
    ]),
    Spacer(1, 5 * mm),
    callout(
        "Secret handling",
        "Keep tokens, service-role keys, webhook URLs and proxy credentials only in Coolify or another deployment secret manager. Never place real values in source control, PDFs or ordinary chat messages.",
        ROSE,
        colors.HexColor("#FFF0F3"),
    ),
]
story.append(PageBreak())

# Production setup
story += [
    P("3. One-time production setup", "H1x"),
    checklist([
        (1, "Deploy the application container and connect it to the production HTTPS domain.", "The dashboard and /api/eventpulse/health respond successfully."),
        (2, "Connect the application to production Supabase using the URL and service-role key stored as secrets.", "The header reports Supabase connected and existing settings load."),
        (3, "Run the Multilogin launcher as a second service on the same private network where possible.", "The application container resolves and reaches the launcher endpoint."),
        (4, "Add the Multilogin automation token, launcher endpoint, CDP host and production headless setting.", "The health endpoint reports a usable token and launcher state."),
        (5, "Enable the scheduler on one application replica only and leave it disabled on any extra web replica.", "Only one process performs due checks."),
        (6, "Configure VAPID, Telegram and Discord secrets. Enable only the channels the client intends to use.", "Test All Channels returns a successful result for every enabled provider."),
        (7, "Save Global Controls & Settings, including the refresh interval.", "The saved interval remains after a page reload."),
        (8, "Add one safe acceptance target and assign an approved profile or the separate rotating scraper pool.", "The target appears with the expected URL, filters, profile and timing window."),
        (9, "Run a controlled real preflight and compare the dashboard, audit record and received messages.", "All surfaces report the same event and ticket details."),
        (10, "Remove the temporary acceptance target or convert it into an approved live target.", "No unapproved repeated test alerts remain active."),
    ]),
    Spacer(1, 6 * mm),
    P("Recommended production values", "H2x"),
    requirement_table([
        ("Scheduler tick", "EVENTPULSE_SCHEDULER_TICK_MS=1000", "The scheduler evaluates due work frequently; it does not force every target to load every second."),
        ("Profile safety interval", "EVENTPULSE_PROFILE_MIN_INTERVAL_SECONDS=60 unless a safer client-approved value is chosen.", "Prevents the same profile from loading ticket pages too aggressively."),
        ("Token warning", "MULTILOGIN_TOKEN_EXPIRY_WARNING_HOURS=72", "Creates advance notice when a finite token enters its warning window."),
        ("Launcher mode", "MULTILOGIN_HEADLESS=true for a supported production launcher; false for local desktop testing.", "Matches the browser environment being used."),
        ("Proxy pool", "MULTILOGIN_SCRAPER_PROXIES=[] when rotating scraping proxies are not approved or configured.", "Avoids accidental use of unknown proxy infrastructure."),
    ]),
    Spacer(1, 5 * mm),
    callout(
        "Interval behaviour",
        "The scheduler reloads Global Controls & Settings from Supabase. Increasing or decreasing the global refresh interval changes when targets next become due without restarting the container. The profile safety interval can still impose a longer minimum between page loads through the same profile.",
        CYAN,
    ),
]
story.append(PageBreak())

# Preflight
story += [
    P("4. Controlled real preflight procedure", "H1x"),
    P("Use this procedure before client acceptance, after credential changes, after moving production infrastructure, or when monitoring has stopped producing trustworthy results."),
    checklist([
        (1, "Confirm Supabase, the application container and the Multilogin launcher are healthy.", "No dependency is offline before the test begins."),
        (2, "Confirm the selected profile and its sticky proxy are already working. Do not edit its proxy settings.", "The profile can open the intended site without an authentication error."),
        (3, "Choose one approved live event URL with known or likely inventory.", "The test uses a real page, not a fabricated alert."),
        (4, "Create a temporary target with a clear test name, quantity, filters and the approved profile.", "The dashboard shows exactly what will be checked."),
        (5, "Set the automatic monitoring start time in the future while recording the one-off test.", "The background scheduler cannot repeat the preflight unexpectedly."),
        (6, "Select Check & send alert once.", "One controlled live request begins."),
        (7, "Wait for the check to finish. Do not click repeatedly while the browser route is still running.", "The target changes to Tickets Available, No Match, Unavailable, Captcha, or a clear failure state."),
        (8, "If tickets are found, compare event, section, row, quantity and price on the dashboard and alert record.", "The stored result matches the ticket website response."),
        (9, "Verify push, Telegram and Discord separately.", "Each enabled provider reports delivery and the received message contains the same ticket details."),
        (10, "Delete the temporary target after evidence is captured, unless the client approves it for continuous monitoring.", "No unintended scheduled checks remain."),
    ]),
    Spacer(1, 5 * mm),
    callout(
        "What a successful preflight proves",
        "At that time, the application could reach Supabase, launch the approved browser route, read a real ticket result, save the alert and deliver it to the configured providers. It does not guarantee that ticket sites, proxies or third-party services will never change later.",
        GREEN,
        colors.HexColor("#ECFAF5"),
    ),
    Spacer(1, 5 * mm),
    callout(
        "Captcha behaviour",
        "Captcha status remains visible on the target, but captcha pages do not create push, Telegram, Discord, SMS or WhatsApp alerts. This prevents repeated challenge notifications on every interval.",
        AMBER,
        colors.HexColor("#FFF7E5"),
    ),
]
story.append(PageBreak())

# Daily operation
story += [
    P("5. How continuous monitoring should be operated", "H1x"),
    P("Once production is accepted, the scheduler performs due checks. Operators control the intended behaviour from the dashboard rather than by restarting containers."),
    P("For every target", "H2x"),
    bullet("Use the exact event URL and platform."),
    bullet("Set the minimum ticket quantity and any section, price, ticket-type or even-quantity filters."),
    bullet("Choose the correct approved Multilogin profile, or use the separately configured rotating scraper pool."),
    bullet("Set start and stop monitoring times when the target should only run within a specific window."),
    bullet("Pause targets that should not be checked. Delete targets only when their monitoring record is no longer needed."),
    P("For Global Controls & Settings", "H2x"),
    bullet("Set the refresh interval to the operational frequency required by the client."),
    bullet("Remember that the same profile is protected by the profile minimum interval, which may be longer than the global interval."),
    bullet("Enable only configured channels. Run Test All Channels after changing any provider credentials."),
    bullet("Keep exactly one scheduler-enabled replica."),
    P("For notification providers", "H2x"),
    requirement_table([
        ("Browser push", "The user must install or open the production site, grant notifications and maintain a valid push subscription.", "VAPID credentials alone do not create a device subscription."),
        ("Telegram", "The bot must remain a member or administrator of the configured destination with permission to post.", "The application queues alerts and honours provider rate limits."),
        ("Discord", "The webhook must remain valid and linked to the intended channel.", "Deleting or regenerating the webhook requires updating the deployment secret."),
    ]),
    Spacer(1, 5 * mm),
    callout(
        "Rate limiting",
        "Telegram and Discord use per-destination queues. When several alerts arrive together, the application spaces requests according to provider limits and may combine queued alerts rather than dropping them.",
        CYAN,
    ),
]
story.append(PageBreak())

# Troubleshooting
story += [
    P("6. Troubleshooting and recovery", "H1x"),
    requirement_table([
        ("No targets are checking", "Verify scheduler enabled on one replica, Supabase connection, saved interval, target pause state, and start/stop window.", "A future start time or paused target is intentionally skipped."),
        ("Multilogin cannot launch", "Check /api/eventpulse/health, token status, launcher endpoint, private-network reachability and launcher logs.", "A valid token does not help if the launcher is unreachable."),
        ("Proxy authentication error", "Ask the proxy owner to repair credentials while preserving approved sticky assignments. Do not replace or rotate a checkout profile without approval.", "Ticket sites may reject the browser route before the event loads."),
        ("Token near expiry", "Create or rotate the automation token in the Multilogin account and update the deployment secret. Re-run health and preflight checks.", "The health endpoint reports the provider-managed expiry; password changes can also invalidate tokens."),
        ("Telegram not received", "Check delivered_telegram, bot token, chat ID, membership, posting permission, queue delay and Telegram network reachability.", "A provider success flag distinguishes accepted delivery from a local UI problem."),
        ("Discord not received", "Check delivered_discord, webhook validity, destination channel and provider response.", "A deleted or regenerated webhook stops delivery until the secret is updated."),
        ("Push not received", "Check VAPID values, HTTPS, browser notification permission and the device's current subscription.", "Push is device-specific and can be revoked by the browser or operating system."),
        ("Repeated duplicate alerts", "Confirm only one scheduler-enabled replica and check for duplicate targets using the same URL.", "Multiple workers or duplicate targets can send the same result more than once."),
        ("Captcha status", "Treat it as a site-access condition. Review profile health and proxy reputation. Do not expect a captcha notification.", "Captcha alerts are intentionally suppressed."),
    ]),
    Spacer(1, 6 * mm),
    P("Evidence to collect when reporting an issue", "H2x"),
    bullet("Production time and timezone of the failed check."),
    bullet("Target name, URL, assigned profile and expected filter result."),
    bullet("Dashboard target status and last response time or status code."),
    bullet("Alert record delivery flags for push, Telegram and Discord."),
    bullet("Relevant application, scheduler and launcher log excerpt without exposing secrets."),
    bullet("Screenshot of the received message or provider error."),
]
story.append(PageBreak())

# Acceptance and handover
story += [
    P("7. Completion and client acceptance checklist", "H1x"),
    checklist([
        (1, "Production dashboard loads over HTTPS and reports Supabase connected.", "PASS / FAIL"),
        (2, "Exactly one production replica has the scheduler enabled.", "PASS / FAIL"),
        (3, "Multilogin health reports a reachable launcher and usable automation token.", "PASS / FAIL"),
        (4, "Approved profiles retain their assigned sticky residential proxies and auto-rotation remains off.", "PASS / FAIL"),
        (5, "Global refresh interval saves and a due target follows it, subject to the profile safety interval.", "PASS / FAIL"),
        (6, "Test All Channels succeeds for every enabled notification provider.", "PASS / FAIL"),
        (7, "A controlled real preflight detects a genuine event result.", "PASS / FAIL"),
        (8, "Push, Telegram and Discord receive matching ticket-specific content.", "PASS / FAIL"),
        (9, "Captcha status does not create repeated external notifications.", "PASS / FAIL"),
        (10, "Temporary targets are removed and approved live targets remain documented.", "PASS / FAIL"),
        (11, "Account ownership and secret-manager access are transferred to the client.", "PASS / FAIL"),
        (12, "The client performs the acceptance test and reports any issue with the evidence list from Section 6.", "PASS / FAIL"),
    ]),
    Spacer(1, 7 * mm),
    callout(
        "Operational definition of complete",
        "The project is operationally complete when production services stay online, an approved target is checked on the saved schedule, a genuine ticket result is detected, and every enabled channel receives the same alert without changing client profiles, proxies or account state.",
        GREEN,
        colors.HexColor("#ECFAF5"),
    ),
    Spacer(1, 8 * mm),
    P("Client responsibilities after handover", "H2x"),
    bullet("Keep Supabase, Coolify, Multilogin, domain, Telegram and Discord accounts active and accessible."),
    bullet("Renew or rotate credentials before expiry and update the deployment secret manager."),
    bullet("Maintain working profiles and proxy subscriptions."),
    bullet("Provide approved event URLs, filters, monitoring windows and profile assignments."),
    bullet("Run acceptance checks after infrastructure, credentials or ticket-site behaviour changes."),
    Spacer(1, 7 * mm),
    P("This guide intentionally contains no passwords, API tokens, service-role keys, webhook URLs or proxy credentials.", "Smallx"),
]


doc = GuideDoc(str(OUT))
doc.build(story)
print(OUT)
