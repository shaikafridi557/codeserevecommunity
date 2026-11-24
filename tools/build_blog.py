"""
CodeServe blog builder.

Reads content/blog-posts.json (the blog content database) and regenerates:
  - blog/index.html        : post grid, category links, search box, Blog JSON-LD
  - blog/category-*.html   : one listing page per category that has posts
  - every article page     : category breadcrumb + badge, dates, share links,
                             author box, articleSection and BreadcrumbList JSON-LD
  - sitemap.xml            : category page entries

Article body content stays in each blog/<slug>.html file.
Safe to run repeatedly (uses <!--cs:...--> markers).

Usage:  python tools/build_blog.py
"""
import html, json, os, re, sys
from datetime import date
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = 'https://codeservecommunity.in'
DB = json.load(open('content/blog-posts.json', encoding='utf-8'))
CATS = {c['slug']: c for c in DB['categories']}
POSTS = sorted(DB['posts'], key=lambda p: (p['date_published'], p['slug']), reverse=True)
BY_CAT = {c: [p for p in POSTS if p['category'] == c] for c in CATS}
MIN_INDEXABLE = 2            # category pages with fewer posts are noindex,follow and kept out of the sitemap
e = lambda s: html.escape(s, quote=True)

def human(d):
    y, m, dd = map(int, d.split('-'))
    return f"{dd} {date(y, m, dd).strftime('%B')} {y}"

def rd(f): return open(f, encoding='utf-8').read()
def wr(f, s): open(f, 'w', encoding='utf-8').write(s)

def put_block(s, name, content, before=None, after=None):
    """Insert or replace a <!--cs:name--> ... <!--/cs:name--> block."""
    block = f'<!--cs:{name}-->{content}<!--/cs:{name}-->'
    pat = re.compile(rf'<!--cs:{name}-->.*?<!--/cs:{name}-->', re.S)
    if pat.search(s): return pat.sub(lambda m: block, s, count=1)
    if before:
        i = s.index(before); return s[:i] + block + s[i:]
    i = s.index(after) + len(after); return s[:i] + block + s[i:]

def rewrite_jsonld(s, fn):
    def repl(m):
        data = json.loads(m.group(2))
        return m.group(1) + '\n' + json.dumps(fn(data), ensure_ascii=False, indent=2) + '\n    ' + m.group(3)
    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', repl, s, flags=re.S)

def card(p, prefix=''):
    c = CATS[p['category']]
    search = f"{p['h1']} {p['short_description']} {c['name']} {p['primary_keyword']}".lower()
    return f'''                    <a data-dsn-animate="up" class="cs-post-card" href="{prefix}{p['slug']}.html" data-category="{c['slug']}" data-search="{e(search)}">
                        <img class="cs-post-thumb" src="../assets/img/blog/{p['slug']}.svg" alt="{e(p['image_alt'])}" width="1200" height="630" loading="lazy">
                        <span class="cs-tag">{e(c['name'])}</span>
                        <h2>{e(p['h1'])}</h2>
                        <p>{e(p['short_description'])}</p>
                        <span class="cs-read">Read more →</span>
                    </a>'''

def cat_nav(active=None):
    items = [f'<a class="cs-cat-chip{" is-active" if active is None else ""}" href="index.html">All articles</a>']
    for slug, c in CATS.items():
        if not BY_CAT[slug]: continue
        cls = ' is-active' if slug == active else ''
        items.append(f'<a class="cs-cat-chip{cls}" href="category-{slug}.html">{e(c["name"])} <span>({len(BY_CAT[slug])})</span></a>')
    return '\n                    '.join(items)

TOOLS_CSS = '''<style>
        .cs-blog-tools{margin-bottom:34px}
        .cs-blog-search{width:100%;max-width:520px;padding:12px 16px;border-radius:8px;border:1px solid var(--border-color);background:var(--assistant-color);color:var(--heading-color,#fff);font-size:15px;margin-bottom:18px}
        .cs-cat-nav{display:flex;flex-wrap:wrap;gap:10px}
        .cs-cat-chip{display:inline-block;padding:7px 14px;border:1px solid var(--border-color);border-radius:999px;font-size:13px;color:var(--font-color);text-decoration:none}
        .cs-cat-chip span{opacity:1}
        .cs-cat-chip:hover,.cs-cat-chip.is-active{border-color:var(--cs-accent);color:var(--cs-accent)}
        .cs-blog-empty{display:none;margin-top:20px}
        .cs-share{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:34px 0 10px}
        .cs-share a{padding:6px 14px;border:1px solid var(--border-color);border-radius:999px;font-size:13px;text-decoration:none}
        .cs-share a:hover{border-color:var(--cs-accent);color:var(--cs-accent)}
        a.cs-tag{text-decoration:none}
    </style>'''

SEARCH_JS = '''<script>
(function(){var i=document.getElementById('cs-blog-search');if(!i)return;var cards=[].slice.call(document.querySelectorAll('.cs-post-card[data-search]')),empty=document.getElementById('cs-blog-empty');
i.addEventListener('input',function(){var q=i.value.trim().toLowerCase(),n=0;cards.forEach(function(c){var ok=!q||c.getAttribute('data-search').indexOf(q)!==-1;c.style.display=ok?'':'none';if(ok)n++;});if(empty)empty.style.display=n?'none':'block';});})();
</script>'''

def tools_html(active=None):
    return f'''
                <div class="cs-blog-tools">
                    <label for="cs-blog-search" class="sr-only" style="position:absolute;left:-9999px">Search articles</label>
                    <input id="cs-blog-search" class="cs-blog-search" type="search" placeholder="Search articles…" autocomplete="off">
                    <nav class="cs-cat-nav" aria-label="Blog categories">
                    {cat_nav(active)}
                    </nav>
                </div>
'''

def set_grid(s, posts, active=None):
    grid = '\n' + '\n'.join(card(p) for p in posts) + '\n                    <p id="cs-blog-empty" class="cs-blog-empty">No articles match your search.</p>\n'
    if '<!--cs:posts-->' not in s:
        m = re.search(r'(                <div class="cs-grid">\n)(.*?)(\n                </div>\n            </div>\n        </section>)', s, re.S)
        s = s[:m.start(2)] + '<!--cs:posts--><!--/cs:posts-->' + s[m.end(2):]
    s = put_block(s, 'posts', grid)
    s = put_block(s, 'tools', tools_html(active), before='                <div class="cs-grid">\n<!--cs:posts-->') if '<!--cs:tools-->' not in s else put_block(s, 'tools', tools_html(active))
    s = put_block(s, 'blogcss', TOOLS_CSS, before='</head>')
    s = put_block(s, 'searchjs', SEARCH_JS, before='</body>')
    return s

# ---------------------------------------------------------------- blog index
idx = rd('blog/index.html')
idx = set_grid(idx, POSTS)
def fix_blog_schema(data):
    for o in (data if isinstance(data, list) else [data]):
        if o.get('@type') == 'Blog':
            o['blogPost'] = [{"@type": "BlogPosting", "headline": p['h1'], "url": p['canonical'], "datePublished": p['date_published'], "image": p['og_image']} for p in POSTS]
    return data
idx = rewrite_jsonld(idx, fix_blog_schema)
wr('blog/index.html', idx)

# ---------------------------------------------------------------- category pages
TPL = idx
written = []
for slug, c in CATS.items():
    posts = BY_CAT[slug]; f = f'blog/category-{slug}.html'
    if not posts:
        if os.path.exists(f): os.remove(f)
        continue
    url = f'{BASE}/blog/category-{slug}.html'
    title = f"{c['name']} Articles | CodeServe Blog"
    desc = c['description']
    s = TPL
    s = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*', rf'\g<1>{e(desc)}', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', rf'\g<1>{e(desc)}', s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', rf'\g<1>{e(title)}', s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', rf'\g<1>{url}', s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', rf'\g<1>{url}', s, count=1)
    robots = 'index, follow' if len(posts) >= MIN_INDEXABLE else 'noindex, follow'
    s = re.sub(r'(<meta name="robots" content=")[^"]*', rf'\g<1>{robots}', s, count=1)
    s = re.sub(r'<p class="hero-tagline cs-breadcrumb"[^>]*>.*?</p>', f'<p class="hero-tagline cs-breadcrumb" data-dsn-animate="up"><a href="../index.html">Home</a> / <a href="index.html">Blog</a> / {e(c["name"])}</p>', s, count=1, flags=re.S)
    s = re.sub(r'(<h1 class="title-h2 text-upper">).*?(</h1>)', rf'\g<1>{e(c["name"])}\2', s, count=1, flags=re.S)
    s = re.sub(r'(<p class="mt-20 max-w750 m-auto hero-subtitle" data-dsn-animate="up">).*?(</p>)',
               lambda m: m.group(1) + e(desc) + f' Related service: <a href="{c["service"]}">{e(c["name"])} at CodeServe</a>.' + m.group(2), s, count=1, flags=re.S)
    s = set_grid(s, posts, active=slug)
    schema = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc, "url": url,
         "isPartOf": {"@type": "Blog", "name": "CodeServe Blog", "url": f"{BASE}/blog/"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": p['canonical'], "name": p['h1']} for i, p in enumerate(posts)]}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": c['name'], "item": url}]},
    ]
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, re.S))
    new = '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2) + '\n    </script>'
    s = s[:blocks[0].start()] + new + s[blocks[-1].end():] if blocks else s
    wr(f, s); written.append((slug, len(posts), robots))

# ---------------------------------------------------------------- article pages
for p in POSTS:
    f = p['content_file']; s = rd(f); c = CATS[p['category']]
    cat_href = f"category-{c['slug']}.html"
    # breadcrumb: Home / Blog / Category / Short title
    m = re.search(r'<p class="hero-tagline cs-breadcrumb"[^>]*>(.*?)</p>', s, re.S)
    short = re.sub(r'<[^>]+>', '', m.group(1)).split(' / ')[-1].strip()
    s = s[:m.start()] + f'<p class="hero-tagline cs-breadcrumb" data-dsn-animate="up"><a href="../index.html">Home</a> / <a href="index.html">Blog</a> / <a href="{cat_href}">{e(c["name"])}</a> / {e(short)}</p>' + s[m.end():]
    # category badge above H1 (replaces any hand-made badge)
    s = re.sub(r'\n\s*<p class="mt-20" data-dsn-animate="up"><span class="cs-tag">[^<]*</span></p>', '', s)
    s = put_block(s, 'badge', f'<p class="mt-20" data-dsn-animate="up"><a class="cs-tag" href="{cat_href}">{e(c["name"])}</a></p>\n                            ',
                  before='<div id="hero_title"')
    # meta line with dates and reading time
    upd = f' · Updated <time datetime="{p["date_modified"]}">{human(p["date_modified"])}</time>' if p['date_modified'] > p['date_published'] else ''
    meta = f'By {e(p["author"])} · <time datetime="{p["date_published"]}">{human(p["date_published"])}</time>{upd} · {p["reading_time_min"]} min read · <a href="{cat_href}">{e(c["name"])}</a>'
    s = re.sub(r'(<p class="cs-hero-meta" data-dsn-animate="up">).*?(</p>)', lambda m: m.group(1) + meta + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<meta property="article:section" content=")[^"]*', rf'\g<1>{e(c["name"])}', s)
    s = re.sub(r'(<meta property="article:modified_time" content=")[^"]*', rf'\g<1>{p["date_modified"]}', s)
    # remove one-off author box added by hand earlier
    if '<!--cs:share-author-->' not in s:
        s = re.sub(r'                <div class="cs-callout">\n                    <h3 style="margin-top:0;">About the author</h3>\n                    <p>.*?</p>\n                </div>\n\n', '', s, flags=re.S)
    # share links + author box, before the closing CTA callout of the article
    u = quote(p['canonical'], safe=''); t = quote(p['h1'], safe='')
    share = f'''
                <div class="cs-share" aria-label="Share this article"><strong>Share:</strong>
                    <a data-share="whatsapp" href="https://api.whatsapp.com/send?text={t}%20{u}" target="_blank" rel="noopener">WhatsApp</a>
                    <a data-share="linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url={u}" target="_blank" rel="noopener">LinkedIn</a>
                    <a data-share="x" href="https://twitter.com/intent/tweet?url={u}&amp;text={t}" target="_blank" rel="noopener">X</a>
                    <a data-share="facebook" href="https://www.facebook.com/sharer/sharer.php?u={u}" target="_blank" rel="noopener">Facebook</a>
                </div>
                <div class="cs-callout">
                    <h3 style="margin-top:0;">About the author</h3>
                    <p><strong>{e(p["author"])}</strong> — the web development and automation team at CodeServe Community in KPHB, Kukatpally, Hyderabad. We build websites, AI chatbots, automation and business software, and write these guides from the questions clients ask us. Related service: <a href="{p["related_service"]}">learn how we can help</a>.</p>
                </div>
'''
    if '<!--cs:share-author-->' in s:
        s = put_block(s, 'share-author', share)
    else:
        art_end = s.index('</article>')
        anchor = s.rfind('<div class="cs-callout">', 0, art_end)
        line_start = s.rfind('\n', 0, anchor) + 1
        s = s[:line_start] + '<!--cs:share-author-->' + share + '<!--/cs:share-author-->\n' + s[line_start:]
    s = put_block(s, 'blogcss', TOOLS_CSS, before='</head>')
    # JSON-LD: section, dates, 4-level breadcrumb
    def fix(data):
        for o in (data if isinstance(data, list) else [data]):
            if o.get('@type') == 'BlogPosting':
                o['articleSection'] = c['name']; o['dateModified'] = p['date_modified']
                o['author'] = {"@type": "Organization", "name": "CodeServe Community", "url": f"{BASE}/"}
            if o.get('@type') == 'BreadcrumbList':
                o['itemListElement'] = [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
                    {"@type": "ListItem", "position": 3, "name": c['name'], "item": f"{BASE}/blog/category-{c['slug']}.html"},
                    {"@type": "ListItem", "position": 4, "name": p['h1'], "item": p['canonical']}]
        return data
    s = rewrite_jsonld(s, fix)
    s = re.sub(r'\n[ \t]*<meta name="keywords" content="[^"]*">', '', s)
    wr(f, s)

# ---------------------------------------------------------------- homepage: latest guides
# The three newest articles, shown on the homepage just above the local "Based in Kukatpally" section.
home = rd('index.html')
latest_cards = '\n'.join(f'''                            <a class="cs-post-card" href="blog/{p['slug']}.html">
                                <img class="cs-post-thumb" src="assets/img/blog/{p['slug']}.svg" alt="{e(p['image_alt'])}" width="1200" height="630" loading="lazy">
                                <span class="cs-tag">{e(CATS[p['category']]['name'])}</span>
                                <h3>{e(p['h1'])}</h3>
                                <p>{e(p['short_description'])}</p>
                                <span class="cs-read">Read more →</span>
                            </a>''' for p in POSTS[:3])
latest = f'''
                <section class="cs-section">
                    <div class="cs-container">
                        <h2>Latest guides for business owners</h2>
                        <p class="cs-section-intro">Practical, no-jargon articles on websites, AI, WhatsApp automation and getting found on Google.</p>
                        <div class="cs-grid">
{latest_cards}
                        </div>
                        <p style="margin-top:24px;"><a class="cs-btn cs-btn-ghost" href="blog/">Read all articles</a></p>
                    </div>
                </section>
'''
if '<!--cs:home-latest-->' in home:
    home = put_block(home, 'home-latest', latest)
else:
    anchor = '                <section class="cs-section">\n                    <div class="cs-container cs-narrow">\n                        <h2>Based in Kukatpally'
    nl = '\r\n' if '\r\n' in home else '\n'
    a = anchor.replace('\n', nl)
    if a in home:
        home = home.replace(a, '<!--cs:home-latest-->' + latest.replace('\n', nl) + '<!--/cs:home-latest-->' + nl + a, 1)
wr('index.html', home)

# ---------------------------------------------------------------- sitemap
sm = rd('sitemap.xml')
sm = re.sub(r'\s*<url>\s*<loc>https://codeservecommunity\.in/blog/category-[^<]*</loc>.*?</url>', '', sm, flags=re.S)
for p in POSTS:
    if p['canonical'] not in sm:
        sm = sm.replace('</urlset>', f'''    <url>
        <loc>{p['canonical']}</loc>
        <lastmod>{p['date_modified']}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
        <image:image><image:loc>{BASE}{p['featured_image']}</image:loc></image:image>
    </url>
</urlset>''')
add = ''
for slug, n, robots in written:
    if robots.startswith('index'):
        last = max(p['date_modified'] for p in BY_CAT[slug])
        add += f'''    <url>
        <loc>{BASE}/blog/category-{slug}.html</loc>
        <lastmod>{last}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.5</priority>
    </url>
'''
sm = sm.replace('</urlset>', add + '</urlset>')
wr('sitemap.xml', sm)

print(f'{len(POSTS)} articles updated; blog index regenerated')
for slug, n, robots in written: print(f'  category-{slug}.html  posts={n}  {robots}')
empty = [c for c in CATS if not BY_CAT[c]]
if empty: print('  categories with no posts (no page generated):', ', '.join(empty))
