// <alpha-video>: plays stacked-alpha clips (colour on the top half, alpha as luma on the bottom half)
// into a WebGL canvas. Two A/B <video> players crossfade on the hub pose, so clip switches never pop.
// The poster <img> child stays visible until the first frame is drawn, and is the fallback on any error.
// A clip may carry its own audio track (talking lines): it plays audible only when asked (`audible`), and the
// caller reads `time` (the front clip's clock) to time captions, so picture, sound and words share one clock.

export type PlayResult = 'ended' | 'started' | 'timeout' | 'error' | 'cancelled';
export interface PlayOptions {
  loop?: boolean;
  markers?: Record<string, number>;
  onMarker?: (name: string) => void;
  /** Max wait for the clip to start, ms. */
  startTimeoutMs?: number;
  /** Expected duration, s (end timeout = duration + 2 s). */
  duration?: number;
  fadeMs?: number;
  /** Start position, s. */
  from?: number;
  /** Play the clip's own audio track (only after the visitor chose sound). */
  audible?: boolean;
  /** Called once the clip is running and is the front clip (its clock is `time` from here on). */
  onStart?: () => void;
}

const VERT = `attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0.,1.);}`;
const FRAG = `precision mediump float;varying vec2 v;uniform sampler2D a;uniform sampler2D b;uniform float m;uniform float pm;
vec4 px(sampler2D t){vec3 c=texture2D(t,vec2(v.x,v.y*.5)).rgb;float al=texture2D(t,vec2(v.x,.5+v.y*.5)).r;return vec4(mix(c*al,min(c,vec3(al)),pm),al);}
void main(){gl_FragColor=mix(px(a),px(b),m);}`;

interface Pending {
  token: number;
  markers: [string, number][];
  onMarker: ((name: string) => void) | undefined;
  resolve: (r: PlayResult) => void;
  loop: boolean;
}

export class AlphaVideo extends HTMLElement {
  private canvas = document.createElement('canvas');
  private gl: WebGLRenderingContext | null = null;
  private tex: [WebGLTexture | null, WebGLTexture | null] = [null, null];
  private uMix: WebGLUniformLocation | null = null;
  private vids: [HTMLVideoElement, HTMLVideoElement];
  private has: [boolean, boolean] = [false, false];
  private front: 0 | 1 = 0;
  private mix = 0;
  private fade: { from: number; to: number; t0: number; ms: number } | null = null;
  private gen = 0;
  private raf = 0;
  private pending: Pending | null = null;
  private visible = true;
  private io: IntersectionObserver | null = null;
  private broken = false;

  constructor() {
    super();
    const mk = (): HTMLVideoElement => {
      const v = document.createElement('video');
      v.muted = true;
      v.defaultMuted = true;
      v.playsInline = true;
      v.setAttribute('playsinline', '');
      v.setAttribute('muted', '');
      v.preload = 'auto';
      v.crossOrigin = 'anonymous';
      v.setAttribute('aria-hidden', 'true');
      v.tabIndex = -1;
      // Not display:none: iOS refuses to play hidden videos without a gesture.
      v.style.cssText = 'position:absolute;width:1px;height:1px;opacity:0;pointer-events:none;left:0;top:0';
      return v;
    };
    this.vids = [mk(), mk()];
  }

  connectedCallback(): void {
    this.canvas.setAttribute('aria-hidden', 'true');
    this.append(this.canvas, ...this.vids);
    this.initGl();
    this.io = new IntersectionObserver((es) => {
      this.visible = es.some((e) => e.isIntersecting);
      if (this.visible) this.kick();
    });
    this.io.observe(this);
  }

  disconnectedCallback(): void {
    this.io?.disconnect();
    cancelAnimationFrame(this.raf);
    this.raf = 0;
  }

  get ok(): boolean {
    return !!this.gl && !this.broken;
  }

  private initGl(): void {
    const gl = this.canvas.getContext('webgl', { premultipliedAlpha: true, alpha: true, antialias: false, preserveDrawingBuffer: false });
    if (!gl) return;
    const sh = (type: number, src: string): WebGLShader | null => {
      const s = gl.createShader(type);
      if (!s) return null;
      gl.shaderSource(s, src);
      gl.compileShader(s);
      return gl.getShaderParameter(s, gl.COMPILE_STATUS) ? s : null;
    };
    const vs = sh(gl.VERTEX_SHADER, VERT);
    const fs = sh(gl.FRAGMENT_SHADER, FRAG);
    const prog = gl.createProgram();
    if (!vs || !fs || !prog) return;
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
    gl.useProgram(prog);
    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, 'p');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    for (const i of [0, 1] as const) {
      const t = gl.createTexture();
      gl.activeTexture(i === 0 ? gl.TEXTURE0 : gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4));
      this.tex[i] = t;
    }
    gl.uniform1i(gl.getUniformLocation(prog, 'a'), 0);
    gl.uniform1i(gl.getUniformLocation(prog, 'b'), 1);
    this.uMix = gl.getUniformLocation(prog, 'm');
    // Colour half already premultiplied by alpha? (attribute `premultiplied`)
    gl.uniform1f(gl.getUniformLocation(prog, 'pm'), this.hasAttribute('premultiplied') ? 1 : 0);
    this.gl = gl;
  }

  /** Play a clip. Loops resolve 'started' once running; one-shots resolve 'ended' (or a failure). */
  play(src: string, opts: PlayOptions = {}): Promise<PlayResult> {
    if (!this.ok || !src) return Promise.resolve('error');
    const token = ++this.gen;
    this.pending?.resolve('cancelled');
    this.pending = null;
    // First clip goes straight into the front player; later clips into the back player, then crossfade.
    const k: 0 | 1 = this.has[0] || this.has[1] ? ((1 - this.front) as 0 | 1) : this.front;
    const v = this.vids[k];
    if (v.dataset['src'] !== src) {
      v.src = src;
      v.dataset['src'] = src;
    }
    v.loop = !!opts.loop;
    v.muted = !opts.audible;
    try {
      v.currentTime = opts.from ?? 0;
    } catch {
      /* not seekable yet */
    }
    const startTimeout = opts.startTimeoutMs ?? 3000;
    return new Promise<PlayResult>((resolve) => {
      let settled = false;
      const done = (r: PlayResult): void => {
        if (settled) return;
        settled = true;
        if (this.pending?.token === token) this.pending = null;
        resolve(r);
      };
      const timer = window.setTimeout(() => {
        if (token === this.gen && !this.has[k]) done('timeout');
      }, startTimeout);
      v.onerror = () => {
        window.clearTimeout(timer);
        if (token === this.gen) this.broken = !this.has[0] && !this.has[1];
        done('error');
      };
      v.play()
        .then(() => {
          window.clearTimeout(timer);
          if (token !== this.gen) {
            v.pause();
            return done('cancelled');
          }
          this.has[k] = true;
          if (k !== this.front || this.mix !== k) {
            this.fade = { from: this.mix, to: k, t0: performance.now(), ms: opts.fadeMs ?? 170 };
          }
          this.front = k;
          this.dataset['ready'] = '';
          opts.onStart?.();
          this.pending = {
            token,
            markers: Object.entries(opts.markers ?? {}).sort((a, b) => a[1] - b[1]),
            onMarker: opts.onMarker,
            resolve: done,
            loop: !!opts.loop,
          };
          if (opts.loop) done('started');
          else {
            const endMs = ((opts.duration ?? (Number.isFinite(v.duration) ? v.duration : 4)) + 2) * 1000;
            window.setTimeout(() => {
              if (token === this.gen) this.flushMarkers(Infinity);
              done('timeout');
            }, endMs);
            v.onended = () => {
              if (token !== this.gen) return;
              this.flushMarkers(Infinity);
              done('ended');
            };
          }
          this.kick();
        })
        .catch(() => {
          window.clearTimeout(timer);
          done('error');
        });
    });
  }

  private flushMarkers(t: number): void {
    const p = this.pending;
    if (!p) return;
    while (p.markers.length && (p.markers[0]?.[1] ?? Infinity) <= t) {
      const m = p.markers.shift();
      if (m) p.onMarker?.(m[0]);
    }
  }

  pause(): void {
    this.vids.forEach((v) => v.pause());
  }

  /** Stop whatever plays (a line cut short), keeping the last frame on the canvas. */
  stop(): void {
    this.gen++;
    this.pending?.resolve('cancelled');
    this.pending = null;
    this.vids.forEach((v) => {
      v.pause();
      v.muted = true;
    });
  }

  /** Mute or unmute the clip that is playing now (sound switched mid-line). */
  setMuted(muted: boolean): void {
    this.vids[this.front].muted = muted;
  }

  /**
   * Call inside a user gesture (the "Sound on" tap): iOS lets a media element play with sound later only
   * if it has played once from a gesture. Both players get that first play; silent idle clips stay silent.
   */
  unlock(): void {
    const src = this.vids[this.front].dataset['src'];
    this.vids.forEach((v, i) => {
      if (!v.dataset['src'] && src) {
        v.src = src;
        v.dataset['src'] = src;
      }
      if (!v.src) return;
      const wasPaused = v.paused;
      const p = v.play();
      if (i !== this.front || wasPaused) p.then(() => v.pause()).catch(() => undefined);
      else p.catch(() => undefined);
    });
  }

  /** Let a looping clip run to its end (talk clips end on the idle pose), then resolve. */
  finishLoop(): Promise<void> {
    const v = this.vids[this.front];
    if (!this.has[this.front] || v.paused || !v.loop) return Promise.resolve();
    v.loop = false;
    const left = Number.isFinite(v.duration) ? Math.max(0, v.duration - v.currentTime) : 5;
    return new Promise((resolve) => {
      const t = window.setTimeout(resolve, left * 1000 + 600);
      v.addEventListener(
        'ended',
        () => {
          window.clearTimeout(t);
          resolve();
        },
        { once: true },
      );
    });
  }

  /** Show one still frame of a clip (e.g. the first beat of an entrance) without playing it. */
  showFrame(src: string, t: number): Promise<boolean> {
    if (!this.ok || !src) return Promise.resolve(false);
    const token = ++this.gen;
    this.pending?.resolve('cancelled');
    this.pending = null;
    const k = this.front;
    const v = this.vids[k];
    v.pause();
    v.loop = false;
    if (v.dataset['src'] !== src) {
      v.src = src;
      v.dataset['src'] = src;
    }
    return new Promise((resolve) => {
      const timer = window.setTimeout(() => resolve(false), 4000);
      const seek = (): void => {
        v.addEventListener(
          'seeked',
          () => {
            window.clearTimeout(timer);
            if (token !== this.gen) return resolve(false);
            this.has[k] = true;
            this.mix = k;
            this.dataset['ready'] = '';
            this.kick();
            resolve(true);
          },
          { once: true },
        );
        v.currentTime = t;
      };
      if (v.readyState >= 1) seek();
      else v.addEventListener('loadedmetadata', seek, { once: true });
    });
  }

  resume(): void {
    const v = this.vids[this.front];
    if (this.has[this.front] && v.paused && !v.ended) v.play().catch(() => undefined);
    this.kick();
  }

  /** Current playback time of the front clip (for video-synced effects). */
  get time(): number {
    return this.vids[this.front].currentTime;
  }
  get frontVideo(): HTMLVideoElement {
    return this.vids[this.front];
  }

  private kick(): void {
    if (!this.raf && this.gl) this.raf = requestAnimationFrame(this.tick);
  }

  private tick = (now: number): void => {
    this.raf = 0;
    const gl = this.gl;
    if (!gl) return;
    if (this.fade) {
      const f = this.fade;
      const p = Math.min(1, (now - f.t0) / f.ms);
      this.mix = f.from + (f.to - f.from) * p;
      if (p >= 1) {
        this.fade = null;
        const back = (1 - this.front) as 0 | 1;
        this.vids[back].pause();
      }
    } else this.mix = this.front;
    const fv = this.vids[this.front];
    if (this.pending && !this.pending.loop) this.flushMarkers(fv.currentTime);
    if (this.visible) {
      for (const i of [0, 1] as const) {
        const v = this.vids[i];
        const weight = i === 1 ? this.mix : 1 - this.mix;
        if (weight > 0.001 && v.readyState >= 2) {
          if (i === this.front && v.videoWidth && (this.canvas.width !== v.videoWidth || this.canvas.height !== v.videoHeight / 2)) {
            this.canvas.width = v.videoWidth;
            this.canvas.height = v.videoHeight / 2;
            gl.viewport(0, 0, this.canvas.width, this.canvas.height);
          }
          gl.activeTexture(i === 0 ? gl.TEXTURE0 : gl.TEXTURE1);
          gl.bindTexture(gl.TEXTURE_2D, this.tex[i]);
          try {
            gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, v);
          } catch {
            this.broken = true;
          }
        }
      }
      gl.uniform1f(this.uMix, this.mix);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    const busy = this.fade || this.vids.some((v) => !v.paused && !v.ended);
    if (busy && this.visible && !document.hidden) this.raf = requestAnimationFrame(this.tick);
  };
}

if (!customElements.get('alpha-video')) customElements.define('alpha-video', AlphaVideo);

declare global {
  interface HTMLElementTagNameMap {
    'alpha-video': AlphaVideo;
  }
}
