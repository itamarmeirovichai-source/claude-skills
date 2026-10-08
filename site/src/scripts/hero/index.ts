// Hero orchestrator: wires DOM events → machine → effects. Modules never talk to each other directly.
import '../alpha-video';
import type { AlphaVideo } from '../alpha-video';
import { reduce, type Clip, type Effect, type Event, type State } from './machine';
import { Ring } from './ring';
import { media, mediaUrl, resolveClip, ringFilms, SPEC_LABEL, VIDEO_TYPES } from '../../lib/media';
import { alphaSrc, pickAlphaCodec, type AlphaCodec } from '../core/codec';
import { prefs, session, soundOn, motionPaused, reducedMotion, saveData } from '../core/prefs';
import { say, hush, heard } from '../core/voice';
import { Flip, gsap, scrollToY, stopSmooth } from '../core/motion';
import { track } from '../core/analytics';

const $ = <T extends Element>(root: ParentNode, sel: string): T => {
  const el = root.querySelector<T>(sel);
  if (!el) throw new Error(`hero: missing ${sel}`);
  return el;
};

export function mountHero(): void {
  const hero = document.getElementById('hero');
  if (!hero) return;
  const main = $<HTMLElement>(document, '#content');
  const otto = $<AlphaVideo>(hero, '#otto');
  const captionEl = $<HTMLElement>(hero, '[data-caption]');
  const stage = $<HTMLElement>(hero, '[data-stage]');
  const stageFilm = $<HTMLElement>(hero, '[data-stage-film]');
  const film = $<HTMLVideoElement>(hero, '[data-film]');
  const filmLabel = $<HTMLElement>(hero, '[data-film-label]');
  const tapSound = $<HTMLButtonElement>(hero, '[data-tap-sound]');
  const motionBtn = $<HTMLButtonElement>(hero, '[data-motion]');
  const continueBtn = $<HTMLButtonElement>(hero, '[data-continue]');
  const anotherBtn = $<HTMLButtonElement>(hero, '[data-pick-another]');
  const ring = new Ring($<HTMLElement>(hero, '[data-ring]'), $<HTMLElement>(hero, '[data-scene]'));
  const films = ringFilms();
  const rm = reducedMotion();
  if (rm) hero.classList.add('rm');

  let state: State = { s: 'boot' };
  let codec: AlphaCodec | null = null;
  let ottoGen = 0;
  let nudge = 0;
  let pull: { cancel: () => void } | null = null;
  let currentFilm = -1;

  // ---------- captions ----------
  let capTimer = 0;
  const caption = (text: string): void => {
    captionEl.textContent = text;
    captionEl.classList.add('on');
    window.clearTimeout(capTimer);
    capTimer = window.setTimeout(() => captionEl.classList.remove('on'), Math.max(2400, text.length * 80));
  };

  // ---------- dispatch ----------
  const dispatch = (ev: Event): void => {
    const step = reduce(state, ev);
    state = step.state;
    hero.dataset['state'] = state.s;
    for (const fx of step.fx) run(fx);
  };

  // ---------- Otto clips ----------
  // Point clips are chosen by the card's screen side; pointMap says which master points that way.
  const clipMeta = (c: Clip) => {
    const m = /^char_point_([LRC])$/.exec(c);
    const key = m ? (media.otto.pointMap?.[m[1] as 'L' | 'R' | 'C'] ?? c) : c;
    const r = resolveClip(media.otto, key);
    // A mapped point clip keeps the markers of the slot it fills when the master lacks them.
    const slot = media.otto.clips[c];
    return r && slot?.markers && !r.markers ? { ...r, markers: slot.markers } : r ?? (slot?.duration ? { av1: '', hevc: '', duration: slot.duration, ...(slot.markers ? { markers: slot.markers } : {}) } : undefined);
  };
  const playOtto = async (clips: Clip[]): Promise<void> => {
    const my = ++ottoGen;
    for (const [idx, c] of clips.entries()) {
      if (my !== ottoGen) return;
      const meta = clipMeta(c);
      if (!meta) continue;
      const loop = !!meta.loop && idx === clips.length - 1;
      const onMarker = (name: string): void => {
        if (my !== ottoGen) return;
        if (name === 'peak') dispatch({ e: 'POINT_PEAK' });
        if (name === 'contact') pullContact?.();
      };
      const live = !!meta.av1 && codec && otto.ok && !rm && !saveData() && !motionPaused();
      if (live && codec && loop && otto.frontVideo.dataset['src'] === alphaSrc(meta, codec) && !otto.frontVideo.paused) return;
      if (live && codec) {
        const r = await otto.play(alphaSrc(meta, codec), { loop, duration: meta.duration, ...(meta.markers ? { markers: meta.markers } : {}), onMarker });
        if (r === 'error' || r === 'timeout') await virtualClip(meta.duration, meta.markers, onMarker, loop, my);
      } else {
        await virtualClip(meta.duration, meta.markers, onMarker, loop, my);
      }
      if (loop) return;
    }
  };
  // Same timing without video (poster Otto, reduced motion, decode failure): markers still fire.
  const virtualClip = (dur: number, markers: Record<string, number> | undefined, onMarker: (n: string) => void, loop: boolean, my: number): Promise<void> =>
    new Promise((resolve) => {
      if (loop) return resolve();
      const scale = rm ? 0.3 : 1;
      for (const [name, t] of Object.entries(markers ?? {})) window.setTimeout(() => my === ottoGen && onMarker(name), t * 1000 * scale);
      window.setTimeout(resolve, dur * 1000 * scale);
    });

  // ---------- film ----------
  const filmSrc = (i: number): string => {
    const f = films[i];
    if (!f) return '';
    const av1 = film.canPlayType(VIDEO_TYPES.av1Audio) || film.canPlayType(VIDEO_TYPES.av1);
    return mediaUrl(av1 && f.full.av1 ? f.full.av1 : f.full.h264);
  };
  const primeFilm = (i: number): void => {
    // Runs synchronously inside the click: sets the source and starts playback so sound is unlocked.
    currentFilm = i;
    const f = films[i];
    film.src = filmSrc(i);
    film.poster = f ? mediaUrl(f.poster) : '';
    film.muted = !soundOn();
    film.currentTime = 0;
    const p = film.play();
    p.then(() => {
      if (state.s === 'pointing') {
        film.pause();
        film.currentTime = 0;
      }
    }).catch(() => undefined);
  };
  const startFilm = (): void => {
    film.muted = !soundOn();
    film.controls = false;
    film
      .play()
      .then(() => {
        tapSound.hidden = !film.muted || !session.gesture || prefs.get().sound === 'off';
        if (!film.muted) track('ad_sound_on', { film: currentFilm });
      })
      .catch(() => {
        // Autoplay with sound refused: play muted, offer a tap.
        film.muted = true;
        film.play().catch(() => (film.controls = true));
        tapSound.hidden = false;
        track('ad_play_failed', { film: currentFilm });
      });
  };

  const enlarge = (i: number): void => {
    const card = ring.card(i);
    const f = films[i];
    filmLabel.textContent = f ? SPEC_LABEL(f) : '';
    film.setAttribute('aria-label', f ? `${f.brand}: ${f.title}. ${SPEC_LABEL(f)}` : 'Spec film');
    stage.hidden = false;
    stage.classList.remove('docked');
    const done = (): void => {
      if (state.s !== 'enlarging') return;
      startFilm();
      dispatch({ e: 'ENLARGED' });
    };
    const img = card?.querySelector('img');
    if (!card || !img || rm) {
      gsap.fromTo(stageFilm, { opacity: 0 }, { opacity: 1, duration: rm ? 0.2 : 0.4, onComplete: done });
      return;
    }
    // Flat 2D clone of the picked card, flipped onto the stage.
    const r = card.getBoundingClientRect();
    const clone = img.cloneNode() as HTMLImageElement;
    clone.alt = '';
    clone.style.cssText = `position:fixed;left:${r.left}px;top:${r.top}px;width:${r.width}px;height:${r.height}px;object-fit:cover;border-radius:10px;z-index:60;pointer-events:none`;
    document.body.append(clone);
    stageFilm.style.opacity = '0';
    Flip.fit(clone, stageFilm, {
      duration: 0.95,
      ease: 'expo.inOut',
      absolute: true,
      onComplete: () => {
        stageFilm.style.opacity = '1';
        gsap.to(clone, { opacity: 0, duration: 0.35, ease: 'power2.out', onComplete: () => clone.remove() });
        done();
      },
    });
    window.setTimeout(() => {
      if (clone.isConnected && state.s === 'enlarging') {
        clone.remove();
        stageFilm.style.opacity = '1';
        done();
      }
    }, 2000);
  };

  const dock = (): void => {
    const st = Flip.getState(stageFilm);
    stage.classList.add('docked');
    Flip.from(st, { duration: rm ? 0 : 0.8, ease: 'expo.inOut' });
  };
  const shrink = (): void => {
    film.pause();
    tapSound.hidden = true;
    if (stage.hidden) return;
    gsap.to(stageFilm, {
      opacity: 0,
      scale: 0.9,
      duration: rm ? 0 : 0.35,
      ease: 'power2.in',
      onComplete: () => {
        stage.hidden = true;
        stage.classList.remove('docked');
        gsap.set(stageFilm, { clearProps: 'opacity,scale,transform' });
      },
    });
  };

  // ---------- pull-up (Continue) ----------
  let pullContact: (() => void) | null = null;
  const pullUp = (): void => {
    const target = (): number => main.getBoundingClientRect().top + window.scrollY - 64;
    const meta = resolveClip(media.otto, 'char_reach');
    const contact = meta?.markers?.['contact'] ?? 0.5;
    const dur = meta?.duration ?? 2;
    let cancelled = false;
    let finished = false;
    const finish = (): void => {
      if (finished) return;
      finished = true;
      removeCancel();
      stopSmooth(false);
      dispatch({ e: 'REACH_DONE' });
    };
    const cancel = (): void => {
      cancelled = true;
      finish();
    };
    const onUser = (): void => cancel();
    const removeCancel = (): void => {
      window.removeEventListener('wheel', onUser);
      window.removeEventListener('touchstart', onUser);
      window.removeEventListener('keydown', onUser);
    };
    window.addEventListener('wheel', onUser, { passive: true });
    window.addEventListener('touchstart', onUser, { passive: true });
    window.addEventListener('keydown', onUser);
    pull = { cancel };

    if (rm) {
      // Reduced motion: a 200 ms fade, no travel.
      scrollToY(target(), { immediate: true });
      gsap.fromTo(main, { opacity: 0 }, { opacity: 1, duration: 0.2, onComplete: finish });
      return;
    }
    const y0 = window.scrollY;
    const drive = (p: number): void => {
      if (cancelled) return;
      const e = p < 0 ? 0 : p > 1 ? 1 : p;
      scrollToY(y0 + (target() - y0) * (1 - Math.pow(1 - e, 2)), { immediate: true });
    };
    const videoDriven = otto.ok && codec && !motionPaused() && !saveData();
    pullContact = () => {
      pullContact = null;
      stopSmooth(true);
      const t0 = performance.now();
      const span = Math.max(0.4, Math.min(1.6, dur - contact));
      const loop = (): void => {
        if (cancelled || finished) return;
        // Driven by the reach clip's own clock, so the sheet edge stays locked to the hand; time fallback if it stalls.
        const vt = videoDriven ? (otto.time - contact) / span : 0;
        const tt = (performance.now() - t0) / 1000 / span;
        const p = videoDriven && otto.time > contact ? Math.max(vt, tt * 0.85) : tt;
        drive(p);
        if (p >= 1) return finish();
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
    };
    // Safety net: never strand the visitor.
    window.setTimeout(() => !finished && (drive(1), finish()), (dur + 2.5) * 1000);
  };

  // ---------- effects runner ----------
  function run(fx: Effect): void {
    switch (fx.fx) {
      case 'otto':
        void playOtto(fx.clips);
        break;
      case 'say': {
        const asking = state.s === 'asking';
        void say(fx.line, { caption, silent: fx.silent ?? false }).then(() => {
          // Talk clips end on the idle pose: let the loop finish, then idle.
          if (asking && state.s === 'asking') void otto.finishLoop().then(() => void (state.s === 'asking' && playOtto(['char_idle'])));
        });
        break;
      }
      case 'hush':
        hush();
        break;
      case 'ring':
        ring.run(fx.run);
        break;
      case 'filmPlay':
        primeFilm(fx.film);
        break;
      case 'enlarge':
        enlarge(fx.film);
        break;
      case 'dock':
        dock();
        break;
      case 'shrink':
        shrink();
        break;
      case 'pullUp':
        pullUp();
        break;
      case 'revealDone': {
        pull = null;
        if (fx.focus) {
          const h = main.querySelector<HTMLElement>('h2');
          h?.setAttribute('tabindex', '-1');
          h?.focus({ preventScroll: true });
        }
        document.dispatchEvent(new CustomEvent('vxo:revealed'));
        break;
      }
      case 'nudgeTimer':
        window.clearTimeout(nudge);
        if (fx.on) nudge = window.setTimeout(() => dispatch({ e: 'NUDGE' }), 6000);
        break;
      case 'pulseButtons':
        for (const b of [anotherBtn, continueBtn]) {
          b.classList.remove('pulse');
          void b.offsetWidth;
          b.classList.add('pulse');
        }
        break;
      case 'track':
        track(fx.name, fx.props ?? {});
        break;
      default: {
        const never: never = fx;
        return never;
      }
    }
  }

  // ---------- DOM events ----------
  const select = (i: number): void => dispatch({ e: 'SELECT', film: i, dir: ring.dirOf(i) });
  hero.querySelectorAll<HTMLAnchorElement>('[data-card]').forEach((card) => {
    card.addEventListener('click', (e) => {
      if (state.s === 'fallback' || state.s === 'boot' || e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      select(Number(card.dataset['card']));
    });
  });
  hero.querySelector<HTMLAnchorElement>('[data-pick-film]')?.addEventListener('click', (e) => {
    if (state.s === 'fallback' || state.s === 'boot') return;
    e.preventDefault();
    select(ring.frontIndex());
  });
  anotherBtn.addEventListener('click', () => {
    dispatch({ e: 'PICK_ANOTHER' });
    ring.card(ring.frontIndex())?.focus({ preventScroll: true });
  });
  continueBtn.addEventListener('click', () => dispatch({ e: 'CONTINUE' }));
  $<HTMLButtonElement>(hero, '[data-close]').addEventListener('click', () => dispatch({ e: 'CLOSE' }));
  film.addEventListener('ended', () => dispatch({ e: 'FILM_END' }));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && (state.s === 'playing' || state.s === 'enlarging')) dispatch({ e: 'CLOSE' });
  });
  $<HTMLAnchorElement>(hero, '[data-skip]').addEventListener('click', (e) => {
    e.preventDefault();
    dispatch({ e: 'LEFT_HERO', via: 'skip' });
    scrollToY(main.getBoundingClientRect().top + window.scrollY - 64);
    main.querySelector<HTMLElement>('h2')?.setAttribute('tabindex', '-1');
    main.querySelector<HTMLElement>('h2')?.focus({ preventScroll: true });
  });
  document.querySelectorAll<HTMLElement>('[data-back-to-show]').forEach((b) =>
    b.addEventListener('click', () => {
      scrollToY(0);
      dispatch({ e: 'BACK_TO_TOP' });
    }),
  );
  const aiLine = hero.querySelector<HTMLElement>('[data-ai-line]');
  const aiHover = (): void => void say('vo_ai', { caption, silent: true });
  // Sound switched on while the hero is on screen: Otto introduces himself (once, after Vee).
  document.addEventListener('vxo:crew-intro-done', () => {
    if (state.s !== 'idle' || heroCovered || window.scrollY > hero.offsetHeight * 0.5 || heard('act_o1')) return;
    void playOtto(['otto_talk_a']);
    void say('act_o1', { caption }).then(() => otto.finishLoop().then(() => void (state.s === 'idle' && playOtto(['char_idle']))));
  });
  aiLine?.addEventListener('pointerenter', aiHover);
  aiLine?.addEventListener('focus', aiHover);

  // Sound lives in the story chrome pill; keep the film in step with it.
  const syncSound = (): void => {
    film.muted = !soundOn();
    if (!film.muted) tapSound.hidden = true;
  };
  document.addEventListener('vxo:sound', syncSound);
  tapSound.addEventListener('click', () => {
    prefs.set({ sound: 'on' });
    film.muted = false;
    tapSound.hidden = true;
    document.dispatchEvent(new CustomEvent('vxo:sound'));
  });

  const syncMotion = (): void => {
    const paused = prefs.get().motion === 'paused';
    motionBtn.setAttribute('aria-pressed', String(paused));
    motionBtn.textContent = paused ? 'Play motion' : 'Pause motion';
    if (paused) otto.pause();
    else if (state.s !== 'revealed') otto.resume();
    ring.setLoops(!paused && state.s !== 'revealed');
  };
  motionBtn.addEventListener('click', () => {
    prefs.set({ motion: prefs.get().motion === 'paused' ? 'running' : 'paused' });
    track('motion_pause', { on: prefs.get().motion === 'paused' });
    syncMotion();
  });

  // Native scroll = the same reveal (no lock); back at the top = the show resumes.
  let heroCovered = false;
  const onScroll = (): void => {
    const h = hero.offsetHeight;
    const y = window.scrollY;
    if (y > h * 0.45 && !pull && state.s !== 'revealed' && state.s !== 'reaching' && state.s !== 'boot' && state.s !== 'fallback') {
      dispatch({ e: 'LEFT_HERO', via: 'scroll' });
    }
    if (y < 8 && state.s === 'revealed' && !pull) dispatch({ e: 'BACK_TO_TOP' });
    const covered = y >= h - 4;
    if (covered !== heroCovered) {
      heroCovered = covered;
      if (covered) {
        otto.pause();
        ring.setLoops(false);
      } else if (prefs.get().motion !== 'paused') {
        otto.resume();
        ring.setLoops(true);
      }
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });

  // ---------- boot ----------
  const boot = async (): Promise<void> => {
    codec = await pickAlphaCodec();
    hero.dataset['codec'] = codec ?? 'poster';
    const idle = resolveClip(media.otto, 'char_idle');
    if (rm || saveData() || !codec || !idle || !otto.ok) {
      dispatch({ e: 'READY' }); // poster Otto, everything else works
      track('hero_ready', { codec: 'poster' });
      return;
    }
    const t0 = performance.now();
    const r = await otto.play(alphaSrc(idle, codec), { loop: true, startTimeoutMs: 5000 });
    if (r === 'started') {
      ottoGen++; // the boot idle is the first clip
      dispatch({ e: 'READY' });
      track('hero_ready', { codec, ms: Math.round(performance.now() - t0) });
    } else {
      // Media failed: static hero; the cards stay plain links to /work/<slug>.
      dispatch({ e: 'FAIL' });
    }
  };
  syncMotion();
  void boot();
  window.addEventListener('pageshow', (e) => {
    if (e.persisted && window.scrollY < 8 && state.s === 'revealed') dispatch({ e: 'BACK_TO_TOP' });
  });
}
