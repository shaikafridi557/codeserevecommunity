# CodeServe website — audit report

Site: https://codeservecommunity.in/ · Repository: `codeserevecommunity` (GitHub `shaikafridi557/codeserevecommunity`, branch `master`)
Audit date: 24 November 2026 · Git checkpoint before changes: tag `pre-audit-2026-11-24`

Severity: **Critical** (breaks leads, trust or indexing) · **High** (clear SEO/conversion loss) · **Medium** · **Low**.
"Status" says whether it was fixed in this round, fixed in an earlier round, or still open. Nothing here is claimed as tested unless it was run.

---

## 1. Project architecture (Phase 1)

| Item | Finding |
|---|---|
| Stack | Static HTML/CSS/JS. No framework, no `package.json`, no build step. Theme: "dsn" creative template (jQuery 3.1.1, `plugins.min.js` ≈1 MB, GSAP/Swiper inside). |
| Hosting | Netlify, `publish = "."` — **every file in the repo is publicly served unless blocked**. |
| Routing | One `.html` file per page; Netlify also serves the same file without `.html`. Canonical tags point to the `.html` URL. |
| Redirects | `netlify.toml`: old `netlify.app` domain → `codeservecommunity.in` (301), `www` → bare domain, 11 renamed service URLs (301), `/tools/*`, `/content/*`, `/docs/*` → 404, custom 404. |
| Blog | Static article files in `blog/`; metadata database `content/blog-posts.json`; generator `tools/build_blog.py` (blog index, 10 category pages, breadcrumbs, share links, author box, sitemap entries, homepage "latest guides"). |
| Forms | Contact form → EmailJS (`emailjs.send`, public key in page — designed to be public). |
| WhatsApp | `wa.me/918186841086` links with pre-filled, page-specific messages; floating chat widget (`assets/js/whatsapp-widget.js`). |
| Analytics | One GA4 tag `G-TCZM6MC8ZL` on every page; `assets/js/ga-events.js` click tracking. Search Console verified (DNS) for `codeservecommunity.in`. |
| Secrets | None in the repo. EmailJS public key is intended to be public. |
| Legacy/duplicate pages | No duplicate page versions. 12 broken font fallback files in `assets/fonts/*.html` (blocked in robots.txt). 5 internal notes (`*.md`) were publicly served — **found this round**. |

## 2. Page inventory (Phase 2)

70 public pages: 28 business pages, 31 blog articles, blog index, 10 blog category pages (9 published, 1 empty category not generated).
All 69 indexable pages have the same header menu and footer (checked by script).

## 3. Findings

### Critical
| # | Issue | Where | Status |
|---|---|---|---|
| C1 | Internal working notes publicly readable (`SEO_IMPLEMENTATION_REPORT.md`, `WHATSAPP_INTEGRATION_GUIDE.md` and 3 more) | site root | **Fixed** — moved to `docs/legacy/`, `/docs/*` returns 404 and is disallowed in robots.txt |
| C2 | Contact form collected only email — no phone/WhatsApp, no service, no spam protection | contact.html | **Fixed** (see fixes report) |

### High
| # | Issue | Where | Status |
|---|---|---|---|
| H1 | Price conflict: AI WhatsApp Assistant ₹24,999 on pricing page, "Quote on request" elsewhere | ai-chatbot-development.html, AI chatbot cost article | **Fixed** |
| H2 | No single source of truth for contact details and prices | site-wide | **Fixed** — `content/site.json` + `tools/check_site.py` |
| H3 | `generate_lead` fired on every submit attempt, even when sending failed, inflating leads in GA4 | ga-events.js | **Fixed** — now only on successful delivery |
| H4 | Homepage hero had no "Start a Project" call to action (only "Our story") | index.html | **Fixed** |
| H5 | Two project cards labelled "View Live" link back to the portfolio (no public site) | index.html | **Fixed** — "See project details" |
| H6 | Mobile performance: LCP 8.1 s, Performance 45 (live, Lighthouse mobile, previous round) | homepage | **Open** — theme JS (`plugins.min.js`) and preloader; needs owner decision |
| H7 | Footer missing "Custom Software" and "AI Chatbots" links | billing-software-development.html, mobile-app-development.html | **Fixed** |

### Medium
| # | Issue | Status |
|---|---|---|
| M1 | No "latest articles" on the homepage (1 blog link only) | **Fixed** — auto-updated "Latest guides" section |
| M2 | CTA and portfolio clicks not tracked | **Fixed** — `cta_click`, `portfolio_click` |
| M3 | Two portfolio projects (Yoda Ratna Awards, Dr. Kammela Medical Center) use stock photos, not real screenshots | **Open** — owner must supply screenshots |
| M4 | Portfolio has no individual case-study pages | **Open** — needs genuine project details from the owner |
| M5 | Footer headings jump H2 → H4 on all pages | **Open** — theme styles target `h4`; low SEO impact |
| M6 | Swiper adds `role="group"` to `<article>` slides (Lighthouse ARIA warning) | **Open** — theme library behaviour |
| M7 | Business hours "Mon–Sat open 24 hours" copied from Google Business Profile | **Open** — owner to confirm |

### Low
| # | Issue | Status |
|---|---|---|
| L1 | 5.4 MB animated GIF in portfolio (project 6) | Open — convert to video |
| L2 | `/page` and `/page.html` both return 200 | Accepted — canonical tags resolve it |
| L3 | Code examples in two articles show placeholder numbers (`919000000000`, `/images/hero.webp`) | Accepted — intentional examples, excluded from checks |

## 4. Already in place from earlier rounds (verified again this round)
- Domain move to `codeservecommunity.in`, 301 redirects from `netlify.app`, Search Console Domain property, sitemap submitted, Change of Address active.
- Unique titles/descriptions, one H1 per page, canonical URLs, Open Graph + share images on every page, JSON-LD (ProfessionalService, WebSite, Service, BreadcrumbList, BlogPosting, FAQPage, CollectionPage).
- Clean service URLs (no place names) with 301s from the old URLs.
- Launch offer (no advance on websites up to ₹34,999 until 31 March 2027) consistent across pricing, FAQ, terms, service pages, emails.
- 31 articles, each with category, related articles, related service link, author box, share links, in-article diagrams.

## 5. Business information audit (Phase 6)

| Item | Result |
|---|---|
| Phone | One number everywhere: +91 81868 41086 (524 occurrences) |
| WhatsApp | One number everywhere: 918186841086 |
| Email | One address everywhere: codeserve.contact@gmail.com |
| Address | KPHB Phase 9, Kukatpally, Hyderabad 500085 (short and full forms) |
| Legacy prices ₹2,499 / ₹5,000 | **Not present as CodeServe prices.** "2499" matches were part of ₹24,999; ₹2,499 is a sample order total inside an article's example message; ₹5,000 values are market-range examples in blog articles |
| ₹2,999 | Genuine current service: Website Audit & Testing |
| ₹29,999 / ₹44,995 / ₹14,996 | Genuine: Startup Launch Kit price / item value / saving |
| Domain | No `netlify.app` references except redirects and one article example |
