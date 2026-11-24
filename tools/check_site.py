"""
Checks every page against content/site.json (the single source of truth for business details and prices)
and runs basic technical SEO checks. Exit code 1 if anything is wrong.

    python tools/check_site.py
"""
import glob, html, json, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding='utf-8')
cfg = json.load(open('content/site.json', encoding='utf-8'))
biz = cfg['business']
BASE = biz['domain'].rstrip('/') + '/'
prices = {v for group in cfg['pricing'].values() for v in group.values()} | set(cfg['estimates_allowed'])
phone10 = biz['phone_e164'][-10:]
placeholders = set(cfg['placeholders_allowed_in_code_examples'])

pages = sorted(p.replace(os.sep, '/') for p in glob.glob('**/*.html', recursive=True) if not p.startswith(('assets', '.')))
sitemap = {u.text for u in ET.parse('sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
problems, titles, descs = [], {}, {}

def strip_code(s):  # code examples in articles may show sample numbers
    return re.sub(r'<(pre|code)\b.*?</\1>', ' ', s, flags=re.S)

for f in pages:
    raw = open(f, encoding='utf-8').read()
    s = strip_code(raw)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    # business details
    for num in re.findall(r'(?<!\d)(?:\+?91[ -]?)?([6-9]\d{4}[ -]?\d{5})(?!\d)', text + ' ' + s):
        d = re.sub(r'\D', '', num)
        if d != phone10 and d not in placeholders: problems.append((f, f'unknown phone number {num}'))
    for w in re.findall(r'wa\.me/(\d+)', s):
        if w != biz['whatsapp_number'] and w not in placeholders: problems.append((f, f'WhatsApp link to {w}'))
    for em in set(re.findall(r'[\w.+-]+@[\w-]+\.(?:com|in|net|org|co)\b', s)):
        if em != biz['email'] and not em.endswith(('@example.com', '@example.invalid')): problems.append((f, f'unknown email {em}'))
    if 'netlify.app' in s and not f.startswith('blog/'): problems.append((f, 'old netlify.app address'))
    for m in re.findall(r'until (\d{1,2} \w+ \d{4})', text):
        if 'launch offer' in text.lower() and m != cfg['payment_terms']['launch_offer_until']: problems.append((f, f'launch offer date {m}'))
    # prices on business pages (blog posts quote market ranges, so only business pages are checked)
    if not f.startswith('blog/') and f != '404.html':
        for p in set(re.findall(r'₹ ?\d[\d,]*\d', text)):
            if p.replace(' ', '') not in prices: problems.append((f, f'price {p} is not in content/site.json'))
    # technical SEO
    if f == '404.html': continue
    t = re.search(r'<title>(.*?)</title>', raw, re.S)
    d = re.search(r'<meta name="description"\s+content="([^"]*)"', raw)
    c = re.search(r'<link rel="canonical" href="([^"]+)"', raw)
    robots = (re.search(r'<meta name="robots" content="([^"]*)"', raw) or [None, ''])[1]
    expected = BASE + ('' if f == 'index.html' else 'blog/' if f == 'blog/index.html' else f)
    if not t: problems.append((f, 'no <title>'))
    else: titles.setdefault(t.group(1).strip(), []).append(f)
    if not d: problems.append((f, 'no meta description'))
    else: descs.setdefault(d.group(1), []).append(f)
    if not c or c.group(1) != expected: problems.append((f, f'canonical {c.group(1) if c else "missing"}'))
    if len(re.findall(r'<h1[\s>]', raw)) != 1: problems.append((f, 'not exactly one H1'))
    if not re.search(r'<html[^>]*lang="en(-[A-Z]{2})?"', raw[:400]): problems.append((f, 'missing lang="en"'))
    if 'og:image' not in raw: problems.append((f, 'no og:image'))
    noindex = 'noindex' in robots
    if not noindex and expected not in sitemap: problems.append((f, 'indexable page missing from sitemap.xml'))
    if noindex and expected in sitemap: problems.append((f, 'noindex page listed in sitemap.xml'))
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try: json.loads(b)
        except Exception as ex: problems.append((f, f'invalid JSON-LD: {ex}'))
    for img in re.findall(r'<img\b[^>]*>', raw):
        if 'alt=' not in img: problems.append((f, 'image without alt'))
    for href in re.findall(r'(?:href|src)="([^"#?:]+\.(?:html|jpg|jpeg|png|webp|svg|css|js))"', strip_code(raw)):
        target = href.lstrip('/') if href.startswith('/') else os.path.normpath(os.path.join(os.path.dirname(f), href)).replace(os.sep, '/')
        if not os.path.exists(target): problems.append((f, f'broken link {href}'))

for t, v in titles.items():
    if len(v) > 1: problems.append((', '.join(v), f'duplicate title "{t}"'))
for d, v in descs.items():
    if len(v) > 1: problems.append((', '.join(v), 'duplicate meta description'))
for loc in sitemap:
    p = loc.replace(BASE, '') or 'index.html'
    if p.endswith('/'): p += 'index.html'
    if not os.path.exists(p): problems.append(('sitemap.xml', f'URL without a page: {loc}'))
rb = open('robots.txt', encoding='utf-8').read()
if f'Sitemap: {BASE}sitemap.xml' not in rb: problems.append(('robots.txt', 'sitemap line missing or wrong'))
if re.search(r'Disallow: /(assets/)?(css|js|img)\b', rb): problems.append(('robots.txt', 'blocks CSS/JS/images'))

print(f'Checked {len(pages)} pages and {len(sitemap)} sitemap URLs against content/site.json')
for where, what in problems: print(f'  ✗ {where}: {what}')
print('✓ No problems found' if not problems else f'{len(problems)} problem(s)')
sys.exit(1 if problems else 0)
