// The home page story: chapter mark, sound pill, sticky CTA, the pinned Act III demo, the schedule fill,
// tile parallax, the film player and the crew's scene-timed lines. One gsap.matchMedia with three branches:
// desktop (Lenis + pins + scrubs), touch (native scroll, one short pin) and reduce (no pins, no scrubs).
import '../alpha-video';
import type { AlphaVideo } from '../alpha-video';
import { gsap, ScrollTrigger, isTouch } from '../core/motion';
import { mountCrew, type Entrance } from './crew';
import { media, mediaUrl, resolveClip, filmBySlug, SPEC_LABEL, VIDEO_TYPES } from '../../lib/media';
import { alphaSrc, pickAlphaCodec } from '../core/codec';
import { prefs, session, soundOn, reducedMotion } from '../core/prefs';
import { say, hush, heard, draw, onLine } from '../core/voice';
import { track } from '../core/analytics';

const $ = <T extends Element = HTMLElement>(sel: string, root: ParentNode = document): T | null => root.querySelector<T>(sel);
const $$ = <T extends Element = HTMLElement>(sel: string, root: ParentNode = document): T[] => [...root.querySelectorAll<T>(sel)];

export async function mountStory(): Promise<void> {
  const rm = reducedMotion();
  const touch = isTouch();
  const root = document.documentElement;

  // ---------- captions for assistive tech: the line that just started, politely ----------
  const liveEl = $('[data-crew-live]');
  onLine((text, key) => {
    if (liveEl) liveEl.textContent = `${/^(vee|act_v|peek_v)/.test(key) ? 'Vee' : 'Otto'}: ${text}`;
  });

  // ---------- message match ----------
  const h1 = $('#hero-h1');
  if (h1?.dataset['variant']) track('utm_headline_variant', { v: h1.dataset['variant'] });

  // ---------- chapter mark + progress + act views ----------
  const chapterTexts = $$('[data-chapter-text]');
  const progress = $('[data-progress]');
  const seen = new Set<string>();
  $$('[data-act]').forEach((act) => {
    const n = act.dataset['act'] ?? '';
    ScrollTrigger.create({
      trigger: act,
      start: 'top 55%',
      end: 'bottom 55%',
      onToggle: (st) => {
        if (!st.isActive) return;
        chapterTexts.forEach((c) => (c.textContent = n === '9' ? 'Coda' : `Scene ${n} · ${act.dataset['chapter'] ?? ''}`));
        if (!seen.has(n)) {
          seen.add(n);
          track('act_view', { n: Number(n) });
        }
      },
    });
  });
  if (progress) {
    ScrollTrigger.create({ start: 0, end: 'max', onUpdate: (st) => gsap.set(progress, { scaleY: st.progress }) });
  }
  const hero = $('#hero');
  if (hero) {
    ScrollTrigger.create({ trigger: hero, start: 'bottom 70%', onToggle: (st) => root.classList.toggle('story-on', st.isActive || st.progress >= 1), end: 'max' });
  }

  // ---------- sticky CTA: after the hero CTA leaves, never next to an in-flow CTA or over the demo ----------
  const sticky = $<HTMLAnchorElement>('[data-sticky-cta]');
  const heroCta = $('[data-frames-cta]');
  const inflow = new Set<Element>();
  let heroCtaVisible = true;
  let demoPinned = false;
  const syncSticky = (): void => void sticky?.classList.toggle('on', !heroCtaVisible && inflow.size === 0 && !demoPinned);
  if (sticky && 'IntersectionObserver' in window) {
    // The hero is sticky on desktop (the story slides over it), so "out of view" = the sheet has covered it.
    if (heroCta) ScrollTrigger.create({ trigger: '#content', start: 'top 45%', end: 'max', onToggle: (st) => ((heroCtaVisible = !st.isActive), syncSticky()) });
    const io = new IntersectionObserver((es) => {
      es.forEach((e) => (e.isIntersecting ? inflow.add(e.target) : inflow.delete(e.target)));
      syncSticky();
    }, { threshold: 0.2 });
    $$('[data-inflow-cta]').filter((el) => !el.closest('#hero')).forEach((el) => io.observe(el));
    sticky.addEventListener('click', () => track('sticky_cta_click'));
  }

  // ---------- sound pill ("Sound on · meet the crew") ----------
  const soundBtn = $<HTMLButtonElement>('[data-crew-sound]');
  const pillVee = $('[data-pill-vee]');
  const pillAv = pillVee?.querySelector<AlphaVideo>('alpha-video') ?? null;
  const pillBubble = $('[data-pill-bubble]');
  const syncPill = (): void => {
    const on = soundOn();
    soundBtn?.setAttribute('aria-pressed', String(on));
    // Update text in place (never replace nodes: a node swapped mid-tap swallows the click).
    const long = soundBtn?.querySelector('.long');
    const short = soundBtn?.querySelector('.short');
    const lt = on ? 'Sound on · mute the crew' : 'Sound on · meet the crew';
    const st = on ? 'Mute' : 'Sound on';
    if (long && long.textContent !== lt) long.textContent = lt;
    if (short && short.textContent !== st) short.textContent = st;
  };
  // A remembered "on" still needs this visit's first tap before audio may play.
  window.addEventListener('pointerdown', () => queueMicrotask(syncPill), { once: true, capture: true });
  syncPill();
  soundBtn?.addEventListener('click', () => {
    const turningOn = !soundOn();
    session.gesture = true;
    prefs.set({ sound: turningOn ? 'on' : 'off' });
    syncPill();
    document.dispatchEvent(new CustomEvent('vxo:sound'));
    if (!turningOn) {
      hush();
      track('crew_sound_off');
      return;
    }
    track('crew_sound_on');
    // Vee introduces herself; play() runs inside this click, which is what unlocks audio.
    const line = heard('act_v1') ? 'vee.pop' : 'act_v1';
    pillVee?.classList.add('on');
    void say(line, { caption: (t) => pillBubble && (pillBubble.textContent = t) }).then(async () => {
      if (pillAv?.ok) await pillAv.finishLoop();
      window.setTimeout(() => pillVee?.classList.remove('on'), 900);
      document.dispatchEvent(new CustomEvent('vxo:crew-intro-done'));
    });
    void pickAlphaCodec().then((codec) => {
      const c = resolveClip(media.vee, 'vee_talk_a');
      if (codec && c && pillAv?.ok && !rm) void pillAv.play(alphaSrc(c, codec), { loop: true, duration: c.duration });
    });
  });
  $$<HTMLButtonElement>('[data-hide-hosts]').forEach((b) =>
    b.addEventListener('click', () => {
      prefs.set({ hosts: 'hidden' });
      hush();
      track('crew_muted');
    }),
  );

  // ---------- the crew (after the pill is wired, so an early tap is never lost) ----------
  const crew = await mountCrew(touch);
  const actor = (id: string): Entrance | undefined => crew.get(id);

  // ---------- Act III · one photo in (pinned demo) ----------
  const demo = $('#demo');
  const monitor = $('[data-monitor]');
  const scrub = $<HTMLVideoElement>('[data-scrub]');
  const steps = $$('[data-mstep]');
  const after = monitor?.querySelector<HTMLElement>('.m-after') ?? null;
  let demoSpoken = false;
  const setStep = (i: number): void => {
    if (monitor?.dataset['step'] === String(i)) return;
    if (monitor) monitor.dataset['step'] = String(i);
    steps.forEach((s, j) => s.classList.toggle('on', j === i));
  };
  setStep(0);
  // Fetch the scrub clip one act early (ref 39 §1.4), never on Save-Data.
  if (scrub && demo && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(([e]) => {
      if (!e?.isIntersecting) return;
      io.disconnect();
      if (!scrub.src && scrub.dataset['src']) {
        scrub.src = scrub.dataset['src'];
        scrub.preload = 'auto';
        scrub.load();
      }
    }, { rootMargin: '100% 0px' });
    io.observe(demo);
  }
  let seekTarget = 0;
  let seekCur = 0;
  gsap.ticker.add(() => {
    if (!scrub || !scrub.duration || scrub.readyState < 1) return;
    seekCur += (seekTarget - seekCur) * 0.18;
    if (Math.abs(scrub.currentTime - seekCur) > 1 / 48) scrub.currentTime = seekCur;
  });
  const drive = (p: number): void => {
    // 0–30 %: the photo · 30–60 %: it resolves into the frame · 60–100 %: the frame becomes the take.
    const wipe = gsap.utils.clamp(0, 1, (p - 0.24) / 0.3);
    const film = gsap.utils.clamp(0, 1, (p - 0.6) / 0.38);
    if (after) after.style.clipPath = `inset(0 0 0 ${(100 * (1 - wipe)).toFixed(2)}%)`;
    if (scrub) {
      scrub.style.opacity = String(gsap.utils.clamp(0, 1, film * 6));
      if (scrub.duration) seekTarget = film * (scrub.duration - 0.05);
    }
    setStep(p < 0.3 ? 0 : p < 0.6 ? 1 : 2);
    if (p > 0.97 && !demoSpoken) {
      demoSpoken = true;
      void actor('otto-demo')?.speak('act_o2');
    }
  };

  const mm = gsap.matchMedia();
  mm.add(
    { desktop: '(min-width: 900px) and (prefers-reduced-motion: no-preference)', mobile: '(max-width: 899px) and (prefers-reduced-motion: no-preference)', reduce: '(prefers-reduced-motion: reduce)' },
    (ctx) => {
      const { desktop, mobile, reduce } = ctx.conditions as { desktop: boolean; mobile: boolean; reduce: boolean };
      if (reduce) {
        // Same story in stills: the frame, every caption, no pins, no scrubs.
        if (after) after.style.clipPath = 'none';
        steps.forEach((s) => s.classList.add('on'));
        return;
      }
      const pinEl = desktop ? $('[data-pin-stage]') : $('[data-monitor-wrap]');
      if (demo && pinEl) {
        ScrollTrigger.create({
          trigger: pinEl,
          start: 'top 64px',
          end: desktop ? '+=200%' : '+=120%',
          pin: true,
          scrub: desktop ? 0.8 : true,
          anticipatePin: 1,
          onUpdate: (st) => drive(st.progress),
          onToggle: (st) => {
            demoPinned = st.isActive;
            syncSticky();
          },
        });
      }
      // Act V: the brass line fills as you read the schedule.
      const fill = $('[data-fill]');
      const sheet = $('[data-callsheet]');
      if (fill && sheet) gsap.fromTo(fill, { scaleX: 0 }, { scaleX: 1, ease: 'none', scrollTrigger: { trigger: sheet, start: 'top 75%', end: 'bottom 45%', scrub: 0.8 } });
      // Act IV: two layers, tiny deltas (≤ 6 %), desktop only.
      if (desktop) {
        $$('[data-parallax]').forEach((el) => {
          const dir = Number(el.dataset['parallax'] ?? 1);
          gsap.fromTo(el, { yPercent: 3 * dir }, { yPercent: -3 * dir, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: 1 } });
        });
      }
      void mobile;
      return () => {
        demoPinned = false;
      };
    },
  );
  // Crew triggers were made before the pins: recompute their positions now.
  ScrollTrigger.sort();
  ScrollTrigger.refresh();

  // ---------- Act IV · film tiles open the player with sound ----------
  const dialog = $<HTMLDialogElement>('[data-film-dialog]');
  const fdVideo = $<HTMLVideoElement>('[data-fd-video]');
  const fdLabel = $('[data-fd-label]');
  const fdMore = $<HTMLAnchorElement>('[data-fd-more]');
  if (dialog && fdVideo && typeof dialog.showModal === 'function') {
    $$<HTMLAnchorElement>('.act-films .tile, .act-risk .tile').forEach((tile) =>
      tile.addEventListener('click', (e) => {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        const slug = tile.getAttribute('href')?.split('/').pop() ?? '';
        const f = filmBySlug(slug);
        if (!f) return;
        e.preventDefault();
        const av1 = fdVideo.canPlayType(VIDEO_TYPES.av1Audio) || fdVideo.canPlayType(VIDEO_TYPES.av1);
        fdVideo.src = mediaUrl(av1 ? f.full.av1 : f.full.h264);
        fdVideo.poster = mediaUrl(f.poster);
        fdVideo.muted = !soundOn(); // sound only after "Sound on"; captions are burned in, controls can unmute
        fdVideo.setAttribute('aria-label', `${f.brand}: ${f.title}. ${SPEC_LABEL(f)}`);
        if (fdLabel) fdLabel.textContent = SPEC_LABEL(f);
        if (fdMore) fdMore.href = `/work/${f.slug}`;
        const from = tile.querySelector('.media')?.getBoundingClientRect();
        dialog.showModal();
        void fdVideo.play().catch(() => {
          fdVideo.muted = true;
          void fdVideo.play().catch(() => undefined);
        });
        if (from && !rm) {
          // Open from the tile: the player grows out of the poster you clicked (FLIP-style).
          const to = fdVideo.getBoundingClientRect();
          gsap.fromTo(
            fdVideo,
            { x: from.left + from.width / 2 - (to.left + to.width / 2), y: from.top + from.height / 2 - (to.top + to.height / 2), scale: from.width / to.width, opacity: 0.4 },
            { x: 0, y: 0, scale: 1, opacity: 1, duration: 0.85, ease: 'expo.out', clearProps: 'transform,opacity' },
          );
        }
        track('ad_play', { film: f.slug, from: 'act4' });
      }),
    );
    dialog.addEventListener('close', () => {
      fdVideo.pause();
      fdVideo.removeAttribute('src');
      fdVideo.load();
    });
    dialog.addEventListener('click', (e) => e.target === dialog.firstElementChild && dialog.close());
    $$<HTMLAnchorElement>('[data-fd-cta]').forEach((a) => a.addEventListener('click', () => dialog.close()));
  }

  // ---------- Act VIII · the close: Vee on first focus, then Otto ----------
  const closeForm = $('[data-close-form]');
  let closeSaid = false;
  const ottoClose = (): void => void actor('otto-close')?.speak('act_o4');
  closeForm?.addEventListener('focusin', () => {
    if (closeSaid || prefs.get().hosts === 'hidden') return;
    closeSaid = true;
    const v = actor('vee-close');
    if (!v) return;
    void v.speak('act_v5').then(() => window.setTimeout(ottoClose, 600));
  });

  // ---------- Coda: "One more take?" / "No." ----------
  const vNo = $('[data-offscreen-vee]');
  const coda = $('.coda');
  if (coda && vNo) {
    ScrollTrigger.create({
      trigger: coda,
      start: 'top 60%',
      once: true,
      onEnter: () =>
        window.setTimeout(() => {
          if (prefs.get().hosts === 'hidden') return;
          vNo.classList.add('on');
          void say(draw('act_v6'), { caption: () => undefined, silent: !soundOn() || heard('act_v6') });
        }, 2600),
    });
  }
}
