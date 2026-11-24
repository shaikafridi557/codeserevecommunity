# CodeServe — SEO implementation report

Site: https://codeservecommunity.in/ · Updated 24 November 2026
(The older root-level report from November 2026 is kept at `docs/legacy/SEO_IMPLEMENTATION_REPORT.md` for history; it predates the domain move.)

## Metadata
- Every indexable page (69) has a unique `<title>`, unique meta description, canonical URL on `https://codeservecommunity.in/`, Open Graph title/description/image, Twitter card, `og:locale` en_IN and `lang="en"`/`en-IN`. Enforced by `python tools/check_site.py`.
- No meta keywords (Google ignores them).

## Keyword map (service pages)
| Page | Primary search |
|---|---|
| `/` | website development company in Hyderabad |
| `/website-development.html` | website development services Hyderabad |
| `/web-design.html` | web design company in Hyderabad (Kukatpally, KPHB) |
| `/ecommerce-website-development.html` | e-commerce website development Hyderabad |
| `/seo-services.html` | SEO services in Hyderabad |
| `/digital-marketing.html` | digital marketing services Hyderabad |
| `/ai-automation-services.html` | AI automation company Hyderabad |
| `/ai-chatbot-development.html` | AI chatbot development company India |
| `/whatsapp-automation.html` | WhatsApp automation / Business API Hyderabad |
| `/mobile-app-development.html` | mobile app development Hyderabad |
| `/custom-software-development.html` | custom software development Hyderabad |
| `/billing-software-development.html` | billing / GST software development |
| `/hire-developers.html` | hire freelancers / developers in Hyderabad |
| `/offshore-web-development.html`, `/white-label-web-development.html`, 4 country pages | offshore, white label, country-specific intent |

Location words (Hyderabad, Kukatpally, KPHB) are in titles, headings and content; URLs are kept clean.

## URLs and redirects
- 11 service URLs renamed without place names; old URLs (with and without `.html`) 301 to the new ones; old `netlify.app` addresses 301 directly to the new pages.
- `netlify.app` → `codeservecommunity.in`, `www` → bare domain (301).
- `/tools/*`, `/content/*`, `/docs/*` return 404 (internal files).

## Sitemap and robots
- `sitemap.xml`: 65 canonical, indexable URLs with image entries; noindex category pages (fewer than 2 articles) are excluded automatically by `tools/build_blog.py`.
- `robots.txt`: allows all public content and AI/search crawlers; blocks `.git`, `.vscode`, `.kiro`, `tools`, `content`, `docs`, broken font fallbacks; references `https://codeservecommunity.in/sitemap.xml`.

## Structured data (JSON-LD, all validated by script)
| Type | Pages |
|---|---|
| ProfessionalService (`@id` …/#business, same name/address/phone) | homepage, contact, web design page, provider on every service page |
| WebSite | homepage |
| Service + Offer (prices from `content/site.json`) | every service page |
| BreadcrumbList | every page except homepage and 404 |
| BlogPosting (Organization author, dates, section) | every article |
| CollectionPage + ItemList | blog category pages |
| FAQPage (visible FAQs only) | homepage, service pages, articles, FAQ, pricing |
No ratings, reviews or awards are marked up.

## Internal linking
- Homepage → 10 service cards → service pages → contact; homepage → latest 3 guides → blog.
- Every article → its service page, 3+ related articles, category page, CTA.
- Every footer → all service pages; service pages → related services and guides.

## Images
- Every `<img>` has alt text (checked by script); in-article diagrams have captions; below-the-fold images lazy-load; homepage images have WebP `srcset` and explicit sizes; blog share images show the real illustration.

## Indexing recommendations (owner actions)
1. Search Console (`codeservecommunity.in` property): resubmit `sitemap.xml` after this deploy; request indexing for `/`, `/contact.html`, `/website-development.html`, `/seo-services.html`.
2. Keep the Change of Address active on the old `netlify.app` property (about 180 days).
3. Bing Webmaster Tools: import from Search Console.
4. Google Business Profile: website `https://codeservecommunity.in`, phone +91 81868 41086, services, photos, genuine reviews.
