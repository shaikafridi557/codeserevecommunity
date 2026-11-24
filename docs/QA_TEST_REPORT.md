# CodeServe website — QA test report

Date: 24 November 2026. Only tests that were actually run are listed as passed. Anything not run is listed under "Not tested".

## 1. Automated site check — `python tools/check_site.py`
**Result: passed.** 70 pages and 65 sitemap URLs checked, 0 problems found.
What it checks on every page:
- phone, WhatsApp and email match `content/site.json`
- no `netlify.app` references
- prices on business pages are in the approved price list
- launch-offer date
- unique title and description
- canonical URL
- exactly one H1
- `lang` attribute
- og:image
- every indexable page is in the sitemap, and no noindex page is
- JSON-LD parses
- every image has alt text
- no broken internal links
- robots.txt allows the site and lists the sitemap

## 2. Contact form (static checks)
- **Inline scripts parse without errors:** passed (3 scripts, 0 errors, checked with Node).
- **Phone field pattern compiles under the browser's regex v-flag:** passed.
  - Accepts "+91 98765 43210" and "98765-43210".
  - Rejects "abc".
- **Spam trap:** the hidden field is off-screen and the submit handler stops if the field is filled. This was checked by reading the code, not in a browser.
- **Not tested:** real delivery through EmailJS. A test would send a real email, so it was not done. See section 6.

## 3. Lighthouse 12.2.1 at 360 px mobile width (local copy of the site, headless Chrome)
First run on 12 pages, then a re-run on the 8 pages that failed colour contrast, after the contrast fixes:

| Page | Accessibility (before → after) | SEO | Best practices |
|---|---|---|---|
| / | 99 | 100 | 100 |
| /services.html | 98 | 100 | 100 |
| /pricing.html | 92 → 98 | 100 | 100 |
| /portfolio.html | 93 → 97 | 100 | 100 |
| /about.html | 98 | 100 | 100 |
| /contact.html | 98 | 100 | 100 |
| /website-development.html | 92 → 98 | 100 | 100 |
| /seo-services.html | 92 → 96 | 100 | 100 |
| /ai-chatbot-development.html | 92 → 98 | 100 | 100 |
| /whatsapp-automation.html | 92 → 98 | 100 | 100 |
| /blog/ | 93 → 98 | 100 | 100 |
| /blog/website-security-checklist-small-business.html | 93 → 98 | 100 | 100 |

Colour-contrast failures fixed:
- WhatsApp buttons: white text on bright green (2.0:1) changed to dark green text (11:1).
- Blue badges and buttons: changed to the darker brand blue `#2563eb` (5.2:1).
- Blog category counts: removed the transparency.
- Portfolio "visit site" links: changed to a lighter blue.

Remaining Lighthouse warnings (no change in this round):
- `heading-order`: the theme footer jumps from H2 to H4.
- `aria-allowed-role`: the Swiper slider adds `role="group"` to `<article>`.
- `valid-source-maps`: the theme's minified files reference source maps that aren't shipped. This is informational and doesn't affect visitors.

Horizontal overflow: Lighthouse 12 no longer reports the `content-width` audit, so this run **did not measure** overflow. Phone-width screenshots from earlier rounds showed none.

Performance was not part of this run. The last live mobile measurement (previous round) was Performance 45, LCP 8.1 s. See the fixes report, "Still open".

## 4. Links
- **Internal links on all 70 pages:** passed (part of `check_site.py`).
- **Portfolio external project links:** all returned HTTP 200 when checked this round. The Project Pusher demo on Render can take around 30 s to wake on first visit.
- **Live homepage `https://codeservecommunity.in/`:** HTTP 200.

## 5. Security and exposure
- **Repo scanned for secrets:** no API keys or passwords found. The EmailJS public key is meant to be public.
- **`/tools/`, `/content/`, `.kiro`, `.vscode` on the live site:** return 404 (checked).
- **Internal notes:** `/SEO_IMPLEMENTATION_REPORT.md` still returns **200 on the live site**, because this round isn't deployed yet. After deploying, it should return 404. Re-check it.

## 6. Not tested (needs you)
| Test | How |
|---|---|
| Contact form email delivery | On the live site, send one message that has a phone number and a service. Check that the email arrives with "Phone / WhatsApp" and "Service" at the top of the message. |
| GA4 events | Open GA4 → Reports → Realtime. Click a WhatsApp button and a "Start a project" button, then submit the form. You should see `whatsapp_click`, `cta_click` and `generate_lead`. |
| Real phones (iPhone Safari, Android Chrome) | Open the homepage, contact and pricing pages and tap the menu, the WhatsApp button and the form. |
| Search Console | Use URL Inspection on the homepage after deploying, and resubmit `sitemap.xml`. |
