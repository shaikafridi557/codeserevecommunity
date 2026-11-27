/* Story hero: a scroll-scrubbed "film" in five scenes (Chaos → Code → Calm).
   Uses the theme's GSAP + ScrollTrigger. Without them, or with reduced motion,
   the section shows only its final frame (pure CSS). */
(function () {
  var root = document.getElementById('story');
  var html = document.documentElement;
  if (!root) return;
  if (!html.classList.contains('st-js') || !window.gsap || !window.ScrollTrigger) {
    html.classList.remove('st-js');
    return;
  }
  window.stReady = true;
  var gsap = window.gsap, ST = window.ScrollTrigger;
  gsap.registerPlugin(ST);

  var $ = function (s) { return root.querySelector(s); };
  var $$ = function (s) { return [].slice.call(root.querySelectorAll(s)); };
  var stage = $('.st-stage'), device = $('.st-device'), screen = $('.st-screen');
  var notes = $$('.st-note'), tiles = $$('.st-tile'), codeLines = $$('.st-l');
  var caps = [1, 2, 3, 4].map(function (i) { return $('.st-cap-' + i); });
  var lines = function (el) { return el.querySelectorAll('.st-line > span'); };
  var mobile = window.matchMedia('(max-width: 767px)').matches;

  function offsetIn(el, ancestor) {
    var x = 0, y = 0;
    while (el && el !== ancestor) { x += el.offsetLeft; y += el.offsetTop; el = el.offsetParent; }
    return { x: x, y: y };
  }
  // Transform that makes the laptop screen fill the stage (the "full-frame" shot).
  function fullShot() {
    var W = stage.clientWidth, H = stage.clientHeight;
    var sw = screen.offsetWidth, sh = screen.offsetHeight;
    var s = Math.max(W / sw, H / sh) * 1.04;
    var so = offsetIn(screen, device);
    var offX = so.x + sw / 2 - device.offsetWidth / 2, offY = so.y + sh / 2 - device.offsetHeight / 2;
    return { s: s, x: W / 2 - device.offsetLeft - s * offX, y: H / 2 - device.offsetTop - s * offY, offX: offX, offY: offY };
  }
  // Where a dashboard tile's centre lands on screen during the full-frame shot.
  function tileTarget(i) {
    var f = fullShot(), t = tiles[i], o = offsetIn(t, device);
    var cx = o.x + t.offsetWidth / 2 - device.offsetWidth / 2, cy = o.y + t.offsetHeight / 2 - device.offsetHeight / 2;
    return { x: device.offsetLeft + f.x + f.s * cx, y: device.offsetTop + f.y + f.s * cy };
  }

  /* ---------- initial states ---------- */
  gsap.set(device, { xPercent: -50, yPercent: -50, autoAlpha: 0 });
  gsap.set(caps, { autoAlpha: 1 });
  gsap.set([lines(caps[1]), lines(caps[2]), lines(caps[3])], { yPercent: 115 });
  gsap.set(lines(caps[0]), { yPercent: 115 });
  gsap.set(notes, { autoAlpha: 0, scale: 0.4, y: 80, rotation: function () { return gsap.utils.random(-14, 14); } });
  gsap.set('.st-chaos', { autoAlpha: 1 });
  gsap.set('.st-code', { autoAlpha: 0, scale: 0.96 });
  gsap.set(tiles, { autoAlpha: 0, scale: 0.7 });
  gsap.set('.st-bars i', { scaleY: 0, transformOrigin: '50% 100%' });
  gsap.set('.st-phone', { autoAlpha: 0, xPercent: 60 });
  gsap.set('.st-card', { autoAlpha: 0, z: -900, rotationY: function (i) { return [-40, 35, -30][i]; }, transformPerspective: 1200 });
  gsap.set('.st-final > *', { autoAlpha: 0, y: 40 });
  gsap.set(lines($('.st-title')), { yPercent: 115 });
  gsap.set('.st-letterbox', { height: '50%' });

  /* ---------- opening titles (plays once, after the preloader) ---------- */
  var intro = gsap.timeline({ paused: true })
    .to('.st-letterbox', { height: '7vh', duration: 1.3, ease: 'expo.inOut' })
    .to(lines(caps[0]), { yPercent: 0, duration: 1, stagger: 0.14, ease: 'expo.out' }, '-=0.5')
    .from('.st-ui, .st-bar, .st-hint, .st-skip', { autoAlpha: 0, duration: 0.6 }, '-=0.4');
  (function waitForPreloader(n) {
    if (!document.getElementById('dsn_preloader') || n > 20) { intro.play(); return; }
    setTimeout(function () { waitForPreloader(n + 1); }, 150);
  })(0);
  // if the visitor scrolls before the opening titles finished, complete them at once (never a black screen)
  function finishIntro() { if (window.scrollY > 20 && intro.progress() < 1) intro.progress(1); }
  window.addEventListener('scroll', finishIntro, { passive: true });

  /* ---------- the film (scrubbed by scroll) ---------- */
  var tl = gsap.timeline({ defaults: { ease: 'power2.out' } });
  var sceneAt = [0, 0.8, 2.6, 4.6, 6.6];
  // Scene 2 — chaos
  tl.fromTo(lines(caps[0]), { yPercent: 0 }, { yPercent: -115, stagger: 0.1, duration: 0.7, ease: 'power2.in', immediateRender: false }, 0)
    .to(notes, { autoAlpha: 1, scale: 1, y: 0, stagger: { each: 0.08, from: 'random' }, duration: 0.8, ease: 'back.out(1.6)' }, 0.3)
    .to(lines(caps[1]), { yPercent: 0, stagger: 0.12, duration: 0.7 }, 0.8)
    .to('.st-shade', { opacity: 0.75, duration: 0.6 }, 0.8)
    .to('.st-shade', { opacity: 0, duration: 0.5 }, 2.6)
    .to('.st-shade', { opacity: 1, duration: 0.6 }, 5.3)
    .to('.st-shade', { opacity: 0, duration: 0.5 }, 6.6)
    .to(notes, { x: function () { return gsap.utils.random(-40, 40); }, rotation: function () { return gsap.utils.random(-18, 18); }, duration: 0.5, ease: 'sine.inOut' }, 1.5)
    .to(notes, { x: function () { return gsap.utils.random(-40, 40); }, rotation: function () { return gsap.utils.random(-18, 18); }, duration: 0.5, ease: 'sine.inOut' }, 2.0)
    .to('.st-glow', { filter: 'hue-rotate(120deg)', duration: 1.2 }, 1.2)
  // Scene 3 — code
    .to(lines(caps[1]), { yPercent: -115, stagger: 0.08, duration: 0.6, ease: 'power2.in' }, 2.6)
    .to(notes, { autoAlpha: 0.18, filter: 'blur(4px)', scale: 0.9, duration: 0.8 }, 2.7)
    .to('.st-glow', { filter: 'hue-rotate(0deg)', duration: 1 }, 2.7)
    .set(device, { x: function () { return fullShot().x; }, y: function () { return fullShot().y; }, scale: function () { return fullShot().s; } }, 2.7)
    .to(device, { autoAlpha: 1, duration: 0.6 }, 2.8)
    .to('.st-code', { autoAlpha: 1, scale: 1, duration: 0.7 }, 2.9)
    .to(codeLines, { clipPath: 'inset(0 0% 0 0)', stagger: 0.17, duration: 0.45, ease: 'none' }, 3.1)
    .to(lines(caps[2]), { yPercent: 0, stagger: 0.12, duration: 0.7 }, 3.3)
  // Scene 4 — calm: the chaos snaps into one dashboard
    .to('.st-code', { autoAlpha: 0, y: -60, scale: 0.94, duration: 0.6, ease: 'power2.in' }, 4.6)
    .to(lines(caps[2]), { yPercent: -115, stagger: 0.08, duration: 0.6, ease: 'power2.in' }, 4.6)
    .to(notes, {
      autoAlpha: 0.9, filter: 'blur(0px)', rotation: 0, scale: 0.55,
      x: function (i, el) { var t = tileTarget(+el.dataset.t); return t.x - (el.offsetLeft + el.offsetWidth / 2); },
      y: function (i, el) { var t = tileTarget(+el.dataset.t); return t.y - (el.offsetTop + el.offsetHeight / 2); },
      stagger: 0.05, duration: 0.9, ease: 'power3.inOut'
    }, 4.7)
    .to(notes, { autoAlpha: 0, scale: 0.4, duration: 0.3, stagger: 0.05 }, 5.6)
    .to(tiles, { autoAlpha: 1, scale: 1, stagger: 0.08, duration: 0.6, ease: 'back.out(1.4)' }, 5.5)
    .to('.st-bars i', { scaleY: 1, stagger: 0.05, duration: 0.5 }, 5.9)
    .to(lines(caps[3]), { yPercent: 0, stagger: 0.12, duration: 0.7 }, 5.6)
  // Scene 5 — the frame pulls back into a laptop; our work flies in
    .to(lines(caps[3]), { yPercent: -115, stagger: 0.08, duration: 0.6, ease: 'power2.in' }, 6.6)
    .to(device, { x: 0, y: 0, scale: 1, duration: 1.5, ease: 'power3.inOut' }, 6.8)
    .to('.st-letterbox', { height: 0, duration: 0.8 }, 7.6)
    .to('.st-phone', { autoAlpha: 1, xPercent: 0, duration: 0.7 }, 7.8)
    .to('.st-card', { autoAlpha: 1, z: 0, rotationY: 0, stagger: 0.15, duration: 1, ease: 'power3.out' }, 7.9)
    .to('.st-final > *', { autoAlpha: 1, y: 0, stagger: 0.1, duration: 0.7 }, 8.2)
    .to(lines($('.st-title')), { yPercent: 0, stagger: 0.12, duration: 0.8, ease: 'expo.out' }, 8.3)
    .to('.st-hint', { autoAlpha: 0, duration: 0.3 }, 0.1)
    .to({}, { duration: 0.8 }, 9.4); // hold the last frame

  var sceneEl = $('.st-scene b'), fill = $('.st-fill'), skip = $('.st-skip'), last = -1;
  // The theme kills every ScrollTrigger while it initialises, so (re)create ours once it is done.
  function bind() {
    if (ST.getById('story')) return;
    ST.create({
    id: 'story',
    trigger: root, start: 'top top', end: 'bottom bottom', scrub: mobile ? 0.6 : 1, animation: tl, invalidateOnRefresh: true,
    onUpdate: function (self) {
      var t = tl.time(), n = 0;
      for (var i = 0; i < sceneAt.length; i++) if (t >= sceneAt[i]) n = i;
      if (n !== last) { last = n; sceneEl.textContent = '0' + (n + 1); }
      fill.style.transform = 'scaleX(' + self.progress.toFixed(3) + ')';
      skip.style.opacity = self.progress > 0.85 ? 0 : 1;
      skip.style.pointerEvents = self.progress > 0.85 ? 'none' : '';
    }
    });
    ST.refresh();
  }

  skip.addEventListener('click', function () {
    var end = root.offsetTop + root.offsetHeight - window.innerHeight;
    window.scrollTo({ top: end, behavior: 'smooth' });
    try { if (window.gtag) window.gtag('event', 'story_skip'); } catch (e) {}
  });

  // bind after the preloader (theme init) has finished, and re-check a few times in case it kills triggers again
  (function waitTheme(n) {
    if (!document.getElementById('dsn_preloader') || n > 40) {
      setTimeout(bind, 200); setTimeout(bind, 1200); setTimeout(bind, 3000);
      return;
    }
    setTimeout(function () { waitTheme(n + 1); }, 150);
  })(0);
  window.addEventListener('load', function () { setTimeout(bind, 400); });
})();
