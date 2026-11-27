"""WhatsApp Business API cluster — built from Search Console queries (Nov 2026)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from write_posts import flow_svg, bars_svg, grid_svg

DATE = "2026-11-28"
RATECARD = "https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing"

PHONE_ART = '''<rect x="130" y="0" width="230" height="440" rx="34" fill="#1f2937" stroke="#3a3a3a" stroke-width="3"/><rect x="146" y="20" width="198" height="400" rx="22" fill="#111b21"/><rect x="146" y="20" width="198" height="56" rx="22" fill="#1f2c34"/><rect x="146" y="56" width="198" height="20" fill="#1f2c34"/><circle cx="176" cy="48" r="16" fill="#25d366"/><rect x="202" y="40" width="90" height="14" rx="7" fill="#e5e7eb"/>'''

POSTS = [
# =========================================================================================== pricing
dict(
    slug="whatsapp-business-api-pricing-india",
    category="whatsapp-automation",
    label="WHATSAPP API PRICING",
    title_lines=["WhatsApp Business", "API Pricing in", "India (2026)"],
    art=PHONE_ART + '''<rect x="160" y="100" width="170" height="70" rx="12" fill="#2a3942"/><text x="176" y="128" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="15" fill="#9ca3af">Marketing</text><text x="176" y="156" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="24" font-weight="700" fill="#ffffff">₹0.86</text><rect x="160" y="186" width="170" height="70" rx="12" fill="#2a3942"/><text x="176" y="214" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="15" fill="#9ca3af">Utility</text><text x="176" y="242" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="24" font-weight="700" fill="#25d366">₹0.115</text><rect x="160" y="272" width="170" height="70" rx="12" fill="#2a3942"/><text x="176" y="300" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="15" fill="#9ca3af">Authentication</text><text x="176" y="328" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="24" font-weight="700" fill="#25d366">₹0.115</text><circle cx="410" cy="80" r="48" fill="#387cf9"/><text x="410" y="96" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="44" font-weight="700" fill="#fff">₹</text>''',
    seo_title="WhatsApp Business API Pricing in India 2026: Per-Message Rates",
    meta_description="WhatsApp Business API pricing in India for 2026: per-message rates for marketing, utility and authentication, the 1 October 2026 change, GST and real monthly cost examples.",
    h1="WhatsApp Business API Pricing in India (2026): Rates, Changes and Real Costs",
    breadcrumb="WhatsApp API Pricing India",
    primary_keyword="WhatsApp Business API pricing India",
    secondary_keywords=["WhatsApp API cost per message", "WhatsApp business API charges", "WhatsApp marketing message price India"],
    short_description="Per-message rates for marketing, utility and authentication messages, what changed on 1 October 2026, and real monthly cost examples.",
    image_alt="WhatsApp Business API per-message prices in India shown on a phone screen",
    intro="Meta charges WhatsApp Business API messages per message, by category and by country. Here are the current India rates, what changed on 1 October 2026, and what a small business actually pays in a month.",
    related=["whatsapp-business-api-guide", "whatsapp-business-api-use-cases", "whatsapp-business-app-vs-api"],
    related_pages=[("../whatsapp-automation.html", "WhatsApp Automation Services")],
    related_service="../whatsapp-automation.html",
    diagrams={"rates": bars_svg("WhatsApp API rate per message in India (before GST)", [
        ("Marketing", 0.8631, "about ₹0.86", "#f59e0b"),
        ("Utility", 0.115, "about ₹0.115", "#25d366"),
        ("Authentication (OTP)", 0.115, "about ₹0.115", "#25d366"),
        ("Service (after 1,000 free)", 0.115, "about ₹0.115", "#387cf9"),
    ], note="Indicative Meta rates for India in 2026. Always check Meta's current rate card.")},
    body=f'''
                <p><strong>Short answer:</strong> in India, Meta charges roughly <strong>₹0.86 per marketing message</strong> and about <strong>₹0.115 per utility or authentication message</strong>, plus GST. Since 1 October 2026, replies inside a customer chat (service messages) are also charged at the utility rate once a number passes <strong>1,000 free service messages a month</strong>. Most small businesses spend a few hundred to a few thousand rupees a month on Meta's charges.</p>
                <div class="cs-callout"><strong>Check before you budget:</strong> Meta updates rates every few months. The figures below are the India rates published for 2026; confirm the latest numbers on <a href="{RATECARD}" target="_blank" rel="noopener">Meta's official pricing page</a> before a large campaign.</div>

                <h2 id="how-it-works">How WhatsApp API pricing works</h2>
                <p>Since July 2025 Meta charges <strong>per delivered message</strong> (it used to charge per 24-hour conversation). The price depends on two things:</p>
                <ul>
                    <li><strong>The message category</strong> — marketing, utility, authentication or service.</li>
                    <li><strong>The customer's country</strong> — a message to an Indian (+91) number uses the India rate, a message to a UAE number uses the UAE rate.</li>
                </ul>
                <p>You pay Meta directly from your WhatsApp Business account. If you use a platform or a Business Solution Provider (BSP), they may add their own monthly fee or a margin per message on top.</p>

                <h2 id="rates">WhatsApp Business API rates in India (2026)</h2>
                <table>
                    <thead><tr><th>Category</th><th>What it is for</th><th>Approx. rate per message (India)</th></tr></thead>
                    <tbody>
                        <tr><td><strong>Marketing</strong></td><td>Offers, new arrivals, festival sales, re-engagement</td><td>about ₹0.86</td></tr>
                        <tr><td><strong>Utility</strong></td><td>Order confirmations, shipping updates, booking reminders, payment due alerts</td><td>about ₹0.115</td></tr>
                        <tr><td><strong>Authentication</strong></td><td>One-time passwords (OTPs) and login codes</td><td>about ₹0.115</td></tr>
                        <tr><td><strong>Service</strong></td><td>Free-form replies inside the 24-hour chat window</td><td>First 1,000 a month free per number, then about ₹0.115</td></tr>
                    </tbody>
                </table>
                <p>All rates are before GST. Indian businesses are billed GST (18%) on Meta's charges, so a marketing message costs a little over ₹1 in practice. Meta also offers lower utility and authentication rates at very high monthly volumes.</p>
                <figure class="cs-figure"><img src="../assets/img/blog/whatsapp-business-api-pricing-india-rates.svg" alt="Bar chart of WhatsApp Business API rates per message in India by category" width="800" height="328" loading="lazy"><figcaption>Marketing messages cost about 7.5 times more than utility messages, so categorise templates correctly.</figcaption></figure>

                <h2 id="october-2026">What changed on 1 October 2026</h2>
                <p>Until September 2026, replies sent inside an open 24-hour customer service window were free. From <strong>1 October 2026</strong> Meta changed this:</p>
                <ul>
                    <li><strong>Service messages are now charged</strong> at the same rate as utility messages — but every business phone number gets <strong>1,000 free service messages per month</strong>. Unused free messages do not roll over.</li>
                    <li><strong>Utility templates sent inside an open window</strong> are now charged as well.</li>
                    <li>You need a <strong>payment method</strong> on your WhatsApp Business account. Without one, service messages stop being delivered after the free 1,000.</li>
                </ul>
                <p>For most small businesses the 1,000 free service messages still cover normal customer chats. Busy businesses — a restaurant taking orders on WhatsApp, a clinic handling hundreds of bookings — should now count service replies in their budget.</p>

                <h2 id="free">What is still free</h2>
                <ul class="cs-checklist">
                    <li>The first 1,000 service messages per phone number every month</li>
                    <li>Messages customers send to you — incoming messages are never charged</li>
                    <li>Conversations started from a Click-to-WhatsApp ad or a Facebook Page "Send message" button, which open a free entry-point window (currently 72 hours)</li>
                    <li>Access to Meta's Cloud API itself — there is no subscription fee to Meta</li>
                </ul>

                <h2 id="examples">Real monthly cost examples</h2>
                <h3>1. Clinic sending reminders</h3>
                <p>600 appointment reminders (utility) + 900 chat replies (service, inside the free 1,000) a month: 600 × ₹0.115 = <strong>about ₹69</strong>, plus GST.</p>
                <h3>2. Online store</h3>
                <p>1,500 order confirmations and 1,500 shipping updates (utility) + 2,000 service replies (1,000 free, 1,000 charged) + one festival offer to 2,000 opted-in customers (marketing): (3,000 + 1,000) × ₹0.115 + 2,000 × ₹0.86 = ₹460 + ₹1,720 = <strong>about ₹2,180</strong>, plus GST.</p>
                <h3>3. Restaurant taking orders on WhatsApp</h3>
                <p>3,000 order chats (service, 2,000 above the free tier) + 3,000 order-status updates (utility) + 4 offers a month to 1,500 regulars (marketing): 5,000 × ₹0.115 + 6,000 × ₹0.86 = ₹575 + ₹5,160 = <strong>about ₹5,700</strong>, plus GST. The offers are the biggest cost — send fewer, better-targeted ones.</p>

                <h2 id="save">How to keep WhatsApp API costs low</h2>
                <ul>
                    <li><strong>Use the right category.</strong> An order update is utility, not marketing. Meta reviews templates and re-categorises wrong ones.</li>
                    <li><strong>Send marketing only to engaged customers.</strong> A smaller list of people who buy beats a big list of people who block you.</li>
                    <li><strong>Let customers start the chat.</strong> "Message us on WhatsApp" buttons and Click-to-WhatsApp ads bring free entry-point conversations.</li>
                    <li><strong>Avoid per-message markups.</strong> Some platforms add 10–30% on every message. A direct Cloud API setup means you pay Meta's rate only.</li>
                    <li><strong>Automate answers well.</strong> One clear reply with buttons costs less than five back-and-forth messages.</li>
                </ul>

                <h2 id="other-countries">Messaging customers outside India</h2>
                <p>The rate depends on the <strong>customer's</strong> country, not yours. If a Hyderabad business messages customers in the UAE, UK or USA, those messages use that country's rate, which is usually higher than India's. Businesses in the Gulf can read our guide to the <a href="whatsapp-business-api-uae.html">WhatsApp Business API in the UAE</a>.</p>

                <h2 id="budget">A simple way to estimate your monthly bill</h2>
                <ol>
                    <li>Count your monthly <strong>utility</strong> messages (order updates, reminders, payment alerts) × ₹0.115.</li>
                    <li>Count your <strong>marketing</strong> messages (each offer × number of customers it goes to) × ₹0.86.</li>
                    <li>Count customer chat <strong>replies</strong>; subtract 1,000; multiply the rest × ₹0.115.</li>
                    <li>Add the three numbers and add 18% GST.</li>
                </ol>
                <p>For most businesses, marketing messages make up more than half the bill — that is the number worth controlling.</p>

                <h2 id="setup-cost">Setup and tool costs on top of Meta's charges</h2>
                <table>
                    <thead><tr><th>Option</th><th>Typical cost</th><th>Good for</th></tr></thead>
                    <tbody>
                        <tr><td>Monthly platform / BSP</td><td>₹1,000–₹5,000+ a month, sometimes with a per-message margin</td><td>Teams that want a ready inbox and campaign tool</td></tr>
                        <tr><td>One-time custom setup (direct Cloud API)</td><td>₹7,999–₹24,999 one time at CodeServe</td><td>Businesses that want automation connected to their website, store or CRM without monthly lock-in</td></tr>
                    </tbody>
                </table>
                <p>See our <a href="../pricing.html#whatsapp-automation">WhatsApp automation plans</a> for what each setup includes.</p>
''',
    faq=[
        ("How much does the WhatsApp Business API cost per message in India?", "In 2026 Meta charges about ₹0.86 per marketing message and about ₹0.115 per utility or authentication message for Indian numbers, before 18% GST. Service replies are free for the first 1,000 a month per number and then charged at the utility rate."),
        ("Is the WhatsApp Business API free in India?", "There is no subscription fee to use Meta's Cloud API, and incoming messages are free. You pay per message for marketing, utility and authentication templates, and for service replies beyond 1,000 a month."),
        ("What changed in WhatsApp API pricing on 1 October 2026?", "Service messages inside the 24-hour window became chargeable at the utility rate after a free tier of 1,000 per phone number per month, and utility templates sent inside an open window also became chargeable."),
        ("Do I pay GST on WhatsApp API charges?", "Yes. Indian businesses are billed GST, currently 18%, on Meta's WhatsApp charges, and you can usually claim input tax credit if you are GST-registered."),
        ("Why are marketing messages so expensive?", "Meta prices marketing messages higher to discourage spam. Sending offers only to customers who opted in and engage with you keeps costs and block rates down."),
    ],
    closing='Want a WhatsApp setup with no per-message markup? See our <a href="../whatsapp-automation.html">WhatsApp automation services</a> or compare plans on the <a href="../pricing.html#whatsapp-automation">pricing page</a>.',
    cta_title="Know your WhatsApp cost before you start",
    cta_text="Tell us how many customers you message and we'll estimate your monthly Meta charges and the right setup — free.",
    cta_wa="Hi%20CodeServe%2C%20I%20read%20your%20WhatsApp%20API%20pricing%20guide%20and%20want%20a%20cost%20estimate.",
    cta_link=("../pricing.html#whatsapp-automation", "See WhatsApp Plans"),
    date=DATE,
),

# =========================================================================================== use cases
dict(
    slug="whatsapp-business-api-use-cases",
    category="whatsapp-automation",
    label="WHATSAPP USE CASES",
    title_lines=["WhatsApp Business", "API Use Cases:", "20 Real Examples"],
    art=PHONE_ART + '''<rect x="160" y="100" width="140" height="44" rx="12" fill="#2a3942"/><rect x="190" y="160" width="140" height="58" rx="12" fill="#005c4b"/><rect x="160" y="234" width="120" height="44" rx="12" fill="#2a3942"/><rect x="190" y="294" width="140" height="70" rx="12" fill="#005c4b"/><rect x="0" y="40" width="110" height="60" rx="14" fill="#387cf9"/><text x="55" y="78" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="20" font-weight="700" fill="#fff">Orders</text><rect x="0" y="190" width="110" height="60" rx="14" fill="#25d366"/><text x="55" y="228" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="20" font-weight="700" fill="#0b0b0b">Bookings</text><rect x="0" y="340" width="110" height="60" rx="14" fill="#f59e0b"/><text x="55" y="378" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="20" font-weight="700" fill="#0b0b0b">Payments</text>''',
    seo_title="WhatsApp Business API Use Cases: 20 Examples by Industry",
    meta_description="20 practical WhatsApp Business API use cases for Indian businesses — retail, restaurants, clinics, real estate, education and services — with sample messages and what to automate first.",
    h1="WhatsApp Business API Use Cases: 20 Real Examples by Industry",
    breadcrumb="WhatsApp API Use Cases",
    primary_keyword="WhatsApp Business API use cases",
    secondary_keywords=["WhatsApp API for business examples", "WhatsApp automation ideas", "WhatsApp API for small business"],
    short_description="Twenty practical ways businesses use the WhatsApp Business API, with sample messages and what to automate first in each industry.",
    image_alt="Phone with WhatsApp chats for orders, bookings and payments",
    intro="The WhatsApp Business API is not just for bulk offers. Here are 20 practical use cases — with sample messages — that save staff time and bring repeat customers, grouped by industry.",
    related=["whatsapp-business-api-guide", "whatsapp-business-api-pricing-india", "whatsapp-api-for-restaurants"],
    related_pages=[("../whatsapp-automation.html", "WhatsApp Automation Services")],
    related_service="../whatsapp-automation.html",
    diagrams={"map": grid_svg("WhatsApp API use cases by type", [
        ("Notifications", "orders, delivery, reminders", "#25d366"),
        ("Support", "FAQs, AI replies, hand-over", "#387cf9"),
        ("Sales", "catalogue, quotes, offers", "#f59e0b"),
        ("Payments", "UPI links, dues, receipts", "#a78bfa"),
        ("Bookings", "slots, reschedule, check-in", "#38bdf8"),
        ("Internal", "staff alerts, approvals", "#f472b6"),
    ])},
    body='''
                <p>The <a href="whatsapp-business-api-guide.html">WhatsApp Business API</a> lets your software send and receive WhatsApp messages. That opens up far more than broadcasts. The best use cases share one thing: they answer a question <em>before</em> the customer has to call you.</p>
                <figure class="cs-figure"><img src="../assets/img/blog/whatsapp-business-api-use-cases-map.svg" alt="Six groups of WhatsApp Business API use cases: notifications, support, sales, payments, bookings and internal alerts" width="800" height="292" loading="lazy"><figcaption>Most use cases fall into six groups. Notifications and support usually pay back fastest.</figcaption></figure>

                <h2 id="every-business">Use cases for every business</h2>
                <ol>
                    <li><strong>Instant answers to common questions.</strong> Timings, location, prices and "is this available?" answered 24/7 with menu buttons or an AI assistant.</li>
                    <li><strong>Lead capture.</strong> Ask 3 quick questions (name, requirement, budget) and save the answers to Google Sheets or your CRM.</li>
                    <li><strong>Human hand-over.</strong> When the bot can't help, the chat moves to the right staff member in a shared inbox.</li>
                    <li><strong>Payment reminders.</strong> <em>"Hi Ravi, invoice #1042 for ₹8,500 is due on 5 Dec. Pay by UPI: [link]"</em></li>
                    <li><strong>Feedback and Google reviews.</strong> A day after the visit or delivery, ask for a rating and share your Google review link with happy customers.</li>
                </ol>

                <h2 id="retail">Retail and online stores</h2>
                <ol start="6">
                    <li><strong>Order confirmation.</strong> <em>"Thanks Priya! Order #5521 is confirmed. Total ₹1,249. We'll message you when it ships."</em></li>
                    <li><strong>Shipping and delivery updates</strong> with tracking links, sent automatically from WooCommerce or Shopify.</li>
                    <li><strong>Cash-on-delivery confirmation.</strong> A Yes/No button before dispatch cuts fake COD orders and returns.</li>
                    <li><strong>Abandoned-cart reminder</strong> to customers who opted in at checkout.</li>
                    <li><strong>Catalogue browsing.</strong> Show products inside WhatsApp and take the order in the chat.</li>
                </ol>
                <p>Step-by-step: <a href="woocommerce-whatsapp-order-notifications.html">WooCommerce order notifications on WhatsApp</a>.</p>

                <h2 id="restaurants">Restaurants and cloud kitchens</h2>
                <ol start="11">
                    <li><strong>Direct ordering</strong> from a menu in WhatsApp — no aggregator commission on repeat customers.</li>
                    <li><strong>Table reservations</strong> with a reminder two hours before.</li>
                    <li><strong>Order status</strong>: accepted, being prepared, out for delivery.</li>
                </ol>
                <p>More in our guide to <a href="whatsapp-api-for-restaurants.html">WhatsApp API for restaurants</a>.</p>

                <h2 id="healthcare">Clinics and hospitals</h2>
                <ol start="14">
                    <li><strong>Appointment booking and reminders.</strong> <em>"Reminder: your appointment with Dr. Rao is tomorrow at 10:30 AM. Reply 1 to confirm, 2 to reschedule."</em></li>
                    <li><strong>Lab report ready alerts</strong> with a secure download link.</li>
                </ol>

                <h2 id="real-estate">Real estate</h2>
                <ol start="16">
                    <li><strong>Brochure and price list on request</strong>, then a site-visit booking — and the lead goes straight to the sales team.</li>
                    <li><strong>Construction progress updates</strong> to buyers every month.</li>
                </ol>

                <h2 id="education">Schools, colleges and coaching centres</h2>
                <ol start="18">
                    <li><strong>Admission enquiries</strong> answered instantly, with a visit booking and document checklist.</li>
                    <li><strong>Fee reminders, attendance and exam results</strong> sent to parents automatically.</li>
                </ol>

                <h2 id="services">Service businesses</h2>
                <ol start="20">
                    <li><strong>Technician visit confirmations</strong> — who is coming, when, and a live update when they are on the way — followed by the invoice and payment link.</li>
                </ol>

                <h2 id="salons-gyms">Salons, spas and gyms</h2>
                <ul>
                    <li><strong>Slot booking and reschedule buttons</strong> — <em>"Your haircut with Anjali is booked for Sat, 4:30 PM. Tap Reschedule if your plans change."</em></li>
                    <li><strong>Membership renewal alerts</strong> seven days before expiry, with a payment link.</li>
                    <li><strong>Birthday offers</strong> to members who opted in.</li>
                </ul>

                <h2 id="hotels-venues">Hotels, banquet halls and event venues</h2>
                <ul>
                    <li><strong>Availability enquiries</strong> — the bot asks the date, number of guests and event type, then shares packages and photos.</li>
                    <li><strong>Booking confirmation and advance payment</strong> with a UPI link and the booking details as a PDF.</li>
                    <li><strong>Check-in details</strong> — location pin, check-in time and a contact person the day before arrival.</li>
                </ul>

                <h2 id="logistics">Logistics, distributors and B2B</h2>
                <ul>
                    <li><strong>Dispatch and proof-of-delivery updates</strong> to customers and dealers.</li>
                    <li><strong>Re-order reminders</strong> to retailers when stock usually runs out.</li>
                    <li><strong>Internal alerts</strong> — a new order, a low-stock item or an approval request sent to the right manager.</li>
                </ul>

                <h2 id="ai">Where AI fits in</h2>
                <p>Button menus work well for fixed choices. An <strong>AI assistant</strong> is better when customers ask questions in their own words — "do you have parking?", "is the paneer dish spicy?", "can I pay in two parts?" — or switch between English, Hindi and Telugu. The AI answers from your own information (menu, price list, policies) and hands the chat to a person when it is unsure. Read more in <a href="how-ai-chatbots-help-small-businesses.html">how AI chatbots help small businesses</a>.</p>

                <h2 id="where-to-start">Which use case should you start with?</h2>
                <p>Pick the one that removes the most phone calls. In our experience that is usually:</p>
                <table>
                    <thead><tr><th>If your staff keep…</th><th>Start with</th></tr></thead>
                    <tbody>
                        <tr><td>Answering the same 5 questions</td><td>FAQ bot or AI assistant (#1)</td></tr>
                        <tr><td>Calling customers to confirm orders</td><td>Order confirmation + COD check (#6, #8)</td></tr>
                        <tr><td>Chasing no-shows</td><td>Booking reminders (#14)</td></tr>
                        <tr><td>Chasing payments</td><td>Payment reminders with UPI link (#4)</td></tr>
                        <tr><td>Losing enquiries from ads</td><td>Lead capture to CRM (#2)</td></tr>
                    </tbody>
                </table>
                <div class="cs-callout"><strong>Cost tip:</strong> notifications like order updates and reminders are <em>utility</em> messages, which cost about ₹0.115 each in India — far less than marketing messages. See <a href="whatsapp-business-api-pricing-india.html">WhatsApp API pricing in India</a>.</div>

                <h2 id="templates">Sample templates and their categories</h2>
                <p>Every message you send outside a customer chat must be an approved template, and its category decides the price:</p>
                <table>
                    <thead><tr><th>Template</th><th>Category</th></tr></thead>
                    <tbody>
                        <tr><td>"Your order #5521 has shipped. Track it here: [link]"</td><td>Utility</td></tr>
                        <tr><td>"Reminder: your appointment is tomorrow at 10:30 AM."</td><td>Utility</td></tr>
                        <tr><td>"Invoice #1042 for ₹8,500 is due on 5 Dec."</td><td>Utility</td></tr>
                        <tr><td>"Your login code is 482913."</td><td>Authentication</td></tr>
                        <tr><td>"Diwali sale: 20% off all sarees this weekend."</td><td>Marketing</td></tr>
                        <tr><td>"We miss you! Here's ₹100 off your next order."</td><td>Marketing</td></tr>
                    </tbody>
                </table>

                <h2 id="measure">How to measure results</h2>
                <ul>
                    <li><strong>Calls saved:</strong> compare phone calls per day before and after.</li>
                    <li><strong>Response time:</strong> first reply time should drop from hours to seconds.</li>
                    <li><strong>No-show and COD return rates</strong> after reminders and confirmations.</li>
                    <li><strong>Repeat orders</strong> from customers who get updates and offers.</li>
                    <li><strong>Block rate</strong> — WhatsApp shows your quality rating; if it falls, send fewer marketing messages.</li>
                </ul>

                <h2 id="rules">Rules that apply to every use case</h2>
                <ul>
                    <li>Message only customers who <strong>opted in</strong> to WhatsApp updates.</li>
                    <li>Use <strong>approved templates</strong> for any message sent outside the 24-hour chat window.</li>
                    <li>Always give a way to <strong>reach a human</strong> and to stop promotional messages.</li>
                </ul>
''',
    faq=[
        ("What is the WhatsApp Business API used for?", "Businesses use it to send automatic order, booking and payment messages, answer common questions with a bot or AI assistant, capture leads into a CRM, and let several staff reply from one shared inbox."),
        ("Can a small business use the WhatsApp Business API?", "Yes. Any verified business can use it, and with Meta's per-message pricing a small business sending a few hundred updates a month usually pays only a few hundred rupees to Meta."),
        ("Which WhatsApp API use case gives the best return?", "Usually the one that removes the most phone calls: booking reminders for clinics, order and COD confirmation for online stores, and instant FAQ answers for most other businesses."),
        ("Can I send offers and broadcasts with the WhatsApp API?", "Yes, using approved marketing templates sent to customers who opted in. Marketing messages cost more than utility messages, so target them to engaged customers."),
    ],
    closing='Not sure which use case fits your business? See our <a href="../whatsapp-automation.html">WhatsApp automation services</a> — we suggest the first three automations for free.',
    cta_title="Pick your first WhatsApp automation",
    cta_text="Tell us what your team does on WhatsApp every day and we'll suggest what to automate first — free consultation.",
    cta_wa="Hi%20CodeServe%2C%20I%20read%20your%20WhatsApp%20API%20use%20cases%20article%20and%20want%20to%20automate%20my%20WhatsApp.",
    cta_link=("../whatsapp-automation.html", "WhatsApp Automation"),
    date=DATE,
),

# =========================================================================================== app vs api
dict(
    slug="whatsapp-business-app-vs-api",
    category="whatsapp-automation",
    label="APP VS API",
    title_lines=["WhatsApp Business", "App vs API:", "Which Do You Need?"],
    art='''<rect x="0" y="40" width="200" height="360" rx="28" fill="#1f2937" stroke="#3a3a3a" stroke-width="3"/><circle cx="100" cy="140" r="46" fill="#25d366"/><text x="100" y="152" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="30" font-weight="700" fill="#0b0b0b">App</text><text x="100" y="240" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="18" fill="#e5e7eb">1 phone</text><text x="100" y="270" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="18" fill="#e5e7eb">manual replies</text><text x="100" y="300" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="18" fill="#e5e7eb">free</text><text x="240" y="230" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="34" font-weight="700" fill="#9ca3af">vs</text><rect x="280" y="40" width="200" height="360" rx="28" fill="#0f1d33" stroke="#387cf9" stroke-width="3"/><circle cx="380" cy="140" r="46" fill="#387cf9"/><text x="380" y="152" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="30" font-weight="700" fill="#fff">API</text><text x="380" y="240" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="18" fill="#e5e7eb">whole team</text><text x="380" y="270" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="18" fill="#e5e7eb">automation + AI</text><text x="380" y="300" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="18" fill="#e5e7eb">pay per message</text>''',
    seo_title="WhatsApp Business App vs API: Which One Does Your Business Need?",
    meta_description="WhatsApp Business app vs WhatsApp Business API compared: features, cost, team access, automation, the official Meta API vs unofficial tools, and when to switch.",
    h1="WhatsApp Business App vs WhatsApp Business API: Which Do You Need?",
    breadcrumb="WhatsApp App vs API",
    primary_keyword="WhatsApp Business app vs API",
    secondary_keywords=["official WhatsApp Business API", "Meta WhatsApp Business API", "WhatsApp Business app API"],
    short_description="The free WhatsApp Business app and the official Meta API compared — features, cost, automation, risks of unofficial tools and when to switch.",
    image_alt="WhatsApp Business app compared with WhatsApp Business API",
    intro="The free WhatsApp Business app is perfect for a one-person shop. The official WhatsApp Business API is built for teams and automation. Here is a clear comparison, the risks of unofficial tools, and a simple test to know when to switch.",
    related=["whatsapp-business-api-guide", "whatsapp-business-api-pricing-india", "whatsapp-business-api-use-cases"],
    related_pages=[("../whatsapp-automation.html", "WhatsApp Automation Services")],
    related_service="../whatsapp-automation.html",
    diagrams={"switch": flow_svg("When to move from the app to the API", [
        ["Free app", "1 person replies"], ["Missed chats", "& slow replies"], ["Team inbox", "+ templates"], ["Automation", "+ AI assistant"]], highlight=(2, 3))},
    body='''
                <p><strong>Quick answer:</strong> use the free <strong>WhatsApp Business app</strong> if one or two people can comfortably reply to every message. Move to the official <strong>WhatsApp Business API</strong> (the WhatsApp Business Platform from Meta) when you need several staff on one number, automatic order or booking messages, a chatbot or AI assistant, or a connection to your website, store or CRM.</p>

                <h2 id="comparison">Side-by-side comparison</h2>
                <table>
                    <thead><tr><th></th><th>WhatsApp Business app</th><th>WhatsApp Business API</th></tr></thead>
                    <tbody>
                        <tr><td>Cost</td><td>Free</td><td>No subscription to Meta; pay per message (see <a href="whatsapp-business-api-pricing-india.html">India rates</a>)</td></tr>
                        <tr><td>Who replies</td><td>One phone plus a few linked devices</td><td>Any number of staff through a shared inbox</td></tr>
                        <tr><td>Automation</td><td>Greeting, away message, quick replies</td><td>Chatbots, AI replies, WhatsApp Flows (forms), integrations</td></tr>
                        <tr><td>Order / booking messages</td><td>Typed by hand</td><td>Sent automatically from your system</td></tr>
                        <tr><td>Broadcasts</td><td>Small lists; only people who saved your number receive them</td><td>Approved templates to opted-in customers at scale</td></tr>
                        <tr><td>Integrations</td><td>None</td><td>Website, WooCommerce, Shopify, CRM, Google Sheets, payment gateways</td></tr>
                        <tr><td>Reports</td><td>Basic message stats</td><td>Delivery, read and reply data you can analyse</td></tr>
                        <tr><td>Setup</td><td>Download and go</td><td>Meta Business verification, number connection, templates</td></tr>
                    </tbody>
                </table>

                <h2 id="official-api">"Official" API vs unofficial WhatsApp tools</h2>
                <p>Search for "WhatsApp API" and you'll find tools that promise bulk messaging by controlling WhatsApp Web or a phone in the background. These are <strong>not</strong> the official API. They break WhatsApp's terms and numbers using them are regularly <strong>banned</strong> — sometimes taking years of customer chats with them.</p>
                <p>The <strong>official WhatsApp Business API</strong> is provided by Meta, either directly through the <strong>Cloud API</strong> (hosted by Meta) or through a Meta-approved Business Solution Provider. You can recognise it because setup always goes through your <strong>Meta Business account</strong>, uses approved message templates and is billed by Meta.</p>
                <div class="cs-callout"><strong>Rule of thumb:</strong> if a provider never asks you to verify your business with Meta and promises unlimited free messages to any number, it is not the official API.</div>

                <h2 id="same-number">Can I use the app and the API on the same number?</h2>
                <p>Traditionally, no — a number moved to the API could no longer be used in the phone app. Meta has since introduced a <strong>coexistence</strong> option that lets many businesses keep using the WhatsApp Business app on their phone while the same number is connected to the platform for automation. Availability and limits vary, so check before moving the number your customers already know. The alternative is to keep your old number on the app and use a new number for automation.</p>

                <h2 id="when-to-switch">When should you switch to the API?</h2>
                <figure class="cs-figure"><img src="../assets/img/blog/whatsapp-business-app-vs-api-switch.svg" alt="Four steps from the free WhatsApp Business app to an automated WhatsApp Business API setup" width="800" height="300" loading="lazy"><figcaption>Most businesses switch when missed chats start costing them sales.</figcaption></figure>
                <p>Switch if you answer <strong>yes</strong> to two or more of these:</p>
                <ul class="cs-checklist">
                    <li>Customers wait hours for a reply, or messages get missed</li>
                    <li>More than one person needs to reply from the business number</li>
                    <li>You type the same order, booking or payment details again and again</li>
                    <li>You get WhatsApp enquiries from ads and lose track of them</li>
                    <li>You want replies at night and on Sundays</li>
                    <li>You want to send updates to hundreds of customers who opted in</li>
                </ul>

                <h2 id="example">What switching looks like: a coaching centre</h2>
                <p>Picture a coaching centre handling admission enquiries on the free app from one phone. In admission season, messages pile up and parents wait hours. On the API, an assistant can answer course, fee and batch-timing questions instantly, book demo classes into a calendar, and pass serious enquiries to counsellors through a shared inbox. Fee reminders and class-change alerts go out automatically as low-cost utility messages — and with coexistence, parents can keep using the same number.</p>

                <h2 id="stay-on-app">When the free app is enough</h2>
                <p>If you get fewer than 20–30 chats a day, one person handles them, and you don't need automatic messages from a website or store, stay on the free app. Set up a greeting message, an away message, quick replies and a product catalogue — that covers most of what a small shop needs.</p>

                <h2 id="api-only">Features you only get with the API</h2>
                <ul>
                    <li><strong>WhatsApp Flows</strong> — forms inside the chat for bookings, lead details, surveys and sign-ups, with no website needed.</li>
                    <li><strong>Interactive messages</strong> — reply buttons and list menus customers tap instead of typing.</li>
                    <li><strong>Payments in the chat</strong> — in India, businesses can collect UPI payments inside WhatsApp through supported payment gateways, or send payment links.</li>
                    <li><strong>Automatic notifications</strong> from your website, store, billing software or CRM.</li>
                    <li><strong>AI assistants</strong> that answer from your business information and hand over to staff.</li>
                    <li><strong>Click-to-WhatsApp ads</strong> tracked end to end, so you know which ad brought which customer.</li>
                </ul>

                <h2 id="how-to-switch">How to switch from the app to the API, step by step</h2>
                <ol>
                    <li><strong>Decide the number</strong>: move your existing number (check coexistence) or start the API on a new number.</li>
                    <li><strong>Back up your chats</strong> from the WhatsApp Business app before any migration.</li>
                    <li><strong>Create and verify your Meta Business account</strong> with GST, Udyam or other business documents, and make sure your website shows the same business details.</li>
                    <li><strong>Connect the number</strong> to the WhatsApp Business Platform and set the display name, logo and description.</li>
                    <li><strong>Create message templates</strong> for order updates, reminders and offers, and submit them for approval.</li>
                    <li><strong>Set up the inbox and automations</strong> — welcome menu, FAQs, hand-over rules, integrations.</li>
                    <li><strong>Tell customers</strong> — update your website, Google Business Profile and Instagram with the WhatsApp link.</li>
                </ol>

                <h2 id="cost">What switching costs</h2>
                <p>Meta's Cloud API has no subscription fee; you pay per message — about ₹0.115 for utility messages and about ₹0.86 for marketing messages in India, with 1,000 free service replies a month per number. The setup (verification, templates, automation) is usually a one-time cost. Our <a href="../pricing.html#whatsapp-automation">WhatsApp plans</a> start at ₹7,999 one time.</p>
''',
    faq=[
        ("What is the difference between the WhatsApp Business app and the API?", "The app is a free phone app for one person or a small team replying by hand. The API is Meta's platform for businesses that need a shared team inbox, automatic messages from their systems, chatbots and integrations, paid per message."),
        ("Is there an official WhatsApp Business API?", "Yes. The official API is Meta's WhatsApp Business Platform, available directly through the Cloud API or through Meta-approved Business Solution Providers. Tools that automate WhatsApp Web are unofficial and risk getting your number banned."),
        ("Can I use the WhatsApp Business app and API on the same number?", "Meta's coexistence option allows many businesses to keep using the app on the same number connected to the platform. Availability varies, so check before moving an important number."),
        ("Is the WhatsApp Business API free?", "There is no subscription fee to Meta, but you pay per message for marketing, utility and authentication templates, and for service replies beyond 1,000 a month per number."),
    ],
    closing='Ready to move from the app to the official API? We handle verification, templates and automation — see <a href="../whatsapp-automation.html">WhatsApp automation services</a>.',
    cta_title="Outgrown the WhatsApp Business app?",
    cta_text="We'll check whether you need the API, move you safely and set up the automations that save the most time.",
    cta_wa="Hi%20CodeServe%2C%20I%20use%20the%20WhatsApp%20Business%20app%20and%20want%20to%20know%20if%20I%20need%20the%20API.",
    cta_link=("../pricing.html#whatsapp-automation", "See WhatsApp Plans"),
    date=DATE,
),

# =========================================================================================== restaurants
dict(
    slug="whatsapp-api-for-restaurants",
    category="whatsapp-automation",
    label="RESTAURANTS",
    title_lines=["WhatsApp Business", "API for", "Restaurants"],
    art=PHONE_ART + '''<rect x="160" y="96" width="170" height="56" rx="12" fill="#2a3942"/><circle cx="184" cy="124" r="14" fill="#f97316"/><rect x="206" y="114" width="90" height="10" rx="5" fill="#e5e7eb"/><rect x="206" y="130" width="50" height="8" rx="4" fill="#9ca3af"/><rect x="160" y="162" width="170" height="56" rx="12" fill="#2a3942"/><circle cx="184" cy="190" r="14" fill="#ef4444"/><rect x="206" y="180" width="80" height="10" rx="5" fill="#e5e7eb"/><rect x="206" y="196" width="50" height="8" rx="4" fill="#9ca3af"/><rect x="160" y="228" width="170" height="56" rx="12" fill="#2a3942"/><circle cx="184" cy="256" r="14" fill="#facc15"/><rect x="206" y="246" width="95" height="10" rx="5" fill="#e5e7eb"/><rect x="206" y="262" width="50" height="8" rx="4" fill="#9ca3af"/><rect x="160" y="350" width="170" height="44" rx="14" fill="#25d366"/><text x="245" y="379" text-anchor="middle" font-family="Poppins, 'Segoe UI', Arial, sans-serif" font-size="17" font-weight="700" fill="#0b0b0b">Order now</text><circle cx="420" cy="70" r="46" fill="#f97316"/><path d="M402 52 v38 M396 52 v14 a6 6 0 0 0 12 0 v-14 M432 52 c-10 6 -10 24 0 28 v10" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>''',
    seo_title="WhatsApp Business API for Restaurants: Orders, Bookings and Offers",
    meta_description="How restaurants and cloud kitchens use the WhatsApp Business API for direct orders, table bookings, order updates and offers — with costs, setup steps and commission savings.",
    h1="WhatsApp Business API for Restaurants: Direct Orders, Bookings and Repeat Customers",
    breadcrumb="WhatsApp API for Restaurants",
    primary_keyword="WhatsApp API for restaurants",
    secondary_keywords=["WhatsApp Business API for restaurants", "WhatsApp ordering for restaurants", "restaurant WhatsApp automation"],
    short_description="How restaurants use the WhatsApp Business API for direct orders, table bookings, order updates and offers — with costs and setup steps.",
    image_alt="Restaurant menu and order button inside a WhatsApp chat",
    intro="Aggregator apps bring new customers, but they also take a big cut of every order. The WhatsApp Business API helps restaurants take repeat orders and table bookings directly — automatically, even at peak hours.",
    related=["whatsapp-business-api-use-cases", "whatsapp-business-api-pricing-india", "whatsapp-business-api-guide"],
    related_pages=[("../whatsapp-automation.html", "WhatsApp Automation Services"), ("../portfolio.html#ordering-app", "Our QR Ordering App")],
    related_service="../whatsapp-automation.html",
    diagrams={"order-flow": flow_svg("How a WhatsApp order flows in a restaurant", [
        ["Customer", "says Hi"], ["Menu", "with buttons"], ["Order + UPI", "payment"], ["Kitchen", "gets ticket"], ["Status", "updates"]], highlight=(2, 3))},
    body='''
                <p>Most restaurants already get orders and reservation requests on WhatsApp — typed by hand, at the busiest time of the day. The <a href="whatsapp-business-api-guide.html">WhatsApp Business API</a> turns that chat into an ordering and booking system that runs itself, and helps you keep regular customers ordering directly instead of through aggregators.</p>

                <h2 id="why">Why restaurants use WhatsApp for orders</h2>
                <ul>
                    <li><strong>Lower commission.</strong> Food delivery apps commonly charge restaurants a commission of roughly 15–30% per order. A repeat customer who orders on WhatsApp costs you a few paise in message charges.</li>
                    <li><strong>You own the customer.</strong> You get the customer's number and order history, so you can bring them back.</li>
                    <li><strong>No app to download.</strong> Every customer already has WhatsApp.</li>
                    <li><strong>Fewer calls at peak hours.</strong> The bot takes the order while staff cook and serve.</li>
                </ul>
                <div class="cs-callout"><strong>Best of both:</strong> keep aggregators for discovery and new customers, and use WhatsApp for the regulars who already know you. Put a "Order direct on WhatsApp" card in every delivery bag.</div>

                <h2 id="what-to-automate">What a restaurant can automate on WhatsApp</h2>
                <table>
                    <thead><tr><th>Automation</th><th>How it works</th></tr></thead>
                    <tbody>
                        <tr><td><strong>Menu and ordering</strong></td><td>Customer sends "Hi", gets the menu with categories and buttons (or a WhatsApp catalogue), picks items and the address</td></tr>
                        <tr><td><strong>Payment</strong></td><td>UPI or payment-gateway link in the chat, or cash on delivery confirmation</td></tr>
                        <tr><td><strong>Kitchen ticket</strong></td><td>The order appears on a kitchen screen, printer or staff group automatically</td></tr>
                        <tr><td><strong>Order status</strong></td><td>"Accepted", "being prepared", "out for delivery" messages sent from your system</td></tr>
                        <tr><td><strong>Table reservations</strong></td><td>Date, time and number of guests collected in the chat, with a reminder two hours before</td></tr>
                        <tr><td><strong>Feedback</strong></td><td>A rating request after the meal, with your Google review link for happy guests</td></tr>
                        <tr><td><strong>Offers and loyalty</strong></td><td>Weekend specials, birthday offers and "your 5th order is free" — only to customers who opted in</td></tr>
                    </tbody>
                </table>
                <figure class="cs-figure"><img src="../assets/img/blog/whatsapp-api-for-restaurants-order-flow.svg" alt="Five steps of a WhatsApp restaurant order: hi, menu, order and UPI payment, kitchen ticket, status updates" width="800" height="300" loading="lazy"><figcaption>The whole order runs inside WhatsApp — the customer never leaves the chat.</figcaption></figure>

                <h2 id="vs-aggregators">WhatsApp ordering vs food delivery apps</h2>
                <table>
                    <thead><tr><th></th><th>Food delivery apps</th><th>Direct WhatsApp ordering</th></tr></thead>
                    <tbody>
                        <tr><td>Finding new customers</td><td>Excellent</td><td>Limited — works best for people who already know you</td></tr>
                        <tr><td>Cost per order</td><td>Commission, often around 15–30% of the order</td><td>A few paise to about ₹1 in WhatsApp message charges</td></tr>
                        <tr><td>Customer data</td><td>Mostly stays with the app</td><td>Yours — number, order history, preferences</td></tr>
                        <tr><td>Delivery</td><td>Handled by the app's riders</td><td>Your own staff or a delivery partner you choose</td></tr>
                        <tr><td>Offers and loyalty</td><td>Run inside the app's rules</td><td>Your own offers to customers who opted in</td></tr>
                    </tbody>
                </table>

                <h2 id="features">Checklist: what a good restaurant WhatsApp setup includes</h2>
                <ul class="cs-checklist">
                    <li>Menu with categories, photos, prices and "sold out" marking</li>
                    <li>Delivery area and minimum order checks</li>
                    <li>UPI or payment-gateway link, plus COD confirmation</li>
                    <li>Kitchen screen, printer or staff group alert for every order</li>
                    <li>Automatic order status messages</li>
                    <li>Table booking with reminders</li>
                    <li>Feedback request and Google review link</li>
                    <li>Simple daily report: orders, revenue, repeat customers</li>
                </ul>

                <h2 id="example">How it looks in practice: a cloud kitchen</h2>
                <p>A customer who ordered last week through an aggregator finds a card in the bag: <em>"Order direct on WhatsApp and get 10% off."</em> They message "Hi". The bot greets them by name next time, shows the menu, takes the order and a UPI payment, and sends the ticket to the kitchen. Ten minutes later: <em>"Your order is out for delivery 🛵."</em> On Sunday the customer gets one weekend-special message — and orders again.</p>

                <h2 id="cost">What it costs a restaurant</h2>
                <p>Meta charges per message. In India, order-status updates are <strong>utility</strong> messages (about ₹0.115 each) and offers are <strong>marketing</strong> messages (about ₹0.86 each), plus GST. Chat replies are free for the first 1,000 a month per number. A restaurant handling 1,000 WhatsApp orders a month typically spends <strong>a few hundred to a few thousand rupees</strong> on Meta charges — mostly on offers. Details: <a href="whatsapp-business-api-pricing-india.html">WhatsApp API pricing in India</a>.</p>
                <p>Compare that with commission: on 1,000 orders averaging ₹400, a 20% commission is ₹80,000 a month.</p>

                <h2 id="setup">How to set it up</h2>
                <ol>
                    <li><strong>Verify your business</strong> on Meta Business (GST or FSSAI/trade licence and a website that shows the same name and address help).</li>
                    <li><strong>Connect a number</strong> — ideally the one printed on your menu and Google Business Profile.</li>
                    <li><strong>Set up your menu</strong> as a catalogue or menu flow with categories, prices and photos.</li>
                    <li><strong>Connect payments and the kitchen</strong> — UPI/payment gateway, kitchen screen or printer, delivery staff group.</li>
                    <li><strong>Create templates</strong> for order status, reservation reminders and offers, and get them approved.</li>
                    <li><strong>Promote it</strong>: QR code on tables and bags, WhatsApp button on your website and Google profile, Instagram bio link.</li>
                </ol>

                <h2 id="promote">How to get customers ordering on WhatsApp</h2>
                <ul>
                    <li><strong>Table QR codes</strong> that open your WhatsApp chat with the message "Menu" pre-filled.</li>
                    <li><strong>Bag inserts and stickers</strong> on every aggregator order: "Order direct on WhatsApp — 10% off your next order."</li>
                    <li><strong>Google Business Profile</strong>: add the WhatsApp link and post your weekly specials.</li>
                    <li><strong>Instagram bio and stories</strong> with a direct WhatsApp link.</li>
                    <li><strong>Click-to-WhatsApp ads</strong> on Instagram and Facebook — conversations started from these ads open a free messaging window.</li>
                    <li><strong>Staff script:</strong> "Next time, just message us on WhatsApp — it's faster."</li>
                </ul>

                <h2 id="measure">What to measure</h2>
                <ul>
                    <li>Direct WhatsApp orders per week and their share of total orders</li>
                    <li>Repeat-order rate of WhatsApp customers</li>
                    <li>Average order value on WhatsApp vs aggregators</li>
                    <li>Commission saved each month</li>
                    <li>Offer opt-outs and blocks — if these rise, send fewer offers</li>
                </ul>

                <h2 id="mistakes">Mistakes restaurants make</h2>
                <ul>
                    <li>Sending daily offers — customers block you and your quality rating drops. One or two a week is plenty.</li>
                    <li>No human fallback for complaints or special requests.</li>
                    <li>Menu prices in the bot not updated when the real menu changes.</li>
                    <li>Using unofficial bulk-messaging tools that get the number banned.</li>
                </ul>
                <p>Want ordering at the table too? See our <a href="../portfolio.html#ordering-app">QR table-ordering app</a>.</p>
''',
    faq=[
        ("Can restaurants take orders on WhatsApp automatically?", "Yes. With the WhatsApp Business API a bot can show the menu, take the order and address, collect a UPI payment and send the ticket to the kitchen, with automatic status updates to the customer."),
        ("How much does WhatsApp ordering cost a restaurant?", "Meta charges per message: about ₹0.115 for order-status updates and about ₹0.86 for offers in India, plus GST, with 1,000 free chat replies a month per number. Setup is usually a one-time cost."),
        ("Should restaurants stop using Swiggy and Zomato?", "Not usually. Aggregators are good for reaching new customers. WhatsApp works best for repeat customers who already know you, so you avoid commission on those orders."),
        ("Can customers book a table on WhatsApp?", "Yes. The bot collects the date, time and number of guests, confirms the booking and sends a reminder before the visit."),
    ],
    closing='Want WhatsApp to take orders and bookings for your restaurant? See our <a href="../whatsapp-automation.html">WhatsApp automation services</a> or message us for a demo.',
    cta_title="Take direct orders on WhatsApp",
    cta_text="We'll set up menu ordering, payments, kitchen tickets and order updates for your restaurant — free demo.",
    cta_wa="Hi%20CodeServe%2C%20I%20run%20a%20restaurant%20and%20want%20WhatsApp%20ordering.",
    cta_link=("../whatsapp-automation.html", "WhatsApp Automation"),
    date=DATE,
),
]
