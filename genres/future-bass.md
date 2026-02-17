# Future Bass

## Overview

Future bass is vivid, emotional, and youthful—born from the intersection of trap, dubstep, and pop. Characterized by bright saturated RGB colors, emotional builds with soaring vocals, and explosive but beautiful drops. The signature sound features "supersaw" chords that shimmer and half-time grooves. Lighting mirrors this duality: both aggressive wobble sections and intimate vocal breakdowns within the same track. The aesthetic is neon-driven, embracing the full color spectrum with heavy color cycling during peaks. Notable artists: Flume, San Holo, Illenium, Said The Sky, Dabin.

## BPM Range

- **Typical**: 140–150 BPM
- **Range**: 130–160 BPM
- **Half-time feel**: Lighting syncs to half-time groove, creating sense of space and power despite fast underlying tempo

## Energy Profile

| Section | Duration | Energy | Intensity | Color Shift | Movement | Strobe | Notes |
|---------|----------|--------|-----------|-------------|----------|--------|-------|
| Intro | 8–16 bars | 20–30% | Subtle | Gradual warm→cool | Minimal, slow converge | Off | Atmospheric setup; soft colors building anticipation |
| Vocal Build | 8–16 bars | 40–70% | Moderate | Smooth primary shift | Slow spread from center | Rare, rare strobes | Emotional climb; soaring melody drives intensity |
| Drop | 16–32 bars | 90–100% | Maximum | Fast primary ↔ accent cycle | Medium sweeps every 2–4 beats | Frequent | All fixtures, vivid colors, shimmering effect |
| Chop Section | 4–8 bars | 80–95% | High | Bright, static or rapid snap | Fast position snaps per chop | Tight pulse | Rapid retriggered elements; flashes match chop rhythm |
| Breakdown | 8–16 bars | 40–60% | Moderate | Intimate, single color | Slow or held center position | Off | Vocal spotlight; reduced fixture count |
| Second Drop | 16–32 bars | 95–100% | Maximum | Different palette, rainbow moments | Fast, aggressive sweeps | Very frequent | Bigger, more effects; color explosion |

## Color Palette

### Primary Colors (3)
1. **Magenta** — RGB: (255, 0, 200) | BSW: 50 (Magenta) | Sharpy: 50 (Purple) | Profile: 50 (split red/mag)
   - The signature future bass anchor. Emotional, energetic, saturated. Use constantly.

2. **Cyan** — RGB: (0, 200, 255) | BSW: 56 (Teal) | Sharpy: 70 (Teal) | Profile: 35 (Teal)
   - Cool counterpoint to magenta. Creates the vivid neon duality. Strobe cyan for maximum pop.

3. **White** — RGB: (255, 255, 255) | BSW: 0 (White) | Sharpy: 0 (White) | Profile: 0 (White)
   - Cleanliness, clarity, emphasis. Use for peaks and emotional moments. Blends all colors.

### Accent Colors (3)
4. **Purple** — RGB: (150, 0, 255) | BSW: 50 (Magenta blend toward purple) | Sharpy: 50 (Purple) | Profile: 50 (split red/mag)
   - Moody, slightly darker than magenta. Good for builds and transitions.

5. **Pink** — RGB: (255, 80, 150) | BSW: 62 (Pink) | Sharpy: 60 (Pink) | Profile: 30 (Pink)
   - Soft, emotional, youthful. Pairs well with blue/cyan. Use during vocal sections and breakdowns.

6. **Blue** — RGB: (0, 60, 255) | BSW: 44 (Blue) | Sharpy: 30 (Blue) | Profile: 15 (Blue)
   - Deep, cool, contrasting. Strobe blue with magenta for intense drops. Good in chop sections.

### Two-Color Pairs (6–8)

1. **Magenta ↔ Cyan** (primary duality)
   - Strobe or fast fade between these for maximum future bass signature
   - Use during main drops and intense sections
   - Most effective on movers (sharp transitions)

2. **Pink ↔ Blue** (emotional duality)
   - Slower fade, more intimate
   - Perfect for vocal builds and breakdown sections
   - Good for par washes during emotional moments

3. **Purple ↔ Cyan** (brooding to bright)
   - Transitions between moody build and explosive drop
   - Use during section transitions
   - Effective on moving lights to create direction

4. **Magenta ↔ Orange** (warm neon)
   - Trapped-out feel, energetic shift
   - Good for chop sections and wobble moments
   - Pairs well with faster movement

5. **White + Magenta** (clarity + emotion)
   - White base with magenta accent
   - Use for emphasis and peak moments
   - Movers white, pars magenta for depth

6. **Pink ↔ Cyan** (soft neon)
   - Gentler version of magenta ↔ cyan
   - Emotional drops and second-verse builds
   - Good for intimate moments with color still present

7. **Rainbow Cycle** (full spectrum moment)
   - Prog through: Red → Orange → Yellow → Green → Cyan → Blue → Magenta → White
   - Reserve for peak moments (second drop finale, climax)
   - Use all fixtures; coordinate with maximum movement
   - Typically 8–16 bars duration

8. **Orange ↔ Blue** (warm-cool contrast)
   - Aggressive, less common than magenta/cyan
   - Good for wobble/aggressive sections
   - Use with fast movement and strobes

### Avoid
- **Dark red/brown**: Feels muddy, conflicts with magenta saturation
- **Yellow (standalone)**: Too cheerful, clashes with future bass melancholy
- **Lime green**: Garish, unprofessional, rarely used except for special effects
- **Desaturated/pastel colors**: Future bass demands vivid, saturated RGB — pale colors kill the aesthetic
- **Monochrome white-only**: Boring, wastes the genre's color potential

## Movement Conventions

### Intro (0–30% energy, 8–16 bars)
- **Movers**: Minimal movement, slow converge to stage center (over 8 bars)
- **Pans**: Subtle slow spreads, 180° span
- **Speed**: `smooth(bpm, 4)` — slow, contemplative
- **Position targets**: DSL→Center, SR→Center (gradual gathering)

### Vocal Build (30–70% energy, 8–16 bars)
- **Movers**: Slow, deliberate spread outward as melody rises
- **Pans**: Widen over 16 bars, reaching wide positions by peak
- **Speed**: `smooth(bpm, 3)` — medium, following vocal arc
- **Position targets**: Ceiling Hit (spotlight feeling), side positions (DSL, SR)
- **Key**: Movement should feel **uplifting** and **expansive**, matching the vocal soar

### Drop (90–100% energy, 16–32 bars, half-time groove)
- **Movers**: Medium-fast sweeps synced to chord changes (every 2–4 beats in half-time)
- **Pans**: Wide position traversals, sharp direction changes
- **Speed**: `beat_step(bpm, 0.5)` to `beat_step(bpm, 1)` — every half-bar or full bar
- **Position targets**: Full stage grid (DSL, DS Center, DSR, Ceiling Hit, audience blinder)
- **Pattern**: Figure-8 or randomized grid walk; never static
- **Key**: Feel of **shimmering**, **cascading**, **energetic** — match color shifting

### Chop Section (80–95% energy, 4–8 bars)
- **Movers**: Rapid position snaps, 4–8 per bar
- **Pans**: Flip between opposite sides in sync with chop rhythm
- **Speed**: `beat_step(bpm, 0.125)` — snap every 8th note (in half-time, = 16th notes of original)
- **Position targets**: 2–3 alternating strong positions (Ceiling Hit ↔ Floor Center, DSL ↔ SR)
- **Key**: **Tightness**, **precision** — flashes match vocal chop exactly

### Breakdown (40–60% energy, 8–16 bars)
- **Movers**: Slow converge to single position or slow oscillation
- **Pans**: Centered or subtle drifts (±45° from center)
- **Speed**: `smooth(bpm, 4)` to `smooth(bpm, 8)` — very slow, intimate
- **Position targets**: Center (Floor Center, Ceiling Center), or slow oscillation between DSL ↔ SR
- **Key**: **Reduced fixture count** (spotlight feeling); **intimate** but still colorful
- **Color emphasis**: Single primary color (pink, white, or blue) with slow crossfades

### Second Drop (95–100% energy, 16–32 bars, often with new section structure)
- **Movers**: Faster than first drop, more aggressive sweeps
- **Pans**: Wide, unpredictable traversals, diagonal paths
- **Speed**: `beat_step(bpm, 0.5)` to `beat_step(bpm, 0.25)` — every half-bar or quarter-bar
- **Position targets**: Full stage; include off-axis positions (audience blinder, rear ceiling)
- **Key**: **Build-up** to this — use it for maximum impact. More **chaos**, more **color variety**

## Timing Presets

Calculated for BPM range 130–160 (reference: 140 BPM).

| Timing Name | Bars | BPM 130 (ms) | BPM 140 (ms) | BPM 150 (ms) | BPM 160 (ms) | Use Case |
|------------|------|--------------|--------------|--------------|--------------|----------|
| snap | 1/4 | 461 | 429 | 400 | 375 | Chop sections, rapid color flashes |
| fast_pulse | 1/2 | 923 | 857 | 800 | 750 | Strobe timing, quick crossfades |
| beat_accent | 1 | 1846 | 1714 | 1600 | 1500 | Main pulse, color change per beat (half-time) |
| half_bar | 2 | 3692 | 3429 | 3200 | 3000 | Mover sweep sync to chord (every 2 beats half-time) |
| bar_accent | 4 | 7385 | 6857 | 6400 | 6000 | Major position change, emotion peak |
| smooth_build | 8 | 14769 | 13714 | 12800 | 12000 | Intro/breakdown/vocal build, slow crossfade |
| phrase | 16 | 29538 | 27429 | 25600 | 24000 | Section transition, full emotional arc |

## Strobe Conventions

- **Intro**: Off (atmospheric)
- **Vocal Build**: Rare, subtle strobes on peak moments only (1–2 per 8 bars)
- **Drop**: Frequent but not constant
  - Magenta strobe: Every 4 beats (half-time), quick (150–200 ms on, 100 ms off)
  - Cyan strobe: Alternate bars with magenta, creates neon flicker
  - White strobe: Peak moments only (every 16 bars max)
- **Chop Section**: Tight pulse strobes in sync with chop (every 8th note original BPM)
  - Use on movers and pars simultaneously for impact
- **Breakdown**: Off (intimate, even if colors present)
- **Second Drop**: Heavy strobe (more frequent than first drop, shorter pulses)
  - Magenta + Cyan strobing in rapid alternation = maximum pop
  - White strobe for emphasis on climactic moments

### Strobe Values by Fixture
- **Sharpy** (Ch6): `SHARPY_OPEN` (252) = no strobe. `SHARPY_STROBE_SLOW` (80), `SHARPY_STROBE_MED` (120), `SHARPY_STROBE_FAST` (160)
- **BSW** (Ch16): `BSW_SHUT_OPEN` (8) = no strobe. `BSW_SHUT_STROBE_SLOW` (30), `BSW_SHUT_STROBE_FAST` (100)
- **Profile** (Ch1): 0 = open. 16–50 = slow strobe, 50–131 = fast strobe
- **4BAR** (Ch2): 0 = off. Strobe ranges TBD (test fixture)

## Laser Conventions

- **Intro**: Off (preserve atmosphere)
- **Vocal Build**: Off or very subtle (laser point, no motion, green only)
- **Drop**: Active, frequent laser moments
  - Alternating red and green during color transitions for visual depth
  - Laser sweeps in sync with mover movement (parallel motion)
  - Typical: Red laser on beat 1, Green laser on beat 3 (every 2 beats half-time)
  - Hold for 2–4 beats, then blackout 1 beat for breathing room
- **Chop Section**: Laser off (movers already snapping rapidly, laser adds too much chaos)
- **Breakdown**: Off or extremely subtle (single color point, not rotating)
- **Second Drop**: Highly active
  - Rapid laser color alternation (red ↔ green every beat half-time)
  - Can use blue laser sparingly for color variety
  - Laser rotation/strobe on final 8-bar climax

### Laser Values (NI3K)
- **Red laser** (Ch14): `LASER_OFF` (0), `LASER_STROBE_SLOW` (100), `LASER_STROBE_MED` (160), `LASER_ON` (250)
- **Green laser** (Ch15): Same as red laser
- **Blue laser** (Ch16): Same as red laser (use sparingly)

## Gobo & Prism Conventions

- **Intro**: Open (no gobos/prisms) for clarity
- **Vocal Build**: Slow gobo rotate, single gobo (G1 or G2) on movers
  - BSW: `BSW_G1_OPEN` (0–7) through `BSW_G2_6` (53–61), rotation off
  - Sharpy: Open gobo (Ch10 = 0)
  - Purpose: Texture without distraction
- **Drop**: Multiple gobos rotating in sync with movement
  - BSW: Gobo 2 (Ch10) with rotation (Ch11) set to fast CCW (Ch11 = 220)
  - Sharpy: Open (no gobo wheel on knockoff)
  - Prism on for sparkle effect (BSW Ch13 = 128 for 3-facet; rotation Ch14 = 200 for spin)
  - Purpose: "Shimmering" effect during drops
- **Chop Section**: Open gobos, prism on with fast rotation
  - Creates visual "strobe-like" effect without actual strobe
- **Breakdown**: Open (intimacy, focus on color)
- **Second Drop**: Heavy prism use with rotation, multiple gobos
  - Gobo 1 + Gobo 2 both rotating (BSW only has Gobo 2, but use it heavily)
  - Prism rotation at max speed for maximum shimmer

### Gobo Values (BSW)
- **Gobo 1** (Ch9): 0–7 = open, 8–16 = G1, 17–25 = G2, 26–34 = G3, 35–43 = G4, 44–52 = G5, 53–61 = G6, 62–67 = G7
- **Gobo 2** (Ch10): 0–7 = open, 8–16 = G1, 17–25 = G2, 26–34 = G3, 35–43 = G4, 44–52 = G5, 53–61 = G6
- **Gobo 2 Rotation** (Ch11): 0–127 = index, 128–189 = CCW fast→slow, 194–255 = CW slow→fast (use 220 for CCW mid-speed)

### Prism Values (BSW)
- **Prism** (Ch13): 0–7 = off, 8–255 = 3-facet prism engaged
- **Prism Rotation** (Ch14): 0–127 = index (static position), 128–189 = CCW fast→slow, 194–255 = CW slow→fast (use 200 for CW medium speed)

## Par Behavior

### Intro (soft, unified)
- **Pattern**: `par_wash()` — all 6 pars same soft color (white or light pink)
- **Dimmer**: 60–70% (atmospheric presence, not bright)
- **Purpose**: Establish emotional foundation

### Vocal Build (building cohesion)
- **Pattern**: `par_wash()` with smooth color transition (white → pink → blue over 16 bars)
- **Dimmer**: Ramp 70% → 90% as melody builds
- **Purpose**: Unite the space, guide energy upward

### Drop (maximum color energy)
- **Pattern**: `par_pairs()` or `par_gradient()` with primary drop colors (magenta + cyan)
  - **Option A** (`par_pairs()`): P1+P3 magenta, P2+P4 cyan, missyees split (e.g., M1 magenta, M2 cyan)
  - **Option B** (`par_gradient()`): 4BAR gradient magenta → white → cyan, missyees split complementary
- **Dimmer**: 100% (maximum presence)
- **Color cycle**: Sync color change with `beat_accent` timing (every 1 bar = 2 beats half-time)
- **Purpose**: Full saturation, maximum visual impact

### Chop Section (energetic texture)
- **Pattern**: `par_chase()` — one par per bar, cycling through primary colors (magenta → cyan → purple → magenta)
- **Dimmer**: 100%
- **Timing**: `snap` (every 1/4 bar = every chop accent in half-time feel)
- **Purpose**: Energetic, fragmented, matches vocal chop

### Breakdown (intimate and focused)
- **Pattern**: `par_wash()` single color (pink, blue, or white)
- **Dimmer**: 50–70% (step back, let movers dominate)
- **Color**: Slow fade-in-place (no cycling); pick one accent color for emotional consistency
- **Purpose**: Spotlighting feeling, color as emotional anchor

### Second Drop (explosive and varied)
- **Pattern**: Mix `par_gradient()` with occasional `par_chase()` sequences
  - Bars 1–4: Gradient magenta → white → cyan (slow hold)
  - Bars 5–8: Chase sequence (rapid color cycling all 4 pars)
  - Bars 9–16: Return to gradient, possibly shifted palette (pink → blue instead)
- **Dimmer**: 100%
- **Color cycle**: Faster than first drop (`half_bar` timing, every 0.5 bars = 1 beat half-time)
- **Rainbow finale**: Last 4–8 bars before next section = full rainbow cycle on all pars
- **Purpose**: Variety, climax building, showcase all colors

## Fixture Layering

### Depth Hierarchy (strongest to weakest)
1. **Movers** (Sharpy, BSW, Nausea Inducer 3K) — Movement, color, strobes. Primary focus.
2. **4BAR/Pars** (4BAR, Missyee RGB) — Color wash, support movers. Secondary.
3. **Profile** (Knockoff) — Gobo work, accent color hits, texture. Tertiary.
4. **Lasers** (NI3K only) — Punctuation, not background. Use sparingly.

### Typical Fixture Assignment

| Section | Primary | Secondary | Accent | Special |
|---------|---------|-----------|--------|---------|
| Intro | Sharpy + BSW (slow movers) | 4BAR (soft wash) | Profile (texture, low intensity) | Lasers off |
| Vocal Build | Sharpy + BSW (spreading) | 4BAR (color transition) | NI3K (laser point, no motion) | Gobo rotation |
| Drop | Sharpy + BSW (fast sweeps) + NI3K (mover or laser) | 4BAR + Missyee (color cycle) | Profile (gobo + prism shimmer) | Lasers active |
| Chop | Sharpy + BSW + NI3K (all snapping) | 4BAR (strobe support) | Profile (off) | Lasers off |
| Breakdown | Single mover (Sharpy or BSW, centered) | 4BAR (single color, dim) | Profile (off) | Lasers minimal/off |
| Second Drop | All movers + NI3K (chaos + lasers) | All pars (gradient + chase) | Profile (heavy gobo rotation) | Lasers rapid color change |

### Color Coordination
- **Movers + Pars same color**: Creates visual unity, impact (e.g., all magenta drop)
- **Movers + Pars complementary**: Creates visual depth (movers magenta, pars cyan)
- **Movers + Lasers sync**: Laser color matches mover color, moves in parallel

## Haze & Atmosphere

- **Intro**: Minimal or no haze (clarity, intimacy)
- **Vocal Build**: Light haze, 20–30% machine output (builds sense of scale as melody rises)
- **Drop**: Heavy haze, 70–100% (gobo/prism projections become visible, color saturation heightened)
- **Chop**: Heavy haze maintained (rapid position snaps create visual streaks in haze)
- **Breakdown**: Reduce to 30–50% (softer, more intimate)
- **Second Drop**: Maximum haze, 100% (color beams cut through, gobo patterns projected across space)

**Haze syncs with energy, not triggered per-beat.** Gradual machine ramp, not strobed.

## Venue Scale Notes

### Small Venue (<2000 capacity, e.g., 150–300 people)
- **Movers**: 2–3 total (e.g., Sharpy × 1, BSW × 2)
- **Pars**: 1 × 4BAR + 2 × Missyee (RGB)
- **Simplify movement**: Use fewer positions, simpler paths (DSL ↔ SR basic alternation)
- **Focus on color cycle**: Small venues = intimate, so color changes are primary visual driver
- **Laser use**: Minimal (can overwhelm small space)

### Medium Venue (2000–5000 capacity, e.g., 500–1500 people)
- **Movers**: 3–4 total (e.g., Sharpy × 2, BSW × 2)
- **Pars**: Multiple 4BAR units or more Missyee fixtures
- **Movement**: Full position grid (DSL, DS Center, DSR, Ceiling Hits)
- **Balanced approach**: Movers + pars equally important
- **Laser use**: Moderate (red + green alternating, active during drops)

### Large Venue (>5000 capacity)
- **Movers**: 6+ total (maximum variety: Sharpy, BSW, NI3K, Profile)
- **Pars**: Extensive rig (multiple 4BAR, many Missyee)
- **Movement**: Complex choreography, diagonal paths, off-axis positions
- **Full expression**: Every fixture type active, full chaos during peaks
- **Laser use**: Heavy (all colors, rapid alternation)

## Notable References

- **Illenium (Trilogy, Ember)** — THE benchmark. Emotional builds with pin-point intensity, massive drops with color explosion, integration of pyro and movement. Study the Trilogy set for breakdown intimacy and first-drop color restraint before second-drop saturation.
- **San Holo** — Magenta-heavy aesthetic, bright neons, frequent color cycling. Excellent example of sustained saturation without fatigue.
- **Flume** — More artistic/abstract, often uses unconventional color choices (heavy pink/purple), understated but precise movement. Less is more; focus quality over quantity.
- **Said The Sky / Dabin** — Emotional vocal integration, soft blues and pinks in breakdowns, explosive magenta/cyan drops. Good balance of intimacy and spectacle.
- **Deadmau5 progressive house** — While different genre, the slow build and color transition philosophy is useful for future bass vocal sections.

## Key Philosophy

**Future bass is about feeling and color.** The vivid RGB palette and emotional dynamics define the genre — lighting should prioritize saturation, smooth builds, and strategic explosions over constant movement. Color cycling is more important than rapid position changes; a held mover position with magenta ↔ cyan flashing reads louder than unmotivated sweeps.

**Vocal moments = intimate.** Reduce fixture count and movement during vocal breakdowns, even if colors remain. This creates emotional focus and makes drops feel bigger by contrast.

**Drops = shimmer.** Fast color cycling + gobo/prism rotation + pulsing movement. The "supersaw" sound has a floating, shimmering quality — lighting should mirror this with overlapping cycles (movers on one rhythm, pars on another, creating visual interference).

**Half-time syncs are crucial.** Because the genre sits at 140–150 BPM but feels slower, sync timing to half-time feel (every 2 beats original = 1 beat half-time). A beat_accent every 2 beats original (1 beat half-time) will feel locked in; every 1 beat original will feel rushed.

**Neon is the color, not the effect.** Avoid chasing and chase effects in busking; instead use smooth crossfades between vivid colors. Future bass audiences expect RGB saturation, not color wheel rotation. Future bass is "bold color choices," not "fast color changes." When color cycles happen, they should feel intentional and emotional, synced to song structure, not just fast for speed's sake.

**Lastly, restraint. More movers ≠ better. A single Sharpy in magenta with a slow pan toward center during a vocal breakdown reads louder than three movers spinning frantically.**
