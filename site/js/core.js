/* Smash House — core: one rAF loop, damped scroll progress, matrix math, small utils.
   No dependencies. Everything that animates is a pure function of a progress value. */
var SH = (function () {
  'use strict';

  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var coarse = matchMedia('(pointer: coarse)').matches;
  var isMobile = matchMedia('(max-width: 800px)').matches;
  var dprCap = isMobile ? 1.5 : 2;

  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  var smooth = function (t) { return t * t * (3 - 2 * t); };
  var inv = function (v, a, b) { return clamp((v - a) / (b - a), 0, 1); };
  function easeBackOut(t, s) { s = s === undefined ? 1.6 : s; t -= 1; return t * t * ((s + 1) * t + s) + 1; }
  function easeExpoIn(t) { return t <= 0 ? 0 : Math.pow(2, 10 * (t - 1)); }
  function easeOut3(t) { return 1 - Math.pow(1 - t, 3); }
  /* frame-rate independent damping: never a fixed 0.1 per frame */
  function damp(cur, target, rate, dt) { return lerp(cur, target, 1 - Math.pow(rate, dt)); }
  function hash(n) { var s = Math.sin(n * 127.1) * 43758.5453; return (s - Math.floor(s)) - 0.5; }

  /* ---- the single animation loop ---- */
  var tasks = [];
  var last = 0, running = false;
  function add(fn) { tasks.push(fn); return fn; }
  function remove(fn) { var i = tasks.indexOf(fn); if (i > -1) tasks.splice(i, 1); }
  function frame(now) {
    var dt = last ? Math.min((now - last) / 1000, 0.1) : 0.016;
    last = now;
    for (var i = 0; i < tasks.length; i++) tasks[i](dt, now / 1000);
    requestAnimationFrame(frame);
  }
  function start() { if (!running) { running = true; requestAnimationFrame(frame); } }

  /* ---- scroll: native scrolling, damped virtual position. No scroll-jacking. ---- */
  var scrollY = window.scrollY || 0, scrollTarget = scrollY, velocity = 0;
  window.addEventListener('scroll', function () { scrollTarget = window.scrollY; }, { passive: true });
  add(function (dt) {
    var prev = scrollY;
    scrollY = reduced ? scrollTarget : damp(scrollY, scrollTarget, 0.0008, dt);
    if (Math.abs(scrollTarget - scrollY) < 0.05) scrollY = scrollTarget;
    velocity = damp(velocity, (scrollY - prev) / Math.max(dt, 0.0001), 0.002, dt);
  });

  /* progress of an element through a pinned range, read from cached geometry */
  function tracker(el) {
    var top = 0, len = 1;
    function measure() {
      var r = el.getBoundingClientRect();
      top = r.top + window.scrollY;
      len = Math.max(1, el.offsetHeight - window.innerHeight);
    }
    measure();
    window.addEventListener('resize', debounce(measure, 200), { passive: true });
    window.addEventListener('load', measure);
    return { progress: function () { return clamp((window.scrollY - top) / len, 0, 1); },
             measure: measure, debug: function () { return { top: top, len: len }; } };
  }

  function debounce(fn, wait) {
    var t = 0;
    return function () { var a = arguments, self = this; clearTimeout(t); t = setTimeout(function () { fn.apply(self, a); }, wait); };
  }

  function inView(el, margin, onChange) {
    var io = new IntersectionObserver(function (e) { onChange(e[0].isIntersecting); },
      { rootMargin: (margin || 20) + '%' });
    io.observe(el);
    return io;
  }

  /* sized canvas with a capped backing store */
  function fitCanvas(cv, cap) {
    var d = Math.min(window.devicePixelRatio || 1, cap || dprCap);
    var w = cv.clientWidth, h = cv.clientHeight;
    if (!w || !h) return false;
    var nw = Math.round(w * d), nh = Math.round(h * d);
    if (cv.width !== nw || cv.height !== nh) { cv.width = nw; cv.height = nh; return true; }
    return false;
  }

  /* ---- mat4 / vec3, column-major, WebGL layout ---- */
  var M = {
    ident: function (o) { o.set([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]); return o; },
    mul: function (o, a, b) {
      for (var c = 0; c < 4; c++) for (var r = 0; r < 4; r++) {
        o[c * 4 + r] = a[r] * b[c * 4] + a[4 + r] * b[c * 4 + 1] + a[8 + r] * b[c * 4 + 2] + a[12 + r] * b[c * 4 + 3];
      }
      return o;
    },
    perspective: function (o, fovy, aspect, near, far) {
      var f = 1 / Math.tan(fovy / 2), nf = 1 / (near - far);
      o.set([f / aspect,0,0,0, 0,f,0,0, 0,0,(far + near) * nf,-1, 0,0,2 * far * near * nf,0]);
      return o;
    },
    lookAt: function (o, eye, center, up) {
      var zx = eye[0] - center[0], zy = eye[1] - center[1], zz = eye[2] - center[2];
      var zl = Math.hypot(zx, zy, zz) || 1; zx /= zl; zy /= zl; zz /= zl;
      var xx = up[1] * zz - up[2] * zy, xy = up[2] * zx - up[0] * zz, xz = up[0] * zy - up[1] * zx;
      var xl = Math.hypot(xx, xy, xz) || 1; xx /= xl; xy /= xl; xz /= xl;
      var yx = zy * xz - zz * xy, yy = zz * xx - zx * xz, yz = zx * xy - zy * xx;
      o.set([xx,yx,zx,0, xy,yy,zy,0, xz,yz,zz,0,
             -(xx * eye[0] + xy * eye[1] + xz * eye[2]),
             -(yx * eye[0] + yy * eye[1] + yz * eye[2]),
             -(zx * eye[0] + zy * eye[1] + zz * eye[2]), 1]);
      return o;
    },
    compose: function (o, pos, rot, scale) {
      /* rot = [rx, ry, rz] applied X then Y then Z; scale = [sx, sy, sz] */
      var cx = Math.cos(rot[0]), sx = Math.sin(rot[0]);
      var cy = Math.cos(rot[1]), sy = Math.sin(rot[1]);
      var cz = Math.cos(rot[2]), sz = Math.sin(rot[2]);
      var m00 = cy * cz, m01 = -cy * sz, m02 = sy;
      var m10 = sx * sy * cz + cx * sz, m11 = -sx * sy * sz + cx * cz, m12 = -sx * cy;
      var m20 = -cx * sy * cz + sx * sz, m21 = cx * sy * sz + sx * cz, m22 = cx * cy;
      o.set([m00 * scale[0], m10 * scale[0], m20 * scale[0], 0,
             m01 * scale[1], m11 * scale[1], m21 * scale[1], 0,
             m02 * scale[2], m12 * scale[2], m22 * scale[2], 0,
             pos[0], pos[1], pos[2], 1]);
      return o;
    },
    /* normal matrix = inverse-transpose of the upper 3x3, written into a mat3 */
    normalFrom: function (o, m) {
      var a = m[0], b = m[1], c = m[2], d = m[4], e = m[5], f = m[6], g = m[8], h = m[9], i = m[10];
      var A = e * i - f * h, B = -(d * i - f * g), C = d * h - e * g;
      var det = a * A + b * B + c * C;
      if (!det) { o.set([1,0,0, 0,1,0, 0,0,1]); return o; }
      det = 1 / det;
      o[0] = A * det; o[1] = B * det; o[2] = C * det;
      o[3] = -(b * i - c * h) * det; o[4] = (a * i - c * g) * det; o[5] = -(a * h - b * g) * det;
      o[6] = (b * f - c * e) * det; o[7] = -(a * f - c * d) * det; o[8] = (a * e - b * d) * det;
      return o;
    },
    /* world point -> normalised viewport coords, origin top-left */
    project: function (out, p, viewProj) {
      var x = p[0], y = p[1], z = p[2];
      var cx = viewProj[0]*x + viewProj[4]*y + viewProj[8]*z + viewProj[12];
      var cy = viewProj[1]*x + viewProj[5]*y + viewProj[9]*z + viewProj[13];
      var cw = viewProj[3]*x + viewProj[7]*y + viewProj[11]*z + viewProj[15];
      if (cw === 0) cw = 1e-6;
      out[0] = (cx / cw) * 0.5 + 0.5;
      out[1] = 0.5 - (cy / cw) * 0.5;
      out[2] = cw;
      return out;
    }
  };

  var boots = [];
  function onBoot(fn) { boots.push(fn); }
  function boot() {
    start();
    for (var i = 0; i < boots.length; i++) {
      try { boots[i](); } catch (e) { console.error('[SH] module failed:', e); }
    }
  }

  return {
    reduced: reduced, coarse: coarse, isMobile: isMobile, dprCap: dprCap,
    clamp: clamp, lerp: lerp, smooth: smooth, inv: inv, damp: damp, hash: hash,
    easeBackOut: easeBackOut, easeExpoIn: easeExpoIn, easeOut3: easeOut3,
    add: add, remove: remove, tracker: tracker, debounce: debounce, inView: inView,
    fitCanvas: fitCanvas, M: M, onBoot: onBoot, boot: boot,
    scroll: function () { return scrollY; },
    velocity: function () { return velocity; }
  };
})();
