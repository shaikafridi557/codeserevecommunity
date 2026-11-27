"""One-off SEO upgrades (Nov 2026, from Search Console queries): sharper titles on existing posts and
internal links from older posts to the new cluster posts. Safe to re-run."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = "2026-11-28"
DB = ROOT / "content/blog-posts.json"
db = json.loads(DB.read_text(encoding="utf-8"))
posts = {p["slug"]: p for p in db["posts"]}

TITLES = {
    "ai-chatbot-development-cost-india": "Chatbot Development Cost in India (2026): How Much Does a Chatbot Cost?",
    "white-label-web-development-guide": "White Label Web Development Services: How Agencies Grow Without Hiring",
    "outsourcing-web-development-india-cost": "Outsource Web Development to India: 2026 Costs and Risks",
}

LINKS = {
    "ai-chatbot-development-cost-india": 'Want a predictable budget? Read <a href="fixed-price-ai-development.html">how fixed-price AI development works</a> — what can be quoted fixed and what can\'t.',
    "hire-offshore-developers-india-guide": 'Planning a longer-term team rather than a single hire? See <a href="build-offshore-team-india.html">how to build an offshore team in India</a> — dedicated team vs EOR vs your own centre.',
    "outsourcing-web-development-india-cost": 'Need an ongoing team instead of a one-off project? Read <a href="build-offshore-team-india.html">how to build an offshore team in India</a>.',
    "white-label-web-development-guide": 'Growing past project-by-project work? See <a href="build-offshore-team-india.html">how to build a dedicated offshore team in India</a>.',
    "rank-in-ai-search-google-ai-mode-chatgpt": 'Want to measure your progress? See the <a href="ai-seo-tools-chatgpt-ai-overviews.html">AI SEO tools that track mentions in ChatGPT and AI Overviews</a>.',
    "mobile-app-cost-india-2026": 'Building a startup product? Read <a href="custom-software-development-startups-hyderabad.html">custom software for startups in Hyderabad: MVP scope, cost and timeline</a>.',
    "whatsapp-business-api-uae": 'Messaging customers in India too? See <a href="whatsapp-business-api-pricing-india.html">WhatsApp Business API pricing in India</a>.',
    "woocommerce-whatsapp-order-notifications": 'What will these messages cost? See <a href="whatsapp-business-api-pricing-india.html">WhatsApp API pricing in India</a> and more <a href="whatsapp-business-api-use-cases.html">WhatsApp API use cases</a>.',
    "freelancer-vs-agency-india": 'Building a startup product? Read <a href="custom-software-development-startups-hyderabad.html">custom software for startups in Hyderabad</a>.',
}

for slug, title in TITLES.items():
    f = ROOT / posts[slug]["content_file"]; s = f.read_text(encoding="utf-8")
    old = posts[slug]["seo_title"]
    s = s.replace(f"<title>{old}</title>", f"<title>{title}</title>")
    s = s.replace(f'<meta property="og:title" content="{old}">', f'<meta property="og:title" content="{title}">')
    f.write_text(s, encoding="utf-8")
    posts[slug]["seo_title"] = title

for slug, text in LINKS.items():
    f = ROOT / posts[slug]["content_file"]; s = f.read_text(encoding="utf-8")
    if "<!--cs:readnext-->" in s:
        s = re.sub(r"<!--cs:readnext-->.*?<!--/cs:readnext-->", lambda m: f'<!--cs:readnext--><div class="cs-callout"><strong>Read next:</strong> {text}</div><!--/cs:readnext-->', s, flags=re.S)
    else:
        m = re.search(r'\n(\s*)<h2 id="faq"', s) or re.search(r'\n(\s*)<h2[^>]*>Frequently asked questions</h2>', s)
        assert m, slug
        block = f'\n{m.group(1)}<!--cs:readnext--><div class="cs-callout"><strong>Read next:</strong> {text}</div><!--/cs:readnext-->\n'
        s = s[:m.start()] + block + s[m.start():]
    f.write_text(s, encoding="utf-8")

DB.write_text(json.dumps(db, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("titles:", len(TITLES), "links:", len(LINKS))
