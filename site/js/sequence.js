/* Smash House — THE TOSS, THE SMASH, THE CUT.
   Hand-written WebGL. Every value is a pure function of scroll progress, so scrubbing
   backwards is exact: no `once`, no accumulated state, no time-dependent integration. */
(function (SH) {
  'use strict';
  var M = SH.M, clamp = SH.clamp, inv = SH.inv, lerp = SH.lerp;

  var BEATS = {
    toss:[0,.11], bullet:[.11,.21], closeup:[.21,.31], explode:[.31,.50],
    turn:[.50,.59], smash:[.59,.69], cut:[.69,.86], slice:[.86,1]
  };
  var COPY = [
    [0,   'THE TOSS',      'Five off the griddle, each on its own arc.'],
    [.11, 'BULLET TIME',   'Time stops at the peak. The camera keeps going.'],
    [.21, 'THE CLOSE-UP',  'The Loaded Smashed. Double patty, beef bacon, caramelized onion.'],
    [.31, 'THE EXPLODE',   'Nine layers. Every one of them named.'],
    [.50, 'THE HALF TURN', 'All the way around, still readable.'],
    [.59, 'THE SMASH',     'Back together. You felt that.'],
    [.69, 'THE CUT',       'The only shot that matters.'],
    [.86, 'THE HAND-OFF',  'Straight to the order.']
  ];
  /* bottom to top — the real Loaded Smashed build [TO CONFIRM exact order with the owner] */
  var LAYERS = [
    { n:'TOASTED BASE',        r:1.00, h:.20, c:[.46,.26,.12], rough:.62, ss:.22, irr:.045 },
    { n:'SMASHED PATTY',       r:1.07, h:.15, c:[.105,.048,.030], rough:.46, ss:.03, irr:.085 },
    { n:'PLANT-BASED CHEESE',  r:1.03, h:.05, c:[.78,.52,.15], rough:.38, ss:.10, irr:.06 },
    { n:'SMASHED PATTY',       r:1.07, h:.15, c:[.105,.048,.030], rough:.46, ss:.03, irr:.085 },
    { n:'PLANT-BASED CHEESE',  r:1.03, h:.05, c:[.78,.52,.15], rough:.38, ss:.10, irr:.06 },
    { n:'BEEF BACON',          r:.95,  h:.07, c:[.33,.048,.030], rough:.34, ss:.04, irr:.09 },
    { n:'CARAMELIZED ONION',   r:.92,  h:.08, c:[.42,.21,.05], rough:.42, ss:.26, irr:.10 },
    { n:'CHEF SAUCE',          r:.94,  h:.04, c:[.60,.23,.06], rough:.18, ss:.06, irr:.07 },
    { n:'SESAME CROWN',        r:1.00, h:.40, c:[.50,.28,.12], rough:.58, ss:.22, irr:.04, dome:.22 }
  ];
  var STACK_H = LAYERS.reduce(function (s, L) { return s + L.h; }, 0);
  var CENTER_I = (LAYERS.length - 1) / 2;
  var GAP = 0.26;
  var INTERIOR = [[.66,.52,.32],[.36,.16,.095],[.76,.52,.16],[.36,.16,.095],[.76,.52,.16],
                  [.36,.075,.05],[.52,.30,.09],[.58,.24,.06],[.68,.55,.35]];

  /* distance / target / rise per beat — distance does the framing, the lens never changes */
  /* [progress, distance, target height, camera rise above target, orbit radians] */
  var CAM = [
    [0,   7.6, 0.10, 0.30, 0.00],
    [.11, 7.4, 2.30, 0.10, 0.00],
    [.21, 7.2, 2.35, 0.05, 1.55],
    [.31, 3.1, 0.00, 0.05, 1.25],
    [.50, 3.1, 0.00, 0.22, 0.50],
    [.59, 3.1, 0.00, 0.22, 0.50],
    [.69, 3.6, 0.00, 0.10, 0.40],
    [.86, 3.6, 0.00, 0.06, 0.30],
    [1,   3.6, 0.00, 0.06, 0.30]
  ];
  function camAt(p) {
    for (var i = 0; i < CAM.length - 1; i++) {
      var a = CAM[i], b = CAM[i + 1];
      if (p >= a[0] && p <= b[0]) {
        var t = b[0] === a[0] ? 0 : SH.smooth((p - a[0]) / (b[0] - a[0]));
        return [lerp(a[1],b[1],t), lerp(a[2],b[2],t), lerp(a[3],b[3],t), lerp(a[4],b[4],t)];
      }
    }
    var L = CAM[CAM.length - 1];
    return [L[1], L[2], L[3], L[4]];
  }

  var VS = [
    'attribute vec3 aPos; attribute vec3 aNormal;',
    'uniform mat4 uModel, uViewProj; uniform mat3 uNormalMat;',
    'varying vec3 vWorld, vNormal; varying float vLocalX; varying vec3 vLocal;',
    'void main(){',
    '  vec4 w = uModel * vec4(aPos,1.0);',
    '  vWorld = w.xyz; vLocal = aPos; vLocalX = aPos.x;',
    '  vNormal = normalize(uNormalMat * aNormal);',
    '  gl_Position = uViewProj * w;',
    '}'
  ].join('\n');

  var FS = [
    'precision highp float;',
    'varying vec3 vWorld, vNormal; varying float vLocalX; varying vec3 vLocal;',
    'uniform vec3 uColor, uCamPos; uniform float uRough, uSS, uClipSign, uSeed, uNoiseAmt;',
    'float h31(vec3 p){ return fract(sin(dot(p, vec3(127.1,311.7,74.7))) * 43758.5453); }',
    'float vn(vec3 p){',
    '  vec3 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f);',
    '  float a = mix(mix(mix(h31(i),h31(i+vec3(1,0,0)),f.x), mix(h31(i+vec3(0,1,0)),h31(i+vec3(1,1,0)),f.x), f.y),',
    '                mix(mix(h31(i+vec3(0,0,1)),h31(i+vec3(1,0,1)),f.x), mix(h31(i+vec3(0,1,1)),h31(i+vec3(1,1,1)),f.x), f.y), f.z);',
    '  return a;',
    '}',
    'float fbm(vec3 p){ return vn(p)*0.62 + vn(p*2.7)*0.26 + vn(p*7.1)*0.12; }',
    'vec3 tonemap(vec3 x){',
    '  x *= 0.9; return clamp((x*(2.51*x+0.03))/(x*(2.43*x+0.59)+0.14), 0.0, 1.0);',
    '}',
    'void main(){',
    '  if (uClipSign != 0.0 && uClipSign * vLocalX < 0.0) discard;',
    '  vec3 sp = vLocal * 9.0 + uSeed;',
    '  float n = fbm(sp);',
    /* cheap bump: perturb the normal along the noise gradient */
    '  float e = 0.09;',
    '  vec3 g = vec3(fbm(sp+vec3(e,0,0))-n, fbm(sp+vec3(0,e,0))-n, fbm(sp+vec3(0,0,e))-n);',
    '  vec3 N = normalize(vNormal - g * uNoiseAmt * 16.0);',
    '  vec3 V = normalize(uCamPos - vWorld);',
    '  vec3 albedo = uColor * (0.86 + n * 0.30);',
    '  float rough = clamp(uRough + (n - 0.5) * 0.30, 0.06, 0.95);',
    '  float shin = mix(220.0, 14.0, rough);',
    '  vec3 kL = normalize(vec3(-0.45, 0.85, 0.60));',   /* key: behind and above */
    '  vec3 fL = normalize(vec3( 0.62, 0.22,-0.70));',   /* fill: camera side, dim */
    '  vec3 rL = normalize(vec3( 0.40, 0.55, 0.72));',   /* brand rim, yellow */
    '  vec3 kC = vec3(1.00,0.95,0.88) * 1.30;',
    '  vec3 fC = vec3(1.00,0.97,0.94) * 0.20;',
    '  vec3 rC = vec3(1.00,0.92,0.08) * 0.30;',
    '  vec3 kick = vec3(0.90,0.07,0.27) * 0.14;',
    '  vec3 col = vec3(0.0);',
    '  col += albedo * kC * max(dot(N,kL), 0.0);',
    '  col += albedo * fC * max(dot(N,fL), 0.0);',
    '  col += albedo * kick * max(dot(N, normalize(vec3(0.95,-0.05,0.10))), 0.0);',
    /* wrapped diffuse stands in for subsurface on bun, onion and cheese */
    '  col += albedo * kC * uSS * max((dot(N,kL) + 0.75) / 1.75, 0.0) * 0.30;',
    '  float fres = pow(1.0 - max(dot(N,V), 0.0), 4.0);',
    '  col += rC * fres * (0.30 + 0.70 * max(dot(N,rL), 0.0));',
    '  vec3 Hk = normalize(kL + V);',
    '  col += kC * pow(max(dot(N,Hk),0.0), shin) * (0.20 - rough * 0.15);',
    '  col += albedo * vec3(0.038,0.034,0.030);',
    '  col *= mix(0.42, 1.0, clamp(N.y * 0.5 + 0.62, 0.0, 1.0));',
    '  gl_FragColor = vec4(pow(tonemap(col), vec3(1.0/2.2)), 1.0);',
    '}'
  ].join('\n');

  function shader(gl, type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }
  function program(gl, vs, fs) {
    var p = gl.createProgram();
    gl.attachShader(p, shader(gl, gl.VERTEX_SHADER, vs));
    gl.attachShader(p, shader(gl, gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    return p;
  }

  /* ---- geometry ---- */
  function pushTri(P, N, a, b, c, na, nb, nc) {
    P.push(a[0],a[1],a[2], b[0],b[1],b[2], c[0],c[1],c[2]);
    N.push(na[0],na[1],na[2], nb[0],nb[1],nb[2], nc[0],nc[1],nc[2]);
  }
  function cylinder(r, h, irr, seed, dome) {
    var SEG = 64, P = [], N = [], i, th, th2;
    var half = h / 2;
    function rad(t) {
      return r * (1 + irr * (Math.sin(t * 3 + seed) * 0.5 + Math.sin(t * 5 - seed * 1.7) * 0.32
                           + Math.sin(t * 9 + seed * 2.3) * 0.18));
    }
    function domeY(t, rr) { return dome ? dome * Math.sqrt(Math.max(0, 1 - Math.pow(rr / r, 2))) : 0; }
    for (i = 0; i < SEG; i++) {
      th = i / SEG * Math.PI * 2; th2 = (i + 1) / SEG * Math.PI * 2;
      var r1 = rad(th), r2 = rad(th2);
      var x1 = Math.cos(th) * r1, z1 = Math.sin(th) * r1;
      var x2 = Math.cos(th2) * r2, z2 = Math.sin(th2) * r2;
      var n1 = [Math.cos(th), 0.14, Math.sin(th)], n2 = [Math.cos(th2), 0.14, Math.sin(th2)];
      var t1 = half + domeY(th, r1), t2 = half + domeY(th2, r2);
      /* side */
      pushTri(P, N, [x1,-half,z1], [x2,-half,z2], [x2,t2,z2], n1, n2, n2);
      pushTri(P, N, [x1,-half,z1], [x2,t2,z2], [x1,t1,z1], n1, n2, n1);
      /* top cap in rings, so a domed crown is round instead of conical */
      var RINGS = dome ? 7 : 1;
      for (var ri = 0; ri < RINGS; ri++) {
        var f0 = ri / RINGS, f1 = (ri + 1) / RINGS;
        var ra0 = 1 - f0, ra1 = 1 - f1;
        function capPt(t, rr, k) {
          var rad2 = rad(t) * k;
          return [Math.cos(t) * rad2, half + (dome ? dome * Math.sqrt(Math.max(0, 1 - k * k)) : 0), Math.sin(t) * rad2];
        }
        function capN(t, k) {
          if (!dome) return [0, 1, 0];
          var slope = k < 0.999 ? (dome * k / Math.sqrt(Math.max(1e-4, 1 - k * k))) / r : 4;
          var n = [Math.cos(t) * slope, 1, Math.sin(t) * slope];
          var l = Math.hypot(n[0], n[1], n[2]);
          return [n[0]/l, n[1]/l, n[2]/l];
        }
        var a0 = capPt(th, r1, ra0), b0 = capPt(th2, r2, ra0);
        var a1 = capPt(th, r1, ra1), b1 = capPt(th2, r2, ra1);
        pushTri(P, N, a0, b0, b1, capN(th, ra0), capN(th2, ra0), capN(th2, ra1));
        pushTri(P, N, a0, b1, a1, capN(th, ra0), capN(th2, ra1), capN(th, ra1));
      }
      /* bottom cap */
      pushTri(P, N, [x2,-half,z2], [x1,-half,z1], [0,-half,0], [0,-1,0], [0,-1,0], [0,-1,0]);
    }
    return { pos: new Float32Array(P), nrm: new Float32Array(N), count: P.length / 3 };
  }
  function box(w, h, d) {
    var P = [], N = [], x = w/2, y = h/2, z = d/2;
    var f = [
      [[-x,-y,z],[x,-y,z],[x,y,z],[-x,y,z],[0,0,1]],
      [[x,-y,-z],[-x,-y,-z],[-x,y,-z],[x,y,-z],[0,0,-1]],
      [[x,-y,z],[x,-y,-z],[x,y,-z],[x,y,z],[1,0,0]],
      [[-x,-y,-z],[-x,-y,z],[-x,y,z],[-x,y,-z],[-1,0,0]],
      [[-x,y,z],[x,y,z],[x,y,-z],[-x,y,-z],[0,1,0]],
      [[-x,-y,-z],[x,-y,-z],[x,-y,z],[-x,-y,z],[0,-1,0]]
    ];
    for (var i = 0; i < 6; i++) {
      var q = f[i], n = q[4];
      pushTri(P, N, q[0], q[1], q[2], n, n, n);
      pushTri(P, N, q[0], q[2], q[3], n, n, n);
    }
    return { pos: new Float32Array(P), nrm: new Float32Array(N), count: P.length / 3 };
  }
  function sphere(r, seg) {
    var P = [], N = [], i, j;
    for (i = 0; i < seg; i++) for (j = 0; j < seg; j++) {
      var u0 = i/seg*Math.PI*2, u1 = (i+1)/seg*Math.PI*2;
      var v0 = j/seg*Math.PI, v1 = (j+1)/seg*Math.PI;
      function pt(u,v){ return [Math.sin(v)*Math.cos(u), Math.cos(v), Math.sin(v)*Math.sin(u)]; }
      var a = pt(u0,v0), b = pt(u1,v0), c = pt(u1,v1), d = pt(u0,v1);
      function s(p){ return [p[0]*r*1.35, p[1]*r*0.5, p[2]*r]; }
      pushTri(P, N, s(a), s(b), s(c), a, b, c);
      pushTri(P, N, s(a), s(c), s(d), a, c, d);
    }
    return { pos: new Float32Array(P), nrm: new Float32Array(N), count: P.length / 3 };
  }
  function quadYZ(hz, hy, dir) {
    var P = [], N = [], n = [dir, 0, 0];
    if (dir > 0) {
      pushTri(P, N, [0,-hy,-hz], [0,-hy,hz], [0,hy,hz], n, n, n);
      pushTri(P, N, [0,-hy,-hz], [0,hy,hz], [0,hy,-hz], n, n, n);
    } else {
      pushTri(P, N, [0,-hy,hz], [0,-hy,-hz], [0,hy,-hz], n, n, n);
      pushTri(P, N, [0,-hy,hz], [0,hy,-hz], [0,hy,hz], n, n, n);
    }
    return { pos: new Float32Array(P), nrm: new Float32Array(N), count: P.length / 3 };
  }

  function upload(gl, g) {
    g.pb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, g.pb); gl.bufferData(gl.ARRAY_BUFFER, g.pos, gl.STATIC_DRAW);
    g.nb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, g.nb); gl.bufferData(gl.ARRAY_BUFFER, g.nrm, gl.STATIC_DRAW);
    return g;
  }

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

    var gl = canvas.getContext('webgl', { antialias: true, alpha: false, powerPreference: 'high-performance' })
          || canvas.getContext('experimental-webgl');
    if (!gl) { section.setAttribute('data-nogl', ''); document.documentElement.setAttribute('data-nogl',''); return; }

    var prog = program(gl, VS, FS);
    var loc = {
      aPos: gl.getAttribLocation(prog, 'aPos'), aNormal: gl.getAttribLocation(prog, 'aNormal'),
      uModel: gl.getUniformLocation(prog, 'uModel'), uViewProj: gl.getUniformLocation(prog, 'uViewProj'),
      uNormalMat: gl.getUniformLocation(prog, 'uNormalMat'), uColor: gl.getUniformLocation(prog, 'uColor'),
      uCamPos: gl.getUniformLocation(prog, 'uCamPos'), uRough: gl.getUniformLocation(prog, 'uRough'),
      uSS: gl.getUniformLocation(prog, 'uSS'), uClipSign: gl.getUniformLocation(prog, 'uClipSign'),
      uSeed: gl.getUniformLocation(prog, 'uSeed'), uNoiseAmt: gl.getUniformLocation(prog, 'uNoiseAmt')
    };

    var geo = LAYERS.map(function (L, i) { return upload(gl, cylinder(L.r, L.h, L.irr, i * 2.3 + 1, L.dome)); });
    var capsR = LAYERS.map(function (L) { return upload(gl, quadYZ(L.r * 1.02, L.h / 2, 1)); });
    var capsL = LAYERS.map(function (L) { return upload(gl, quadYZ(L.r * 1.02, L.h / 2, -1)); });
    var knifeBlade = upload(gl, box(0.026, 0.62, 2.5));
    var knifeHandle = upload(gl, box(0.10, 0.20, 0.95));
    var seed = upload(gl, sphere(0.027, 7));

    /* sesame scattered on the crown, with a deliberate bald patch */
    var SESAME = [];
    (function () {
      var crown = LAYERS[LAYERS.length - 1], base = STACK_H - crown.h / 2;
      for (var i = 0; i < 150 && SESAME.length < 46; i++) {
        var a = SH.hash(i * 3.7) * Math.PI * 4 + i;
        var rr = Math.sqrt(Math.abs(SH.hash(i * 1.9)) * 2) * 0.86;
        if (rr > 0.34 && rr < 0.5) continue;
        if (Math.abs(SH.hash(i * 5.1)) > 0.21) continue;
        var rad = rr * crown.r;
        SESAME.push({
          x: Math.cos(a) * rad, z: Math.sin(a) * rad,
          y: base + crown.h / 2 + (crown.dome || 0) * Math.sqrt(Math.max(0, 1 - rr * rr)) - 0.012,
          ry: SH.hash(i * 7.3) * 6.28, rx: SH.hash(i * 2.1) * 0.7, s: 0.85 + Math.abs(SH.hash(i * 4.4))
        });
      }
    })();

    var TOSS = [0,1,2,3,4].map(function (i) {
      return { v0: 7.6 + i * 0.38, phase: i * 0.06, dx: (i - 2) * 0.52,
               dz: (i % 2 ? 0.40 : -0.40), ax: [SH.hash(i+1), 1, SH.hash(i+7)], w0: 5.2 + i * 0.9 };
    });
    var HERO = 2, G = 6.2;

    var mModel = new Float32Array(16), mView = new Float32Array(16), mProj = new Float32Array(16);
    var mVP = new Float32Array(16), mNorm = new Float32Array(9);
    var eye = [0,0,0], target = [0,0,0], up = [0,1,0], pr = [0,0,0];

    /* one DOM label per layer */
    var labels = LAYERS.map(function (L) {
      var s = document.createElement('span'); s.textContent = L.n; labelWrap.appendChild(s); return s;
    });

    var track = SH.tracker(section);
    var visible = false;
    SH.inView(stage, 25, function (v) { visible = v; });
    var shown = -1, pSmooth = 0;

    function drawGeo(g, model, color, rough, ss, clipSign, seedv, noiseAmt) {
      gl.uniformMatrix4fv(loc.uModel, false, model);
      M.normalFrom(mNorm, model);
      gl.uniformMatrix3fv(loc.uNormalMat, false, mNorm);
      gl.uniform3fv(loc.uColor, color);
      gl.uniform1f(loc.uRough, rough);
      gl.uniform1f(loc.uSS, ss);
      gl.uniform1f(loc.uClipSign, clipSign || 0);
      gl.uniform1f(loc.uSeed, seedv || 0);
      gl.uniform1f(loc.uNoiseAmt, noiseAmt === undefined ? 0.07 : noiseAmt);
      gl.bindBuffer(gl.ARRAY_BUFFER, g.pb);
      gl.vertexAttribPointer(loc.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, g.nb);
      gl.vertexAttribPointer(loc.aNormal, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, g.count);
    }

    function render(p) {
      var W = canvas.width, H = canvas.height;
      gl.viewport(0, 0, W, H);
      gl.clearColor(0.0745, 0.0667, 0.047, 1);
      gl.enable(gl.DEPTH_TEST);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.useProgram(prog);
      gl.enableVertexAttribArray(loc.aPos);
      gl.enableVertexAttribArray(loc.aNormal);

      var tToss = inv(p, BEATS.toss[0], BEATS.toss[1]);
      var settle = inv(p, BEATS.closeup[0], BEATS.closeup[1]);
      var eRaw = inv(p, BEATS.explode[0], BEATS.explode[1]);
      var turn = inv(p, BEATS.turn[0], BEATS.turn[1]);
      var smashT = inv(p, BEATS.smash[0], BEATS.smash[1]);
      var antic = clamp(smashT / 0.30, 0, 1);
      var impact = SH.easeExpoIn(clamp((smashT - 0.30) / 0.20, 0, 1));
      var recoil = clamp((smashT - 0.50) / 0.50, 0, 1);
      var shake = impact * (1 - recoil);
      var tCut = inv(p, BEATS.cut[0], BEATS.cut[1]);
      var cutting = clamp((tCut - 0.12) / 0.34, 0, 1);
      var opening = clamp((tCut - 0.52) / 0.48, 0, 1);
      var split = cutting > 0.5;

      /* the hero's height feeds the camera, so solve it before the camera */
      var heroD = TOSS[HERO], heroApexT = heroD.v0 / G;
      var heroTT = Math.max(0, (tToss - heroD.phase) / (1 - heroD.phase)) * heroApexT;
      var heroPosY = (-3.2 + heroD.v0 * heroTT - 0.5 * G * heroTT * heroTT) * (1 - settle);

      /* ---------- camera: one continuous take ---------- */
      var c = camAt(p);
      var orbit = c[3];
      /* the explode and the cut change how big the subject is, so the distance is derived
         from the real extent rather than guessed in a keyframe */
      var spreadNow = SH.easeBackOut(eRaw) * (1 - impact);
      var halfExtent = STACK_H / 2 + CENTER_I * GAP * spreadNow + 0.28;
      var openExtent = 1.0 + opening * 0.42;
      var needV = halfExtent * 2 * 1.22;
      var needH = openExtent * 2 * 1.22;
      var aspect = W / H;
      var fitV = needV / (2 * Math.tan(0.31));
      var fitH = needH / (2 * Math.tan(0.31) * aspect);
      var dist = Math.max(c[0], fitV, fitH);
      var tgtY = c[1];
      eye[0] = Math.sin(orbit) * dist + SH.hash(p * 900) * 0.10 * shake;
      eye[1] = tgtY + c[2] + SH.hash(p * 770) * 0.08 * shake;
      eye[2] = Math.cos(orbit) * dist;
      target[0] = 0; target[1] = tgtY; target[2] = 0;
      M.perspective(mProj, 0.62, W / H, 0.05, 120);
      M.lookAt(mView, eye, target, up);
      M.mul(mVP, mProj, mView);
      window.__cam = { dist: +dist.toFixed(2), orbit: +orbit.toFixed(2), tgtY: +tgtY.toFixed(2),
        eye: eye.map(function(v){return +v.toFixed(2)}), heroY: +heroPosY.toFixed(2), fitV: +fitV.toFixed(2), fitH: +fitH.toFixed(2) };
      gl.uniformMatrix4fv(loc.uViewProj, false, mVP);
      gl.uniform3fv(loc.uCamPos, eye);

      /* ---------- beats 1-3: toss, freeze, settle ---------- */
      var heroPos = [0,0,0], heroAng = 0, heroAxis = TOSS[HERO].ax;
      for (var b = 0; b < 5; b++) {
        var d = TOSS[b];
        var apexT = d.v0 / G;
        var tt = Math.max(0, (tToss - d.phase) / (1 - d.phase)) * apexT;
        var px = d.dx * tt, pz = d.dz * tt;
        var py = -3.2 + d.v0 * tt - 0.5 * G * tt * tt;
        var ang = (d.w0 / 2.4) * (1 - Math.exp(-2.4 * (tToss + settle)));
        if (b === HERO) {
          heroPos = [px * (1 - settle), py * (1 - settle), pz * (1 - settle)];
          heroAng = ang * (settle > 0.85 ? (1 - (settle - 0.85) / 0.15) : 1);
          continue;
        }
        if (settle > 0.96) continue;
        var fy = py - settle * 9;
        for (var li = 0; li < LAYERS.length; li++) {
          var L = LAYERS[li], base = 0;
          for (var k = 0; k < li; k++) base += LAYERS[k].h;
          M.compose(mModel, [px, fy + base + L.h / 2 - STACK_H / 2, pz],
                    [d.ax[0] * ang, d.ax[1] * ang, d.ax[2] * ang], [1,1,1]);
          drawGeo(geo[li], mModel, L.c, L.rough, L.ss, 0, li * 3.1, 0.07);
        }
      }

      /* ---------- the hero: explode, turn, smash, cut ---------- */
      var sy = 1 - 0.18 * shake, sxz = 1 / Math.sqrt(sy);
      var heroRotY = turn * Math.PI + heroAxis[1] * heroAng;
      var heroRotX = heroAxis[0] * heroAng, heroRotZ = heroAxis[2] * heroAng;
      var halves = split ? [-1, 1] : [0];

      for (var hi = 0; hi < halves.length; hi++) {
        var sign = halves[hi];
        /* a small turn, so both cut faces stay nearly parallel to the screen and both
           catch the key light. A wide book turn puts the two faces back to back. */
        var bookTurn = sign === 0 ? 0 : -sign * opening * (Math.PI * 0.13);
        /* each half slides along ITS OWN local +X, which is the cut-plane normal after
           both the half turn and the book turn. Using the un-turned angle made the two
           halves cross through each other instead of opening. */
        var faceA = heroRotY + bookTurn;
        var gap = opening * 0.30 * sign;
        var offX = gap * Math.cos(faceA), offZ = -gap * Math.sin(faceA);
        for (var i2 = 0; i2 < LAYERS.length; i2++) {
          var L2 = LAYERS[i2], y0 = 0;
          for (var k2 = 0; k2 < i2; k2++) y0 += LAYERS[k2].h;
          var restY = y0 + L2.h / 2 - STACK_H / 2;
          var stagger = clamp((eRaw - i2 * 0.05) / (1 - i2 * 0.05), 0, 1);
          var spread = SH.easeBackOut(stagger) * (1 + antic * 0.08) * (1 - impact);
          var underBlade = clamp(1 - Math.abs(cutting - 0.5) * 4, 0, 1);
          var ly = restY + (i2 - CENTER_I) * GAP * spread;
          var tilt = (i2 % 2 ? 0.06 : -0.06) * spread;
          var roll = (i2 % 3 ? -0.04 : 0.04) * spread;
          var px2 = heroPos[0] + offX;
          var pz2 = heroPos[2] + offZ;
          M.compose(mModel,
            [px2, heroPos[1] + ly * sy, pz2],
            [heroRotX + tilt, heroRotY + bookTurn, heroRotZ + roll],
            [sxz, sy * (1 - 0.06 * underBlade), sxz]);
          drawGeo(geo[i2], mModel, L2.c, L2.rough, L2.ss, sign, i2 * 3.1, 0.085);
          if (sign !== 0) {
            M.compose(mModel,
              [px2 + Math.cos(faceA) * sign * 0.005, heroPos[1] + ly * sy,
               pz2 - Math.sin(faceA) * sign * 0.005],
              [heroRotX + tilt, heroRotY + bookTurn, heroRotZ + roll],
              [1, sy, 1]);
            drawGeo(sign > 0 ? capsR[i2] : capsL[i2], mModel, INTERIOR[i2], 0.52, 0.40, 0, i2 * 7.7 + 3.3, 0.075);
          }
        }
        /* sesame rides the crown */
        if (settle > 0.15 || tToss > 0.2) {
          for (var s2 = 0; s2 < SESAME.length; s2++) {
            var S = SESAME[s2];
            if (sign !== 0 && sign * S.x < 0) continue;
            var crownIdx = LAYERS.length - 1;
            var stag2 = clamp((eRaw - crownIdx * 0.05) / (1 - crownIdx * 0.05), 0, 1);
            var spr2 = SH.easeBackOut(stag2) * (1 + antic * 0.08) * (1 - impact);
            var sYoff = (crownIdx - CENTER_I) * GAP * spr2;
            var ca = Math.cos(heroRotY + bookTurn), sa = Math.sin(heroRotY + bookTurn);
            var wx = S.x * ca + S.z * sa, wz = -S.x * sa + S.z * ca;
            M.compose(mModel,
              [heroPos[0] + offX + wx * sxz,
               heroPos[1] + (S.y - STACK_H / 2 + sYoff) * sy,
               heroPos[2] + offZ + wz * sxz],
              [S.rx, S.ry, 0], [S.s, S.s, S.s]);
            drawGeo(seed, mModel, [0.86,0.74,0.50], 0.44, 0.30, 0, s2 * 1.7, 0.02);
          }
        }
      }

      /* ---------- the knife ---------- */
      if (tCut > 0.001 && tCut < 0.56) {
        var ky = 2.7 - tCut * 5.6;
        var tiltK = 0.0;
        M.compose(mModel, [0, ky, 0], [0, 0, tiltK], [1,1,1]);
        drawGeo(knifeBlade, mModel, [0.66,0.70,0.76], 0.07, 0, 0, 41, 0.003);
        M.compose(mModel, [0, ky + 0.06, -1.95], [0, 0, tiltK], [1,1,1]);
        drawGeo(knifeHandle, mModel, [0.07,0.055,0.045], 0.64, 0, 0, 12, 0.03);
      }

      /* ---------- DOM layers on the same progress ---------- */
      var showLabels = p >= BEATS.explode[0] + 0.02 && p <= BEATS.turn[1];
      for (var l2 = 0; l2 < labels.length; l2++) {
        var el = labels[l2];
        if (!showLabels) { if (el.style.opacity !== '0') el.style.opacity = '0'; continue; }
        var Ly = 0; for (var k3 = 0; k3 < l2; k3++) Ly += LAYERS[k3].h;
        var restY2 = Ly + LAYERS[l2].h / 2 - STACK_H / 2;
        var stag3 = clamp((eRaw - l2 * 0.05) / (1 - l2 * 0.05), 0, 1);
        var spr3 = SH.easeBackOut(stag3);
        var wy = heroPos[1] + restY2 + (l2 - CENTER_I) * GAP * spr3;
        var side = Math.cos(heroRotY) >= 0 ? 1 : -1;
        M.project(pr, [side * (LAYERS[l2].r + 0.62), wy, 0], mVP);
        var appear = clamp((eRaw - l2 * 0.055) / 0.22, 0, 1);
        el.style.opacity = String(appear * (1 - clamp((p - BEATS.turn[1] + 0.03) / 0.03, 0, 1)));
        el.style.transform = 'translate(' + (pr[0] * 100) + 'vw,' + (pr[1] * 100) + 'vh)'
          + (side < 0 ? ' translateX(-100%) scaleX(-1)' : '');
        el.style.textAlign = side < 0 ? 'right' : 'left';
      }

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

      flash.style.opacity = String(shake * 0.16);
      /* beat 8: cross-dissolve the burger into the page surface, then split it apart.
         Both are near-black, so the dissolve reads as the burger leaving, not as a cut. */
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
        disc.style.borderRadius = lerp(50, 50, te) + '%';
      } else { disc.style.opacity = '0'; }

      /* beat copy */
      var idx = 0;
      for (var ci = 0; ci < COPY.length; ci++) if (p >= COPY[ci][0]) idx = ci;
      if (idx !== shown) {
        shown = idx;
        beatName.textContent = COPY[idx][1];
        beatLine.textContent = COPY[idx][2];
      }
    }

    function resize() { if (SH.fitCanvas(canvas, SH.dprCap)) track.measure(); }
    window.addEventListener('resize', SH.debounce(function () { track.measure(); resize(); }, 200), { passive: true });
    resize();

    /* QA hook: with #qa in the URL, the beat can be driven directly instead of by scroll,
       so every frame of the sequence can be inspected deterministically. */
    var forced = null;
    if (location.hash === '#qa') window.__setP = function (v) { forced = v; };

    SH.add(function (dt) {
      if (!visible || document.hidden) return;
      resize();
      var target2 = forced === null ? track.progress() : forced;
      pSmooth = (SH.reduced || forced !== null) ? target2 : SH.damp(pSmooth, target2, 0.0015, dt);
      if (Math.abs(target2 - pSmooth) < 0.0002) pSmooth = target2;
      render(pSmooth);
      window.__seq = { p: +pSmooth.toFixed(3), target: +target2.toFixed(3), cam: window.__cam, track: track.debug(), visible: visible, drew: (window.__drew=(window.__drew||0)+1) };
    });
  });
})(SH);
