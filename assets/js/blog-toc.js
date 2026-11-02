// Highlights the table-of-contents link for the section currently being read
(function () {
    var toc = document.querySelector('.cs-article-aside .cs-toc');
    if (!toc) return;

    var links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
    var sections = links
        .map(function (link) { return document.getElementById(link.getAttribute('href').slice(1)); })
        .filter(Boolean);

    function setActive() {
        var offset = window.innerHeight * 0.3;
        var current = sections[0];
        sections.forEach(function (section) {
            if (section.getBoundingClientRect().top - offset <= 0) current = section;
        });
        links.forEach(function (link) {
            var active = current && link.getAttribute('href') === '#' + current.id;
            link.classList.toggle('active', active);
            if (active) link.setAttribute('aria-current', 'true');
            else link.removeAttribute('aria-current');
        });
    }

    // Capture-phase handler on the TOC runs before the theme's own hash-link handler,
    // which scrolls to offsetTop and lands in the wrong place for nested headings.
    toc.addEventListener('click', function (e) {
        var link = e.target.closest('a[href^="#"]');
        if (!link) return;
        var target = document.getElementById(link.getAttribute('href').slice(1));
        if (!target) return;
        e.preventDefault();
        e.stopPropagation();
        var top = target.getBoundingClientRect().top + window.pageYOffset - 100;
        var lenis = window.$effectScroll && window.$effectScroll.getScrollbar && window.$effectScroll.getScrollbar();
        if (lenis) lenis.scrollTo(top);
        else window.scrollTo({ top: top, behavior: 'smooth' });
        history.replaceState(null, '', link.getAttribute('href'));
    }, true);

    window.addEventListener('scroll', setActive, { passive: true });
    window.addEventListener('resize', setActive);
    setActive();
})();
