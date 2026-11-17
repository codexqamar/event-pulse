from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, HRFlowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from pathlib import Path

ROOT = Path(r"D:\projects\event-pulse")
OUT = ROOT / "output" / "pdf" / "HD1_Drop_Monitor_Client_Testing_Guide.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = HexColor("#0B1426")
NAVY_2 = HexColor("#14213A")
CYAN = HexColor("#13B8D3")
GREEN = HexColor("#16A879")
RED = HexColor("#DC4C64")
AMBER = HexColor("#D99614")
SLATE = HexColor("#526176")
LIGHT = HexColor("#EEF3F8")
PALE_CYAN = HexColor("#E8F8FB")
PALE_GREEN = HexColor("#EAF8F3")
WHITE = colors.white

font_regular = "Helvetica"
font_bold = "Helvetica-Bold"
dejavu = Path(r"C:\Windows\Fonts\DejaVuSans.ttf")
dejavu_bold = Path(r"C:\Windows\Fonts\DejaVuSans-Bold.ttf")
if dejavu.exists() and dejavu_bold.exists():
    pdfmetrics.registerFont(TTFont("DejaVu", str(dejavu)))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(dejavu_bold)))
    font_regular, font_bold = "DejaVu", "DejaVu-Bold"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", fontName=font_bold, fontSize=27, leading=33,
    textColor=WHITE, alignment=TA_LEFT, spaceAfter=10
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName=font_regular, fontSize=12, leading=18,
    textColor=HexColor("#C7D7E8"), spaceAfter=6
))
styles.add(ParagraphStyle(
    name="H1x", fontName=font_bold, fontSize=19, leading=24,
    textColor=NAVY, spaceBefore=2, spaceAfter=10
))
styles.add(ParagraphStyle(
    name="H2x", fontName=font_bold, fontSize=13.5, leading=18,
    textColor=NAVY_2, spaceBefore=10, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="H3x", fontName=font_bold, fontSize=10.5, leading=14,
    textColor=CYAN, spaceBefore=7, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="Bodyx", fontName=font_regular, fontSize=9.3, leading=14,
    textColor=HexColor("#263447"), spaceAfter=5
))
styles.add(ParagraphStyle(
    name="Smallx", fontName=font_regular, fontSize=7.8, leading=11,
    textColor=SLATE
))
styles.add(ParagraphStyle(
    name="StepNum", fontName=font_bold, fontSize=11, leading=14,
    textColor=WHITE, alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    name="StepTitle", fontName=font_bold, fontSize=10.4, leading=14,
    textColor=NAVY
))
styles.add(ParagraphStyle(
    name="Cell", fontName=font_regular, fontSize=8.2, leading=11,
    textColor=HexColor("#263447")
))
styles.add(ParagraphStyle(
    name="CellBold", fontName=font_bold, fontSize=8.2, leading=11,
    textColor=NAVY
))
styles.add(ParagraphStyle(
    name="CellHeader", fontName=font_bold, fontSize=8.2, leading=11,
    textColor=WHITE
))
styles.add(ParagraphStyle(
    name="Callout", fontName=font_regular, fontSize=8.8, leading=13,
    textColor=NAVY
))

def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])

def bullet(text):
    return P(f"<font color='#13B8D3'>•</font> {text}")

def checkbox(text):
    return P(f"<font color='#526176'>[ ]</font>&nbsp;&nbsp;{text}")

def callout(title, text, colour=CYAN, bg=PALE_CYAN):
    data = [[P(title, "CellBold"), P(text, "Callout")]]
    t = Table(data, colWidths=[38*mm, 132*mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX", (0,0), (-1,-1), 0.5, colour),
        ("LINEBEFORE", (0,0), (0,-1), 4, colour),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
        ("RIGHTPADDING", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

def step(number, title, actions, expected):
    num = Table([[P(str(number), "StepNum")]], colWidths=[11*mm], rowHeights=[11*mm])
    num.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CYAN),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOX", (0,0), (-1,-1), 0, CYAN),
    ]))
    body = [P(title, "StepTitle")]
    for action in actions:
        body.append(P(f"<font color='#13B8D3'>•</font> {action}", "Cell"))
    body.append(P(f"<b>Expected:</b> {expected}", "Cell"))
    body_table = Table([[x] for x in body], colWidths=[154*mm])
    body_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 1),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
    ]))
    t = Table([[num, body_table]], colWidths=[16*mm, 154*mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LINEBELOW", (0,0), (-1,-1), 0.4, HexColor("#D9E2EC")),
    ]))
    return KeepTogether([t, Spacer(1, 2*mm)])

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page > 1:
        canvas.setStrokeColor(HexColor("#D9E2EC"))
        canvas.line(18*mm, 15*mm, w-18*mm, 15*mm)
        canvas.setFont(font_regular, 7.5)
        canvas.setFillColor(SLATE)
        canvas.drawString(18*mm, 10*mm, "Controlled testing only - no basket or checkout automation")
        canvas.drawRightString(w-18*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
    topMargin=22*mm, bottomMargin=19*mm,
    title="HD-1 Drop Monitor - Client Testing and Acceptance Guide",
    author="HD-1 Drop Monitor Project Team",
    subject="Step-by-step client testing instructions",
)

story = []

# Cover
cover = Table([
    [P("HD-1 DROP MONITOR", "CoverTitle")],
    [P("Client Testing and Acceptance Guide", "CoverSub")],
    [Spacer(1, 12*mm)],
    [P("A practical, step-by-step procedure for testing the portal, target monitoring, scheduled checks, browser push, Telegram, Discord, Multilogin and safe ticket-page handoff.", "CoverSub")],
    [Spacer(1, 12*mm)],
    [P("Version 1.0  |  Prepared 16 November 2026", "CoverSub")],
], colWidths=[174*mm], rowHeights=[None]*6)
cover.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), NAVY),
    ("LEFTPADDING", (0,0), (-1,-1), 17*mm),
    ("RIGHTPADDING", (0,0), (-1,-1), 17*mm),
    ("TOPPADDING", (0,0), (0,0), 28*mm),
    ("BOTTOMPADDING", (0,-1), (-1,-1), 28*mm),
]))
story += [Spacer(1, 22*mm), cover, Spacer(1, 12*mm)]
story.append(callout(
    "Purpose",
    "This guide lets the client prove each function on their own deployment. Record each result in the acceptance table at the end. Tests must use approved profiles, approved target URLs and non-destructive actions only.",
    GREEN, PALE_GREEN,
))
story += [Spacer(1, 7*mm), P("Safety boundaries", "H2x")]
for x in [
    "Do not change existing Multilogin proxy assignments, sticky IPs, profile fingerprints or ticket-site account details.",
    "Do not enable automatic basket or checkout actions. Open Ticket Page only hands the user to the event page.",
    "Use one safe target first. Avoid high-frequency live testing until notifications and rate limits are confirmed.",
    "Keep tokens, service-role keys, webhooks and proxy passwords in the deployment secret manager.",
]: story.append(bullet(x))
story.append(PageBreak())

# Preflight
story += [P("1. Before testing", "H1x"), P("The portal cannot be tested correctly until every required service is online. Complete this checklist first.")]
preflight_rows = [[P("Check", "CellHeader"), P("Required condition", "CellHeader"), P("Done", "CellHeader")]]
preflight = [
    ("Application", "Production URL loads over HTTPS without a certificate warning."),
    ("Supabase", "Database is online; dashboard does not show a Supabase error or zero data caused by an outage."),
    ("Scheduler", "Exactly one application replica has EVENTPULSE_SCHEDULER_ENABLED=true."),
    ("Multilogin", "Launcher is reachable from the application; approved profiles are available and their ticket-site sessions are logged in."),
    ("Telegram", "Bot token and chat IDs are configured; the bot can post messages in the destination chat or channel."),
    ("Discord", "At least one current webhook URL is configured for the intended alert channel."),
    ("Web push", "VAPID public key, private key and subject are configured; HTTPS is active."),
    ("Test device", "Desktop or mobile browser allows notifications; Focus/Do Not Disturb is disabled for the test."),
]
for a,b in preflight: preflight_rows.append([P(a,"CellBold"), P(b,"Cell"), P("[ ]", "CellBold")])
t=Table(preflight_rows,colWidths=[29*mm,128*mm,13*mm],repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY_2),("TEXTCOLOR",(0,0),(-1,0),WHITE),
    ("GRID",(0,0),(-1,-1),0.35,HexColor("#CFD9E5")),("VALIGN",(0,0),(-1,-1),"TOP"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LIGHT]),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
]))
story += [t, Spacer(1,5*mm)]
story.append(callout("Stop condition", "If Supabase is unavailable, the target list, settings, alert log and scheduler state cannot be trusted. Restore Supabase before continuing. If Telegram is blocked on the tester's network, test from the production server or another permitted network route.", RED, HexColor("#FCECEF")))
story += [Spacer(1,4*mm), P("Recommended first-test settings", "H2x")]
for x in [
    "Start with a 30-second refresh interval to avoid repeated alerts while settings are being verified.",
    "Enable browser push, Telegram and Discord. Leave SMS and WhatsApp off unless their provider credentials are already approved.",
    "Use a client-approved event URL and one approved Multilogin profile.",
    "Keep auto-rotate disabled for permanent client profiles. Use the separate scraper proxy pool only when deliberately testing server-side rotation.",
]: story.append(checkbox(x))
story.append(PageBreak())

# Health and portal
story += [P("2. Open the portal and confirm system health", "H1x")]
story.append(step(1, "Open the production portal", [
    "Open the supplied production URL in Chrome or another supported Chromium browser.",
    "Confirm the page loads over HTTPS and the HD-1 Drop Monitor dashboard appears.",
], "No browser security warning, blank page or server error is shown."))
story.append(step(2, "Check the dashboard header", [
    "Confirm the Supabase status is connected.",
    "Confirm the target count is believable and the Multilogin state policy is ready.",
    "Review Active Monitors, Ticket Alerts Detected, Connected Proxy Profiles and Average Response Time.",
], "The dashboard shows live project data rather than fallback or empty data."))
story.append(step(3, "Check the server health endpoint", [
    "Open /api/eventpulse/health on the production domain.",
    "Confirm ok is true and the Multilogin automation token status is valid.",
    "If an expiry warning is shown, replace the token before the reported expiry window.",
], "Health returns successfully without exposing the token value."))
story.append(step(4, "Review all portal modules", [
    "Open Monitors, Profiles, Alerts and Settings from the left sidebar.",
    "Confirm every modal or panel fits the desktop screen and can be closed.",
    "Repeat on a narrow mobile viewport if mobile use is planned.",
], "Each control opens the correct responsive module and no content is clipped."))
story.append(callout("Evidence to keep", "Capture the dashboard header, health result and one screenshot of each module. Do not include secrets in screenshots.", CYAN, PALE_CYAN))
story.append(PageBreak())

# Notifications
story += [P("3. Test notification channels", "H1x"), P("Run channel tests before adding a live target. This separates delivery configuration from ticket-site behaviour.")]
story.append(step(5, "Save a controlled refresh interval", [
    "Open Settings.",
    "Set Global Refresh Interval to 30 seconds for the first test.",
    "Enable Desktop / Mobile Push, Telegram Alerts and Discord Alerts.",
    "Select Save Backend Settings and wait for Settings saved to Supabase.",
], "The saved values remain after refreshing the page."))
story.append(step(6, "Enable browser push", [
    "Select Enable Push.",
    "Choose Allow when the browser asks for notification permission.",
    "Select Test Notification.",
], "A browser notification appears. If it does not, check browser permission, operating-system notification settings and Focus/Do Not Disturb."))
story.append(step(7, "Send the controlled multi-channel test", [
    "Select Test All Channels once.",
    "Wait for the result line under the buttons.",
    "Do not click repeatedly while the button is busy or while provider queues are delivering.",
], "The result reports push 1, Telegram 1 and Discord 1 when one destination is configured for each channel. Higher values are valid when several destinations are configured."))
story.append(step(8, "Verify Telegram", [
    "Open the configured Telegram destination.",
    "Confirm a sample HD-1 ticket alert arrives with event, venue, ticket details, price, quantity and ticket-page link.",
    "Confirm the timestamp matches the portal test.",
], "The message is readable and its button or link points to the sample ticket URL."))
story.append(step(9, "Verify Discord", [
    "Open the configured Discord channel.",
    "Confirm the webhook message contains the same event information as Telegram.",
    "Open the link only far enough to verify the target address; do not purchase tickets.",
], "The embed is delivered once, contains the expected fields and links to the correct ticket page."))
story.append(callout("Delivery meaning", "Test All Channels uses the same server-side delivery pipeline as real monitor alerts. It proves credentials, provider access and message formatting, but it does not prove that a ticket site can be scraped. That is tested next.", AMBER, HexColor("#FFF6DF")))
story.append(PageBreak())

# Target creation
story += [P("4. Add and validate a target URL", "H1x")]
story.append(step(10, "Prepare one safe test target", [
    "Use a client-approved live event page from a supported ticket site.",
    "Choose an event where repeated page checks will not interfere with a customer purchase.",
    "Confirm the assigned Multilogin profile is already logged in and has its existing sticky proxy.",
], "The URL opens normally in the approved profile before it is added to the monitor."))
story.append(step(11, "Add the target", [
    "Select Add New Target URL.",
    "Enter Event Name, Venue and the full Target URL.",
    "Set section filters only when required, for example Arena A, Arena B or Standing.",
    "Set minimum ticket quantity and an optional maximum price.",
    "Choose normal tickets only or even quantities only when the test requires those filters.",
    "Assign an approved profile. Add start or stop times only if a monitoring window is required.",
    "Select Save Target.",
], "The target appears in Monitors with the chosen filters, profile and refresh timing."))
story.append(step(12, "Run Check now", [
    "Select Check now on the target card.",
    "Wait for the card to update; do not open or edit the Multilogin profile during the check.",
], "A successful check reports either matching tickets, no matching tickets, paused state or a clear ticket-site error. Check now does not deliberately send a notification."))
story.append(step(13, "Run Check and send alert", [
    "Select Check & send alert once.",
    "Wait for the result before clicking any other target action.",
    "Check the alert log, browser push, Telegram and Discord.",
], "When matching ticket information is available, all enabled channels receive the same structured snapshot and the alert log records the event."))
story.append(step(14, "Test the ticket-page handoff", [
    "Select Open Ticket Page.",
    "Confirm the correct event page opens in the user's normal browser and network context.",
    "Stop before any basket or checkout action.",
], "The destination URL is correct. The monitor does not automate basket creation, payment or checkout."))
story.append(PageBreak())

# Scheduler
story += [P("5. Prove scheduled monitoring and interval changes", "H1x")]
story.append(step(15, "Confirm the scheduler is active", [
    "Verify exactly one production replica has the scheduler enabled.",
    "Keep the test target active and note the current time.",
    "Wait for at least two saved refresh intervals.",
], "The target's last-check time advances automatically. There are no duplicate checks caused by multiple scheduler replicas."))
story.append(step(16, "Increase the interval", [
    "Change Global Refresh Interval from 30 seconds to a longer value, such as 60 seconds, and save.",
    "Observe the next due checks without restarting the application.",
], "Future checks follow the new interval. The scheduler reads the saved Supabase setting on every pass."))
story.append(step(17, "Decrease the interval", [
    "Return the interval to the approved operational value and save.",
    "Observe at least two more checks.",
], "Checks become more frequent according to the saved value, subject to per-profile safety spacing and provider queues."))
story.append(step(18, "Verify a live ticket snapshot", [
    "Use an approved target that currently exposes ticket information.",
    "Allow a due scheduler check or use Check & send alert for a controlled test.",
    "Compare the target card, alert log, Telegram and Discord messages.",
], "Event, venue, site, sections, ticket type, quantity, price and direct link are consistent wherever the source page exposes them."))
story.append(callout("Important limitation", "The monitor reports information available to its browser-backed check. A ticket site may hide inventory behind authentication, JavaScript APIs, seat maps, queues or captcha. In that case, confirm the approved Multilogin profile and proxy are healthy before treating the result as an application defect.", AMBER, HexColor("#FFF6DF")))
story.append(PageBreak())

# Multilogin and negative tests
story += [P("6. Multilogin, proxies and negative tests", "H1x")]
story.append(step(19, "Confirm approved-profile safety", [
    "Open Profiles and note the profile name, current state and sticky proxy label.",
    "Run a target check assigned to that profile.",
    "Recheck Multilogin after the test.",
], "No fingerprint, login, permanent proxy or sticky IP assignment changes. The profile remains usable by the client."))
story.append(step(20, "Test optional rotating scraper proxies", [
    "Run this only when MULTILOGIN_SCRAPER_PROXIES is deliberately configured with client-supplied residential or mobile proxies.",
    "Run several due checks and review server logs or provider traffic for sequential proxy use.",
    "Confirm temporary quick profiles are stopped and removed after each check.",
], "Scraper IPs rotate without modifying approved permanent profiles. If the pool is empty, regular assigned profiles remain in use."))
story.append(step(21, "Confirm captcha suppression", [
    "Use an existing captcha result or wait for a natural challenge. Do not intentionally attack or bypass a ticket site.",
    "Check the target card and notification destinations.",
], "Captcha status remains visible on the dashboard, but it does not create repeated push, Telegram, Discord, SMS or WhatsApp alerts."))
story.append(step(22, "Test pause and resume", [
    "Pause one target and wait longer than its refresh interval.",
    "Confirm checks stop, then select Resume and observe the next due check.",
    "If available, repeat with a profile pause to confirm all assigned targets are skipped safely.",
], "Paused items do not check or notify; resumed items return to normal scheduling."))
story.append(step(23, "Install and test the progressive web app", [
    "Select Install app from the lower-right prompt and complete browser installation.",
    "Launch the installed app and repeat the browser push test.",
], "The installed portal opens correctly, receives notifications when permitted, and no longer shows the install prompt."))
story.append(PageBreak())

# Troubleshooting
story += [P("7. Troubleshooting guide", "H1x")]
troubles = [
    ("Supabase error or zero targets", "Confirm the Supabase project and database are online. Verify SUPABASE_URL and the service-role key in the deployment secrets. Do not continue acceptance testing with fallback data."),
    ("Telegram count is zero", "Verify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_IDS, bot post permission, chat ID format and production-server access to api.telegram.org. Test from the production network, not a locally blocked network."),
    ("Discord count is zero", "Verify DISCORD_WEBHOOK_URLS and that the webhook still exists. Check provider response errors and rate limits."),
    ("Push does not appear", "Use HTTPS, allow browser notifications, enable operating-system notifications, disable Focus/Do Not Disturb and verify VAPID settings. Each device needs its own subscription."),
    ("Target says Check Failed", "Confirm the URL, ticket-site availability, approved profile mapping, Multilogin launcher connection, proxy authentication and account login. Review the exact card error before retrying."),
    ("Captcha appears", "Treat it as a ticket-site access condition. Check proxy reputation and profile health. Captcha itself should not generate repeated external alerts."),
    ("Duplicate alerts", "Confirm only one scheduler-enabled replica is running. Wait for Telegram or Discord provider queues before repeating a test."),
    ("Wrong check timing", "Save Global Refresh Interval again, refresh the portal, and compare the target card timing. Per-profile safety spacing can prevent simultaneous checks."),
    ("Profile is open elsewhere", "Close the profile on the other machine or let the server holding the profile run the check. Do not force-edit the profile."),
]
rows=[[P("Symptom","CellHeader"),P("Action","CellHeader")]]+[[P(a,"CellBold"),P(b,"Cell")] for a,b in troubles]
t=Table(rows,colWidths=[48*mm,122*mm],repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY_2),("TEXTCOLOR",(0,0),(-1,0),WHITE),
    ("GRID",(0,0),(-1,-1),0.35,HexColor("#CFD9E5")),("VALIGN",(0,0),(-1,-1),"TOP"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LIGHT]),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
]))
story.append(t)
story.append(PageBreak())

# Acceptance
story += [P("8. Client acceptance record", "H1x"), P("Complete this table during the client test. Attach screenshots or message links separately where useful.")]
acceptance = [
    ("Portal and HTTPS load", "Dashboard opens without certificate or server error"),
    ("Supabase and health", "Connected data and valid health result"),
    ("Responsive modules", "Monitors, Profiles, Alerts and Settings open correctly"),
    ("Browser push", "Test notification received"),
    ("Telegram", "Controlled alert received with correct fields and link"),
    ("Discord", "Controlled alert received with correct embed and link"),
    ("Target creation", "Safe target saved with correct filters and profile"),
    ("Manual check", "Check now returns a clear result"),
    ("Manual alert", "Check & send alert reaches enabled channels"),
    ("Scheduler", "Automatic checks follow saved interval"),
    ("Interval change", "New interval applies without restart"),
    ("Ticket-page handoff", "Correct event page opens; no checkout automation"),
    ("Captcha suppression", "Visible on dashboard without repeated external pings"),
    ("Profile safety", "No permanent profile or sticky proxy changes"),
    ("PWA", "Install and push test succeed on client device"),
]
rows=[[P("Test","CellHeader"),P("Pass condition","CellHeader"),P("Pass / Fail","CellHeader"),P("Notes","CellHeader")]]
for a,b in acceptance: rows.append([P(a,"CellBold"),P(b,"Cell"),P("[ ] Pass  [ ] Fail","Smallx"),P("", "Cell")])
t=Table(rows,colWidths=[39*mm,76*mm,27*mm,28*mm],repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY_2),("TEXTCOLOR",(0,0),(-1,0),WHITE),
    ("GRID",(0,0),(-1,-1),0.35,HexColor("#BFCBDA")),("VALIGN",(0,0),(-1,-1),"TOP"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LIGHT]),
    ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
story += [t, Spacer(1,6*mm)]
sign = Table([
    [P("Client tester", "CellBold"), "", P("Date", "CellBold"), ""],
    [P("Deployment / URL", "CellBold"), "", P("Final result", "CellBold"), P("[ ] Accepted   [ ] Accepted with notes   [ ] Retest required", "Smallx")],
    [P("Signature / approval", "CellBold"), "", "", ""],
], colWidths=[31*mm,58*mm,25*mm,56*mm], rowHeights=[12*mm,14*mm,17*mm])
sign.setStyle(TableStyle([
    ("GRID",(0,0),(-1,-1),0.5,HexColor("#BFCBDA")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("BACKGROUND",(0,0),(0,-1),LIGHT),("BACKGROUND",(2,0),(2,1),LIGHT),
    ("SPAN",(1,2),(3,2)),("LEFTPADDING",(0,0),(-1,-1),6),
]))
story += [sign, Spacer(1,6*mm)]
story.append(callout("Completion rule", "The system is ready for normal operation only after all required tests pass, the final operating interval is agreed, the approved target list is loaded, and account owners retain control of deployment and notification credentials.", GREEN, PALE_GREEN))

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(str(OUT))
