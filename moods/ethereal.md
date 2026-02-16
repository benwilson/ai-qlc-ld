# Mood: Ethereal

## Overview

Dreamy, floating, otherworldly. Light should feel like it exists independent of the room —
shafts of color drifting through space, slow movements that seem to breathe on their own.
The audience should feel weightless, transported. Think sunrise over clouds, bioluminescent
ocean, cathedral light through stained glass.

Use when: melodic and atmospheric sets, ambient intros, emotional breakdowns, liquid DnB,
deep/progressive house, uplifting trance breakdowns.

## Category

emotional

## Visual References

- Sunrise seen from above the clouds — soft light filtering through mist
- Underwater bioluminescence — gentle organic glowing in deep blue-black water
- Cathedral light through stained glass — colored shafts drifting through dusty air

## Color Scheme

- **Type**: analogous
- **Rationale**: Adjacent colors on the wheel (blue→cyan→teal or purple→blue→cyan) create
  smooth, harmonious blends that feel unified and dreamlike.

## Color Filtering

- **Temperature bias**: Cool-to-neutral. Prefer cool colors but allow soft warm accents.
- **Saturation preference**: Medium-low. Slightly washed out or pastel feels more ethereal
  than full saturation. For RGB fixtures, mix in some white to desaturate (e.g., (100, 150, 255)
  instead of (0, 0, 255)).
- **Palette selection**: From the genre's two-color pairs, prefer pairs with blue, cyan, teal,
  or purple. Avoid any pair containing red or orange.
- **Preferred colors**: Soft blues, cyans, teals, lavender purples, pale pinks, cool whites.
- **Max simultaneous colors**: 2–3. Ethereal mood allows more color blending than most moods —
  layered washes create depth.
- **Par behavior override**: Pars at medium intensity creating ambient fill. Use `par_gradient()`
  or `par_wash()` for soft, enveloping color. Pars are essential to the ethereal feeling —
  they fill the space that movers can't reach.

## Intensity Modifiers

- **Base brightness**: 50% of genre default. Soft, not dim. The room should glow, not hide.
- **Contrast ratio**: Low. Smooth transitions between brightness levels. No harsh jumps
  from dark to bright.
- **Blackout frequency**: Very rare. Blackouts break the dreamlike state. Instead, fade to
  a minimal glow (10–15% single color wash) for "quiet" moments.
- **Number of fixtures active**: Medium-high. More fixtures at lower intensity creates a
  richer, more enveloping atmosphere than fewer fixtures at high intensity.
- **Dimmer behavior**: Keep all fixtures in the 30–60% range. Full intensity is too harsh.
  Even peak moments should max around 75%.

## Movement Modifiers

- **Speed multiplier**: 0.4x genre default. Very slow, drifting movements. Movers should
  feel like they're floating, not being driven.
- **Width preference**: Wide. Movers spread across the room creating a broad wash of light.
  Avoid tight convergence — it feels too focused for ethereal.
- **Movement style**: Smooth curves only. No angular movements, no snaps, no sharp changes.
  Long, sweeping arcs. Figure-8 and circular patterns.
- **Position hold time**: Short holds between long smooth transitions. The light should
  always be moving, even if barely perceptibly.
- **Preferred positions**: Wide sweeps (LR Sweep, Diamond), Ceiling Hit (beams through haze),
  spread positions (SL+SR). Avoid Audience Blinder entirely.

## Effect Density

- **Strobe**: None. Zero strobe in ethereal mood. Strobe shatters the dreamlike state.
- **Lasers**: None or minimal. If used, single color at low intensity as a subtle accent.
  Never strobing lasers.
- **Gobos**: Optional. Soft, organic gobo patterns (not sharp geometric) with very slow
  rotation creates beautiful texture in haze. Think flowing water or dappled light.
- **Prism**: Optional. Single prism with slow rotation creates multiplied drifting beams.
  Beautiful in haze.
- **Frost**: Yes. Frost on movers softens beams from hard points to gentle washes. This is
  the signature look of ethereal mood.
- **Haze**: Essential at medium density. Too thick and it becomes soup; too thin and the
  beams don't float.

## Timing Modifiers

- **Fade speed**: 3x genre default (much slower fades). Everything crossfades over long
  periods. A color change should take 4–8 bars, not 1.
- **Exception**: None. Even "impact" moments should be softened to smooth transitions.
- **Hold duration**: 0.5x genre default (shorter holds). Light should always be in motion
  between states — never sitting static.
- **Chase speed**: 0.3x genre default. Any chases should be barely perceptible slow drifts.

## Energy Curve

- **Baseline**: Medium-low. Ethereal mood maintains a gentle, consistent glow.
- **Peak scaling**: 50% of genre peak. Ethereal mood never gets loud — peaks are "brighter"
  and "wider" rather than "more intense."
- **Rise time**: Very slow. Energy rises over 16–32 bars, not 4–8.
- **Fall time**: Very slow. Energy fades down equally gently. No sudden drops.
- **Sustain**: Medium. Ethereal mood prefers constant gentle evolution over sustained states.

## Genre Interaction Notes

- **DnB**: Liquid DnB and atmospheric DnB pair beautifully. Suppress the aggressive drop
  behavior — ethereal DnB drops should "bloom" rather than "hit." Use rolling bass timing.
- **Dubstep**: Unusual pairing — melodic dubstep or chillstep only. Completely suppress
  wobble-synced behavior. Treat drops as gentle arrivals.
- **House**: Perfect match for deep and progressive house. Already smooth genre + ethereal
  mood = peak dreamy atmosphere. Extend all fade times to maximum.
- **Techno**: Works for ambient/dub techno. Suppress the industrial/stark aesthetic, lean
  into the hypnotic qualities. Soft rather than hard.
- **Trance**: Excellent for breakdowns and emotional sections. Trance's sweeping movements
  + ethereal's slow speed = gorgeous floating light. Apply heavily during breakdowns.
