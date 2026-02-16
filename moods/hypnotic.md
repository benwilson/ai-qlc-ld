# Mood: Hypnotic

## Overview

Repetitive, trance-inducing, mesmerizing. Light patterns should lock into a rhythm and
hold it — the audience's eyes following predictable, repeating movements until they lose
themselves in the pattern. Think pendulum swing, spiraling tunnel, a single light pulsing
in perfect sync with a relentless kick drum.

Use when: deep grooves, repetitive sections, rolling basslines, minimal/hypnotic techno,
rolling DnB, any sustained rhythmic section where the music locks into a groove.

## Category

emotional

## Visual References

- A pendulum swinging in a dark room — predictable, rhythmic, mesmerizing
- The spiraling tunnel sequence from Vertigo — pulling you deeper
- A single candle flame — flickering in perfect rhythm, impossible to look away from

## Color Scheme

- **Type**: monochromatic
- **Rationale**: Monochromatic keeps visual focus on the pattern and rhythm rather than
  color variation. One hue in varying intensity creates the trance state.

## Color Filtering

- **Temperature bias**: Neutral to cool. Avoid warm colors that "wake you up."
- **Saturation preference**: Medium. Enough color to be visible but not so intense it demands
  attention. The pattern is the focus, not the color.
- **Palette selection**: From the genre's two-color pairs, prefer pairs with similar tones
  (blue/cyan, purple/blue) over high-contrast pairs (red/white). Subtle variation within
  a color family.
- **Preferred colors**: Blues, cyans, purples, teals. Monochromatic schemes work well —
  different shades of the same hue.
- **Max simultaneous colors**: 1–2. Keep the color story simple so the pattern is the star.
- **Par behavior override**: Pars in a slow, repeating chase pattern synced to the beat.
  `par_chase()` at 1-beat or 2-beat speed. The chase IS the hypnotic element for pars.

## Intensity Modifiers

- **Base brightness**: 60% of genre default. Moderate — enough to see clearly, not so bright
  it breaks the trance state.
- **Contrast ratio**: Low-medium. Smooth, repeating intensity variations. No sudden jumps —
  the predictability is the point.
- **Blackout frequency**: Very rare. Blackouts break the hypnotic loop. Avoid them.
- **Number of fixtures active**: Medium. Enough to create the pattern, not so many that it's
  chaotic. 3–4 fixtures in a coordinated pattern.
- **Dimmer behavior**: Gently pulsing 40–70% range, synced to the beat or a multiple of it.
  The pulse should be subtle enough to feel subliminal.

## Movement Modifiers

- **Speed multiplier**: 1.0x genre default, but LOCKED TO BPM. Movement must be perfectly
  beat-synced — this is critical for hypnotic mood. Off-beat movement breaks the spell.
- **Width preference**: Medium. Consistent sweep width — the same arc every time. Predictable,
  repeating paths.
- **Movement style**: Smooth, repeating loops. PingPong sweeps, figure-8 patterns, circular
  motion. The same path, over and over. Smooth transitions, never angular.
- **Position hold time**: Brief between movements (the loop should be near-continuous).
- **Preferred positions**: Sweep paths — LR Sweep (PingPong), Narrow LR, Diamond. Any
  repeating path. Avoid static positions (no movement = no hypnosis).

## Effect Density

- **Strobe**: None. Strobe breaks the hypnotic state.
- **Lasers**: Minimal. If used, NI3K in slow pan sweep creating a sweeping laser line. The
  laser becomes part of the pattern.
- **Gobos**: Optional. A single rotating gobo at slow, constant speed adds mesmerizing
  texture. The rotation must be beat-synced or at a constant mathematical relationship to
  the BPM.
- **Prism**: Optional. Slow, constant prism rotation creates spiraling beam patterns that
  are inherently hypnotic. Single prism only.
- **Frost**: Avoid. Hard beams with visible movement paths are more hypnotic than soft washes.
- **Haze**: Medium. Enough to see the beam patterns clearly.

## Timing Modifiers

- **Fade speed**: 1.0x genre default, but MUST BE beat-locked. Every transition should be
  an exact number of beats.
- **Exception**: None. Everything is beat-locked. No freeform timing.
- **Hold duration**: 1.0x genre default, beat-locked. Even holds are exact beat multiples.
- **Chase speed**: 1.0x genre default, beat-locked. Chases at 1-beat, 2-beat, or 1-bar
  intervals. Never off-beat.
- **Loop behavior**: Everything should loop (RunOrder: Loop or PingPong). No SingleShot.
  The repetition is the point.

## Energy Curve

- **Baseline**: Medium. Hypnotic mood maintains a steady, sustained energy.
- **Peak scaling**: 80% of genre peak. Don't go to full peak — that breaks the trance.
  Peaks should feel like the groove intensifying, not breaking.
- **Rise time**: Very slow. Energy rises so gradually it's barely perceptible.
- **Fall time**: Very slow. Energy reduces equally gradually.
- **Sustain**: Maximum. Hypnotic mood is about sustaining a state, not changing it.

## Genre Interaction Notes

- **DnB**: Excellent for rolling DnB sections. Lock par chase to the breakbeat pattern.
  Movers in slow PingPong sweep. Suppress drop chaos — keep the groove locked.
- **Dubstep**: Difficult pairing. Only works for deep/minimal dubstep. Suppress all wobble-
  synced behavior. Use the half-time feel as the hypnotic pulse.
- **House**: Natural pairing. House's steady groove + hypnotic mood = pure dancefloor
  hypnosis. Lock everything to the four-on-the-floor kick.
- **Techno**: Perfect pairing. Techno IS hypnotic. Reinforce the repetition — same look
  sustained for 16–32 bars, subtle variations only. Minimal color changes.
- **Trance**: Natural for the extended groove sections. Suppress the emotional build/release
  in favor of sustained hypnotic state. Works best for the mid-track groove, not breakdowns.
