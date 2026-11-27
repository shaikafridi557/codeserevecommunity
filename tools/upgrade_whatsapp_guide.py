"""One-off upgrade of blog/whatsapp-business-api-guide.html (Nov 2026): new title/description,
October 2026 pricing change, official-API and small-business sections, links to the new cluster posts."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
f = ROOT / 'blog/whatsapp-business-api-guide.html'
s = f.read_text(encoding='utf-8')
if 'id="official"' in s:
    raise SystemExit('already upgraded')


def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new)


OLD_T = "WhatsApp Business API Guide for Indian Businesses (2026)"
NEW_T = "WhatsApp Business API for Business in India: Complete 2026 Guide"
rep(f"<title>{OLD_T}</title>", f"<title>{NEW_T}</title>")
rep(f'<meta property="og:title" content="{OLD_T}">', f'<meta property="og:title" content="{NEW_T}">')
OLD_D = "A simple guide to the WhatsApp Business API for Indian businesses: how it differs from the free app, what it costs, what you need and how to get started."
NEW_D = "The official WhatsApp Business API explained for Indian businesses: how to get it, 2026 per-message pricing, features, use cases, rules and step-by-step setup for small businesses."
rep(OLD_D, NEW_D)
OLD_H = "WhatsApp Business API: A Simple Guide for Indian Businesses (2026)"
NEW_H = "WhatsApp Business API: The Complete Guide for Businesses in India (2026)"
rep(OLD_H, NEW_H)

OLD_A = "Access to Meta's Cloud API itself has no separate subscription fee, but Meta charges per template message (marketing, utility and authentication). Replies inside a 24-hour window opened by the customer are generally free. You may also pay for a platform tool or a one-time custom setup."
NEW_A = ("There is no subscription fee for Meta's Cloud API, and incoming messages are free. Meta charges per message: in India about ₹0.86 "
         "for marketing and about ₹0.115 for utility and authentication messages, plus GST. Since 1 October 2026, replies inside the 24-hour chat "
         "window are free for the first 1,000 a month per number and then charged at the utility rate.")
rep(OLD_A, NEW_A)

a = s.index('<p>When a customer messages you first, a <strong>24-hour customer service window</strong>')
b = s.index("<p>On top of Meta's charges, you may pay for:</p>")
s = s[:a] + '''<p>When a customer messages you first, a <strong>24-hour customer service window</strong> opens, and you can reply freely (without a template). Outside that window you must use an approved template.</p>
                <p><strong>What changed on 1 October 2026:</strong> replies inside the window (service messages) used to be free. Now every phone number gets <strong>1,000 free service messages a month</strong>, and further replies are charged at the utility rate. Utility templates sent inside an open window are also charged.</p>
                <table>
                    <thead><tr><th>Category</th><th>Approx. India rate per message (2026, before GST)</th></tr></thead>
                    <tbody>
                        <tr><td>Marketing</td><td>about ₹0.86</td></tr>
                        <tr><td>Utility</td><td>about ₹0.115</td></tr>
                        <tr><td>Authentication</td><td>about ₹0.115</td></tr>
                        <tr><td>Service replies</td><td>first 1,000/month free, then about ₹0.115</td></tr>
                    </tbody>
                </table>
                <div class="cs-callout"><strong>Full breakdown:</strong> rates, GST, what is still free and real monthly cost examples are in our <a href="whatsapp-business-api-pricing-india.html">WhatsApp Business API pricing in India</a> guide. Meta updates rates every few months, so check Meta's current rate card before a large campaign. Charges are billed by Meta to the business's own account.</div>
                ''' + s[b:]

rep('''<p>If you get only a handful of messages a day, the free app is fine. If you are missing messages, copying order details by hand, or want replies at 11 pm on a Sunday, the API is the next step.</p>''',
    '''<p>If you get only a handful of messages a day, the free app is fine. If you are missing messages, copying order details by hand, or want replies at 11 pm on a Sunday, the API is the next step. Full comparison: <a href="whatsapp-business-app-vs-api.html">WhatsApp Business app vs API</a>.</p>

                <h2 id="official">How to get the official WhatsApp Business API in India</h2>
                <p>There are two official routes, and both go through your <strong>Meta Business account</strong>:</p>
                <ul>
                    <li><strong>Directly through Meta's Cloud API</strong> — you (or a developer) connect your number to the WhatsApp Business Platform and build the automation. You pay Meta's per-message rates only, with no middleman margin.</li>
                    <li><strong>Through a Business Solution Provider (BSP)</strong> — a Meta partner gives you a ready dashboard, usually for a monthly fee and sometimes a margin per message.</li>
                </ul>
                <p>Be careful with tools that send "WhatsApp API" messages by controlling WhatsApp Web or a phone in the background. They are <strong>not</strong> the official API, break WhatsApp's terms, and numbers using them are often banned.</p>

                <h2 id="small-business">Is the WhatsApp API worth it for a small business?</h2>
                <p>Usually yes, once WhatsApp is a real sales or support channel for you. With per-message pricing, a small business sending a few hundred reminders or order updates a month typically pays Meta only <strong>a few hundred rupees</strong>, and most customer chats fall inside the 1,000 free service messages. The bigger cost is the one-time setup of the automation — and the saving is staff time and missed enquiries.</p>''')

rep('''<p>A good rule: automate the three questions you answer most often and the one update customers ask for most. That alone usually saves hours of staff time every week.</p>''',
    '''<p>A good rule: automate the three questions you answer most often and the one update customers ask for most. That alone usually saves hours of staff time every week. More ideas with sample messages: <a href="whatsapp-business-api-use-cases.html">20 WhatsApp Business API use cases</a>, and a deep dive for <a href="whatsapp-api-for-restaurants.html">restaurants and cloud kitchens</a>.</p>''')

rep('''                        <li><a href="#what-you-can-do">What you can do with it</a></li>''',
    '''                        <li><a href="#official">How to get the official WhatsApp API in India</a></li>
                        <li><a href="#small-business">Is it worth it for a small business?</a></li>
                        <li><a href="#what-you-can-do">What you can do with it</a></li>''')

extra = [
    ("How do I get the official WhatsApp Business API in India?",
     "Create and verify a Meta Business account, connect a phone number to the WhatsApp Business Platform, and either build on Meta's Cloud API directly or use a Meta Business Solution Provider. Tools that automate WhatsApp Web are not official."),
    ("Can a small business use the WhatsApp Business API?",
     "Yes. Any verified business can use it. With per-message pricing, a small business sending a few hundred updates a month usually pays Meta only a few hundred rupees."),
]
faq_start = s.index('<div class="cs-faq">')
faq_end = s.index('<!--cs:share-author-->', faq_start)
j = s.rfind('</details>', faq_start, faq_end) + len('</details>')
s = s[:j] + ''.join(f'''
                    <details>
                        <summary>{q}</summary>
                        <p>{a}</p>
                    </details>''' for q, a in extra) + s[j:]

m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
data = json.loads(m.group(1))
for o in data:
    if o.get('@type') == 'FAQPage':
        o['mainEntity'] += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in extra]
    if o.get('@type') == 'BlogPosting':
        o['dateModified'] = '2026-11-28'
s = s[:m.start(1)] + '\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n    ' + s[m.end(1):]
f.write_text(s, encoding='utf-8')

dbf = ROOT / 'content/blog-posts.json'
db = json.loads(dbf.read_text(encoding='utf-8'))
for p in db['posts']:
    if p['slug'] == 'whatsapp-business-api-guide':
        p.update(seo_title=NEW_T, meta_description=NEW_D, h1=NEW_H, date_modified='2026-11-28', reading_time_min=8,
                 secondary_keywords=["WhatsApp API for business", "official WhatsApp Business API", "WhatsApp Business API India", "WhatsApp API for small business"],
                 related_articles=["whatsapp-business-api-pricing-india", "whatsapp-business-api-use-cases", "whatsapp-business-app-vs-api"])
dbf.write_text(json.dumps(db, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('upgraded; links to pricing post:', s.count('whatsapp-business-api-pricing-india.html'))
