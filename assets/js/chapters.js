/* Home chapters: four scroll-scrubbed 3D scenes (video screen, service ring, project tunnel, mask reveal).
   Needs GSAP + ScrollTrigger (from the theme) and html.st-js; otherwise the static layout stays. */
(function () {
  var html = document.documentElement;
  if (!html.classList.contains('st-js') || !window.gsap || !window.ScrollTrigger) return;
  var gsap = window.gsap, ST = window.ScrollTrigger;
  gsap.registerPlugin(ST);
  var mobile = window.matchMedia('(max-width: 767px)').matches;
  var q = function (s, r) { return (r || document).querySelector(s); };
  var qa = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var builders = [];

  /* ---------- CH.01 — the brand film grows to full screen while the headline splits apart ---------- */
  var who = document.getElementById('ch-who');
  if (who) {
    var film = q('.ch-film', who), vid = q('.ch-video-el', who);
    // load and play the film only when the chapter is near; pause it when far away
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) {
            if (!vid.src) { vid.src = vid.dataset.src; vid.preload = 'auto'; }
            var p = vid.play(); if (p && p.catch) p.catch(function () {});
          } else if (vid.src) { vid.pause(); }
        });
      }, { rootMargin: '60% 0px' }).observe(who);
    } else { vid.src = vid.dataset.src; vid.autoplay = true; }

    builders.push(function () {
      var items = qa('.ch-manifesto li', who);
      gsap.set([q('.ch-who-h', who), q('.ch-link', who)], { autoAlpha: 0, y: 30 });
      gsap.set(items, { autoAlpha: 0, y: 40 });
      var full = function () { return Math.max(innerWidth / film.offsetWidth, innerHeight / film.offsetHeight) * 1.01; };
      var tl = gsap.timeline({ defaults: { ease: 'power2.out' } });
      tl.to(q('.ch-sl', who), { yPercent: -160, autoAlpha: 0, duration: 3, ease: 'power2.in' }, 0.3)
        .to(q('.ch-sr', who), { yPercent: 160, autoAlpha: 0, duration: 3, ease: 'power2.in' }, 0.3)
        .to(q('.ch-scroll-note', who), { autoAlpha: 0, duration: 0.6 }, 0.3)
        .to(film, { scale: full, borderRadius: 0, duration: 3.6, ease: 'power2.inOut' }, 0.4)
        .to(q('.ch-film-shade', who), { opacity: 1, duration: 1.2 }, 4.0)
        .to(q('.ch-who-h', who), { autoAlpha: 1, y: 0, duration: 0.8 }, 4.4);
      items.forEach(function (li, i) { tl.to(li, { autoAlpha: 1, y: 0, duration: 0.8 }, 5.0 + i * 0.8); });
      tl.to(q('.ch-link', who), { autoAlpha: 1, y: 0, duration: 0.6 }, 8.4)
        .to({}, { duration: 1 }, 9.2);
      return { id: 'ch-who', trigger: who, animation: tl };
    });
  }

  /* ---------- CH.02 — services on a rotating 3D ring ---------- */
  var ring = document.getElementById('ch-build');
  if (ring) {
    var world = q('.ch-ring-world', ring), cards = qa('.ch-card', ring), numEl = q('.ch-ring-num b', ring);
    var n = cards.length, step = 360 / n, rot = { a: 0 };
    function radius() { return cards[0].offsetWidth / (2 * Math.tan(Math.PI / n)) * (mobile ? 1.02 : 1.18); }
    function shade() {
      var front = Math.round(-rot.a / step) % n; if (front < 0) front += n;
      cards.forEach(function (c, i) {
        var d = Math.abs(((i * step + rot.a) % 360 + 540) % 360 - 180); // 0 = facing camera, 180 = at the back
        var f = 1 - d / 180; // 1 at front, 0 at back
        c.style.filter = 'brightness(' + (0.28 + 0.72 * Math.pow(f, 2.2)).toFixed(3) + ')';
        c.classList.toggle('is-front', i === front);
        c.style.pointerEvents = i === front ? 'auto' : 'none';
      });
      numEl.textContent = '0' + (front + 1);
    }
    builders.push(function () {
      // cards sit on a cylinder around the world's centre
      cards.forEach(function (c, i) { gsap.set(c, { rotationY: i * step, transformOrigin: '50% 50%' }); });
      var R = radius();
      cards.forEach(function (c, i) {
        var a = i * step * Math.PI / 180;
        gsap.set(c, { x: Math.sin(a) * R, z: Math.cos(a) * R, rotationY: i * step });
      });
      gsap.set(world, { rotationX: -6, z: -R });
      rot.a = 0; shade();
      var tl = gsap.timeline();
      tl.to(rot, { a: -(n - 1) * step, duration: n - 1, ease: 'none', onUpdate: function () { gsap.set(world, { rotationY: rot.a }); shade(); } }, 0)
        .fromTo(world, { rotationX: -14 }, { rotationX: -4, duration: n - 1, ease: 'sine.inOut' }, 0)
        .to({}, { duration: 0.6 }, n - 1);
      return { id: 'ch-build', trigger: ring, animation: tl };
    });
  }

  /* ---------- CH.03 — fly through a tunnel of projects ---------- */
  var tun = document.getElementById('ch-proof');
  if (tun) {
    var tworld = q('.ch-tunnel-world', tun), frames3 = qa('.ch-frame', tun), title = q('.ch-tunnel-title', tun), all = q('.ch-tunnel-all', tun);
    var D = mobile ? 700 : 820, cam = { z: 0 };
    function fog() {
      frames3.forEach(function (f, i) {
        var dz = cam.z - (i + 1) * D;            // >0 means the frame is behind the camera
        var o = dz > -200 ? Math.max(0, 1 - (dz + 200) / 500) : Math.max(0, Math.min(1, 1 - (-dz - 2000) / 1400));
        f.style.opacity = o.toFixed(3);
        f.style.pointerEvents = o > 0.6 ? 'auto' : 'none';
      });
    }
    builders.push(function () {
      frames3.forEach(function (f, i) {
        var side = i % 2 ? 1 : -1;
        gsap.set(f, {
          xPercent: -50, yPercent: -50,
          x: side * (mobile ? 20 : 27) * innerWidth / 100,
          y: (i % 3 - 1) * innerHeight * 0.12,
          z: -(i + 1) * D, rotationY: -side * 14, rotationZ: side * 2
        });
      });
      gsap.set(qa('.ch-line > span', tun), { yPercent: 115 });
      gsap.set(all, { autoAlpha: 0 });
      cam.z = 0; gsap.set(tworld, { z: 0 }); fog();
      var total = (frames3.length + 0.6) * D;
      var tl = gsap.timeline();
      tl.to(qa('.ch-line > span', tun), { yPercent: 0, stagger: 0.15, duration: 0.6, ease: 'expo.out' }, 0)
        .to(title, { scale: 0.6, autoAlpha: 0.1, duration: 1.2, ease: 'power1.in' }, 0.8)
        .to(cam, { z: total, duration: 10, ease: 'none', onUpdate: function () { gsap.set(tworld, { z: cam.z }); fog(); } }, 1.2)
        .to(title, { autoAlpha: 1, scale: 1, duration: 0.8 }, 9.6)
        .to(all, { autoAlpha: 1, duration: 0.5 }, 10)
        .to({}, { duration: 0.6 }, 10.4);
      return { id: 'ch-proof', trigger: tun, animation: tl };
    });
  }

  /* ---------- CH.04 — circle mask reveal ---------- */
  var you = document.getElementById('ch-you');
  if (you) {
    builders.push(function () {
      var img = q('.ch-mask-img', you);
      gsap.set(q('img', img), { scale: 1.35 });
      gsap.set(qa('.ch-line > span', you), { yPercent: 115 });
      gsap.set(['.ch-you-k', '.ch-you-p', '.ch-cta'], { autoAlpha: 0, y: 30 });
      var tl = gsap.timeline();
      tl.fromTo(img, { clipPath: 'circle(7% at 50% 50%)' }, { clipPath: 'circle(80% at 50% 50%)', duration: 4, ease: 'power2.inOut' }, 0)
        .to(q('img', img), { scale: 1, duration: 4, ease: 'power2.out' }, 0)
        .to('.ch-you-k', { autoAlpha: 1, y: 0, duration: 0.8 }, 3)
        .to(qa('.ch-line > span', you), { yPercent: 0, stagger: 0.25, duration: 1.2, ease: 'expo.out' }, 3.3)
        .to(['.ch-you-p', '.ch-cta'], { autoAlpha: 1, y: 0, stagger: 0.25, duration: 0.8 }, 4)
        .to({}, { duration: 1 }, 5);
      return { id: 'ch-you', trigger: you, animation: tl };
    });
  }

  /* ---------- bind (after the theme has initialised; it kills triggers on start) ---------- */
  var built = false, specs = [];
  function bind() {
    if (!built) { specs = builders.map(function (b) { return b(); }); built = true; }
    specs.forEach(function (s) {
      if (ST.getById(s.id)) return;
      ST.create({ id: s.id, trigger: s.trigger, start: 'top top', end: 'bottom bottom', scrub: mobile ? 0.5 : 0.9, animation: s.animation, invalidateOnRefresh: true });
    });
    ST.refresh();
  }
  (function waitTheme(k) {
    if (!document.getElementById('dsn_preloader') || k > 40) { setTimeout(bind, 250); setTimeout(bind, 1300); setTimeout(bind, 3100); return; }
    setTimeout(function () { waitTheme(k + 1); }, 150);
  })(0);
  window.addEventListener('load', function () { setTimeout(bind, 500); });
})();
