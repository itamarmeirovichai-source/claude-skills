/* Smash House — hero, live status, menu rail, smash press, neon, footer griddle, cursor. */
(function (SH) {
  'use strict';
  var clamp = SH.clamp, lerp = SH.lerp;

  /* real Boca Raton menu items, by name. No invented prices, ever. */
  var MENU = [
    ['LOADED SMASHED', 'Double smashed burger, plant-based cheese, caramelized onion, beef bacon.', ['beef','plant']],
    ['DOUBLE SMASHED', 'Two smashed patties, the house build.', ['beef']],
    ['DIRTY FRIES', 'Fries under pulled brisket and chef sauce.', ['beef']],
    ['BLOOMING ONION', 'A whole onion, battered and opened up.', ['side']],
    ['POPCORN CHICKEN', 'Bite-size, fried to order.', ['chicken']],
    ['PHILLY CHEESE SANDO', 'Griddled steak with plant-based cheese.', ['beef','plant']],
    ['THE CRISPITY CRUNCH', 'House crunch build.', ['chicken']],
    ['KIDS MENU', 'Smaller portions for smaller people.', ['kids']],
    ['DESSERTS', 'Ask what came out of the kitchen today.', ['side']]
  ];
  var TAGCLASS = { beef:'beef', plant:'plant', kids:'kids', chicken:'', side:'' };
  var TAGLABEL = { beef:'Beef', plant:'Plant-based cheese', kids:'Kids', chicken:'Chicken', side:'Side' };

  /* ---------- preloader ---------- */
  SH.onBoot(function () {
    var pre = document.getElementById('preloader');
    if (!pre) return;
    var patty = pre.querySelector('.pre-patty span');
    var bar = pre.querySelector('.pre-bar i');
    var t0 = performance.now(), done = false;
    function finish() {
      if (done) return; done = true;
      bar.style.width = '100%';
      patty.style.transform = 'scaleY(.18) scaleX(1.5)';
      setTimeout(function () { pre.classList.add('done'); }, 220);
      setTimeout(function () { pre.remove(); }, 800);
    }
    SH.add(function () {
      if (done) return;
      var t = clamp((performance.now() - t0) / 1500, 0, 1);   /* hard cap at 1.5s */
      bar.style.width = (t * 100) + '%';
      patty.style.transform = 'scaleY(' + (1 - t * 0.78) + ') scaleX(' + (1 + t * 0.42) + ')';
      if (t >= 1) finish();
    });
    if (document.readyState === 'complete') setTimeout(finish, 420);
    else window.addEventListener('load', function () { setTimeout(finish, 420); });
  });

  /* ---------- hero: split text, velocity squash, heat haze ---------- */
  SH.onBoot(function () {
    var title = document.querySelector('[data-split]');
    if (title) {
      var lines = title.innerHTML.split(/<br\s*\/?>/i);
      title.innerHTML = '';
      var all = [];
      lines.forEach(function (line) {
        var ln = document.createElement('span'); ln.className = 'ln';
        line.trim().split('').forEach(function (ch) {
          var s = document.createElement('span'); s.className = 'ch';
          s.textContent = ch === ' ' ? ' ' : ch;
          ln.appendChild(s); all.push(s);
        });
        title.appendChild(ln);
      });
      all.forEach(function (s, i) { setTimeout(function () { s.classList.add('in'); }, 420 + i * 42); });

      if (!SH.reduced) {
        var sy = 1, sx = 1;
        SH.add(function (dt) {
          var v = clamp(SH.velocity() / -2600, -0.16, 0.16);
          sy = SH.damp(sy, 1 + v, 0.002, dt);
          sx = 1 / Math.sqrt(Math.max(sy, 0.2));
          title.style.transform = 'scale(' + sx.toFixed(4) + ',' + sy.toFixed(4) + ')';
        });
      }
    }

    var haze = document.querySelector('[data-haze]');
    if (haze && !SH.reduced) {
      var ctx = haze.getContext('2d'), hero = document.querySelector('[data-hero]');
      var on = true; SH.inView(hero, 10, function (v) { on = v; });
      SH.add(function (dt, time) {
        if (!on || document.hidden) return;
        SH.fitCanvas(haze, 1.25);
        var w = haze.width, h = haze.height;
        ctx.clearRect(0, 0, w, h);
        var amp = 1 + clamp(Math.abs(SH.velocity()) / 1400, 0, 2.2);
        for (var i = 0; i < 22; i++) {
          var seed = i * 12.9;
          var x = ((SH.hash(seed) + 0.5) * w + Math.sin(time * 0.5 + i) * 26 * amp);
          var rise = ((time * (26 + i % 7 * 9) + i * 160) % (h * 1.25));
          var y = h - rise;
          var r = (34 + (i % 5) * 22) * (0.6 + rise / h);
          var a = 0.055 * amp * (1 - rise / (h * 1.25));
          if (a <= 0) continue;
          var g = ctx.createRadialGradient(x, y, 0, x, y, r);
          g.addColorStop(0, 'rgba(255,190,120,' + a.toFixed(3) + ')');
          g.addColorStop(1, 'rgba(255,120,60,0)');
          ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 6.284); ctx.fill();
        }
      });
    }
  });

  /* ---------- live status everywhere ---------- */
  SH.onBoot(function () {
    if (!SH.hours) return;
    function paint() {
      var s = SH.hours.state();
      document.documentElement.setAttribute('data-status', s.key);
      var pill = document.querySelector('[data-status-text]');
      var line = document.querySelector('[data-status-line]');
      var neon = document.querySelector('[data-neon]');
      var word = document.querySelector('[data-neon-word]');
      var note = document.querySelector('[data-shabbat-note]');

      var short = s.open ? 'Open now' : s.isShabbat ? 'Closed for Shabbat' : 'Closed';
      if (pill) pill.textContent = s.open ? 'Open until ' + SH.hours.fmt(s.closesAt) : short;
      if (line) {
        line.innerHTML = s.open
          ? 'Open now until <b>' + SH.hours.fmt(s.closesAt) + '</b>. Boca Raton.'
          : s.isShabbat
            ? 'Closed for Shabbat. Back <b>' + (s.opensLabel || '') + '</b>.'
            : 'Closed right now. Back <b>' + (s.opensLabel || 'soon') + '</b>.';
      }
      if (neon && word) {
        neon.classList.toggle('lit', !!s.open);
        neon.classList.toggle('shabbat', !!s.isShabbat);
        word.textContent = s.open ? 'OPEN' : s.isShabbat ? 'BACK AFTER SHABBAT' : 'CLOSED';
        if (s.open && !SH.reduced) {
          /* two false starts, then the tube holds */
          var seq = [60,90,150,60,240];
          var t = 0;
          seq.forEach(function (d, i) {
            t += d;
            setTimeout(function () { neon.classList.toggle('lit', i % 2 === 1); }, t);
          });
          setTimeout(function () { neon.classList.add('lit'); }, t + 120);
        }
      }
      if (note) {
        note.textContent = s.isShabbat
          ? s.note + ' Opening ' + (s.opensLabel || '') + ', one hour after Shabbat ends.'
          : 'Friday closed. Saturday opens one hour after Shabbat ends, from real sunset times for Boca Raton.';
      }

      var tb = document.querySelector('[data-hours] tbody');
      if (tb && !tb.childElementCount) {
        SH.hours.week().forEach(function (row) {
          var tr = document.createElement('tr');
          if (row.today) tr.className = 'today';
          if (row.closed) tr.className += ' closed';
          tr.innerHTML = '<td>' + row.name + '</td><td>' + row.value + '</td>';
          tb.appendChild(tr);
        });
      }
    }
    paint();
    setInterval(paint, 60000);
  });

  /* ---------- menu ticket rail ---------- */
  SH.onBoot(function () {
    var rail = document.querySelector('[data-rail]');
    if (!rail) return;
    MENU.forEach(function (item, i) {
      var b = document.createElement('button');
      b.className = 'ticket';
      b.type = 'button';
      b.style.setProperty('--tilt', (SH.hash(i * 3.3) * 2.6).toFixed(2) + 'deg');
      b.setAttribute('data-cursor', 'PULL');
      var tags = item[2].map(function (t) {
        return '<li class="' + (TAGCLASS[t] || '') + '">' + TAGLABEL[t] + '</li>';
      }).join('');
      b.innerHTML = '<h3>' + item[0] + '</h3><p>' + item[1] + '</p><ul class="tags">' + tags + '</ul>';
      b.addEventListener('click', function () {
        window.open('https://order.toasttab.com/online/smashhouseboca', '_blank', 'noopener');
      });
      rail.appendChild(b);
      if (!SH.reduced) {
        var phase = i * 0.7;
        SH.add(function (dt, time) {
          if (b.matches(':hover')) return;
          b.style.transform = 'rotate(' + (Math.sin(time * 0.9 + phase) * 0.75).toFixed(3) + 'deg)';
        });
      }
    });
  });

  /* ---------- press and hold to smash ---------- */
  SH.onBoot(function () {
    var pad = document.querySelector('[data-pad]');
    if (!pad) return;
    var cv = pad.querySelector('[data-smash-canvas]'), ctx = cv.getContext('2d');
    var btn = pad.querySelector('[data-smash-btn]');
    var ring = pad.querySelector('[data-ring]');
    var verdict = document.querySelector('[data-verdict]');
    var hold = 0, holding = false, released = -1, sparks = [];
    var PERFECT = [0.62, 0.78], CIRC = 339;

    function down(e) { e.preventDefault(); holding = true; released = -1; verdict.classList.remove('show'); }
    function up() {
      if (!holding) return;
      holding = false;
      released = hold;
      var good = hold >= PERFECT[0] && hold <= PERFECT[1];
      verdict.textContent = good ? 'PERFECT CRUST' : hold < PERFECT[0] ? 'TOO EARLY — GO DEEPER' : 'HELD TOO LONG';
      verdict.parentElement.style.color = good ? 'var(--yellow)' : 'var(--smash-red)';
      verdict.classList.add('show');
      if (good && navigator.vibrate) navigator.vibrate([12, 30, 8]);
      for (var i = 0; i < 26; i++) {
        sparks.push({ x: 0.5, y: 0.62, vx: (Math.random() - 0.5) * 1.9, vy: -Math.random() * 1.5 - 0.3, life: 1 });
      }
    }
    btn.addEventListener('pointerdown', down);
    window.addEventListener('pointerup', up);
    btn.addEventListener('keydown', function (e) { if (e.key === ' ' || e.key === 'Enter') down(e); });
    window.addEventListener('keyup', function (e) { if (e.key === ' ' || e.key === 'Enter') up(); });

    var on = false; SH.inView(pad, 15, function (v) { on = v; });
    SH.add(function (dt) {
      if (!on || document.hidden) return;
      SH.fitCanvas(cv, 1.5);
      var w = cv.width, h = cv.height;
      if (holding) hold = clamp(hold + dt / 1.4, 0, 1);
      else hold = SH.damp(hold, 0, 0.02, dt);
      ring.style.strokeDashoffset = String(CIRC - CIRC * hold);
      ring.style.stroke = (hold >= PERFECT[0] && hold <= PERFECT[1]) ? 'var(--yellow)' : 'var(--smash-red)';

      ctx.clearRect(0, 0, w, h);
      /* griddle */
      var g = ctx.createLinearGradient(0, 0, 0, h);
      g.addColorStop(0, '#241f19'); g.addColorStop(1, '#0c0a07');
      ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = 'rgba(255,255,255,.035)'; ctx.lineWidth = Math.max(1, w * 0.004);
      for (var i = 0; i < 9; i++) {
        var y = h * (0.16 + i * 0.085);
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
      }
      /* the patty */
      var cx = w * 0.5, cy = h * 0.62;
      var rx = w * (0.15 + hold * 0.13), ry = h * (0.17 - hold * 0.115);
      var heat = hold;
      var pg = ctx.createRadialGradient(cx - rx * 0.3, cy - ry * 0.7, ry * 0.15, cx, cy, rx);
      pg.addColorStop(0, 'rgb(' + Math.round(120 - heat * 52) + ',' + Math.round(66 - heat * 34) + ',' + Math.round(40 - heat * 22) + ')');
      pg.addColorStop(1, 'rgb(' + Math.round(52 - heat * 26) + ',' + Math.round(26 - heat * 13) + ',' + Math.round(16 - heat * 8) + ')');
      ctx.fillStyle = pg;
      ctx.beginPath(); ctx.ellipse(cx, cy, rx, Math.max(ry, h * 0.012), 0, 0, 6.284); ctx.fill();
      /* crust rim */
      ctx.strokeStyle = 'rgba(255,' + Math.round(150 - heat * 80) + ',60,' + (0.15 + heat * 0.5).toFixed(2) + ')';
      ctx.lineWidth = Math.max(1, w * 0.005 * (1 + heat));
      ctx.beginPath(); ctx.ellipse(cx, cy, rx, Math.max(ry, h * 0.012), 0, 0, 6.284); ctx.stroke();
      /* spatula */
      var sy2 = cy - Math.max(ry, h * 0.012) - h * (0.34 - hold * 0.30);
      ctx.fillStyle = '#b9c1c8';
      ctx.fillRect(cx - w * 0.20, sy2, w * 0.40, h * 0.035);
      ctx.fillStyle = '#2a221c';
      ctx.fillRect(cx + w * 0.18, sy2 - h * 0.055, w * 0.055, h * 0.09);
      /* grease sparks */
      for (var s = sparks.length - 1; s >= 0; s--) {
        var sp = sparks[s];
        sp.x += sp.vx * dt * 0.5; sp.y += sp.vy * dt * 0.5; sp.vy += dt * 1.8; sp.life -= dt * 1.5;
        if (sp.life <= 0) { sparks.splice(s, 1); continue; }
        ctx.fillStyle = 'rgba(255,' + Math.round(190 * sp.life) + ',90,' + sp.life.toFixed(2) + ')';
        ctx.beginPath(); ctx.arc(sp.x * w, sp.y * h, w * 0.006 * sp.life, 0, 6.284); ctx.fill();
      }
    });
  });

  /* ---------- footer griddle marks ---------- */
  SH.onBoot(function () {
    var cv = document.querySelector('[data-griddle]');
    if (!cv || SH.reduced) return;
    var ctx = cv.getContext('2d'), pts = [], on = false;
    SH.inView(cv.parentElement, 15, function (v) { on = v; });
    function push(e) {
      var r = cv.getBoundingClientRect();
      pts.push({ x: (e.clientX - r.left) / r.width, y: (e.clientY - r.top) / r.height, life: 1 });
      if (pts.length > 90) pts.shift();
    }
    cv.parentElement.addEventListener('pointermove', push, { passive: true });
    SH.add(function (dt) {
      if (!on || document.hidden) return;
      SH.fitCanvas(cv, 1.25);
      var w = cv.width, h = cv.height;
      ctx.clearRect(0, 0, w, h);
      ctx.globalCompositeOperation = 'lighter';
      for (var i = pts.length - 1; i >= 0; i--) {
        var p = pts[i];
        p.life -= dt * 0.42;
        if (p.life <= 0) { pts.splice(i, 1); continue; }
        var r = w * 0.05 * (1.4 - p.life * 0.5);
        var g = ctx.createRadialGradient(p.x * w, p.y * h, 0, p.x * w, p.y * h, r);
        g.addColorStop(0, 'rgba(255,' + Math.round(120 + 110 * p.life) + ',30,' + (0.5 * p.life).toFixed(3) + ')');
        g.addColorStop(0.55, 'rgba(229,17,68,' + (0.16 * p.life).toFixed(3) + ')');
        g.addColorStop(1, 'rgba(64,28,16,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x * w, p.y * h, r, 0, 6.284); ctx.fill();
      }
      ctx.globalCompositeOperation = 'source-over';
    });
  });

  /* ---------- header hide-on-scroll, cursor, order hand-off ---------- */
  SH.onBoot(function () {
    var header = document.querySelector('.site-header');
    var lastY = window.scrollY, hidden = false;
    window.addEventListener('scroll', function () {
      var y = window.scrollY;
      if (y < 240) { hidden = false; }
      else if (y > lastY + 12) { hidden = true; }
      else if (y < lastY - 12) { hidden = false; }
      if (Math.abs(y - lastY) > 12 || y < 240) lastY = y;
      if (header) header.classList.toggle('hidden', hidden);
    }, { passive: true });

    /* order clicks navigate FIRST, the flourish plays on the page being left */
    document.querySelectorAll('[data-order]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        window.open(a.href, '_blank', 'noopener');
        if (SH.reduced) return;
        a.animate([{ transform: 'scale(1)' }, { transform: 'scale(.93)' }, { transform: 'scale(1)' }],
          { duration: 320, easing: 'cubic-bezier(.2,1.5,.4,1)' });
      });
    });

    if (SH.coarse) return;
    var cur = document.querySelector('[data-cursor-root]');
    var label = cur.querySelector('[data-cursor-text]');
    var x = innerWidth / 2, y = innerHeight / 2, tx = x, ty = y;
    window.addEventListener('pointermove', function (e) {
      tx = e.clientX; ty = e.clientY; cur.style.opacity = '1';
      var hit = e.target.closest('[data-cursor], a, button');
      var txt = hit && hit.getAttribute && hit.getAttribute('data-cursor');
      if (hit && (txt || hit.tagName === 'A' || hit.tagName === 'BUTTON')) {
        cur.classList.add('wide');
        label.textContent = txt || (hit.closest('[data-order]') ? 'ORDER' : 'OPEN');
      } else { cur.classList.remove('wide'); label.textContent = ''; }
    }, { passive: true });
    SH.add(function (dt) {
      x = SH.damp(x, tx, 0.0001, dt); y = SH.damp(y, ty, 0.0001, dt);
      cur.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)';
    });
  });
})(SH);
