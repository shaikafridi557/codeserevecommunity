// Sends lead-related clicks to Google Analytics 4 as events.
// Event names (GA4 style, snake_case):
//   whatsapp_click, phone_click, email_click   contact attempts
//   cta_click                                  main buttons (Start a project, Get a quote, plan buttons)
//   portfolio_click                            links to live client projects
//   share                                      article share buttons
//   form_submit_attempt                        a form was submitted
//   generate_lead                              the contact form was actually delivered (sent from contact.html)
(function () {
    function track(name, params) {
        if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
    }

    document.addEventListener('click', function (e) {
        var link = e.target.closest && e.target.closest('a[href]');
        if (!link) return;
        var href = link.getAttribute('href') || '';
        var label = (link.textContent || '').trim().slice(0, 80);
        if (link.hasAttribute('data-share')) {
            track('share', { method: link.getAttribute('data-share'), content_type: 'article', item_id: location.pathname });
            return;
        }
        if (href.indexOf('wa.me/') !== -1 || href.indexOf('api.whatsapp.com') !== -1) {
            track('whatsapp_click', { link_url: href, link_text: label, page_path: location.pathname });
        } else if (href.indexOf('tel:') === 0) {
            track('phone_click', { phone_number: href.slice(4), page_path: location.pathname });
        } else if (href.indexOf('mailto:') === 0) {
            track('email_click', { page_path: location.pathname });
        } else if (/^https?:/.test(href) && link.hostname !== location.hostname &&
                   link.closest('[class*="portfolio"], [class*="project"], [class*="work"], #work')) {
            track('portfolio_click', { link_url: href, link_text: label, page_path: location.pathname });
        } else if (link.matches('.cs-btn, .pricing-card__cta, .startup-kit__cta, .btn.primary, .creative-button')) {
            track('cta_click', { link_url: href, link_text: label, page_path: location.pathname });
        }
    }, true);

    // The floating chat widget opens WhatsApp with window.open instead of a link
    window.addEventListener('load', function () {
        if (typeof window.sendWhatsAppMessage !== 'function') return;
        var original = window.sendWhatsAppMessage;
        window.sendWhatsAppMessage = function (message) {
            track('whatsapp_click', { link_text: String(message).slice(0, 80), source: 'chat_widget', page_path: location.pathname });
            return original.apply(this, arguments);
        };
    });

    document.addEventListener('submit', function (e) {
        var form = e.target;
        if (!form || form.tagName !== 'FORM') return;
        track('form_submit_attempt', { form_id: form.id || 'form', page_path: location.pathname });
    }, true);
})();
