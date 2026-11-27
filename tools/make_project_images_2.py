"""Second batch of portfolio covers: AI agents, more apps, and poster covers for two client projects.
Run:  python tools/make_project_images_2.py
"""
import random
from PIL import ImageDraw
from make_project_images import background, panel, text, title_block, chrome, ring, area_chart, save, hexrgb, p, font, S


def intro(d, tag, name, accent, lines, bullets, dot, sub="#d6dbea"):
    title_block(d, tag, name, accent)
    for i, l in enumerate(lines):
        text(d, (62, 160 + i*28), l, 20, sub)
    for i, s in enumerate(bullets):
        d.ellipse(p(64, 250+i*42, 76, 262+i*42), fill=hexrgb(dot))
        text(d, (88, 242+i*42), s, 17, "#ffffff")


def stat(img, box, label, value, col, sub):
    panel(img, box, 16); d = ImageDraw.Draw(img, "RGBA")
    x0, y0 = box[0], box[1]
    text(d, (x0+22, y0+18), label, 14, sub); text(d, (x0+22, y0+44), value, 32, col, True)
    return d


# ---------------------------------------------------------------- AI lead research agent
def ai_lead_agent():
    img = background("#0a120a", "#101d12", [(1060, 160, 260, "#84cc16"), (240, 700, 220, "#22c55e")])
    d = ImageDraw.Draw(img, "RGBA")
    intro(d, "AI AGENT", "Lead Research Agent", "#bef264",
          ("Finds local businesses, checks", "their online presence, drafts a report."),
          ("Runs on a schedule", "PDF report per business", "Human approves every email"), "#84cc16", "#d9f0c4")
    box = (430, 70, 1200, 730); panel(img, box); d = ImageDraw.Draw(img, "RGBA"); chrome(d, box)
    text(d, (460, 132), "Agent run · today 09:00", 20, "#ffffff", True)
    text(d, (460, 160), "4 steps · 26 businesses analysed", 14, "#a3c48a")
    steps = (("Find", "Public listings", "#84cc16"), ("Audit", "Site · speed · security", "#22c55e"),
             ("Report", "PDF per business", "#14b8a6"), ("Review", "You approve", "#facc15"))
    for i, (n, s, col) in enumerate(steps):
        x = 460 + i*182
        panel(img, (x, 200, x+160, 300), 16, (255, 255, 255, 14), hexrgb(col, 120), False); d = ImageDraw.Draw(img, "RGBA")
        d.ellipse(p(x+16, 216, x+44, 244), fill=hexrgb(col)); text(d, (x+25, 216), str(i+1), 16, "#0a120a", True)
        text(d, (x+16, 252), n, 18, "#ffffff", True); text(d, (x+16, 276), s, 12, "#a3c48a")
        if i < 3:
            d.line(p(x+160, 250, x+182, 250), fill=hexrgb(col), width=3*S)
    # log
    panel(img, (460, 330, 820, 700), 16, (0, 0, 0, 90), (255, 255, 255, 26), False); d = ImageDraw.Draw(img, "RGBA")
    logs = (("✓", "Bakery · KPHB", "site checked"), ("✓", "Dental clinic", "report ready"), ("✓", "Banquet hall", "report ready"),
            ("•", "Coaching centre", "checking speed"), ("•", "Boutique hotel", "queued"), ("•", "Café · Madhapur", "queued"))
    for i, (m, n, s) in enumerate(logs):
        y = 352 + i*56; done = m == "✓"
        text(d, (480, y), m, 18, "#84cc16" if done else "#5f7a52", True)
        text(d, (508, y), n, 16, "#ffffff" if done else "#a3c48a", done)
        text(d, (660, y+2), s, 13, "#a3c48a")
    # report card
    panel(img, (850, 330, 1170, 700), 16, (255, 255, 255, 235), (255, 255, 255, 255), False); d = ImageDraw.Draw(img, "RGBA")
    text(d, (874, 350), "PRESENCE REPORT", 12, "#4d7c0f", True); text(d, (874, 372), "Dental clinic", 22, "#0a120a", True)
    d.ellipse(p(874, 420, 974, 520), outline=hexrgb("#e5e7eb"), width=12*S)
    d.arc(p(874, 420, 974, 520), -90, -90 + 360*.61, fill=hexrgb("#f59e0b"), width=12*S)
    text(d, (904, 450), "61", 28, "#0a120a", True)
    for i, (k, col) in enumerate((("Security", "#ef4444"), ("Google profile", "#f59e0b"), ("Speed", "#22c55e"))):
        y = 540 + i*44
        d.rounded_rectangle(p(874, y, 1146, y+30), 8*S, fill=hexrgb("#f4f4f5"))
        d.ellipse(p(886, y+10, 896, y+20), fill=hexrgb(col)); text(d, (906, y+4), k, 14, "#27272a")
    text(d, (994, 448), "Needs work", 15, "#b45309", True); text(d, (994, 472), "3 things to fix", 13, "#52525b")
    save(img, "ai-lead-agent")


# ---------------------------------------------------------------- AI WhatsApp assistant
def ai_chat_assistant():
    img = background("#04140f", "#072019", [(950, 380, 300, "#25d366"), (180, 120, 200, "#0ea5e9")])
    d = ImageDraw.Draw(img, "RGBA")
    intro(d, "AI AGENT", "WhatsApp AI Assistant", "#86efac",
          ("Answers customers 24/7 and books", "appointments while you work."),
          ("Replies in English, Telugu, Hindi", "Books slots into your calendar", "Hands over to staff anytime"), "#25d366", "#c8eedb")
    d = stat(img, (62, 430, 380, 540), "Replied in under 10 sec", "92%", "#86efac", "#9cc9b4")
    ph = (520, 40, 840, 760)
    panel(img, ph, 46, (11, 20, 26, 255), (255, 255, 255, 70)); d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle(p(640, 58, 720, 76), 9*S, fill=(0, 0, 0, 255))
    d.rectangle(p(522, 86, 838, 150), fill=hexrgb("#1f2c34"))
    d.ellipse(p(540, 98, 580, 138), fill=hexrgb("#25d366")); text(d, (551, 104), "AI", 16, "#04140f", True)
    text(d, (592, 98), "Smile Dental", 17, "#ffffff", True); text(d, (592, 122), "online · replies instantly", 12, "#8fd1ae")
    msgs = ((False, "Hi, is the clinic open on Sunday?"),
            (True, "Hi! Yes, we're open Sunday 10am–2pm. Would you like to book a check-up?"),
            (False, "Yes, tomorrow morning"),
            (True, "I have 10:30 or 11:15 free. Which works for you?"),
            (False, "10:30"))
    y = 170
    for me, m in msgs:
        words, lines, cur = m.split(), [], ""
        for w in words:
            if d.textlength(cur + " " + w, font=font(14)) / S > 196:
                lines.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        h = 22 + len(lines)*20
        x0 = 600 if not me else 540
        if not me:
            x0 = 812 - max(d.textlength(l, font=font(14)) / S for l in lines) - 28
        x1 = x0 + max(d.textlength(l, font=font(14)) / S for l in lines) + 28
        d.rounded_rectangle(p(x0, y, x1, y+h), 14*S, fill=hexrgb("#005c4b" if not me else "#1f2c34"))
        for i, l in enumerate(lines):
            text(d, (x0+14, y+10+i*20), l, 14, "#e9edef")
        y += h + 12
    # booking card
    d.rounded_rectangle(p(540, y, 812, y+84), 14*S, fill=hexrgb("#1f2c34"), outline=hexrgb("#25d366"), width=2*S)
    text(d, (556, y+12), "✓ Booked", 15, "#25d366", True); text(d, (556, y+36), "Tue · 10:30 AM · Dr. Rao", 14, "#e9edef")
    text(d, (556, y+58), "Reminder set for 9:30 AM", 12, "#8fd1ae")
    # side panel
    box = (880, 200, 1200, 560); panel(img, box); d = ImageDraw.Draw(img, "RGBA")
    text(d, (906, 222), "This week", 20, "#ffffff", True); text(d, (906, 252), "handled by the assistant", 14, "#9cc9b4")
    for i, (k, v, col) in enumerate((("Chats", "318", "#86efac"), ("Bookings", "64", "#38bdf8"), ("Sent to staff", "12", "#facc15"))):
        yy = 300 + i*80
        text(d, (906, yy), k, 14, "#9cc9b4"); text(d, (906, yy+20), v, 30, col, True)
        d.rounded_rectangle(p(1030, yy+30, 1170, yy+40), 5*S, fill=(255, 255, 255, 30))
        d.rounded_rectangle(p(1030, yy+30, 1030 + 140*(.9, .55, .2)[i], yy+40), 5*S, fill=hexrgb(col))
    save(img, "ai-chat-assistant")


# ---------------------------------------------------------------- AI document reader
def ai_doc_reader():
    img = background("#110c1f", "#1b1233", [(1080, 600, 260, "#6366f1"), (200, 100, 200, "#f59e0b")])
    d = ImageDraw.Draw(img, "RGBA")
    intro(d, "AI AGENT", "Invoice Reader AI", "#fcd34d",
          ("Reads bills and invoices, and", "fills your books automatically."),
          ("PDF, photo or email", "GST, totals, due dates", "Flags duplicates & errors"), "#f59e0b", "#e2d9f3")
    d = stat(img, (62, 430, 380, 540), "Manual entry time", "−80%", "#fcd34d", "#b9acd6")
    # paper invoice (tilted look via layered shadow)
    panel(img, (440, 110, 740, 690), 10, (250, 250, 247, 255), (255, 255, 255, 255)); d = ImageDraw.Draw(img, "RGBA")
    text(d, (466, 136), "TAX INVOICE", 18, "#111827", True); text(d, (466, 164), "Sri Lakshmi Traders", 13, "#6b7280")
    d.line(p(466, 196, 714, 196), fill=hexrgb("#e5e7eb"), width=2*S)
    for i in range(6):
        y = 214 + i*40
        d.rounded_rectangle(p(466, y, 466 + (150, 120, 170, 110, 140, 130)[i], y+12), 6*S, fill=hexrgb("#d1d5db"))
        d.rounded_rectangle(p(650, y, 714, y+12), 6*S, fill=hexrgb("#d1d5db"))
    d.line(p(466, 470, 714, 470), fill=hexrgb("#e5e7eb"), width=2*S)
    text(d, (466, 486), "Total", 16, "#111827", True); text(d, (620, 486), "₹48,260", 16, "#111827", True)
    # scan highlights
    for y0, y1, col in ((128, 190, "#f59e0b"), (478, 512, "#6366f1"), (560, 600, "#22c55e")):
        d.rounded_rectangle(p(456, y0, 726, y1), 8*S, outline=hexrgb(col), width=3*S)
    text(d, (466, 566), "Due 15 Dec 2026", 14, "#111827", True)
    # scan line
    d.rectangle(p(440, 400, 740, 404), fill=hexrgb("#a78bfa", 200))
    # arrow
    d.line(p(760, 400, 820, 400), fill=hexrgb("#a78bfa"), width=4*S)
    d.polygon([tuple(p(820, 390)), tuple(p(836, 400)), tuple(p(820, 410))], fill=hexrgb("#a78bfa"))
    # extracted fields
    box = (850, 150, 1200, 650); panel(img, box); d = ImageDraw.Draw(img, "RGBA")
    text(d, (874, 172), "Extracted", 20, "#ffffff", True); text(d, (874, 200), "ready for Tally / Zoho", 13, "#b9acd6")
    fields = (("Vendor", "Sri Lakshmi Traders", "#f59e0b"), ("GSTIN", "36ABCDE1234F1Z5", "#f59e0b"), ("Total", "₹48,260", "#818cf8"),
              ("GST", "₹7,362", "#818cf8"), ("Due date", "15 Dec 2026", "#22c55e"))
    for i, (k, v, col) in enumerate(fields):
        y = 240 + i*66
        d.rounded_rectangle(p(874, y, 1176, y+54), 12*S, fill=(255, 255, 255, 14), outline=(255, 255, 255, 26), width=2*S)
        d.rounded_rectangle(p(874, y, 880, y+54), 3*S, fill=hexrgb(col))
        text(d, (894, y+6), k, 12, "#b9acd6"); text(d, (894, y+24), v, 16, "#ffffff", True)
    d.rounded_rectangle(p(874, 584, 1176, 628), 12*S, fill=hexrgb("#22c55e", 60))
    text(d, (892, 594), "✓  99% confident · no duplicate", 14, "#bbf7d0", True)
    save(img, "ai-document-reader")


# ---------------------------------------------------------------- clinic booking app
def clinic_booking():
    img = background("#03141f", "#062234", [(1050, 140, 260, "#06b6d4"), (200, 700, 220, "#3b82f6")])
    d = ImageDraw.Draw(img, "RGBA")
    intro(d, "BOOKING APPLICATION", "Clinic Booking App", "#67e8f9",
          ("Patients book online; doctors see", "a clean day plan."),
          ("Online slot booking", "SMS & WhatsApp reminders", "Patient history in one place"), "#06b6d4", "#cde8f2")
    d = stat(img, (62, 430, 380, 540), "No-shows after reminders", "−35%", "#67e8f9", "#9cc3d4")
    box = (430, 70, 1200, 730); panel(img, box); d = ImageDraw.Draw(img, "RGBA"); chrome(d, box)
    text(d, (460, 132), "December 2026", 20, "#ffffff", True); text(d, (460, 160), "Dr. Rao · Dental", 14, "#9cc3d4")
    days = "MTWTFSS"
    for i, ch in enumerate(days):
        text(d, (470 + i*50, 200), ch, 13, "#6b9cb0", True)
    n = 1
    for r in range(5):
        for c in range(7):
            if r == 0 and c < 1: continue
            if n > 31: break
            x, y = 460 + c*50, 228 + r*48
            sel = n == 15
            busy = n in (2, 3, 8, 9, 10, 16, 22, 23)
            if sel:
                d.ellipse(p(x, y, x+38, y+38), fill=hexrgb("#06b6d4"))
            text(d, (x + (13 if n < 10 else 8), y+7), str(n), 15, "#03141f" if sel else ("#ffffff" if not busy else "#4b7486"), sel)
            if busy and not sel:
                d.ellipse(p(x+17, y+34, x+21, y+38), fill=hexrgb("#f97316"))
            n += 1
    text(d, (820, 200), "Tue 15 · slots", 15, "#ffffff", True)
    slots = (("09:30", "Booked", "#475569"), ("10:30", "Booked", "#475569"), ("11:15", "Free", "#06b6d4"),
             ("12:00", "Free", "#06b6d4"), ("16:30", "Booked", "#475569"), ("17:15", "Free", "#06b6d4"))
    for i, (t, s, col) in enumerate(slots):
        x, y = 820 + (i % 2)*180, 232 + (i // 2)*64
        free = s == "Free"
        d.rounded_rectangle(p(x, y, x+164, y+52), 12*S, fill=hexrgb(col, 70 if free else 50), outline=hexrgb(col, 200 if free else 80), width=2*S)
        text(d, (x+16, y+6), t, 17, "#ffffff", True); text(d, (x+16, y+28), s, 12, "#a5f3fc" if free else "#94a3b8")
    # patient queue
    panel(img, (460, 500, 1170, 700), 16, (255, 255, 255, 12), (255, 255, 255, 24), False); d = ImageDraw.Draw(img, "RGBA")
    text(d, (484, 516), "Today's patients", 16, "#ffffff", True)
    for i, (nm, tm, st, col) in enumerate((("Anitha K.", "09:30", "Checked in", "#22c55e"), ("Ravi T.", "10:30", "On the way", "#f59e0b"), ("Meena S.", "11:15", "Reminder sent", "#38bdf8"))):
        y = 552 + i*46
        d.ellipse(p(484, y, 514, y+30), fill=hexrgb(("#f472b6", "#60a5fa", "#a78bfa")[i]))
        text(d, (528, y+4), nm, 15, "#ffffff", True); text(d, (700, y+4), tm, 15, "#9cc3d4")
        d.rounded_rectangle(p(940, y+2, 1150, y+30), 14*S, fill=hexrgb(col, 50)); text(d, (956, y+5), st, 13, col, True)
    save(img, "clinic-booking-app")


# ---------------------------------------------------------------- school parent app
def school_app():
    img = background("#0c1229", "#131c3d", [(1000, 380, 280, "#facc15"), (180, 100, 200, "#6366f1")])
    d = ImageDraw.Draw(img, "RGBA")
    intro(d, "EDUCATION APPLICATION", "School & Parent App", "#fde047",
          ("Admissions, fees, attendance and", "notices in one parent app."),
          ("Online admissions", "UPI fee payments", "Daily attendance alerts"), "#facc15", "#dbe0f5")
    d = stat(img, (62, 430, 380, 540), "Fees collected on time", "94%", "#fde047", "#a9b2d6")
    ph = (520, 40, 840, 760)
    panel(img, ph, 46, (250, 250, 252, 255), (255, 255, 255, 255)); d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle(p(640, 58, 720, 76), 9*S, fill=(20, 20, 30, 255))
    text(d, (548, 96), "Hello, Lakshmi", 14, "#6b7280"); text(d, (548, 116), "Aarav · Class 6B", 22, "#111827", True)
    d.rounded_rectangle(p(544, 164, 816, 270), 18*S, fill=hexrgb("#4f46e5"))
    text(d, (564, 180), "Attendance this month", 13, "#c7d2fe"); text(d, (564, 202), "96%", 34, "#ffffff", True)
    for i in range(10):
        h = (30, 36, 34, 40, 38, 40, 22, 40, 36, 40)[i]
        d.rounded_rectangle(p(700 + i*11, 250-h, 707 + i*11, 250), 3*S, fill=hexrgb("#fde047" if h < 30 else "#a5b4fc"))
    d.rounded_rectangle(p(544, 286, 816, 370), 18*S, fill=hexrgb("#fef3c7"))
    text(d, (564, 300), "Term 2 fee due", 13, "#92400e"); text(d, (564, 322), "₹18,500", 22, "#111827", True)
    d.rounded_rectangle(p(716, 316, 800, 352), 12*S, fill=hexrgb("#111827")); text(d, (734, 321), "Pay", 15, "#ffffff", True)
    text(d, (548, 392), "Notices", 16, "#111827", True)
    notes = (("Annual Day rehearsal", "Fri · 3 PM", "#f472b6"), ("PTM — Saturday", "10 AM – 1 PM", "#38bdf8"), ("Maths test result out", "Score 46/50", "#22c55e"))
    for i, (a, b, col) in enumerate(notes):
        y = 426 + i*72
        d.rounded_rectangle(p(544, y, 816, y+60), 14*S, fill=hexrgb("#f3f4f6"))
        d.rounded_rectangle(p(556, y+14, 588, y+46), 9*S, fill=hexrgb(col))
        text(d, (600, y+10), a, 14, "#111827", True); text(d, (600, y+32), b, 12, "#6b7280")
    d.rounded_rectangle(p(544, 664, 816, 724), 20*S, fill=hexrgb("#111827"))
    for i, t in enumerate(("Home", "Fees", "Chat", "Me")):
        text(d, (566 + i*66, 684), t, 13, "#fde047" if i == 0 else "#9ca3af", i == 0)
    # admissions panel
    box = (880, 160, 1200, 620); panel(img, box); d = ImageDraw.Draw(img, "RGBA")
    text(d, (906, 182), "Admissions 2027", 20, "#ffffff", True); text(d, (906, 212), "school office view", 13, "#a9b2d6")
    for i, (k, v, col) in enumerate((("Enquiries", 248, "#a5b4fc"), ("Applied", 162, "#fde047"), ("Visited", 104, "#f472b6"), ("Admitted", 71, "#22c55e"))):
        y = 250 + i*84; w = 260 * v / 248
        text(d, (906, y), k, 14, "#a9b2d6"); text(d, (1120, y), str(v), 16, "#ffffff", True)
        d.rounded_rectangle(p(906, y+26, 906 + w, y+56), 10*S, fill=hexrgb(col, 210))
    save(img, "school-parent-app")


# ---------------------------------------------------------------- billing & inventory POS
def billing_pos():
    img = background("#1f0716", "#2b0a20", [(1050, 200, 280, "#ec4899"), (200, 700, 220, "#f43f5e")])
    d = ImageDraw.Draw(img, "RGBA")
    intro(d, "RETAIL SOFTWARE", "Billing & Stock POS", "#f9a8d4",
          ("Fast GST billing with stock that", "updates itself."),
          ("Barcode & GST billing", "Low-stock alerts", "Daily sales on your phone"), "#ec4899", "#f3d3e4")
    d = stat(img, (62, 430, 380, 540), "Bill time per customer", "20 sec", "#f9a8d4", "#d3a3bd")
    box = (430, 70, 1200, 730); panel(img, box); d = ImageDraw.Draw(img, "RGBA"); chrome(d, box)
    text(d, (460, 132), "Counter 1", 20, "#ffffff", True); text(d, (460, 160), "Search or scan barcode…", 14, "#d3a3bd")
    random.seed(3)
    items = (("Basmati 5kg", "₹640", "#f59e0b"), ("Sunflower oil", "₹185", "#facc15"), ("Toor dal", "₹160", "#fb923c"), ("Tea 500g", "₹260", "#a3e635"),
             ("Shampoo", "₹199", "#38bdf8"), ("Biscuits", "₹40", "#f472b6"), ("Detergent", "₹310", "#818cf8"), ("Sugar 1kg", "₹48", "#e5e7eb"), ("Milk 1L", "₹66", "#93c5fd"))
    for i, (n, pr, col) in enumerate(items):
        x, y = 460 + (i % 3)*140, 200 + (i // 3)*130
        panel(img, (x, y, x+124, y+114), 14, (255, 255, 255, 14), (255, 255, 255, 26), False); d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle(p(x+14, y+14, x+54, y+54), 10*S, fill=hexrgb(col, 220))
        text(d, (x+14, y+62), n, 13, "#ffffff", True); text(d, (x+14, y+84), pr, 14, "#f9a8d4", True)
    d.rounded_rectangle(p(460, 600, 864, 700), 16*S, fill=hexrgb("#f43f5e", 50), outline=hexrgb("#f43f5e", 160), width=2*S)
    text(d, (480, 614), "⚠  Low stock", 15, "#fecdd3", True); text(d, (480, 640), "Toor dal · 6 left  ·  Tea 500g · 4 left", 14, "#fecdd3")
    text(d, (480, 664), "Reorder list sent to supplier", 12, "#d3a3bd")
    # bill
    panel(img, (890, 200, 1176, 700), 16, (255, 255, 255, 240), (255, 255, 255, 255), False); d = ImageDraw.Draw(img, "RGBA")
    text(d, (910, 218), "Bill #4417", 18, "#111827", True); text(d, (910, 244), "28 Nov · 6:42 PM", 12, "#6b7280")
    rows = (("Basmati 5kg", "1", "640"), ("Sunflower oil", "2", "370"), ("Tea 500g", "1", "260"), ("Biscuits", "4", "160"))
    for i, (n, q, a) in enumerate(rows):
        y = 284 + i*40
        text(d, (910, y), n, 14, "#111827"); text(d, (1060, y), "×" + q, 14, "#6b7280"); text(d, (1110, y), a, 14, "#111827", True)
    d.line(p(910, 450, 1156, 450), fill=hexrgb("#e5e7eb"), width=2*S)
    text(d, (910, 464), "GST", 14, "#6b7280"); text(d, (1104, 464), "₹71", 14, "#111827")
    text(d, (910, 500), "Total", 20, "#111827", True); text(d, (1060, 500), "₹1,501", 20, "#be185d", True)
    d.rounded_rectangle(p(910, 610, 1156, 676), 16*S, fill=hexrgb("#ec4899"))
    text(d, (952, 628), "Pay by UPI", 18, "#ffffff", True)
    save(img, "billing-pos")


# ---------------------------------------------------------------- poster covers (no real screenshots available)
def poster(name, tag, title_lines, sub, c1, c2, accent, motif):
    img = background(c1, c2, [(980, 200, 300, accent), (200, 680, 240, accent)])
    d = ImageDraw.Draw(img, "RGBA")
    motif(img, d)
    d = ImageDraw.Draw(img, "RGBA")
    tw = d.textlength(tag, font=font(14, True)) / S
    d.rounded_rectangle(p(80, 90, 80 + tw + 36, 126), 18*S, fill=hexrgb(accent, 40), outline=hexrgb(accent, 160), width=2*S)
    d.text(p(98, 98), tag, font=font(14, True), fill=hexrgb(accent))
    for i, l in enumerate(title_lines):
        text(d, (76, 180 + i*96), l, 88, "#ffffff", True)
    text(d, (82, 190 + len(title_lines)*96 + 10), sub, 22, "#e5e7eb")
    save(img, name)


def awards_motif(img, d):
    for i in range(26):
        random.seed(i)
        x, y, r = random.randint(700, 1220), random.randint(40, 740), random.randint(2, 6)
        d.ellipse(p(x-r, y-r, x+r, y+r), fill=hexrgb("#fde68a", random.randint(90, 220)))
    # trophy
    cx = 960
    d.pieslice(p(cx-120, 140, cx+120, 380), 0, 180, fill=hexrgb("#f59e0b"))
    d.rectangle(p(cx-120, 140, cx+120, 260), fill=hexrgb("#fbbf24"))
    d.arc(p(cx-190, 170, cx-90, 290), 90, 270, fill=hexrgb("#fbbf24"), width=16*S)
    d.arc(p(cx+90, 170, cx+190, 290), -90, 90, fill=hexrgb("#fbbf24"), width=16*S)
    d.rectangle(p(cx-22, 380, cx+22, 470), fill=hexrgb("#d97706"))
    d.rounded_rectangle(p(cx-110, 470, cx+110, 520), 10*S, fill=hexrgb("#b45309"))
    d.rounded_rectangle(p(cx-150, 520, cx+150, 580), 12*S, fill=hexrgb("#78350f"))
    import math
    star = [(cx + (46 if k % 2 == 0 else 19) * math.cos(math.radians(-90 + k*36)), 250 + (46 if k % 2 == 0 else 19) * math.sin(math.radians(-90 + k*36))) for k in range(10)]
    d.polygon([tuple(p(*q)) for q in star], fill=hexrgb("#fff7ed"))


def medical_motif(img, d):
    cx, cy = 960, 380
    for r, a in ((300, 30), (220, 45), (150, 70)):
        d.ellipse(p(cx-r, cy-r, cx+r, cy+r), outline=hexrgb("#5eead4", a), width=3*S)
    d.rounded_rectangle(p(cx-40, cy-130, cx+40, cy+130), 22*S, fill=hexrgb("#14b8a6"))
    d.rounded_rectangle(p(cx-130, cy-40, cx+130, cy+40), 22*S, fill=hexrgb("#14b8a6"))
    pts = [(640, 600), (760, 600), (790, 540), (830, 670), (870, 580), (900, 600), (1240, 600)]
    d.line([tuple(p(*q)) for q in pts], fill=hexrgb("#99f6e4"), width=5*S, joint="curve")


if __name__ == "__main__":
    ai_lead_agent(); ai_chat_assistant(); ai_doc_reader(); clinic_booking(); school_app(); billing_pos()
    poster("yoda-ratna-awards", "EVENT WEBSITE", ("Yoda Ratna", "Awards"), "Nominations, schedule and gallery in one place",
           "#1c1206", "#2a1a07", "#f59e0b", awards_motif)
    poster("kammela-medical", "HEALTHCARE WEBSITE", ("Dr. Kammela", "Medical Center"), "Specialist care, explained clearly",
           "#03181a", "#062628", "#14b8a6", medical_motif)
