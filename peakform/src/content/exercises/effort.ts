import type { FailurePolicy } from '../types';

// Shared stop rules, so every exercise describes effort the same way.

export const EFFORT_RULE: Record<FailurePolicy, string> = {
  all: 'When the plan says to failure, end the set on the last rep you can finish with clean form. No cheating, bouncing, or grinding out a rep.',
  last: 'Stop one rep short of failure on the first sets. On the last set, go to the last rep you can finish with clean form. No cheating or grinding.',
  never: 'Stop at the prescribed reps in reserve. This exercise is never taken to failure, because a failed rep is hard to escape safely when you train alone.',
};

export const PAIN_RULE =
  'Pain of 4 out of 10 or higher, or pain that worsens or changes your technique, pauses this exercise. Report it to a parent, coach, or clinician.';

/** Jumps, hops, and bounds are power work: every rep at full speed with a quiet landing. */
export const QUALITY_RULE =
  'Quality first, never to failure. End the set as soon as jump height, speed, or landing control drops, even if reps are left.';
