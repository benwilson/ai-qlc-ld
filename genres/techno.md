# Genre: Techno

## Overview

Techno is minimal, repetitive, and hypnotic. Originating from Detroit and Berlin, it values
precision, restraint, and industrial aesthetics. Lighting should be stark, geometric, and
controlled — darkness is as important as light. Unlike other EDM genres, techno rarely has
a "big drop" moment. Energy evolves slowly through subtle layering.

## BPM Range

- Typical: 125–145 BPM
- Common: 130–138 BPM
- Time signature: 4/4 (relentless four-on-the-floor)

## Energy Profile

Techno energy builds gradually over long arcs (sometimes across an entire set rather than
per track). There are no "drops" in the DnB/dubstep sense — instead, there are moments of
tension and release driven by filter sweeps and layering.

| Section | Energy | Duration | Lighting Character |
|---------|--------|----------|--------------------|
| Opening | Low | 16–32 bars | Near darkness, single element, stark |
| Tension Build | Low–Medium | 16–32 bars | Slowly add fixtures, industrial colors |
| Groove Lock | Medium | 16–64 bars | Sustained hypnotic look, rhythmic movement |
| Filter Build | Medium–High | 8–16 bars | Intensify current look, not change it |
| Release | High | 8–32 bars | Full rig but still controlled, geometric |
| Strip Back | Low–Medium | 8–16 bars | Remove elements, return to minimal |

## Color Palette

### Primary Colors
- **White** (255, 255, 255) — industrial, stark, the signature techno color
- **Deep Red** (200, 0, 0) — Berghain aesthetic, intense but controlled
- **Off/Black** — darkness itself is a "color" in techno. Use it liberally.

### Accent Colors
- **Cool Blue** (0, 0, 200) — cold, industrial, late-night
- **Amber** (255, 128, 0) / Sharpy Amber — warm industrial, vintage feel
- **Minimal Green** (0, 180, 0) — subtle, matrix-like, for accents only

### Two-Color Pairs
| Combo Name | Color A | Color B | Best For |
|------------|---------|---------|----------|
| Berghain | Deep Red | White | Classic techno, high energy |
| Industrial | White | Black (off) | Stark, strobe-like chase |
| Warehouse | Amber | Deep Red | Warm industrial, acid techno |
| Cold Steel | Cool Blue | White | Minimal techno, clean |
| Void | Deep Red | Black (off) | Dark techno, tension |
| Machine | White | Cool Blue | Clinical, precise |
| Monochrome | White (dim) | White (full) | Pure intensity play |

### Avoid
- Bright, saturated rainbow colors (too "festival mainstage")
- Magenta/pink (too "house/disco")
- More than 2 colors at once (techno is minimal — 1 or 2 max)
- Rapid color changes (techno prefers static or slow evolution)

## Movement Conventions

### Release/Peak Movement
- Geometric patterns: straight lines, sharp angles, deliberate movements
- Movers doing synchronized parallel sweeps (all same direction)
- Slow, heavy movements — never fast/chaotic
- Precision is more important than speed

### Groove Sections
- Minimal or no movement
- Movers in a fixed position, letting the color/intensity do the work
- Optional: very slow drift (16–32 bar sweep) barely perceptible
- Static looks sustained for long periods (4–8 bars without change)

### Tension/Build Movement
- Subtle tightening: movers slowly converging to a point
- Or: movers slowly rising (ceiling hit approach) to build tension
- Movement should feel inevitable, not surprising

### Strip Back
- Return to opening position
- Movers converge to center or go dark
- Reduce to single fixture

## Timing Presets

| Preset | FadeIn (ms) | Hold (ms) | Use |
|--------|-------------|-----------|-----|
| Techno Static | 0 | 8000 | Hold look for 4 bars at 128 (sustain!) |
| Techno Slow | 16000 | 0 | 8-bar smooth evolution |
| Techno Very Slow | 32000 | 0 | 16-bar imperceptible fade |
| Techno Beat | 0 | 462 | Beat-synced (1 beat at 130) |
| Techno 2Bar | 4000 | 0 | 2-bar smooth transition |
| Techno Pulse | 0 | 231 | Half-beat industrial pulse |
| Techno Strobe | 0 | 115 | 1/4 beat strobe (rare, use for peak only) |

## Strobe Conventions

- **White only**: Techno strobes are almost always white — color strobes feel wrong
- **Rare and impactful**: Use strobe far less than any other EDM genre
- **Industrial pulse**: Rather than rapid strobe, use a slower on/off pulse (half-beat)
- **Brief**: 2–4 bars at most, then back to controlled looks
- **Fixture strobes preferred**: Use Sharpy/BSW strobe channels for beam-only strobe rather
  than full rig — creates geometric strobe patterns in haze

## Laser Conventions

- **Minimal**: Techno doesn't typically use lasers as heavily as bass music
- **Single color**: If used, one laser color at a time (red preferred for Berghain aesthetic)
- **Static beams**: Lasers as static beams cutting through haze, not patterns or strobes
- **Optional**: Some industrial/hard techno does use lasers aggressively — context-dependent

## Gobo & Prism Conventions

- **Static gobos**: A single gobo held for an entire section creates geometric patterns
- **No rotation**: Static projection is more "techno" than spinning gobos
- **Prism optional**: Single prism for multiplied geometric beams, never both
- **Industrial textures**: Gobo patterns should feel architectural, not decorative

## Par Behavior

- **Release/Peak**: `par_wash()` single color, full intensity for unified impact
- **Grooves**: `par_wash()` at reduced intensity, or all pars off for mover-only looks
- **Tension**: Pars slowly fading up from black
- **Minimal looks**: Often just movers with pars off — embrace the darkness

## Fixture Layering

Techno's visual impact relies entirely on layering movers and pars in a deliberate, architectural
manner. The order and timing of fixture introduction drives tension.

### Mover Precedence
- **Movers are always the primary visual element.** Beams create the spatial geometry that makes
  techno distinctive. A single white beam in haze is more powerful than all pars at full intensity.
- **Introduce movers first during builds** — they establish the architectural space
- **Pars enter afterward** — as support wash or secondary color

### Layering Strategy
1. **Opening/Tension (0–30% energy)**: One mover, white or deep red. Pars off or very dim.
2. **Build (30–60% energy)**: Two movers (parallel or convergent), same color. Introduce pars at
   50% intensity, same color. No color mixing yet.
3. **Groove Lock (40–70% energy)**: Two mover beams (static), pars at 60–80% intensity. Hold this
   look for extended periods (4–16 bars). This is where hypnotic repetition takes over.
4. **Filter Build (60–80% energy)**: Add a third mover or introduce a second color (via movers
   only, not pars). Intensify pars to full. Still geometric — no chaos.
5. **Release/Peak (80–100% energy)**: Full mover array geometric pattern, pars full wash. Color
   pair active (e.g., Berghain red+white). Maximum visual density but still controlled.
6. **Strip Back (30–50% energy)**: Remove one color, reduce mover array to 2 fixtures, dim pars
   or bring to off. Return to minimal state.

### Fixture-Specific Notes
- **Sharpy (movers)**: Primary geometry builders. Use color macro for clean, industrial colors.
  Ch6 (strobe) set to 252 (open) for most looks; save strobe effect for 2–4 bar peaks only.
- **BSW (movers)**: Secondary geometric support. Color wheel (Ch8) for palette variation. Shutter
  (Ch16) at 8 (open) for normal operation; use for strobe accents on industrial sections.
- **Profiles (wash/uplighting)**: Large area coverage. Use for colored backlight or stage wash.
  Dim during minimal sections; use `par_wash()` at single color for cohesion.
- **4BAR (RGB pars)**: Quick color changes via RGB channels. Best for secondary accent, not
  primary wash. Keep dimmed or off in groove sections.
- **Missyees (RGB wash/effect)**: Subtle background tone. Hold a single color for long stretches
  (same as pars). Rarely animate; let movers carry all movement.
- **NI3K (special effects)**: Reserved for climax sections. Lasers or halo only — dim all RGBW
  channels. Use as a "surprise" element late in arc.

## Haze & Atmosphere

Haze is **not optional** in techno lighting design — it is essential. Without haze, the geometric
beam architecture that defines the genre becomes invisible. Haze is the canvas; beams are the paint.

### Haze Philosophy
- **Haze level**: Heavy and consistent. Aim for 70–80% saturation during all sections after opening.
- **Opening**: Light haze (30–40%), builds anticipation for the first beam reveal
- **Tension Build**: Increase haze gradually to 70% as movers enter
- **Groove Lock / Peak**: Heavy haze (75–90%) for maximum beam visibility and geometric impact
- **Strip Back**: Maintain haze at 60–70% even as fixtures dim — the darkness is revealed through haze, not by killing haze
- **Visibility principle**: If you can't see the beam path in haze, the lighting design has failed

### Beam Visibility in Haze
- **White beams**: Most visible in heavy haze; cool blue and amber next best
- **Deep red beams**: Slightly less bright than white but still effective; add intensity (dimmer) to compensate
- **Mover geometry**: Parallel beams, grid intersections, and fan patterns are invisible without haze
  — this is why techno never works in a haze-free environment
- **Distance and depth**: Heavy haze creates perceived depth — beams seem to travel further,
  creating "rooms within rooms" of light and shadow

### Haze & Darkness Ratio
- **Dark-to-light ratio**: Maintain at least 3:1 during groove sections. More darkness = more hypnotic.
  The haze reveals structure in the darkness.
- **Beam cuts**: Position movers so beams cross the performance space, creating angular
  intersections in haze. This is pure geometric architecture.

### Practical Haze Notes
- Haze dissipates over time; refresh continuously during long sets
- Heavy haze + white beam at low intensity = more visible than heavy haze + white beam at high
  intensity with poor positioning
- Amber and red beams in haze create a "warm industrial" feel; white is "cold industrial"
- Haze makes color wheels visible in beams — use gobos and prisms for texture, not for their light
  output, but for their modulation in the haze

## Venue Scale Notes

Techno's "less is more" philosophy scales differently depending on venue size and fixture count.

### Club / Small Venue (1–3 movers, 4 pars)
- **Opening**: 1 Sharpy white, center position. Pars off.
- **Groove**: 2 Sharpys (e.g., parallel beams). Pars at 50% white wash.
- **Peak**: Both Sharpys + color (Berghain red); pars full white.
- **Key technique**: Leverage darkness aggressively. Beam placement and haze matter more than
  fixture count. A single well-placed white beam in haze creates more visual interest than lazy
  pan/tilt chases.

### Mid-Scale / Warehouse (5–8 movers, 10 pars, potential NI3K)
- **Opening**: 1 mover. Pars off.
- **Groove**: 2–3 movers in parallel or grid. Pars at 60% wash.
- **Build**: 4–5 movers entering geometric pattern. Pars at 80%, introduce second color via movers.
- **Peak**: All movers geometric pattern (grid, fan, etc.). Full pars both colors. NI3K lasers optional.
- **Key technique**: Use the full mover array to define geometric rooms. Symmetry creates impact —
  movers mirrored left/right. Slow, synchronized movement across all movers.

### Large Festival / Club (12+ movers, pars everywhere, full NI3K + lasers)
- **Opening**: 1–2 movers, very minimal. Pars off or 20% ambient only.
- **Groove**: 3–4 movers central pattern. Pars at 40% (selective, not full wash).
- **Build**: 6–8 movers entering in sections. Pars layer by area (stage wash, backlight separately).
- **Peak**: Full geometric mover ballet. All pars full. Lasers from NI3K. This is where "precision
  engineering of light" becomes visible.
- **Key technique**: DON'T use all fixtures at once. Hold them back. Introduce movers in phases
  during builds. Techno with a 50-fixture rig that only uses 8 at a time is more powerful than
  using all 50. Restraint at large scale is harder and more impactful.

### Scaling Philosophy
- Small venue: maximize impact per fixture through positioning and timing
- Mid-scale: use geometric patterns with 4–6 fixtures, leave darkness between
- Large scale: use space itself as a design tool; fixtures define areas, not fill areas

## Notable References

### Classic Berghain Aesthetic
- **Venue**: Berghain, Berlin — iconic techno temple
- **Lighting approach**: Minimal fixture count, heavy white beams in haze, geometric precision
- **Lesson**: Restraint and darkness are features, not limitations. A warehouse with 8 white beams
  and strategic darkness can outshine a festival with 200 automated fixtures.

### Charlotte de Witte / Amelie Lens Modern Techno
- **Aesthetic**: Synchronized mover choreography across large rigs, sharp angular movements
- **Timing**: Slower than house/DnB but more movement than classic minimal
- **Color**: White primary, occasional deep red or cool blue accents
- **Lesson**: Modern techno adds choreography without losing geometric precision. Movers work as
  a unified "light orchestra," not as random chase effects.

### Richie Hawtin ENTER. (Ibiza, Pacha)
- **Aesthetic**: Precision-placed fixtures creating grid patterns, rotating geometric shapes
- **Timing**: Extended holds (8+ bars) punctuated by slow architectural transitions
- **Movement style**: Deliberate, synchronized, almost robotic precision
- **Lesson**: Geometry IS the content. A rotating grid of beams is more interesting than elaborate
  color sequences. Light architecture > light effects.

### Harder Subgenres (Hard Techno, Industrial Techno)
- **Color palette**: White + deep red only, maximum contrast, stroboscopic tension
- **Strobe usage**: More frequent than melodic techno, but still restrained — 2–4 bar bursts
- **Movement**: Sharper, less flowing; angular convergence creates menace
- **Fixture layering**: Extreme minimalism in opening, explosive geometric release
- **Laser usage**: More aggressive red lasers cutting through haze; used for "assault" sections
- **Lesson**: Harder subgenres push the limits of restraint — darker, more stripped back, more
  industrial. Even at peak, there's more darkness than light.

### Acid Techno (303, Warm Groove Focus)
- **Color palette**: Amber + warm red (Warehouse pair), occasional teal accents
- **Pacing**: Slightly more movement than classic minimal, follows 303 modulation (filter sweeps)
- **Fixture approach**: Movers follow filter contour — static during locked bass, slow sweep as
  filter opens
- **Lesson**: Color temperature follows energy. Warm palette = warmer, more hypnotic groove.
  Movements should feel organic (flowing) rather than architectural.

### Minimal Techno (Stripped-Back, Meditative)
- **Fixture count used**: Often 1–2 movers, pars off or very dim
- **Timing**: Even longer holds (8–16 bars per look), virtually no animation
- **Color**: Monochrome white only, or white + black (darkness)
- **Philosophy**: The absence of change is the content. Techno audiences sit in darkness with one
  perfect white beam for 10 minutes. This is not boring — it's meditative.
- **Lesson**: True restraint in minimal techno. Less than less.

## Key Philosophy

Techno lighting is about **restraint, geometry, and darkness**. Less is always more. A single
white beam cutting through haze can be more powerful than every fixture at full blast. Hold
looks for longer than feels comfortable — techno audiences appreciate the hypnotic repetition.
Maximum 2 colors at any time. Movements should be deliberate and geometric. The darkness
between the light is as much a design choice as the light itself.

Beams are the primary design element — they create spatial geometry that is invisible without haze.
Haze is mandatory. Pars are secondary support. Movers establish hierarchy through introduction order
during builds. Avoid filling the space; instead, architect it. A 10,000-square-foot warehouse lit
by 8 precisely-positioned white beams is more visually interesting than the same space filled with
diffuse color washes.

Techno is precision engineering of light. Every fixture placement, color choice, timing decision,
and hold duration should feel intentional and inevitable.
