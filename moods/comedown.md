# Mood: Comedown

## Overview

Gradually reducing, cooling off, winding down. Light should feel like the morning after —
energy slowly draining away, intensity fading, the room returning to normal. The audience
should feel a gentle release of tension, like exhaling after holding your breath. Think
post-drop recovery, last few tracks of the night, sunrise at an afterparty.

Use when: after a peak section, transition between bangers, final tracks of a set, the
gradual wind-down at end of night, any time the energy needs to consciously decrease.

## Category

energy

## Visual References

- Sunrise at an afterparty — the energy fading as daylight creeps in
- The last embers of a campfire — still warm, slowly dimming
- Post-rain calm — everything washed clean, quiet, settling

## Color Scheme

- **Type**: analogous (narrowing)
- **Rationale**: Start with whatever scheme the peak used, progressively narrow to analogous
  and then monochromatic as energy reduces. The color palette simplifies as things wind down.

## Color Filtering

- **Temperature bias**: Cooling. Start at whatever temperature the previous section used,
  shift progressively toward cooler tones. Warm → neutral → cool over the comedown duration.
- **Saturation preference**: Decreasing. Start at full saturation, progressively desaturate.
  Colors should "fade" like a sunset dimming.
- **Palette selection**: Transition from the genre's high-energy pair toward its
  lowest-energy pair. If coming out of a peak, start with the peak colors and gradually
  shift to the coolest, softest pair.
- **Preferred colors**: Transition from bright/warm to cool/muted. End on soft blues, muted
  purples, or warm-but-dim ambers.
- **Max simultaneous colors**: Decreasing. Start with 2–3 (leftover richness from the peak),
  reduce to 1.
- **Par behavior override**: Pars gradually dimming. Start at 80% (still warm from peak),
  fade to 30–40% in a muted color. Transition from `par_wash()` bright to `par_wash()` soft.

## Intensity Modifiers

- **Base brightness**: Decreasing. Start at 80% of genre default, end at 30%.
- **Contrast ratio**: Decreasing. Start with medium contrast, end with minimal. As the
  comedown progresses, the dynamic range compresses toward "quiet."
- **Blackout frequency**: None. No jarring blackouts during comedown — smooth fades only.
  Let the light fade gently without shocking the eye.
- **Number of fixtures active**: Decreasing. Start with all fixtures, remove one every 4–8
  bars. End with 1–2 fixtures providing ambient glow.
- **Fixture density**: Decreasing — remove fixtures one at a time, starting with effects
  (lasers, strobes) then movers then pars. This creates a graceful descent rather than an
  abrupt drop.
- **Key-to-fill ratio**: Starts at 2:1, ends at 5:1 — light becomes more focused and isolated
  as energy drops. Early in the comedown, maintain some directional interest. By the end,
  the fill should dominate, creating a soft, intimate glow.
- **Dimmer behavior**: Gradually ramping down. Dimmers decrease by 10–15% every 4–8 bars.

## Movement Modifiers

- **Speed multiplier**: Decreasing. Start at 1.0x genre default, end at 0.3x. Movements
  slow down as energy fades.
- **Width preference**: Narrowing. Start wide (leftover from peak), gradually converge
  toward center. The room "shrinks" as energy reduces.
- **Movement style**: Transitioning from the peak's style to smooth, gentle drift. Angular
  movements soften into curves. Fast snaps become slow sweeps.
- **Position hold time**: Increasing. Start at 1x genre default, end at 3x. Movements
  become less frequent.
- **Preferred positions**: Converge sweep path (wide → center). Start with whatever
  positions the peak used, gradually come home to center.

## Effect Density

- **Strobe**: Rapidly decreasing. If the peak used strobe, kill it within the first 4 bars
  of comedown. No strobe after that.
- **Lasers**: Decreasing. If the peak used lasers, reduce to single color, then off. Lasers
  should be off by the midpoint of comedown.
- **Gobos**: Remove. Transition to open beam early in the comedown. Clean, simple light.
- **Prism**: Remove. Kill prism in the first 4–8 bars. Return to clean single beams.
- **Frost**: Add. As the comedown progresses, add frost to soften beams. The light should
  get softer as energy decreases.
- **Haze**: Decreasing — let haze thin naturally as energy drops, start at heavy, end at
  light. The haze removal parallels fixture removal, creating an open, breathing space.

## Timing Modifiers

- **Fade speed**: Increasing. Start at 1x genre default, end at 3x (slow, gentle fades).
  Transitions become progressively slower and smoother.
- **Exception**: None. Everything slows down through the comedown.
- **Hold duration**: Increasing. Start at 1x, end at 3x. Changes become less frequent.
- **Chase speed**: Decreasing. Chases slow down and eventually stop. End with no active
  chases.

## Energy Curve

- **Baseline**: Falling. Comedown mood IS a falling energy curve.
- **Peak scaling**: Decreasing from 80% to 30% of genre peak over the comedown duration.
- **Rise time**: N/A — comedown doesn't rise.
- **Fall time**: This IS the fall. Typically 8–32 bars depending on genre and context.
- **Sustain**: None during the fall. Once the comedown reaches its target low energy, it
  either sustains there (transition to chill mood) or the next build begins.

## Progression Template

| Stage | Bars | Intensity | Colors | Fixtures | Movement | Effects |
|-------|------|-----------|--------|----------|----------|---------|
| Early | 1–8 | 80% → 60% | Peak colors fading | All | Fast → Medium | Kill strobe, reduce lasers |
| Mid | 9–16 | 60% → 40% | Shifting cooler | Remove 1–2 | Medium → Slow | Kill lasers, remove gobo/prism |
| Late | 17–24 | 40% → 30% | Cool, muted | 2–3 fixtures | Slow → Drift | Add frost, clean beams |
| Floor | 25+ | 30% stable | Single soft color | 1–2 fixtures | Near-static | None, soft glow only |

## Effect Removal Order (Critical)

The ORDER of effect removal matters — this creates a graceful descent rather than a jarring
drop:

1. **Strobe off first** (bars 1–4) — Removes the most aggressive element immediately
2. **Lasers off** (bars 5–8) — Red/green/blue lasers dark, room feels calmer
3. **Gobos/prisms off** (bars 9–12) — Return to clean, open beams
4. **Reduce mover count** (bars 13–20) — Remove movers one at a time
5. **Reduce par intensity** (bars 17–24) — Pars dim gradually
6. **Final single fixture** (bars 25+) — End with one soft beam, usually a par at 30–40%

This sequence ensures the space feels like it's breathing, not getting strangled.

## Genre Interaction Notes

- **DnB**: After a drop, the comedown is 8–16 bars. Rapid fixture reduction — from full rig
  to 2 fixtures in 8 bars. Kill lasers and strobe immediately. End on a single blue wash.
- **Dubstep**: Similar to DnB but can be more abrupt. The drop ends, darkness returns.
  Comedown can be as short as 4 bars — snap to near-blackout, then gentle glow.
- **House**: Longer, smoother comedown (16–32 bars). Gradual dimming, warm colors cooling.
  The groove continues at lower energy. End on soft amber wash.
- **Techno**: Comedown is about removing layers. Strip fixtures one at a time over 16 bars.
  Return to single beam or minimal look. Techno comedowns can be very long.
- **Trance**: The comedown after the release is bittersweet. 16–32 bars of gentle fading.
  Colors cooling from euphoric warm to reflective cool. End with a single soft blue or
  purple, setting up for the next section or the outro.
- **Melodic Techno**: Elegant decline over 20–24 bars. Emphasize color cooling and smooth
  mover paths. Remove strobes and effects early, let fixtures fade gradually with emphasis
  on melodic elements.
- **Psytrance**: Hypnotic descent over 16–20 bars. Slow the repetitive movement patterns.
  Reduce laser intensity gradually. Let the hypnotic elements fade to silence naturally.
- **Liquid DnB**: Smooth, melodic comedown over 16–20 bars. Emphasize warm colors cooling.
  Remove effects early but let movers make graceful closing sweeps. End on soft, warm glow.
- **Future Bass**: Emotional resolution over 16–24 bars. Color temperature should cool from
  the emotional peak warmth. Movers should make final elegant sweeps. Pars should fade to
  a single intimate wash. This is the resolution of the emotional arc.
- **Hardstyle**: Relatively quick comedown (8–12 bars) as the hardstyle kick intensity
  drops. Rapid fixture and effect removal. But still smooth — no jarring blackouts. Snap to
  cooler colors. End on near-silence with minimal light.
