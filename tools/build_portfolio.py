"""Builds the 'Selected work' section of portfolio.html from the PROJECTS list below.
Run:  python tools/build_portfolio.py
Edit the list, re-run, and the section (cards, index list, case-study pop-ups and schema) is regenerated.
"""
import json, re
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# kind: client = built for a client · product = our own tool · lab = solution we designed and built in-house
# size: grid span on desktop (12-column bento)
PROJECTS = [
    dict(slug="ai-lead-agent", img="ai-lead-agent", cat="ai", kind="lab", size=7, sticker="NEW",
         title="Lead Research Agent", type="AI Agent",
         tags=["AI agent", "Automation", "PDF reports"],
         problem="Finding the right local businesses and understanding what each one actually needs takes hours of manual research per lead.",
         solution="An AI agent that collects public business listings, checks each website, Google presence, speed and security, and writes a branded PDF report. A person reviews and approves every message before anything is sent.",
         features=["Runs on a schedule", "Website, speed & security checks", "Branded PDF report per business", "Human approval before sending"]),
    dict(slug="ai-chat-assistant", img="ai-chat-assistant", cat="ai", kind="lab", size=5, sticker="AI",
         title="WhatsApp AI Assistant", type="AI Agent",
         tags=["AI agent", "WhatsApp", "Bookings"],
         problem="Customers message at all hours, and every unanswered question on WhatsApp is a lost booking.",
         solution="An AI assistant that answers common questions instantly, books appointments into your calendar and hands the chat to your staff when a human is needed.",
         features=["Replies in English, Telugu & Hindi", "Books slots and sends reminders", "Hands over to staff anytime", "Weekly summary of chats"]),
    dict(slug="garishtha-infra", pos="0% 50%", img="garishta-infra", cat="web", kind="client", size=4,
         title="Garishtha Infra Developers", type="Real Estate Website",
         tags=["Website", "Real estate", "Lead capture"],
         problem="A real estate developer needed to present its residential plots and venture layouts along the Hyderabad–Warangal corridor and get site-visit enquiries online.",
         solution="We built a modern corporate website with project pages, gallery, downloadable brochures and a schedule-a-visit flow with WhatsApp chat.",
         features=["Project & layout pages", "Gallery and brochures", "Schedule-a-visit flow", "WhatsApp chat"]),
    dict(slug="ordering-app", img="ordering-app", cat="apps", kind="lab", size=4,
         title="Order & Table QR App", type="Ordering Application",
         tags=["Restaurant", "QR ordering", "UPI"],
         problem="Restaurants lose time and orders at peak hours by taking orders by hand and passing slips to the kitchen.",
         solution="A QR table-ordering app: customers scan, order and pay by UPI from their phone, and orders go straight to a kitchen display with live status.",
         features=["Scan-to-order menu", "Kitchen display", "UPI payments", "Loyalty & repeat offers"]),
    dict(slug="sabari-studios", img="sabari-studios", cat="web", kind="client", size=4,
         title="Sabari Studios", type="Creative Studio Website",
         tags=["Website", "Film & media", "Showreel"],
         problem="A film production and motion-capture studio wanted a website that reflects its creative work and attracts production clients.",
         solution="We designed a visual, media-rich website showcasing their studio, motion-capture services, show reel and client list.",
         features=["Media-rich design", "Services & studio pages", "Show reel", "Client list"]),
    dict(slug="insight-dashboard", img="data-visualization-app", cat="apps", kind="lab", size=5,
         title="Insight Dashboard", type="Data Visualization Application",
         tags=["Dashboard", "Charts", "Reports"],
         problem="When sales, stock and customer data live in separate spreadsheets, owners can't see what is working.",
         solution="An interactive dashboard that brings the data together into live charts, KPI cards and filters, with one-click report export.",
         features=["Live KPI cards", "Interactive filters", "Branch comparison", "Export & share reports"]),
    dict(slug="ai-invoice-reader", img="ai-document-reader", cat="ai", kind="lab", size=7, sticker="AI",
         title="Invoice Reader AI", type="AI Agent",
         tags=["AI agent", "Accounts", "GST"],
         problem="Typing bills and invoices into accounting software is slow and full of small mistakes.",
         solution="An AI agent that reads invoices from PDFs, photos or email, extracts vendor, GST, totals and due dates, flags duplicates, and sends clean data to your books.",
         features=["PDF, photo or email input", "GST, totals & due dates", "Duplicate & error checks", "Export to Tally / Zoho"]),
    dict(slug="clinic-booking", img="clinic-booking-app", cat="apps", kind="lab", size=6,
         title="Clinic Booking App", type="Booking Application",
         tags=["Healthcare", "Appointments", "Reminders"],
         problem="Phone-only booking keeps reception busy, and missed appointments leave empty slots.",
         solution="An appointment app where patients book online and get SMS/WhatsApp reminders, and doctors see a clean day plan with patient history.",
         features=["Online slot booking", "SMS & WhatsApp reminders", "Doctor day view", "Patient history"]),
    dict(slug="sireeshna-solutions", img="sireeshna-solutions", cat="web", kind="client", size=6,
         title="Sireeshna Solutions", type="IT Services Platform",
         tags=["Website", "Training", "Careers"],
         problem="An IT services company in Vijayawada needed one platform to showcase training programmes, job placement services and visa processing.",
         solution="We developed a professional website highlighting their IT services, training courses and global career opportunities, with clear enquiry options.",
         features=["Services & courses", "Placement & visa pages", "Enquiry options", "Professional design"]),
    dict(slug="school-parent-app", img="school-parent-app", cat="apps", kind="lab", size=4,
         title="School & Parent App", type="Education Application",
         tags=["Education", "Fees", "Attendance"],
         problem="Schools juggle admissions, fee reminders, attendance and notices across registers, calls and WhatsApp groups.",
         solution="One app for parents and the school office: online admissions, UPI fee payments, daily attendance alerts and notices.",
         features=["Online admissions", "UPI fee payments", "Attendance alerts", "Notices & results"]),
    dict(slug="seo-analytics", img="seo-analytics-app", cat="apps", kind="lab", size=4,
         title="Search Insight Web App", type="SEO Analytics Web Application",
         tags=["SEO", "Analytics", "Google"],
         problem="Businesses can't tell which searches bring customers or whether their SEO work is paying off.",
         solution="A web app that combines Google Search Console and GA4 data to track keyword rankings, clicks and monthly growth in one clear view.",
         features=["Keyword rank tracking", "Search Console + GA4", "Monthly growth reports", "Page-level insights"]),
    dict(slug="kammela-medical", pos="0% 50%", img="kammela-medical", cat="web", kind="client", size=4,
         title="Dr. Kammela Medical Center", type="Healthcare Website",
         tags=["Website", "Healthcare", "Appointments"],
         problem="A medical specialist needed a professional online presence for kidney treatment, robotic surgery and IVF services.",
         solution="We created a medical website featuring the doctor's credentials, specialisations and appointment options.",
         features=["Doctor profile", "Specialisation pages", "Appointment options", "Mobile-first design"]),
    dict(slug="operations-app", img="management-app", cat="apps", kind="lab", size=7,
         title="Streamlined Operations", type="Management Application",
         tags=["Operations", "Tasks", "Approvals"],
         problem="Daily operations run on spreadsheets and WhatsApp follow-ups, so tasks, approvals and staff updates keep slipping.",
         solution="A management application with a task board, staff roles, approvals and automatic reminders that cuts manual follow-up.",
         features=["Task board", "Staff roles", "Approvals", "Automatic reminders"]),
    dict(slug="billing-pos", img="billing-pos", cat="apps", kind="lab", size=5,
         title="Billing & Stock POS", type="Retail Software",
         tags=["Retail", "GST billing", "Inventory"],
         problem="Slow billing queues and stock that is only counted at month-end mean lost sales and surprise shortages.",
         solution="A fast GST billing counter with barcode scanning, stock that updates itself, low-stock alerts and daily sales on the owner's phone.",
         features=["Barcode & GST billing", "Live stock", "Low-stock alerts", "Daily sales report"]),
    dict(slug="project-pusher", img="project-pusher", cat="tools", kind="product", size=4,
         title="Project Pusher", type="Web Application",
         tags=["Developer tool", "GitHub", "Web app"],
         problem="Developers and students needed a simpler way to upload and manage projects on GitHub without using the command line.",
         solution="We built a web app with secure GitHub sign-in that lets users upload projects, manage repositories and see analytics from one dashboard.",
         features=["GitHub sign-in", "Upload projects", "Manage repositories", "Analytics dashboard"]),
    dict(slug="project-generator", img="project-generator", cat="tools", kind="product", size=4,
         title="Project Structure Generator", type="Development Tool",
         tags=["Developer tool", "Templates", "Productivity"],
         problem="Setting up folder structures for new React, Next.js, Node.js, Django or Flutter projects is repetitive and error-prone.",
         solution="We created a tool with ready templates, a visual editor and live preview that generates and exports a clean project structure in seconds.",
         features=["Ready templates", "Visual editor", "Live preview", "One-click export"]),
    dict(slug="yoda-ratna-awards", pos="0% 50%", img="yoda-ratna-awards", cat="web", kind="client", size=4,
         title="Yoda Ratna Awards", type="Event Website",
         tags=["Website", "Events", "Awards"],
         problem="An awards event needed one place for nominations, the event schedule and highlights.",
         solution="We built an event website that presents the awards, the schedule and the gallery clearly on every device.",
         features=["Awards & categories", "Event schedule", "Gallery", "Mobile-first design"]),
]

CATS = [("all", "All"), ("ai", "AI Agents"), ("apps", "Apps & Software"), ("web", "Websites"), ("tools", "Dev Tools")]
KIND = {"client": "Client project", "product": "Our product", "lab": "CodeServe Lab"}
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def picture(p, sizes, cls="", eager=False):
    i = p["img"]
    lazy = "" if eager else 'loading="lazy" '
    if p.get("pos") and cls == "":
        lazy += f'style="object-position:{p["pos"]}" '
    return (f'<img class="{cls}" src="assets/img/portfolio/{i}.jpg" '
            f'srcset="assets/img/portfolio/{i}-640.webp 640w, assets/img/portfolio/{i}.webp 1260w" sizes="{sizes}" '
            f'width="1260" height="788" alt="{e(p["title"])} — {e(p["type"])}" {lazy}decoding="async">')


def card(n, p):
    sticker = f'<span class="wk-sticker">{e(p["sticker"])}</span>' if p.get("sticker") else ""
    tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
    feats = "".join(f"<li>{e(f)}</li>" for f in p["features"])
    problem_label = "Challenge" if p["kind"] == "client" else "The problem"
    solution_label = "What we built"
    return f'''
                <article class="wk-card wk-span-{p["size"]} wk-k-{p["kind"]}" data-cat="{p["cat"]}" data-slug="{p["slug"]}">
                    <button class="wk-hit" type="button" data-cursor="open" aria-haspopup="dialog" aria-label="Open case study: {e(p["title"])}">
                        <span class="wk-media">{picture(p, "(max-width: 767px) 100vw, 60vw", eager=n <= 2)}{sticker}</span>
                        <span class="wk-info">
                            <span class="wk-num">{n:02d}</span>
                            <span class="wk-txt">
                                <span class="wk-kind">{KIND[p["kind"]]}</span>
                                <span class="wk-name">{e(p["title"])}</span>
                                <span class="wk-type">{e(p["type"])}</span>
                            </span>
                            <span class="wk-go">{ARROW}</span>
                        </span>
                    </button>
                    <ul class="wk-tags">{tags}</ul>
                    <div class="wk-detail" hidden>
                        <p class="wk-d-kind">{KIND[p["kind"]]} · {e(p["type"])}</p>
                        <h3>{e(p["title"])}</h3>
                        <div class="wk-d-cols">
                            <div><h4>{problem_label}</h4><p>{e(p["problem"])}</p></div>
                            <div><h4>{solution_label}</h4><p>{e(p["solution"])}</p></div>
                        </div>
                        <h4>Key features</h4>
                        <ul class="wk-d-feats">{feats}</ul>
                    </div>
                </article>'''


def row(n, p):
    return f'''
                <li class="wk-row" data-cat="{p["cat"]}" data-slug="{p["slug"]}" data-img="assets/img/portfolio/{p["img"]}-640.webp">
                    <button type="button" class="wk-row-hit" data-cursor="open" aria-label="Open case study: {e(p["title"])}">
                        <span class="wk-row-num">{n:02d}</span>
                        <span class="wk-row-name">{e(p["title"])}</span>
                        <span class="wk-row-type">{e(p["type"])}</span>
                        <span class="wk-row-kind">{KIND[p["kind"]]}</span>
                        <span class="wk-go">{ARROW}</span>
                    </button>
                </li>'''


def section():
    counts = {c: sum(1 for p in PROJECTS if c == "all" or p["cat"] == c) for c, _ in CATS}
    chips = "".join(
        f'<button type="button" class="wk-chip{" is-on" if c == "all" else ""}" data-filter="{c}" aria-pressed="{"true" if c == "all" else "false"}">{lab}<sup>{counts[c]}</sup></button>'
        for c, lab in CATS)
    words = ["Websites", "AI Agents", "Web Apps", "Dashboards", "Automation", "Mobile Apps", "SEO"]
    marquee = "".join(f"<span>{w}</span><i>✦</i>" for w in words) * 2
    cards = "".join(card(i + 1, p) for i, p in enumerate(PROJECTS))
    rows = "".join(row(i + 1, p) for i, p in enumerate(PROJECTS))
    return f'''<!-- WORK:START (generated by tools/build_portfolio.py — edit the PROJECTS list there, not this HTML) -->
        <section class="wk" id="work" aria-labelledby="wk-title">
            <div class="wk-marquee" aria-hidden="true"><div class="wk-track">{marquee}</div></div>

            <div class="wk-head container">
                <h2 id="wk-title" class="wk-title">Selected<sup>({len(PROJECTS)})</sup> <span class="wk-outline">work</span></h2>
                <p class="wk-lede">Client websites, business software and AI agents — designed and built by our team in Hyderabad.
                    <span class="wk-legend"><span><b class="wk-dot wk-k-client"></b>Client project</span> <span><b class="wk-dot wk-k-product"></b>Our product</span> <span><b class="wk-dot wk-k-lab"></b>CodeServe Lab</span><small>Lab = solutions we've built in-house, ready to customise for your business.</small></span></p>
            </div>

            <div class="wk-bar container">
                <div class="wk-chips" role="group" aria-label="Filter projects">{chips}</div>
                <div class="wk-views" role="group" aria-label="Layout">
                    <button type="button" class="wk-view is-on" data-view="grid" aria-pressed="true">Grid</button>
                    <button type="button" class="wk-view" data-view="list" aria-pressed="false">Index</button>
                </div>
            </div>

            <div class="wk-grid container" data-layout="grid">{cards}
            </div>

            <ol class="wk-list container" hidden>{rows}
            </ol>
            <img class="wk-float" alt="" aria-hidden="true" width="320" height="200">

            <div class="wk-cta container">
                <p class="wk-cta-k">Got an idea?</p>
                <a class="wk-cta-big" href="contact.html">Let's build it <span class="wk-go">{ARROW}</span></a>
            </div>

            <dialog class="wk-modal" data-lenis-prevent aria-label="Project case study">
                <button type="button" class="wk-close" aria-label="Close">&times;</button>
                <div class="wk-m-media"></div>
                <div class="wk-m-body"></div>
                <div class="wk-m-actions">
                    <a class="wk-btn wk-btn-main" href="contact.html">Build something similar</a>
                    <a class="wk-btn" href="https://wa.me/918186841086" target="_blank" rel="noopener">WhatsApp us</a>
                    <span class="wk-m-nav"><button type="button" class="wk-prev" aria-label="Previous project">&larr;</button><button type="button" class="wk-next" aria-label="Next project">&rarr;</button></span>
                </div>
            </dialog>
        </section>
        <!-- WORK:END -->'''


def schema():
    items = []
    for p in PROJECTS:
        items.append({"@type": "WebSite" if p["cat"] == "web" else "SoftwareApplication",
                      "name": p["title"], "description": f'{p["type"]}: {p["solution"]}',
                      **({} if p["cat"] == "web" else {"applicationCategory": "BusinessApplication"})})
    return items


def main():
    f = ROOT / "portfolio.html"; s = f.read_text(encoding="utf-8")
    new = section()
    if "<!-- WORK:START" in s:
        s = re.sub(r"<!-- WORK:START.*?<!-- WORK:END -->", lambda m: new, s, count=1, flags=re.S)
    else:
        a = s.index("<!-- ========== Horizontal Scrolling Portfolio Section ========== -->")
        b = s.index("<!-- ========== End Horizontal Scrolling Portfolio Section ========== -->") + len("<!-- ========== End Horizontal Scrolling Portfolio Section ========== -->")
        s = s[:a] + new + s[b:]
    # schema.org workExample
    m = re.search(r'("workExample": )(\[.*?\n  \])', s, re.S)
    s = s[:m.start(2)] + json.dumps(schema(), indent=2, ensure_ascii=False).replace("\n", "\n  ") + s[m.end(2):]
    # stylesheet + script
    if "assets/css/work.css" not in s:
        s = s.replace('<link rel="stylesheet" id="page-specific-css"', '<link rel="stylesheet" href="assets/css/work.css?v=1">\n    <link rel="stylesheet" id="page-specific-css"', 1)
    if "assets/js/work.js" not in s:
        s = s.replace('<script src="assets/js/custom.js?v=4"></script>', '<script src="assets/js/custom.js?v=4"></script>\n<script src="assets/js/work.js?v=1" defer></script>', 1)
    f.write_text(s, encoding="utf-8")
    print("portfolio.html: built", len(PROJECTS), "projects")


if __name__ == "__main__":
    main()
