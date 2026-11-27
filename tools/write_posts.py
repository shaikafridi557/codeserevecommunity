"""
Creates new blog articles from content/new_posts/*.py, using an existing article as the page template.

For every post it writes:
  blog/<slug>.html                          the article (head, schema, hero, TOC, body, FAQ, related, CTA)
  assets/img/blog/<slug>.svg                featured image (same style as the existing posts)
  assets/img/blog/<slug>-<diagram>.svg      in-article diagram(s)
  assets/img/blog/<slug>-og.png             1200x630 share image (rendered from the SVG)
and adds / updates the post in content/blog-posts.json.

Then run:  python tools/build_blog.py   (index, categories, share links, sitemap)

Usage:  python tools/write_posts.py [slug ...]
"""
import html, importlib.util, json, math, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
BASE = "https://codeservecommunity.in"
TEMPLATE = "blog/whatsapp-business-api-guide.html"
FONT = "Poppins, 'Segoe UI', Arial, sans-serif"
e = lambda s: html.escape(s, quote=True)


# ----------------------------------------------------------------------------- images
def _grid():
    v = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="630"/>' for x in range(40, 1200, 40))
    h = "".join(f'<line x1="0" y1="{y}" x2="1200" y2="{y}"/>' for y in range(40, 630, 40))
    return f'<g stroke="#ffffff0d" stroke-width="1">{v}{h}</g>'


def featured_svg(label, lines, art, accent="#387cf9"):
    pill_w = 26 + len(label) * 13.5
    size = 56 if max(len(l) for l in lines) <= 19 else 50
    tsp = "".join(f'<tspan x="70" dy="{0 if i == 0 else size + 12}">{e(l)}</tspan>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <radialGradient id="glow" cx="78%" cy="40%" r="55%">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.2"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="630" fill="#131313"/>
  {_grid()}
  <rect width="1200" height="630" fill="url(#glow)"/>
  <rect x="70" y="70" width="{pill_w:.1f}" height="44" rx="22" fill="none" stroke="#387cf9" stroke-width="2"/>
  <text x="{70 + pill_w / 2:.1f}" y="100" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="600" fill="#387cf9" letter-spacing="1">{e(label)}</text>
  <text y="215" font-family="{FONT}" font-size="{size}" font-weight="700" fill="#ffffff">{tsp}</text>
  <text x="70" y="545" font-family="{FONT}" font-size="30" font-weight="700"><tspan fill="#ffffff">Code</tspan><tspan fill="#387cf9">Serve</tspan></text>
  <text x="70" y="578" font-family="{FONT}" font-size="18" fill="#9ca3af">codeservecommunity.in</text>
  <g transform="translate(700 90)">{art}</g>
</svg>
'''


def _box(x, y, w, h, lines, fill="#1f2937", stroke="#3a3a3a", color="#ffffff", size=17):
    n = len(lines)
    ty = y + h / 2 - (n - 1) * (size + 6) / 2 + size * 0.35
    t = "".join(f'<text x="{x + w / 2:.1f}" y="{ty + i * (size + 6):.1f}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="600" fill="{color}">{e(l)}</text>' for i, l in enumerate(lines))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>{t}'


def flow_svg(title, steps, highlight=(), width=800):
    """Boxes left to right with arrows. steps = [["line1","line2"], ...]."""
    n = len(steps); gap = 34; bw = (width - 60 - gap * (n - 1)) / n
    parts = [f'<rect width="{width}" height="300" rx="12" fill="#191919"/>',
             f'<text x="30" y="50" font-family="{FONT}" font-size="22" font-weight="700" fill="#ffffff">{e(title)}</text>']
    for i, s in enumerate(steps):
        x = 30 + i * (bw + gap)
        hi = i in highlight
        parts.append(_box(round(x, 1), 110, round(bw, 1), 100, s, fill="#387cf9" if hi else "#1f2937", stroke="#387cf9" if hi else "#3a3a3a", size=16 if bw < 150 else 17))
        if i < n - 1:
            ax = x + bw + 4
            parts.append(f'<path d="M{ax:.1f} 160 H{ax + gap - 10:.1f}" stroke="#25d366" stroke-width="3"/><path d="M{ax + gap - 12:.1f} 153 L{ax + gap - 4:.1f} 160 L{ax + gap - 12:.1f} 167 Z" fill="#25d366"/>')
        parts.append(f'<text x="{x + bw / 2:.1f}" y="250" text-anchor="middle" font-family="{FONT}" font-size="15" fill="#9ca3af">Step {i + 1}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 300" width="{width}" height="300">\n  ' + "\n  ".join(parts) + "\n</svg>\n"


def bars_svg(title, rows, unit="", note="", width=800):
    """Horizontal bars. rows = [(label, value, display_text, colour?)]."""
    h = 90 + len(rows) * 52 + (30 if note else 0)
    mx = max(r[1] for r in rows)
    parts = [f'<rect width="{width}" height="{h}" rx="12" fill="#191919"/>',
             f'<text x="30" y="50" font-family="{FONT}" font-size="22" font-weight="700" fill="#ffffff">{e(title)}</text>']
    for i, r in enumerate(rows):
        label, val, shown = r[0], r[1], r[2]
        col = r[3] if len(r) > 3 else "#387cf9"
        y = 84 + i * 52
        w = max(6, (width - 400) * val / mx)
        parts.append(f'<text x="30" y="{y + 24}" font-family="{FONT}" font-size="16" fill="#e5e7eb">{e(label)}</text>')
        parts.append(f'<rect x="250" y="{y + 6}" width="{w:.1f}" height="26" rx="6" fill="{col}"/>')
        parts.append(f'<text x="{250 + w + 10:.1f}" y="{y + 25}" font-family="{FONT}" font-size="16" font-weight="600" fill="#ffffff">{e(shown)}</text>')
    if note:
        parts.append(f'<text x="30" y="{h - 22}" font-family="{FONT}" font-size="14" fill="#9ca3af">{e(note)}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="{width}" height="{h}">\n  ' + "\n  ".join(parts) + "\n</svg>\n"


def grid_svg(title, cells, cols=3, width=800):
    """Tiles: cells = [(heading, sub, colour)]."""
    rows = math.ceil(len(cells) / cols)
    cw = (width - 60 - (cols - 1) * 16) / cols
    h = 80 + rows * 96 + 20
    parts = [f'<rect width="{width}" height="{h}" rx="12" fill="#191919"/>',
             f'<text x="30" y="50" font-family="{FONT}" font-size="22" font-weight="700" fill="#ffffff">{e(title)}</text>']
    for i, (hd, sub, col) in enumerate(cells):
        x = 30 + (i % cols) * (cw + 16); y = 76 + (i // cols) * 96
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="80" rx="10" fill="#1f2937" stroke="{col}" stroke-width="2"/>')
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="6" height="80" rx="3" fill="{col}"/>')
        parts.append(f'<text x="{x + 20:.1f}" y="{y + 34}" font-family="{FONT}" font-size="17" font-weight="700" fill="#ffffff">{e(hd)}</text>')
        parts.append(f'<text x="{x + 20:.1f}" y="{y + 60}" font-family="{FONT}" font-size="14" fill="#9ca3af">{e(sub)}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="{width}" height="{h}">\n  ' + "\n  ".join(parts) + "\n</svg>\n"


def render_png(svg_path, png_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.set_content(f'<html><body style="margin:0;background:#131313">{Path(svg_path).read_text(encoding="utf-8")}</body></html>')
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(png_path), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        b.close()


# ----------------------------------------------------------------------------- page
def words(html_text):
    return len(re.sub(r"<[^>]+>", " ", html_text).split())


def build_page(P, related_titles):
    T = Path(TEMPLATE).read_text(encoding="utf-8")
    url = f"{BASE}/blog/{P['slug']}.html"
    og = f"{BASE}/assets/img/blog/{P['slug']}-og.png"
    body = P["body"].strip("\n")
    # table of contents from the h2s
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    faq_html = "\n".join(f'''                    <details>
                        <summary>{e(q)}</summary>
                        <p>{a}</p>
                    </details>''' for q, a in P["faq"])
    heads.append(("faq", "Frequently asked questions"))
    toc = "\n".join(f'                        <li><a href="#{i}">{t}</a></li>' for i, t in heads)
    figure = f'<figure class="cs-figure cs-featured"><img src="../assets/img/blog/{P["slug"]}.svg" alt="{e(P["image_alt"])}" width="1200" height="630"></figure>'
    article = f'''<article class="cs-article">
            <div class="cs-container cs-article-layout">
                <aside class="cs-article-aside">
    <nav class="cs-toc" aria-label="Table of contents">
                    <strong>In this guide</strong>
                    <ol>
{toc}
                    </ol>
                </nav>
                </aside>
                <div class="cs-article-body">
                    {figure}
{body}
                <h2 id="faq">Frequently asked questions</h2>
                <div class="cs-faq">
{faq_html}
                </div>

                <div class="cs-callout">
                    {P["closing"]}
                </div>

                </div>
            </div>
        </article>'''
    s = re.sub(r"<article class=\"cs-article\">.*?</article>", lambda m: article, T, count=1, flags=re.S)

    related = "\n".join(f'                    <a href="{h}">{e(t)} →</a>' for h, t in related_titles)
    tail = f'''<section data-dsn-animate="section" class="cs-section cs-section-soft">
            <div class="cs-container">
                <h2>Related reading</h2>
                <div class="cs-related">
{related}
                </div>
            </div>
        </section>

        <section data-dsn-animate="section" class="cs-cta">
            <div class="cs-container">
                <h2>{e(P["cta_title"])}</h2>
                <p>{e(P["cta_text"])}</p>
                <div class="cs-btns">
                    <a class="cs-btn cs-btn-whatsapp" href="https://wa.me/918186841086?text={P["cta_wa"]}" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> Chat on WhatsApp</a>
                    <a class="cs-btn cs-btn-ghost" href="{P["cta_link"][0]}">{e(P["cta_link"][1])}</a>
                </div>
            </div>
        </section>'''
    s = re.sub(r'<section data-dsn-animate="section" class="cs-section cs-section-soft">.*?<section data-dsn-animate="section" class="cs-cta">.*?</section>', lambda m: tail, s, count=1, flags=re.S)

    # head
    s = re.sub(r"<title>.*?</title>", lambda m: f"<title>{e(P['seo_title'])}</title>", s, count=1, flags=re.S)
    for prop, val in (("og:url", url), ("og:title", P["seo_title"]), ("og:description", P["meta_description"]), ("og:image", og)):
        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m: m.group(1) + e(val), s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(P["meta_description"]), s, count=1)
    s = re.sub(r'(<meta name="twitter:image" content=")[^"]*', lambda m: m.group(1) + og, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    schema = [
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": P["h1"], "description": P["meta_description"],
         "datePublished": P["date"], "dateModified": P["date"],
         "author": {"@type": "Organization", "name": "CodeServe Community", "url": f"{BASE}/"},
         "publisher": {"@type": "Organization", "name": "CodeServe Community", "url": f"{BASE}/", "@id": f"{BASE}/#business"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "inLanguage": "en-IN", "image": og,
         "keywords": ", ".join([P["primary_keyword"]] + P["secondary_keywords"])},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
            {"@type": "ListItem", "position": 4, "name": P["h1"], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in P["faq"]]},
    ]
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               lambda m: '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2) + "\n    </script>", s, count=1, flags=re.S)
    # hero
    s = re.sub(r'<p class="hero-tagline cs-breadcrumb"[^>]*>.*?</p>',
               lambda m: f'<p class="hero-tagline cs-breadcrumb" data-dsn-animate="up"><a href="../index.html">Home</a> / <a href="index.html">Blog</a> / {e(P["breadcrumb"])}</p>', s, count=1, flags=re.S)
    s = re.sub(r'(<h1 class="title-h2 text-upper">).*?(</h1>)', lambda m: m.group(1) + e(P["h1"]) + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<p class="mt-20 max-w750 m-auto hero-subtitle" data-dsn-animate="up">).*?(</p>)', lambda m: m.group(1) + P["intro"] + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<!--cs:share-author-->.*?<!--/cs:share-author-->\n?', "", s, flags=re.S)
    s = s.replace('<meta property="article:published_time" content="2026-11-02">', f'<meta property="article:published_time" content="{P["date"]}">')
    return s


def load_posts():
    out = []
    for f in sorted(Path("content/new_posts").glob("*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        out.extend(m.POSTS)
    return out


def main(only):
    db_path = Path("content/blog-posts.json")
    db = json.loads(db_path.read_text(encoding="utf-8"))
    titles = {p["slug"]: p["h1"] for p in db["posts"]}
    posts = load_posts()
    for P in posts:
        titles[P["slug"]] = P["h1"]
    for P in posts:
        if only and P["slug"] not in only:
            continue
        img = Path("assets/img/blog")
        svg = img / f"{P['slug']}.svg"
        svg.write_text(featured_svg(P["label"], P["title_lines"], P["art"]), encoding="utf-8")
        for name, content in P.get("diagrams", {}).items():
            (img / f"{P['slug']}-{name}.svg").write_text(content, encoding="utf-8")
        render_png(svg, img / f"{P['slug']}-og.png")
        rel = [(f"{s}.html", titles[s]) for s in P["related"] if s in titles] + P.get("related_pages", [])
        Path(f"blog/{P['slug']}.html").write_text(build_page(P, rel), encoding="utf-8")
        entry = {
            "slug": P["slug"], "url": f"/blog/{P['slug']}.html", "canonical": f"{BASE}/blog/{P['slug']}.html",
            "content_file": f"blog/{P['slug']}.html", "seo_title": P["seo_title"], "meta_description": P["meta_description"],
            "h1": P["h1"], "primary_keyword": P["primary_keyword"], "secondary_keywords": P["secondary_keywords"],
            "category": P["category"], "short_description": P["short_description"], "author": "CodeServe Team",
            "date_published": P["date"], "date_modified": P["date"],
            "reading_time_min": max(3, round((words(P["body"]) + sum(words(a) + 10 for _, a in P["faq"])) / 220)),
            "featured_image": f"/assets/img/blog/{P['slug']}.svg", "og_image": f"{BASE}/assets/img/blog/{P['slug']}-og.png",
            "image_alt": P["image_alt"], "related_articles": [s for s in P["related"] if s in titles][:3],
            "related_service": P["related_service"],
        }
        db["posts"] = [p for p in db["posts"] if p["slug"] != P["slug"]] + [entry]
        print(f"wrote blog/{P['slug']}.html  ({entry['reading_time_min']} min, {words(P['body'])} words)")
    db_path.write_text(json.dumps(db, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
