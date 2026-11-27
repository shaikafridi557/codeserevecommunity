"""Draws the four software-project cover images for the portfolio (1260x788 + webp sizes).
Run:  python tools/make_project_images.py
"""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent.parent / "assets" / "img" / "portfolio"
W, H, S = 1260, 788, 2          # draw at 2x, scale down for smooth edges
F = "C:/Windows/Fonts/"

def font(size, bold=False):
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    try:
        return ImageFont.truetype(F + name, size * S)
    except OSError:
        return ImageFont.load_default()

def hexrgb(h, a=255):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)

def p(*v):  # scale coordinates
    return [x * S for x in v]

def background(c1, c2, glow):
    img = Image.new("RGBA", (W*S, H*S))
    d = ImageDraw.Draw(img, "RGBA")
    a, b = hexrgb(c1), hexrgb(c2)
    for y in range(H*S):
        t = y / (H*S)
        d.line([(0, y), (W*S, y)], fill=tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3)) + (255,))
    # soft glows
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for (x, y, r, col) in glow:
        gd.ellipse(p(x-r, y-r, x+r, y+r), fill=hexrgb(col, 110))
    g = g.filter(ImageFilter.GaussianBlur(120*S))
    img = Image.alpha_composite(img, g).convert("RGB")
    # fine dot grid
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 28):
        for y in range(0, H, 28):
            d.ellipse(p(x, y, x+1.6, y+1.6), fill=(255, 255, 255, 18))
    return img

def panel(img, box, r=22, fill=(255, 255, 255, 16), line=(255, 255, 255, 40), shadow=True):
    x0, y0, x1, y1 = box
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle(p(x0+10, y0+24, x1+10, y1+24), r*S, fill=(0, 0, 0, 120))
        sh = sh.filter(ImageFilter.GaussianBlur(26*S)); img.paste(sh, (0, 0), sh)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle(p(*box), r*S, fill=fill, outline=line, width=2*S)
    img.paste(lay, (0, 0), lay)

def text(d, xy, s, size, col="#ffffff", bold=False, a=255):
    if any(c in s for c in "✓⚠★"):   # symbols Segoe UI lacks
        f = ImageFont.truetype(F + "seguisym.ttf", size * S)
    else:
        f = font(size, bold)
    d.text(p(*xy), s, font=f, fill=hexrgb(col, a))

def title_block(d, tag, name, accent):
    tw = d.textlength(tag, font=font(13, True)) / S
    d.rounded_rectangle(p(62, 60, 62 + tw + 32, 92), 16*S, fill=hexrgb(accent, 40), outline=hexrgb(accent, 140), width=2*S)
    d.text(p(78, 66), tag, font=font(13, True), fill=hexrgb(accent))
    text(d, (62, 104), name, 32, "#ffffff", True)

def chrome(d, box):
    x0, y0, x1, _ = box
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse(p(x0+22+i*20, y0+20, x0+34+i*20, y0+32), fill=hexrgb(c))
    d.line(p(x0, y0+50, x1, y0+50), fill=(255, 255, 255, 30), width=2*S)

def smooth(pts, n=16):
    """Catmull-Rom curve through the points."""
    out = []; P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P)-2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        for k in range(n):
            t = k/n; t2, t3 = t*t, t*t*t
            out.append(tuple(.5*((2*p1[j]) + (-p0[j]+p2[j])*t + (2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t2 + (-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t3) for j in (0, 1)))
    out.append(pts[-1]); return out

def area_chart(img, box, vals, col, fill_a=70):
    x0, y0, x1, y1 = box
    mx, mn = max(vals), min(vals)
    pts = [(x0 + (x1-x0)*i/(len(vals)-1), y1 - (y1-y0)*(v-mn)/(mx-mn or 1)) for i, v in enumerate(vals)]
    pts = smooth(pts)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.polygon([tuple(p(*q)) for q in pts] + [tuple(p(x1, y1)), tuple(p(x0, y1))], fill=hexrgb(col, fill_a))
    lay = lay.filter(ImageFilter.GaussianBlur(2*S)); img.paste(lay, (0, 0), lay)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([tuple(p(*q)) for q in pts], fill=hexrgb(col), width=4*S, joint="curve")
    lx, ly = pts[-1]
    d.ellipse(p(lx-8, ly-8, lx+8, ly+8), fill=hexrgb(col), outline=(255, 255, 255, 255), width=3*S)

def ring(d, c, r, pct, col, w=16):
    x, y = c
    d.ellipse(p(x-r, y-r, x+r, y+r), outline=(255, 255, 255, 30), width=w*S)
    d.arc(p(x-r, y-r, x+r, y+r), -90, -90 + 360*pct, fill=hexrgb(col), width=w*S)

def save(img, name):
    out = img.resize((W, H), Image.LANCZOS).convert("RGB")
    out.save(OUT / f"{name}.jpg", quality=90, optimize=True, progressive=True)
    out.save(OUT / f"{name}.webp", quality=84)
    out.resize((640, round(640*H/W)), Image.LANCZOS).save(OUT / f"{name}-640.webp", quality=82)
    print("saved", name)

# ---------------------------------------------------------------- 1. Data visualisation
def data_viz():
    random.seed(4)
    img = background("#0b1026", "#141a3d", [(1050, 120, 260, "#387cf9"), (220, 720, 240, "#8b5cf6")])
    d = ImageDraw.Draw(img, "RGBA")
    title_block(d, "DATA VISUALISATION", "Insight Dashboard", "#7aa7ff")
    box = (430, 70, 1200, 730); panel(img, box); d = ImageDraw.Draw(img, "RGBA"); chrome(d, box)
    text(d, (460, 132), "Revenue overview", 20, "#ffffff", True)
    text(d, (460, 160), "Last 12 months  ·  all branches", 14, "#9aa6d1")
    for i, (lab, val, col) in enumerate((("Revenue", "₹48.2L", "#7aa7ff"), ("Orders", "12,940", "#34d399"), ("Growth", "+23%", "#f472b6"))):
        bx = 460 + i*240
        panel(img, (bx, 196, bx+220, 276), 16, (255, 255, 255, 14), (255, 255, 255, 26), False); d = ImageDraw.Draw(img, "RGBA")
        text(d, (bx+18, 206), lab, 14, "#9aa6d1"); text(d, (bx+18, 228), val, 26, col, True)
    area_chart(img, (470, 320, 900, 500), [12, 18, 15, 24, 22, 30, 27, 36, 33, 42, 40, 51], "#387cf9")
    area_chart(img, (470, 360, 900, 500), [8, 10, 14, 12, 18, 16, 22, 20, 26, 24, 29, 31], "#8b5cf6", 50)
    d = ImageDraw.Draw(img, "RGBA")
    for i, m in enumerate("JFMAMJJASOND"):
        text(d, (466 + i*36.5, 510), m, 12, "#6f7aa8")
    # donut
    cx, cy, r = 1050, 410, 86
    segs = (("#387cf9", .42), ("#34d399", .26), ("#f472b6", .18), ("#fbbf24", .14)); a = -90
    for col, v in segs:
        d.arc(p(cx-r, cy-r, cx+r, cy+r), a, a + v*360 - 2, fill=hexrgb(col), width=24*S); a += v*360
    text(d, (cx-34, cy-22), "4", 30, "#ffffff", True); text(d, (cx-6, cy-14), " cities", 14, "#9aa6d1")
    # bars
    for i in range(10):
        h = random.randint(40, 150); x = 470 + i*48
        col = "#387cf9" if i % 4 else "#34d399"
        d.rounded_rectangle(p(x, 700-h, x+28, 700), 6*S, fill=hexrgb(col, 200))
    text(d, (980, 600), "Live data from", 14, "#9aa6d1"); text(d, (980, 622), "sales · stock · CRM", 18, "#ffffff", True)
    text(d, (62, 160), "Turns raw business data", 20, "#c7cff0"); text(d, (62, 188), "into clear, live charts.", 20, "#c7cff0")
    for i, s in enumerate(("Real-time KPIs", "Interactive filters", "Export & share reports")):
        d.ellipse(p(64, 250+i*42, 76, 262+i*42), fill=hexrgb("#387cf9"))
        text(d, (88, 242+i*42), s, 17, "#ffffff")
    save(img, "data-visualization-app")

# ---------------------------------------------------------------- 2. SEO analytics
def seo_analytics():
    img = background("#06141a", "#0c2430", [(1100, 680, 260, "#10b981"), (300, 80, 220, "#06b6d4")])
    d = ImageDraw.Draw(img, "RGBA")
    title_block(d, "SEO ANALYTICS", "Search Insight Web App", "#5eead4")
    box = (430, 70, 1200, 730); panel(img, box); d = ImageDraw.Draw(img, "RGBA"); chrome(d, box)
    text(d, (460, 132), "Organic performance", 20, "#ffffff", True)
    text(d, (460, 160), "Clicks · impressions · rankings", 14, "#8fb9c0")
    ring(d, (560, 300), 72, .92, "#10b981"); text(d, (528, 270), "92", 40, "#ffffff", True); text(d, (536, 318), "SEO score", 12, "#8fb9c0")
    area_chart(img, (680, 220, 1170, 370), [20, 22, 21, 28, 31, 30, 38, 44, 43, 55, 61, 70], "#10b981")
    d = ImageDraw.Draw(img, "RGBA")
    text(d, (690, 200), "Clicks  +184%", 15, "#5eead4", True)
    # keyword table
    rows = (("best cafe in kukatpally", "3", "↑ 9"), ("dental clinic near me", "1", "↑ 4"),
            ("banquet hall hyderabad", "5", "↑ 12"), ("school admissions 2026", "2", "↑ 6"))
    y = 420
    text(d, (460, y), "KEYWORD", 12, "#6f9aa1", True); text(d, (960, y), "RANK", 12, "#6f9aa1", True); text(d, (1060, y), "CHANGE", 12, "#6f9aa1", True)
    for i, (k, rnk, ch) in enumerate(rows):
        yy = y + 34 + i*62
        panel(img, (452, yy, 1170, yy+50), 12, (255, 255, 255, 10), (255, 255, 255, 18), False); d = ImageDraw.Draw(img, "RGBA")
        text(d, (472, yy+12), k, 16, "#e6fffb")
        d.rounded_rectangle(p(958, yy+10, 1000, yy+40), 10*S, fill=hexrgb("#10b981", 60)); text(d, (972, yy+12), rnk, 16, "#5eead4", True)
        text(d, (1062, yy+12), ch, 16, "#34d399", True)
    text(d, (62, 160), "Shows where customers", 20, "#c4e6ea"); text(d, (62, 188), "find you on Google.", 20, "#c4e6ea")
    for i, s in enumerate(("Keyword rank tracking", "Search Console + GA4", "Monthly growth reports")):
        d.ellipse(p(64, 250+i*42, 76, 262+i*42), fill=hexrgb("#10b981"))
        text(d, (88, 242+i*42), s, 17, "#ffffff")
    panel(img, (62, 430, 380, 540), 16); d = ImageDraw.Draw(img, "RGBA")
    text(d, (84, 448), "Keywords in top 3", 14, "#8fb9c0"); text(d, (84, 474), "14 of 20", 34, "#5eead4", True)
    save(img, "seo-analytics-app")

# ---------------------------------------------------------------- 3. Streamlined management
def management():
    img = background("#160d24", "#241338", [(1000, 100, 260, "#a855f7"), (200, 700, 220, "#387cf9")])
    d = ImageDraw.Draw(img, "RGBA")
    title_block(d, "MANAGEMENT SYSTEM", "Streamlined Operations", "#d8b4fe")
    box = (430, 70, 1200, 730); panel(img, box); d = ImageDraw.Draw(img, "RGBA"); chrome(d, box)
    text(d, (460, 132), "Operations board", 20, "#ffffff", True)
    text(d, (460, 160), "Staff · tasks · approvals in one place", 14, "#b9a6d6")
    cols = (("To do", "#f59e0b", ("Vendor invoices", "New staff onboarding", "Stock audit")),
            ("In progress", "#387cf9", ("Payroll — March", "Client renewal")),
            ("Done", "#22c55e", ("GST filing", "Branch report", "Leave approvals")))
    for i, (name, col, cards) in enumerate(cols):
        x = 456 + i*246
        panel(img, (x, 200, x+226, 700), 16, (255, 255, 255, 10), (255, 255, 255, 22), False); d = ImageDraw.Draw(img, "RGBA")
        d.ellipse(p(x+16, 220, x+28, 232), fill=hexrgb(col)); text(d, (x+38, 214), name, 16, "#ffffff", True)
        text(d, (x+190, 214), str(len(cards)), 14, "#b9a6d6")
        for j, c in enumerate(cards):
            y = 254 + j*110
            panel(img, (x+12, y, x+214, y+96), 12, (255, 255, 255, 22), (255, 255, 255, 30), False); d = ImageDraw.Draw(img, "RGBA")
            d.rounded_rectangle(p(x+26, y+14, x+84, y+24), 5*S, fill=hexrgb(col, 200))
            text(d, (x+26, y+32), c, 15, "#ffffff", True)
            for k in range(2):
                d.ellipse(p(x+26+k*20, y+64, x+46+k*20, y+84), fill=hexrgb(("#f472b6", "#60a5fa")[k]), outline=(36, 19, 56, 255), width=2*S)
            d.rounded_rectangle(p(x+120, y+70, x+196, y+78), 4*S, fill=(255, 255, 255, 30))
            d.rounded_rectangle(p(x+120, y+70, x+120+76*(.3+.3*j), y+78), 4*S, fill=hexrgb(col))
    text(d, (62, 160), "Replaces spreadsheets and", 20, "#ddd0f0"); text(d, (62, 188), "WhatsApp follow-ups.", 20, "#ddd0f0")
    for i, s in enumerate(("Tasks & approvals", "Staff and roles", "Automatic reminders")):
        d.ellipse(p(64, 250+i*42, 76, 262+i*42), fill=hexrgb("#a855f7"))
        text(d, (88, 242+i*42), s, 17, "#ffffff")
    panel(img, (62, 430, 380, 540), 16); d = ImageDraw.Draw(img, "RGBA")
    text(d, (84, 448), "Hours saved / week", 14, "#b9a6d6"); text(d, (84, 474), "18 hrs", 34, "#d8b4fe", True)
    save(img, "management-app")

# ---------------------------------------------------------------- 4. Ordering application
def ordering():
    img = background("#1f0d06", "#2e1409", [(980, 380, 300, "#f97316"), (200, 120, 200, "#ef4444")])
    d = ImageDraw.Draw(img, "RGBA")
    title_block(d, "ORDERING APPLICATION", "Order & Table QR App", "#fdba74")
    text(d, (62, 160), "Customers scan, order", 20, "#f3d8c8"); text(d, (62, 188), "and pay from the table.", 20, "#f3d8c8")
    for i, s in enumerate(("QR table ordering", "Kitchen display", "UPI payments & loyalty")):
        d.ellipse(p(64, 250+i*42, 76, 262+i*42), fill=hexrgb("#f97316"))
        text(d, (88, 242+i*42), s, 17, "#ffffff")
    # QR block
    random.seed(7)
    panel(img, (62, 430, 222, 590), 16, (255, 255, 255, 235), (255, 255, 255, 255)); d = ImageDraw.Draw(img, "RGBA")
    for gx in range(11):
        for gy in range(11):
            corner = (gx < 3 and gy < 3) or (gx > 7 and gy < 3) or (gx < 3 and gy > 7)
            if corner or random.random() < .45:
                d.rectangle(p(78+gx*12, 446+gy*12, 89+gx*12, 457+gy*12), fill=hexrgb("#2e1409"))
    text(d, (240, 490), "Table 7", 22, "#ffffff", True); text(d, (240, 522), "Scan to order", 15, "#f3d8c8")
    # phone
    ph = (520, 40, 840, 760)
    panel(img, ph, 46, (20, 12, 10, 255), (255, 255, 255, 70)); d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle(p(640, 58, 720, 76), 9*S, fill=(0, 0, 0, 255))
    text(d, (548, 96), "Good evening 👋".replace("👋", ""), 15, "#f3d8c8"); text(d, (548, 118), "Today's menu", 24, "#ffffff", True)
    items = (("Masala Dosa", "₹120", "#f97316"), ("Paneer Tikka", "₹240", "#ef4444"), ("Cold Coffee", "₹150", "#a16207"), ("Gulab Jamun", "₹90", "#db2777"))
    for i, (n, pr, col) in enumerate(items):
        y = 170 + i*112
        panel(img, (544, y, 816, y+96), 18, (255, 255, 255, 18), (255, 255, 255, 26), False); d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle(p(558, y+14, 626, y+82), 14*S, fill=hexrgb(col, 210))
        d.ellipse(p(574, y+30, 610, y+66), fill=(255, 255, 255, 70))
        text(d, (640, y+18), n, 16, "#ffffff", True); text(d, (640, y+46), pr, 16, "#fdba74", True)
        d.ellipse(p(770, y+34, 800, y+64), fill=hexrgb("#f97316")); text(d, (778, y+32), "+", 20, "#ffffff", True)
    d.rounded_rectangle(p(544, 640, 816, 706), 20*S, fill=hexrgb("#f97316"))
    text(d, (566, 656), "3 items · ₹510", 16, "#ffffff", True); text(d, (726, 656), "Pay →", 16, "#ffffff", True)
    # order status card
    box = (880, 200, 1200, 560); panel(img, box); d = ImageDraw.Draw(img, "RGBA")
    text(d, (906, 222), "Order #2048", 20, "#ffffff", True); text(d, (906, 252), "Table 7 · 3 items", 14, "#f3d8c8")
    steps = (("Order placed", True), ("Sent to kitchen", True), ("Being prepared", True), ("Served", False))
    for i, (s, ok) in enumerate(steps):
        y = 300 + i*60
        d.ellipse(p(906, y, 932, y+26), fill=hexrgb("#22c55e" if ok else "#5b3a2c"))
        if i < 3:
            d.line(p(919, y+28, 919, y+58), fill=hexrgb("#22c55e" if steps[i+1][1] else "#5b3a2c"), width=3*S)
        text(d, (948, y), s, 16, "#ffffff" if ok else "#a88b7c", ok)
    panel(img, (880, 590, 1200, 700), 16); d = ImageDraw.Draw(img, "RGBA")
    text(d, (906, 606), "Today", 14, "#f3d8c8"); text(d, (906, 630), "214 orders", 30, "#fdba74", True)
    save(img, "ordering-app")

if __name__ == "__main__":
    data_viz(); seo_analytics(); management(); ordering()
