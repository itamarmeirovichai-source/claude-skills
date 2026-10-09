/* Smash House — THE TOSS, THE SMASH, THE CUT.

   The burger is no longer drawn in real time. It is a photoreal Cycles render
   of a modelled burger — bun, two smash patties, melted cheese, beef bacon,
   caramelised onion, chef sauce — played back as a frame sequence that scrubs
   with the scroll. Everything on screen is still a pure function of scroll
   progress, so scrubbing backwards is exact: no `once`, no accumulated state.

   Frames are RGBA WebP on a transparent film, so the page supplies its own
   background and the burger composites straight onto it. */
(function (SH) {
  'use strict';
  var clamp = SH.clamp, inv = SH.inv, lerp = SH.lerp;

  var BEATS = {
    toss:[0,.11], bullet:[.11,.21], closeup:[.21,.31], explode:[.31,.50],
    turn:[.50,.59], smash:[.59,.69], cut:[.69,.86], slice:[.86,1]
  };
  var COPY = [
    [0,   'THE TOSS',      'Straight off the flat-top, into the light.'],
    [.11, 'BULLET TIME',   'Time stops at the peak. The camera keeps going.'],
    [.21, 'THE CLOSE-UP',  'The Loaded Smashed. Double patty, beef bacon, caramelized onion.'],
    [.31, 'THE EXPLODE',   'Nine layers. Every one of them named.'],
    [.50, 'THE HALF TURN', 'All the way around, still readable.'],
    [.59, 'THE SMASH',     'Back together. You felt that.'],
    [.69, 'THE CUT',       'The only shot that matters.'],
    [.86, 'THE HAND-OFF',  'Straight to the order.']
  ];
  /* the render's layer names, bottom to top, and what the label says
     [TO CONFIRM exact build order with the owner] */
  var LAYERS = [
    ['bun_bottom',        'TOASTED BASE'],
    ['patty_lower',       'SMASHED PATTY'],
    ['cheese_lower',      'PLANT-BASED CHEESE'],
    ['patty_upper',       'SMASHED PATTY'],
    ['cheese_upper',      'PLANT-BASED CHEESE'],
    ['bacon_beef',        'BEEF BACON'],
    ['onion_caramelized', 'CARAMELIZED ONION'],
    ['sauce_chef',        'CHEF SAUCE'],
    ['bun_top',           'SESAME CROWN']
  ];

  var VARIANTS = {
    desktop: { dir: 'frames/desktop/', n: 108, w: 1440, h: 810 },
    mobile:  { dir: 'frames/mobile/',  n: 54,  w: 810,  h: 1080 }
  };

  function variantFor() {
    return (window.innerWidth < 820 && window.innerHeight > window.innerWidth)
      ? 'mobile' : 'desktop';
  }
  function pad(n) { return ('0000' + n).slice(-4); }

  SH.onBoot(function () {
    var section = document.querySelector('[data-seq]');
    if (!section) return;
    var stage = section.querySelector('[data-seq-stage]');
    var canvas = section.querySelector('[data-seq-canvas]');
    var labelWrap = section.querySelector('[data-seq-labels]');
    var beatName = section.querySelector('[data-beat-name]');
    var beatLine = section.querySelector('[data-beat-line]');
    var flash = section.querySelector('[data-flash]');
    var splitTop = section.querySelector('[data-split-top]');
    var splitBottom = section.querySelector('[data-split-bottom]');
    var reveal = section.querySelector('[data-reveal]');
    var bar = section.querySelector('[data-seq-bar]');
    var disc = document.querySelector('[data-match]');
    var kong = section.querySelector('[data-kong-arm]');
    var orderBtn = document.querySelector('.btn-order');

    var ctx = canvas.getContext('2d');
    if (!ctx) { section.setAttribute('data-noframes', ''); return; }

    var vkey = variantFor();
    var V = VARIANTS[vkey];
    var imgs = new Array(V.n);
    var state = new Array(V.n);      /* 0 idle, 1 loading, 2 ready, 3 failed */
    var readyCount = 0, firstFailed = false;
    var anchors = null;

    for (var i = 0; i < V.n; i++) state[i] = 0;

    function request(i, done) {
      if (i < 0 || i >= V.n) return;
      if (state[i] === 2 || state[i] === 3) { if (done) done(); return; }
      if (state[i] === 1) return;                 /* already in flight */
      state[i] = 1;
      var im = new Image();
      im.decoding = 'async';
      im.onload = function () { state[i] = 2; imgs[i] = im; readyCount++; if (done) done(); };
      im.onerror = function () {
        state[i] = 3;
        if (i === 0 && !firstFailed) {
          /* no frames at all: fall back to the poster the CSS holds */
          firstFailed = true;
          section.setAttribute('data-noframes', '');
          document.documentElement.setAttribute('data-noframes', '');
        }
        if (done) done();
      };
      im.src = V.dir + 'smash_' + pad(i + 1) + '.webp';
    }

    /* Load order matters more than load count: frame one first so something is
       on screen, then every eighth frame so a fast scrub already has somewhere
       to land, then the gaps filled in. Six in flight at a time. */
    var queue = [0];
    [8, 4, 2, 1].forEach(function (stride) {
      for (var q = 0; q < V.n; q += stride) if (queue.indexOf(q) < 0) queue.push(q);
    });
    /* Everything past the coarse pass waits until the section is near. A visitor
       who never scrolls this far should not pay for four megabytes of frames. */
    var eager = 1 + Math.ceil(V.n / 8);
    var limit = eager, qi = 0, inflight = 0;
    function pump() {
      while (inflight < 6 && qi < Math.min(limit, queue.length)) {
        var idx = queue[qi++];
        if (state[idx]) continue;
        inflight++;
        request(idx, function () { inflight--; pump(); });
      }
    }
    function loadAll() { limit = queue.length; pump(); }
    pump();

    fetch(V.dir.replace(/(desktop|mobile)\/$/, '') + 'labels.' + vkey + '.json')
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { if (j && j.anchors) anchors = j; })
      .catch(function () { anchors = null; });

    /* the nearest frame we can actually draw, so scrubbing never goes blank */
    function nearestReady(i) {
      if (state[i] === 2) return i;
      for (var d = 1; d < V.n; d++) {
        if (i - d >= 0 && state[i - d] === 2) return i - d;
        if (i + d < V.n && state[i + d] === 2) return i + d;
      }
      return -1;
    }

    var labels = LAYERS.map(function (L) {
      var el = document.createElement('span');
      el.textContent = L[1];
      labelWrap.appendChild(el);
      return el;
    });

    var track = SH.tracker(section);
    var visible = false;
    SH.inView(stage, 25, function (v) { visible = v; if (v) loadAll(); });
    /* and if the visitor lands deep-linked past the fold, do not wait */
    if (window.scrollY > 0) setTimeout(loadAll, 4000);
    var shown = -1, pSmooth = 0;
    var fit = { x: 0, y: 0, w: 1, h: 1 };

    /* contain-fit with a little bleed, so the burger never crops and the frame
       maps 1:1 onto the label coordinates the render wrote out */
    function layout() {
      var cw = canvas.width, ch = canvas.height;
      var k = Math.min(cw / V.w, ch / V.h);
      fit.w = V.w * k; fit.h = V.h * k;
      fit.x = (cw - fit.w) / 2; fit.y = (ch - fit.h) / 2;
    }

    function drawFrame(p) {
      var want = Math.round(p * (V.n - 1));
      var use = nearestReady(want);
      /* keep a small window around the playhead hot */
      for (var d = 0; d <= 3; d++) { request(want + d); request(want - d); }
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      if (use < 0) return;
      ctx.drawImage(imgs[use], fit.x, fit.y, fit.w, fit.h);
    }

    function placeLabels(p) {
      var e = inv(p, BEATS.explode[0], BEATS.explode[1]);
      var fade = (1 - clamp((p - BEATS.turn[1] + 0.03) / 0.03, 0, 1));
      var frameKey = pad(Math.round(p * (V.n - 1)) + 1);
      var row = anchors && anchors.anchors[frameKey];
      var dpr = canvas.width / canvas.clientWidth || 1;
      for (var i = 0; i < labels.length; i++) {
        var el = labels[i];
        if (!row || e <= 0 || fade <= 0) { el.style.opacity = '0'; continue; }
        var a = row[LAYERS[i][0]];
        if (!a) { el.style.opacity = '0'; continue; }
        var px = (fit.x + a[0] * fit.w) / dpr;
        var py = (fit.y + a[1] * fit.h) / dpr;
        var cw = canvas.clientWidth;
        /* Flip the label to the other side when it would run off the edge,
           measured against its own width. Choosing the side by which half of
           the stage the anchor sits in put every mobile label off the right
           of a 390px screen, with the text cut in half. */
        var w = el.offsetWidth || 150;
        var side = (px + w + 12 > cw) ? -1 : 1;
        if (side < 0 && px - w < 12) side = 1;       /* no room either way */
        px = Math.max(12, Math.min(px, cw - 12));
        var appear = clamp((e - i * 0.055) / 0.22, 0, 1);
        el.style.opacity = String(appear * fade * (a[2] ? 1 : 0.25));
        el.style.transform = 'translate(' + px + 'px,' + py + 'px)'
          + (side < 0 ? ' translateX(-100%)' : '');
        /* flipping direction moves the leader dash and dot to the inside edge,
           which is what makes a label read as pointing at the layer */
        el.style.direction = side < 0 ? 'rtl' : 'ltr';
        el.style.textAlign = side < 0 ? 'right' : 'left';
      }
    }

    function render(p) {
      drawFrame(p);
      placeLabels(p);

      /* beat 2: Kong's hand comes in from the right and takes one */
      if (kong && kong.dataset.ready === '1') {
        var kb = inv(p, BEATS.bullet[0], BEATS.bullet[1]);
        var grab = clamp((kb - 0.25) / 0.6, 0, 1);
        var show = kb > 0.2 && kb < 0.98;
        kong.style.display = show ? 'block' : 'none';
        if (show) {
          var ease = SH.easeOut3(grab);
          kong.style.right = (-30 + ease * 26) + 'vw';
          kong.style.top = (34 - ease * 6) + 'vh';
          kong.style.transform = 'rotate(' + (-16 + ease * 12) + 'deg) scale(' + (0.92 + ease * 0.12) + ')';
          kong.style.opacity = String(clamp((kb - 0.2) / 0.12, 0, 1) * (1 - clamp((kb - 0.86) / 0.12, 0, 1)));
        }
      }

      /* the smash kicks the whole stage, the same way the render kicks the camera */
      var sm = inv(p, BEATS.smash[0], BEATS.smash[1]);
      var shake = sm > 0 && sm < 1 ? Math.exp(-sm * 9) * (1 - SH.smooth(sm)) : 0;
      flash.style.opacity = String(shake * 0.16);
      canvas.style.transform = shake > 0.002
        ? 'translate3d(' + (Math.sin(sm * 71) * shake * 7).toFixed(2) + 'px,'
          + (Math.sin(sm * 53) * shake * 5).toFixed(2) + 'px,0)'
        : '';

      /* beat 8: cross-dissolve the burger into the page surface, then split it
         apart. Both are near-black, so it reads as the burger leaving. */
      var sl = inv(p, BEATS.slice[0], BEATS.slice[1]);
      var shutter = clamp(sl / 0.18, 0, 1);
      var part = SH.easeOut3(clamp((sl - 0.18) / 0.82, 0, 1));
      splitTop.style.opacity = splitBottom.style.opacity = String(shutter);
      splitTop.style.transform = 'translate3d(0,' + (-part * 52) + 'vh,0)';
      splitBottom.style.transform = 'translate3d(0,' + (part * 52) + 'vh,0)';
      reveal.style.opacity = String(clamp((sl - 0.2) / 0.3, 0, 1));
      canvas.style.opacity = String(1 - shutter);
      bar.style.width = (p * 100) + '%';

      /* match cut: the round cut face becomes the order button */
      if (sl > 0.45 && orderBtn) {
        var t = clamp((sl - 0.45) / 0.5, 0, 1), te = SH.easeOut3(t);
        var r = orderBtn.getBoundingClientRect();
        var startS = Math.min(innerWidth, innerHeight) * 0.26;
        var size = lerp(startS, Math.max(r.width, r.height), te);
        disc.style.opacity = String(t < 0.96 ? 1 : (1 - (t - 0.96) / 0.04));
        disc.style.width = size + 'px'; disc.style.height = size + 'px';
        disc.style.left = lerp(innerWidth / 2 - size / 2, r.left + r.width / 2 - size / 2, te) + 'px';
        disc.style.top = lerp(innerHeight / 2 - size / 2, r.top + r.height / 2 - size / 2, te) + 'px';
        disc.style.borderRadius = '50%';
      } else if (disc) { disc.style.opacity = '0'; }

      var idx = 0;
      for (var ci = 0; ci < COPY.length; ci++) if (p >= COPY[ci][0]) idx = ci;
      if (idx !== shown) {
        shown = idx;
        beatName.textContent = COPY[idx][1];
        beatLine.textContent = COPY[idx][2];
      }
    }

    function resize() { if (SH.fitCanvas(canvas, SH.dprCap)) { layout(); track.measure(); } }
    window.addEventListener('resize', SH.debounce(function () {
      track.measure(); resize(); layout();
    }, 200), { passive: true });
    resize(); layout();

    /* QA hook: with #qa in the URL the beat can be driven directly instead of
       by scroll, so every frame can be inspected deterministically. */
    var forced = null;
    if (location.hash === '#qa') window.__setP = function (v) { forced = v; };

    SH.add(function (dt) {
      if (!visible || document.hidden) return;
      resize();
      var target = forced === null ? track.progress() : forced;
      pSmooth = (SH.reduced || forced !== null) ? target : SH.damp(pSmooth, target, 0.0015, dt);
      if (Math.abs(target - pSmooth) < 0.0002) pSmooth = target;
      render(pSmooth);
      window.__seq = {
        p: +pSmooth.toFixed(3), target: +target.toFixed(3), variant: vkey,
        frames: V.n, ready: readyCount, labels: !!anchors,
        track: track.debug(), visible: visible,
        drew: (window.__drew = (window.__drew || 0) + 1)
      };
    });
  });
})(SH);
