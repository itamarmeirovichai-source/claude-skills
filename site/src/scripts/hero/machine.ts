// Hero state machine: a pure reducer (state, event) → { state, effects }. No DOM, no timers here.
// boot → idle → pointing → enlarging → playing → asking → reaching → revealed (+ fallback).

export type Dir = 'L' | 'R' | 'C';

export type State =
  | { s: 'boot' }
  | { s: 'fallback' }
  | { s: 'idle'; picks: number }
  | { s: 'pointing'; film: number; picks: number }
  | { s: 'enlarging'; film: number; picks: number }
  | { s: 'playing'; film: number; picks: number }
  | { s: 'asking'; film: number; picks: number }
  | { s: 'reaching'; picks: number }
  | { s: 'revealed'; picks: number };

export type Event =
  | { e: 'READY' }
  | { e: 'FAIL' }
  | { e: 'NUDGE' }
  | { e: 'SELECT'; film: number; dir: Dir }
  | { e: 'POINT_PEAK' }
  | { e: 'ENLARGED' }
  | { e: 'FILM_END' }
  | { e: 'CLOSE' }
  | { e: 'PICK_ANOTHER' }
  | { e: 'CONTINUE' }
  | { e: 'REACH_DONE' }
  | { e: 'LEFT_HERO'; via: 'skip' | 'scroll' }
  | { e: 'BACK_TO_TOP' };

export type Clip =
  | 'char_idle'
  | 'char_point_L'
  | 'char_point_R'
  | 'char_point_C'
  | 'char_talk'
  | 'char_reach'
  | 'char_nod'
  | 'char_think'
  | 'char_stepin';

export type Effect =
  | { fx: 'otto'; clips: Clip[] } // play in sequence; last one loops if it is idle/talk
  | { fx: 'say'; line: string; silent?: boolean }
  | { fx: 'hush' }
  | { fx: 'ring'; run: boolean }
  | { fx: 'enlarge'; film: number }
  | { fx: 'filmPlay'; film: number }
  | { fx: 'dock' }
  | { fx: 'shrink' }
  | { fx: 'pullUp' }
  | { fx: 'revealDone'; focus: boolean }
  | { fx: 'nudgeTimer'; on: boolean }
  | { fx: 'pulseButtons' }
  | { fx: 'track'; name: string; props?: Record<string, string | number> };

export interface Step {
  state: State;
  fx: Effect[];
}

const PICK_LINES = ['vo_pick_1', 'vo_pick_2', 'vo_pick_3'] as const;
export const pickLine = (picks: number): string => (picks >= 1 ? 'vo_pick_again' : (PICK_LINES[picks % 3] ?? 'vo_pick_1'));

const point = (film: number, dir: Dir, picks: number, fromStage: boolean): Step => ({
  state: { s: 'pointing', film, picks: picks + 1 },
  fx: [
    { fx: 'nudgeTimer', on: false },
    ...(fromStage ? [{ fx: 'shrink' } as const] : []),
    { fx: 'ring', run: false },
    { fx: 'otto', clips: [`char_point_${dir}`] },
    { fx: 'say', line: pickLine(picks) },
    { fx: 'filmPlay', film }, // primes the film inside the click gesture (unlocks sound)
    { fx: 'track', name: 'ad_select', props: { film, dir } },
  ],
});

const reveal = (picks: number, via: 'skip' | 'scroll'): Step => ({
  state: { s: 'revealed', picks },
  fx: [
    { fx: 'nudgeTimer', on: false },
    { fx: 'ring', run: false },
    ...(via === 'skip' ? [{ fx: 'say', line: 'vo_skip' } as const] : []),
    { fx: 'revealDone', focus: false },
    { fx: 'track', name: via === 'skip' ? 'skip_click' : 'hero_scrolled' },
  ],
});

export function reduce(state: State, ev: Event): Step {
  const same: Step = { state, fx: [] };
  switch (state.s) {
    case 'boot':
      if (ev.e === 'READY')
        return {
          state: { s: 'idle', picks: 0 },
          fx: [{ fx: 'otto', clips: ['char_idle'] }, { fx: 'ring', run: true }, { fx: 'say', line: 'vo_idle', silent: true }, { fx: 'nudgeTimer', on: true }],
        };
      if (ev.e === 'FAIL') return { state: { s: 'fallback' }, fx: [{ fx: 'track', name: 'hero_fallback' }] };
      if (ev.e === 'LEFT_HERO') return same;
      return same;

    case 'fallback':
      return same;

    case 'idle':
      switch (ev.e) {
        case 'NUDGE':
          return { state, fx: [{ fx: 'otto', clips: ['char_think', 'char_idle'] }, { fx: 'say', line: 'vo_nudge', silent: true }] };
        case 'SELECT':
          return point(ev.film, ev.dir, state.picks, false);
        case 'CONTINUE':
          return { state: { s: 'reaching', picks: state.picks }, fx: [{ fx: 'nudgeTimer', on: false }, { fx: 'ring', run: false }, ...reachFx()] };
        case 'LEFT_HERO':
          return reveal(state.picks, ev.via);
        default:
          return same;
      }

    case 'pointing':
      switch (ev.e) {
        case 'POINT_PEAK':
          return {
            state: { s: 'enlarging', film: state.film, picks: state.picks },
            fx: [{ fx: 'enlarge', film: state.film }, { fx: 'otto', clips: ['char_nod', 'char_idle'] }],
          };
        case 'CONTINUE':
          return { state: { s: 'reaching', picks: state.picks }, fx: [{ fx: 'shrink' }, ...reachFx()] };
        case 'LEFT_HERO':
          return { ...reveal(state.picks, ev.via), fx: [{ fx: 'shrink' }, ...reveal(state.picks, ev.via).fx] };
        default:
          return same; // ignore extra input while the point plays
      }

    case 'enlarging':
      switch (ev.e) {
        case 'ENLARGED':
          return { state: { s: 'playing', film: state.film, picks: state.picks }, fx: [{ fx: 'track', name: 'ad_play', props: { film: state.film } }] };
        case 'CONTINUE':
          return { state: { s: 'reaching', picks: state.picks }, fx: [{ fx: 'shrink' }, ...reachFx()] };
        case 'LEFT_HERO':
          return { ...reveal(state.picks, ev.via), fx: [{ fx: 'shrink' }, ...reveal(state.picks, ev.via).fx] };
        default:
          return same;
      }

    case 'playing':
    case 'asking':
      switch (ev.e) {
        case 'FILM_END':
        case 'CLOSE':
          if (state.s === 'asking') return same;
          return {
            state: { s: 'asking', film: state.film, picks: state.picks },
            fx: [{ fx: 'dock' }, { fx: 'otto', clips: ['char_talk'] }, { fx: 'say', line: 'vo_ask' }, { fx: 'pulseButtons' }],
          };
        case 'PICK_ANOTHER':
          return {
            state: { s: 'idle', picks: state.picks },
            fx: [{ fx: 'hush' }, { fx: 'shrink' }, { fx: 'otto', clips: ['char_idle'] }, { fx: 'ring', run: true }, { fx: 'say', line: 'vo_idle', silent: true }],
          };
        case 'SELECT':
          return point(ev.film, ev.dir, state.picks, true);
        case 'CONTINUE':
          return { state: { s: 'reaching', picks: state.picks }, fx: [{ fx: 'shrink' }, ...reachFx()] };
        case 'LEFT_HERO':
          return { ...reveal(state.picks, ev.via), fx: [{ fx: 'shrink' }, ...reveal(state.picks, ev.via).fx] };
        default:
          return same;
      }

    case 'reaching':
      if (ev.e === 'REACH_DONE')
        return {
          state: { s: 'revealed', picks: state.picks },
          fx: [{ fx: 'otto', clips: ['char_idle'] }, { fx: 'revealDone', focus: true }, { fx: 'track', name: 'continue_done' }],
        };
      return same;

    case 'revealed':
      if (ev.e === 'BACK_TO_TOP')
        return {
          state: { s: 'idle', picks: state.picks },
          fx: [{ fx: 'otto', clips: ['char_stepin', 'char_idle'] }, { fx: 'ring', run: true }, { fx: 'say', line: 'vo_idle', silent: true }, { fx: 'nudgeTimer', on: true }],
        };
      if (ev.e === 'SELECT') return point(ev.film, ev.dir, state.picks, false);
      return same;

    default: {
      const never: never = state;
      return never;
    }
  }
}

function reachFx(): Effect[] {
  return [
    { fx: 'hush' },
    { fx: 'otto', clips: ['char_reach'] },
    { fx: 'say', line: 'vo_continue' },
    { fx: 'pullUp' },
    { fx: 'track', name: 'continue_click' },
  ];
}
