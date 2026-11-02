// Sends lead-related clicks to Google Analytics 4 as events
(function () {
    function track(name, params) {
        if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
    }

    document.addEventListener('click', function (e) {
        var link = e.target.closest && e.target.closest('a[href]');
        if (!link) return;
        var href = link.getAttribute('href') || '';
        var label = (link.textContent || '').trim().slice(0, 80);
        if (href.indexOf('wa.me/') !== -1 || href.indexOf('api.whatsapp.com') !== -1) {
            track('whatsapp_click', { link_url: href, link_text: label, page_path: location.pathname });
        } else if (href.indexOf('tel:') === 0) {
            track('phone_click', { phone_number: href.slice(4), page_path: location.pathname });
        } else if (href.indexOf('mailto:') === 0) {
            track('email_click', { page_path: location.pathname });
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
        track('generate_lead', { form_id: form.id || 'form', page_path: location.pathname });
    }, true);
})();
