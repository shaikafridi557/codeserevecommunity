/* Selected work: filters, grid/index views, hover preview, tilt and case-study pop-up. */
(function () {
  var root = document.querySelector('.wk');
  if (!root) return;
  root.classList.add('wk-js');

  var grid = root.querySelector('.wk-grid');
  var list = root.querySelector('.wk-list');
  var cards = [].slice.call(root.querySelectorAll('.wk-card'));
  var rows = [].slice.call(root.querySelectorAll('.wk-row'));
  var hover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var filter = 'all';

  function track(name, params) { try { if (window.gtag) window.gtag('event', name, params); } catch (e) {} }

  /* reveal on scroll */
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    cards.forEach(function (c) { io.observe(c); });
  } else {
    cards.forEach(function (c) { c.classList.add('is-in'); });
  }

  /* filters */
  var chips = [].slice.call(root.querySelectorAll('.wk-chip'));
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      filter = chip.dataset.filter;
      chips.forEach(function (c) { var on = c === chip; c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', on); });
      var apply = function () {
        grid.classList.toggle('is-filtered', filter !== 'all');
        cards.concat(rows).forEach(function (el) {
          el.hidden = !(filter === 'all' || el.dataset.cat === filter);
          if (!el.hidden) el.classList.add('is-in');
        });
      };
      if (document.startViewTransition && !reduce) document.startViewTransition(apply); else apply();
      track('portfolio_filter', { filter: filter });
    });
  });

  /* grid / index view */
  var views = [].slice.call(root.querySelectorAll('.wk-view'));
  views.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var v = btn.dataset.view;
      views.forEach(function (b) { var on = b === btn; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); });
      grid.hidden = v !== 'grid';
      list.hidden = v !== 'list';
      track('portfolio_view', { view: v });
    });
  });

  /* index view: floating preview that follows the pointer */
  var floatImg = root.querySelector('.wk-float');
  if (hover && floatImg) {
    var tx = 0, ty = 0, x = 0, y = 0, running = false;
    var loop = function () {
      x += (tx - x) * 0.18; y += (ty - y) * 0.18;
      floatImg.style.left = x + 'px'; floatImg.style.top = y + 'px';
      if (Math.abs(tx - x) > 0.5 || Math.abs(ty - y) > 0.5) requestAnimationFrame(loop); else running = false;
    };
    rows.forEach(function (r) {
      r.addEventListener('pointerenter', function (ev) {
        if (floatImg.getAttribute('src') !== r.dataset.img) floatImg.src = r.dataset.img;
        if (!floatImg.classList.contains('is-on')) { x = tx = ev.clientX; y = ty = ev.clientY; }
        floatImg.classList.add('is-on');
      });
    });
    list.addEventListener('pointermove', function (ev) {
      tx = ev.clientX + 40; ty = ev.clientY;
      if (!running) { running = true; requestAnimationFrame(loop); }
    });
    list.addEventListener('pointerleave', function () { floatImg.classList.remove('is-on'); });
  }

  /* gentle 3D tilt on cards */
  if (hover && !reduce) {
    cards.forEach(function (c) {
      var m = c.querySelector('.wk-media');
      c.querySelector('.wk-hit').addEventListener('pointermove', function (ev) {
        var r = m.getBoundingClientRect();
        var px = (ev.clientX - r.left) / r.width - 0.5, py = (ev.clientY - r.top) / r.height - 0.5;
        m.style.setProperty('--ry', (px * 6).toFixed(2) + 'deg');
        m.style.setProperty('--rx', (-py * 6).toFixed(2) + 'deg');
      });
      c.querySelector('.wk-hit').addEventListener('pointerleave', function () {
        m.style.setProperty('--ry', '0deg'); m.style.setProperty('--rx', '0deg');
      });
    });
  }

  /* case-study pop-up */
  var modal = root.querySelector('.wk-modal');
  if (!modal || typeof modal.showModal !== 'function') return;
  var mMedia = modal.querySelector('.wk-m-media');
  var mBody = modal.querySelector('.wk-m-body');
  var current = null;

  function visible() { return cards.filter(function (c) { return !c.hidden; }); }
  function bySlug(slug) { return cards.filter(function (c) { return c.dataset.slug === slug; })[0]; }

  function show(card) {
    current = card;
    var img = card.querySelector('.wk-media img');
    mMedia.innerHTML = '';
    var big = document.createElement('img');
    big.src = img.getAttribute('src');
    big.alt = img.alt;
    big.width = 1260; big.height = 788;
    mMedia.appendChild(big);
    mBody.innerHTML = card.querySelector('.wk-detail').innerHTML;
    modal.scrollTop = 0;
    if (!modal.open) {
      modal.showModal();
      document.documentElement.style.overflow = 'hidden';
    }
    try { history.replaceState(null, '', '#' + card.dataset.slug); } catch (e) {}
    track('portfolio_open', { project: card.dataset.slug });
  }

  function step(dir) {
    var v = visible();
    var i = v.indexOf(current);
    show(v[(i + dir + v.length) % v.length]);
  }

  cards.forEach(function (c) {
    c.querySelector('.wk-hit').addEventListener('click', function () { show(c); });
  });
  rows.forEach(function (r) {
    r.querySelector('.wk-row-hit').addEventListener('click', function () {
      if (floatImg) floatImg.classList.remove('is-on');
      show(bySlug(r.dataset.slug));
    });
  });

  modal.querySelector('.wk-close').addEventListener('click', function () { modal.close(); });
  modal.querySelector('.wk-prev').addEventListener('click', function () { step(-1); });
  modal.querySelector('.wk-next').addEventListener('click', function () { step(1); });
  modal.addEventListener('click', function (ev) { if (ev.target === modal) modal.close(); });
  modal.addEventListener('keydown', function (ev) {
    if (ev.key === 'ArrowRight') step(1);
    if (ev.key === 'ArrowLeft') step(-1);
  });
  modal.addEventListener('close', function () {
    document.documentElement.style.overflow = '';
    try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
    if (current) current.querySelector('.wk-hit').focus({ preventScroll: true });
  });

  /* open a project directly from a link like portfolio.html#ai-lead-agent */
  var fromHash = location.hash && bySlug(location.hash.slice(1));
  if (fromHash) {
    setTimeout(function () { show(fromHash); }, 900);
  }
})();
