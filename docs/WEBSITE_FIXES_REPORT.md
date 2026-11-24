# CodeServe website — fixes report

Round of 24 November 2026. Roll back everything in this round with: `git reset --hard pre-audit-2026-11-24` (before pushing) or `git revert` of the commit (after pushing).

## Implemented in this round

| # | Change | Files |
|---|---|---|
| 1 | **Contact form**: added optional Phone / WhatsApp field (validated: digits, spaces, + and -), "What do you need?" service dropdown, hidden spam-trap field, `aria-live` status messages. Phone and service are added to the message so they arrive through the existing EmailJS template without any EmailJS change. Switched `sendForm` → `send` with explicit parameters. | `contact.html`, `assets/css/contact-style.css` (cache version `?v=2`) |
| 2 | **Lead tracking**: `generate_lead` now fires only after EmailJS confirms delivery; submit attempts are `form_submit_attempt`. Added `cta_click` (main buttons) and `portfolio_click` (links to live client projects). Event names documented at the top of the file. | `assets/js/ga-events.js` (`?v=3` on all pages), `contact.html` |
| 3 | **Price consistency**: AI WhatsApp Assistant shown as ₹24,999 one-time setup (matches the pricing page) instead of "Quote on request"; added to the page's Service offers. | `ai-chatbot-development.html`, `blog/ai-chatbot-development-cost-india.html` |
| 4 | **Single source of truth**: `content/site.json` holds business details, every price, allowed estimates and payment terms. `tools/check_site.py` checks all pages against it plus technical SEO (titles, descriptions, canonicals, H1, lang, og:image, sitemap/noindex consistency, JSON-LD validity, image alt, broken internal links, robots.txt). | `content/site.json`, `tools/check_site.py` |
| 5 | **Homepage hero**: first slide now has "Start a project" (→ contact) and "Explore our work" (→ portfolio), same button style as the theme. | `index.html` |
| 6 | **Misleading buttons**: two "View Live" links to projects without a public site renamed "See project details". | `index.html` |
| 7 | **Homepage "Latest guides"**: three newest articles, regenerated automatically by the blog builder. | `tools/build_blog.py`, `index.html` |
| 8 | **Footer**: added "Custom Software" and "AI Chatbots" links on the two pages missing them. | `billing-software-development.html`, `mobile-app-development.html` |
| 9 | **Internal files no longer public**: 5 working notes moved from the site root to `docs/legacy/`; `/docs/*` returns 404 and is disallowed in robots.txt. | `docs/`, `netlify.toml`, `robots.txt` |
| 10 | **Colour contrast** (Lighthouse): WhatsApp buttons dark text, blue buttons/badges `#2563eb`, blog category counts, portfolio links. Accessibility now 96–99 on all 12 tested pages. CSS cache versions bumped. | `assets/css/theme-content.css` (`?v=3`), `assets/css/portfolio-style.css` (`?v=2`), `tools/build_blog.py`, blog pages |
| 11 | **codeserve-intel** (separate local project): email fact-checker price list synced with `content/site.json`. | `codeserve-intel/dashboard/server.js` |

## Implemented in earlier rounds (for completeness)
Domain move and redirects · clean service URLs · keyword-mapped titles/H1s · two new service pages (AI chatbots, custom software) · SEO services and e-commerce pages · homepage services/why/industries/process/local/FAQ sections · blog system (database, generator, categories, search, share links, author box) · 9 new articles · 22 in-article diagrams · real share images · launch offer across pricing/FAQ/terms · WebP images, preloader shortened, icons resized · button contrast and heading-order fixes.

## Still open (needs you or a decision)
| Item | Why it is open | What is needed |
|---|---|---|
| Mobile LCP (≈8 s) / Performance score | Caused mainly by the theme's 1 MB script and preloader animation | Decide whether to remove the preloader / slim the theme script (changes the look) |
| Real screenshots for Yoda Ratna Awards and Dr. Kammela Medical Center | Currently stock photos | Send screenshots (or permission to remove those cards) |
| Case-study pages | Need genuine problem/solution details per project | Short brief per project from you |
| About page team details | No verified team information in the repo | Names/roles/photos you are happy to publish |
| Business hours "open 24 hours" | Copied from the Google Business Profile | Confirm real hours |
| EmailJS delivery on the new domain | Not tested — a real test sends a real email | Send one test message from the live contact page; if it fails, add `codeservecommunity.in` to EmailJS allowed origins |
| GA4 key events | Event names exist; marking them as key events is done in GA4 | GA4 → Admin → Events → mark `generate_lead`, `whatsapp_click`, `phone_click` as key events |
| Footer heading levels, Swiper ARIA role | Theme markup | Low priority |

## How to keep the site consistent
1. Change a price or contact detail in `content/site.json` first, then on the pages.
2. Run `python tools/check_site.py` — it lists every page that disagrees.
3. After adding or editing articles, run `python tools/build_blog.py`.
