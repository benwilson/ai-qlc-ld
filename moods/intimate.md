# Mood: Intimate

## Overview

Close, personal, warm, small-feeling. Light should make a big room feel like a small one —
pools of warm light, tight focus areas, the space between people shrinking. The audience
should feel connected, like they're sharing a private moment. Think candlelit bar, late-night
conversation, the moment a DJ plays a track just for you.

Use when: vocal-heavy tracks, quiet moments between bangers, deep house grooves, the DJ
talking to the crowd, b2b moments between artists.

## Category

emotional

## Visual References

- A candlelit dinner — warm pools of amber light, soft shadows
- A jazz club at midnight — smoky, warm, the spotlight barely reaching the edges
- Campfire in the woods — faces lit by warm glow, darkness just beyond reach

## Color Scheme

- **Type**: monochromatic
- **Rationale**: A single warm hue (amber or warm white) in varying intensities creates
  the simplest, most intimate feeling. Multiple colors create visual complexity that
  fights the closeness.

## Color Filtering

- **Temperature bias**: Warm. Strongly prefer warm colors — ambers, warm whites, soft pinks.
- **Saturation preference**: Low-medium. Soft, approachable colors. Nothing harsh or
  electric. Colors should feel like firelight, not neon.
- **Palette selection**: From the genre's two-color pairs, prefer pairs with amber, warm
  white, pink, or soft colors. Avoid pairs with cold blues or harsh whites.
- **Preferred colors**: Amber (255, 128, 0), warm white (255, 200, 150), soft pink
  (255, 150, 130), gold (255, 200, 50), muted red (200, 50, 30).
- **Max simultaneous colors**: 1–2. Keep it simple and warm. A single warm wash is often
  perfect.
- **Par behavior override**: Pars at medium intensity (40–60%) in warm tones. `par_wash()`
  for unified warmth. Pars create the intimate ambient fill that wraps around the audience.

## Intensity Modifiers

- **Base brightness**: 40% of genre default. Moderate-low. Enough to see faces, not so
  bright it feels clinical.
- **Contrast ratio**: Very low. Subtle brightness variations. Everything stays in a narrow,
  comfortable range.
- **Blackout frequency**: None. Blackouts are too dramatic and break the intimate connection.
  Minimum brightness is a soft warm glow (15–20%).
- **Number of fixtures active**: Medium. 3–4 fixtures creating overlapping pools of warm
  light. Not too many (overwhelming) or too few (sparse/cold).
- **Dimmer behavior**: 30–60% range. Moderate brightness that feels comfortable and inviting.

## Movement Modifiers

- **Speed multiplier**: 0.3x genre default. Very slow, gentle movements.
- **Width preference**: Narrow. Movers converged close to center or DJ booth position.
  The light should feel like it's drawing people closer together, not pushing apart.
- **Movement style**: Smooth, gentle, almost imperceptible. Small movements within a tight
  area. Like breathing — subtle expansion and contraction.
- **Position hold time**: 2x genre default. Long, comfortable holds. No urgency.
- **Preferred positions**: Center (community), DJ Booth (connection with performer),
  Narrow LR sweep (gentle). Avoid Audience Blinder (hostile), wide spreads (too open),
  Ceiling Hit (too dramatic).

## Effect Density

- **Strobe**: None. Strobe is the opposite of intimate. It pushes people apart.
- **Lasers**: None. Lasers are a spectacle — intimate is not a spectacle.
- **Gobos**: Optional. A soft gobo pattern (no sharp edges) can add warmth and texture.
  Static only, no rotation.
- **Prism**: None. Too much visual complexity.
- **Frost**: Yes. Heavy frost on all movers. Soft pools of light, not hard beams. Intimate
  mood is about softness and warmth.
- **Haze**: Light. Just enough atmosphere to soften the edges. Heavy haze creates drama;
  intimate mood avoids drama.

## Timing Modifiers

- **Fade speed**: 3x genre default (slow, gentle fades). Colors shift so gradually you
  barely notice.
- **Exception**: None. Everything moves gently.
- **Hold duration**: 2x genre default. Lingering, comfortable holds.
- **Chase speed**: 0.25x genre default. Any chase is glacially slow.

## Energy Curve

- **Baseline**: Low-medium. Comfortable, sustained warmth.
- **Peak scaling**: 50% of genre peak. Even the "brightest" intimate moment feels personal,
  not overwhelming.
- **Rise time**: Slow. Gentle brightening over 8–16 bars.
- **Fall time**: Slow. Gentle dimming, never abrupt.
- **Sustain**: Maximum. Intimate mood is about sustaining a feeling, not changing it.

## Genre Interaction Notes

- **DnB**: Unusual but works for deep/liquid DnB with vocals. Suppress all drop behavior.
  Warm wash, minimal movement, let the vocals shine.
- **Dubstep**: Very rare. Only for the most melodic, vocal-heavy dubstep intros. Not for
  drops or wobble sections.
- **House**: Natural pairing. Deep house + intimate = perfect late-night club moment. Warm
  ambers and soft pinks. `par_wash()` in gold. Movers at DJ Booth for "spotlight on the
  moment" feeling.
- **Techno**: Unusual but works for deeper, more soulful techno. Replace the industrial
  aesthetic with warmth. Amber and warm white palette.
- **Trance**: Works for breakdowns with vocals. The intimate moment before the release.
  Pull everything in close, warm it up, then let the euphoric release blow it wide open.
