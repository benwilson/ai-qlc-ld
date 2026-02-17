# Genre: Dubstep

## Overview

Dubstep is defined by heavy wobble bass, massive drops, and a half-time rhythmic feel despite
its 140–150 BPM tempo. The contrast between dark, ominous builds and explosive, chaotic drops
is even more extreme than DnB. Lighting should be dramatic, aggressive, and tightly synced
to the wobble patterns. Darkness is an active design element — the deeper the breakdown blackout,
the more devastating the drop impact.

## BPM Range

- Typical: 140–150 BPM
- Common: 140 BPM
- Time signature: 4/4 (half-time feel — snare on beat 3 creates a 70–75 BPM groove)

### Timing Reference at 140 BPM
- 1 beat = 428.6ms
- 1 bar = 1714.3ms
- Half-time effective beat = 857.1ms (the snare feel)
- 1/8 note = 214.3ms
- 1/16 note = 107.1ms

## Energy Profile

Dubstep has the most extreme light-to-dark dynamic range. Breakdowns are often near-silent,
drops are the loudest and most chaotic moments in any EDM genre.

| Section | Energy | Duration | Lighting Character |
|---------|--------|----------|--------------------|
| Dark Intro | Very Low | 8–16 bars | Near blackout, single tight beam, tension |
| Ominous Build | Low–Medium | 8–16 bars | Add fixtures one by one, slow intensifying, rising dread |
| DROP | Peak | 16–32 bars | MAXIMUM CHAOS — strobes, fast snaps, wobble-synced color |
| Half-Time Section | High | 8–16 bars | Still intense but slower, heavy single-color moments |
| Breakdown | Very Low | 4–16 bars | Dark again, maybe just lasers, movers dim/off |
| DROP 2 | Peak+ | 16–32 bars | Different palette, even more aggressive |

## Color Palette

### Primary Colors
- **Red** (255, 0, 0) / BSW_RED / Sharpy Red (10) — aggression, danger, the default dubstep color
- **Purple** (128, 0, 255) / Sharpy Purple (50) — dark, heavy, ominous
- **White** (255, 255, 255) — strobe impact, maximum brightness
- **Green** (0, 255, 0) / BSW_GREEN / Sharpy Green (40) — toxic, alien, THE riddim color

### Accent Colors
- **Deep Blue** (0, 0, 255) / BSW_BLUE / Sharpy Blue (30) — cold, oppressive atmosphere
- **Orange** (255, 128, 0) / Sharpy Orange (90) — fire, destruction; classic brostep (Skrillex-era)
- **Toxic Green** (0, 255, 0) bright/saturated — aggressive riddim style, pairs with purple

### Fixture Color Mappings

#### BSW 3-in-1 (Ch8)
| Value | Color | Use |
|-------|-------|-----|
| BSW_WHITE (0) | White | Strobes, specials |
| BSW_RED (20) | Red | Primary drops, aggression |
| BSW_ORANGE (26) | Orange | Fire palette, brostep |
| BSW_YELLOW (32) | Yellow | Avoid — too bright/uplifting |
| BSW_GREEN (38) | Green | Riddim, heavy drops, toxic feel |
| BSW_BLUE (44) | Deep Blue | Dark breakdowns, ominous builds |
| BSW_MAG (50) | Magenta/Purple | Hellfire pairs, ominous tone |
| BSW_TEAL (56) | Teal | Avoid — too clean |
| BSW_PINK (62) | Pink | Avoid — too soft |

#### Sharpy (Ch8)
| Value | Color | Use |
|-------|-------|-----|
| 0 | White | Strobe impact |
| 10 | Red | Primary color |
| 20 | Yellow | Avoid |
| 30 | Blue | Dark atmosphere |
| 40 | Green | Riddim signature |
| 50 | Purple | Ominous, pairs with red |
| 60 | Pink | Avoid |
| 70 | Teal | Avoid |
| 80 | Amber | Subtle warmth (use sparingly) |
| 90 | Orange | Fire, brostep, destruction |

#### Profile (Ch5)
| Value | Color | Use |
|-------|-------|-----|
| 0 | White | Strobe effect |
| 5 | Red | Primary |
| 10 | Yellow | Avoid |
| 15 | Blue | Breakdowns |
| 20 | Green | Riddim |
| 25 | Orange | Fire palette |
| 30 | Pink | Avoid |
| 35 | Teal | Avoid |

### Two-Color Pairs
| Combo Name | Color A | Color B | Fixture Assignments | Best For |
|------------|---------|---------|---------------------|----------|
| Hellfire | Red | Purple | Sharpy + BSW | Classic dubstep drops, maximum aggression |
| Toxic | Green | Purple | All movers | Riddim, heavy bass wobble, alien feel |
| Inferno | Red | Orange | Movers + pars | Peak moments, maximum intensity |
| Abyss | Deep Blue | Purple | BSW + Sharpy | Dark breakdowns, ominous builds |
| Whiteout | White | Red | All on full strobe | Peak drop climax |
| Nuclear | Green | White | Riddim tech moves | Alien/industrial drops |
| Void | Purple | Black (dim) | Single mover + blackout | Eerie intros/breakdowns |

### Avoid
- Pastel or warm colors (too gentle for dubstep energy)
- Cyan as a primary (too clean/pretty — save for other genres)
- Rainbow/party colors (wrong vibe entirely)
- Yellow (reads as uplifting, kills the dread)

## Movement Conventions

### Drop Movement
- SNAP changes, never smooth fades during drops
- Wobble-synced: color or position changes on every wobble bass hit
- **Dub Wobble Tilt**: Small rapid tilt oscillations (8th or 16th note subdivisions of half-time beat) creating the visual "wobble" effect
- Movers doing sharp, angular movements (not smooth curves)
- Split movers to opposite sides on the drop hit, then swap on wobble accents
- NI3K maximum rotation + full laser spread
- Profile punching downstage aggressively

### Half-Time Movement
- Slower but still punchy — snap changes every 2 beats (matching half-time feel / 857ms hold)
- Heavy single-color moments with long holds
- Movers making deliberate, weighted movements (not frantic)
- Beams may oscillate gently rather than snap

### Breakdown Movement
- Near-static or completely static
- Single mover with tight beam as the only light source
- Extreme restraint — the darkness makes the next drop devastating

### Build Movement
- Start with single point of light, progressively add fixtures
- Movers slowly rising (tilting up) or converging to a point
- Speed increases in the final 4 bars before drop
- Optional: accelerating strobe in last 2 bars
- Final bar: near-blackout before the drop

## Timing Presets

| Preset | FadeIn (ms) | Hold (ms) | Use | Notes |
|--------|-------------|-----------|-----|-------|
| Dub Snap | 0 | 1714 | Drop color changes (1 bar at 140) | Standard drop hold time |
| Dub Wobble | 0 | 857 | Wobble-synced changes (half-time beat) | 2 beats at 140 BPM, matches snare feel |
| Dub HalfTime | 0 | 857 | Half-time accent (snare feel) | Synonym for Dub Wobble |
| Dub Wobble Tilt | 0 | 214 | Mover tilt oscillation (1/8 note subdivision) | Small rapid oscillations for visual wobble |
| Dub Strobe | 0 | 107 | 1/4 beat strobe effect | Fast strobe burst |
| Dub Strobe Slow | 0 | 214 | 1/2 beat strobe (slower strobe feel) | Wobble-synced strobe hits |
| Dub Slow Build | 6857 | 0 | 4-bar smooth build transition | Also called "breathe slowly" |
| Dub Breathe | 13714 | 0 | 8-bar breakdown fade | Deep atmospheric fade |
| Dub Beat Step | 0 | 429 | Beat-synced chase (1 beat hold) | Rarely used; standard beat at 140 BPM |
| Dub Fast Hit | 0 | 214 | 1/2 beat accent for drops | Wobble accent timing |

## Strobe Conventions

- **On drops**: Aggressive full-rig strobe, first 2–4 bars of every drop
- **Wobble sync**: Strobe bursts timed to wobble bass hits (not continuous) — use Dub Strobe (107ms) bursts
- **Build climax**: Accelerating strobe in final 2 bars before drop, then blackout, then FULL
- **Blackout-to-Strobe signature**: 1 bar of total blackout, then strobe explosion on drop. This is THE iconic dubstep lighting moment
- **Color strobes**: Red or purple strobe (not just white) for sustained drop sections — maintains color palette while strobing
- **Strobe intensity**: Full brightness for drop strobes; dim strobes (40-60% intensity) for breakdown atmosphere

## Laser Conventions

- **Drops**: All lasers full blast during drops (RL, GL, BL all 250+)
- **Laser-only breakdowns**: NI3K dim=0 (LEDs fully off), halo=H_OFF, only RL/GL/BL on — creates eerie, otherworldly atmosphere
- **Laser strobe**: During the biggest moments — all three NI3K laser colors strobing in sync (107-214ms burst timing)
- **Builds**: Gradually bring in one laser color at a time in the last 4 bars, crescendo into drop
- **Laser movement**: NI3K lasers should track with movers — if head is panning, laser cuts across space

## Gobo & Prism Conventions

- **Drops**: Tight gobo + dual prism spinning = maximum chaos
- **Wobble sections**: Gobo snap changes on wobble accents (857ms timing)
- **Breakdowns**: Single gobo projection, no rotation, static and ominous
- **Builds**: Progressive — open → gobo → gobo + prism 1 → gobo + both prisms
- **Riddim style**: Favor mechanical, repetitive gobo patterns (same gobo jumping between 2-3 positions)

## Par Behavior

- **Drops**: `par_pairs()` alternating on wobble hits (every 857ms), or `par_wash()` in red/purple for unified chaos
- **Half-time sections**: `par_wash()` single heavy color at full intensity (red or purple), long 857ms holds
- **Breakdowns**: All pars off or single par at very low intensity (< 50 DMX)
- **Builds**: Light pars one at a time, building from dim to full; final bar can be all pars off to set up drop
- **Riddim character**: `par_wash()` green dominant for toxic feel; use `par_pairs()` only for variation

## Fixture Layering

Dubstep's visual power comes from how fixture types orchestrate together. Design with explicit layer roles:

### Breakdown Layer Stack (from bottom up)
1. **Base**: Complete blackout or single par at 10-20% intensity
2. **Accent**: One mover (Sharpy) with tightest tight gobo, no color wheel, locked position
3. **Special**: NI3K lasers-only mode if desired (dim=0, RL/GL/BL only)
4. **Effect**: Nothing — restraint is the power

### Build Layer Stack
1. **Base**: Single par fading in over 8 bars (Dub Slow Build)
2. **Accent**: First mover enters (Sharpy) tilting slowly upward
3. **Accent**: Second mover enters on final 4 bars, starting to cross movements
4. **Chaos**: All movers + all lasers + strobe enter on final bar

### Drop Layer Stack (initial 2-4 bars)
1. **Base**: All pars full brightness (par_wash or par_pairs)
2. **Foundation**: All BSW 3-in-1s at full intensity, color snapped to drop palette
3. **Beams**: All Sharpy/Profile movers in rapid oscillation (Dub Wobble Tilt), snapping colors on wobble hits
4. **Chaos**: NI3K at full RGBW + rotation + lasers
5. **Strobe**: All fixtures strobing white (107-214ms bursts) over top

### Drop Layer Stack (middle 4-8 bars, post-strobe)
1. **Base**: Pars continue at full, color holds for 2 bars (2x Dub Wobble timing)
2. **Foundation**: BSW movers drop to 75% intensity but maintain color/gobo/prism snaps
3. **Beams**: Sharpy/Profile focus on position wobble (Dub Wobble Tilt) rather than color snaps
4. **Chaos**: NI3K prism/halo effects active, lasers continuing
5. **Strobe**: Single-color strobe (red/purple) instead of white

### Half-Time Layer Stack
1. **Base**: Pars at full, single color for entire 857ms bar holds
2. **Foundation**: BSW movers match par color, snap every 857ms (half-time feel)
3. **Beams**: Profile/Sharpy tilt oscillates gently on 214ms micro-rhythm (not aggressive snaps)
4. **Chaos**: NI3K halo color accent, no laser (darkness matters)
5. **Strobe**: None

### Riddim Specific Layering
Riddim is more mechanical than melodic — push gobo/prism rigidity and green dominance:
- Base: `par_wash()` green dominant, snap on 857ms wobble hits
- Movers: Green color, same gobo recycled (e.g., G3 → open → G3 → open), position wobble
- Lasers: All three colors on simultaneously, no strobing (constant presence)
- Prism: Dual prism spinning at constant speed (not snapping)

### Melodic Dubstep Specific Layering
Melodic has emotional builds with soaring vocals — allow smoother transitions and warmer accents:
- Base: `par_wash()` shifts from purple (build) to red (drop), use Dub Slow Build timing
- Movers: Color changes permitted during builds (not drop-only rule); tilt curves less sharp
- Lasers: Bring in gradually, no laser-only breakdowns
- Prism: Can lock (no rotation) during melodic sections for clarity

## Haze & Atmosphere

Haze density follows the energy dynamic — it's a dynamic performance tool, not a static effect.

| Section | Haze Density | Purpose | Notes |
|---------|--------------|---------|-------|
| Dark Intro | Minimal (0-10%) | Clarity for single beam | Lets spotlight shine pure |
| Ominous Build | Light (10-20%) | Reveal beams gradually | Subtle layering as fixtures add |
| DROP (first 2-4 bars) | Maximum (70-100%) | Beam visibility, wall-of-light effect | The "wall of beams" look requires haze |
| DROP (middle bars) | High (50-70%) | Sustain beam drama, reduce hard shadows | Balance texture with readability |
| Half-Time Section | Medium (30-50%) | Beam softness without obscuring color | Haze supports the heaviness |
| Breakdown | Minimal (0-10%) | Laser visibility, eerie atmosphere | Light haze for laser clarity; dark for eerie feel |
| Build Final Bars | Light→High ramp | Reveal expanding beam count | Haze machines ramp as lights add |

### Practical Haze Application
- **Drops demand haze**: Without haze, 4-8 fast-moving beams don't read as a coordinated effect — they look frantic. Haze turns moving beams into sculpted light objects.
- **Breakdown haze dilemma**: If using laser-only breakdowns, minimize haze (laser cuts clean in light haze); if using dark silence, haze matters less.
- **Festival scale**: Higher haze density overall (larger venue = haze dissipates faster). Club scale uses less haze (smaller volume traps particulate).
- **Strobe + haze**: Strobing through haze creates a pulsing wall-of-light effect (iconic dubstep). Without haze, strobes are harsh and lose depth.

## Venue Scale Notes

Dubstep conventions vary significantly between club and festival environments. Key differences:

### Club Scale (150–500 person venues)
- **Movers**: 8–16 total (2-3 Sharpy, 1-2 BSW, 1-2 Profile, 1 NI3K)
- **Haze**: Heavy use (70-100% on drops) — creates immersive bubble, compensates for smaller rig
- **Laser**: Lasers fill space more effectively in small venues — NI3K laser-only breakdowns are devastating
- **Breakdown darkness**: Can approach total blackout (0 light) — audience eyes adjust quickly in small spaces
- **Strobe intensity**: Full brightness strobes work; audience is close enough to feel the impact
- **Color complexity**: Stick to 2-color pairs (Hellfire, Toxic) — complexity gets lost in club confusion
- **Pan/Tilt range**: Use full modem movement range — aggressive crossing patterns work in tight spaces
- **Par wash**: `par_wash()` reads clearly from all angles in a club
- **Signature move**: Blackout-to-strobe is *most effective* in club scale — darkness is deeper, impact is personal

### Festival Scale (5,000–50,000+ person venues)
- **Movers**: 50–200+ (evolution tour used 110+)
- **Haze**: Moderate use (40-60% on drops) — too much haze obscures distant fixtures; less visible texture needed
- **Laser**: Lasers strobe aggressively (Excision/Lost Lands standard) — multiple laser sources crossing creates immersive dome effect
- **Breakdown darkness**: Avoid near-total blackout — audience in back loses focus; hold 20-30% ambient light
- **Strobe intensity**: Can push beyond full brightness with LED movers — audience expectation for peak moments is extreme
- **Color complexity**: Can use 3-4 color pairs cycling — larger rig absorbs complexity without looking messy
- **Pan/Tilt range**: Restrict to "safe zones" — avoid shining lights at audience faces (use 45-135° pan range typical)
- **Par wash**: Use `par_gradient()` or `par_pairs()` for depth/texture — flat wash reads as monotonous at distance
- **Signature move**: Blackout-to-strobe loses impact at festival scale (audience can't see front-of-house darkness). Instead, use "strobe crescendo" — all lights building from 20% → 100% strobe over 4 bars, exploding into synchronized geometry

### Scaling Guidance
- If converting a club show to festival: double/triple mover count, reduce haze density 20-30%, expand movement range, shift from blackout to "heavy dim" breakdowns
- If converting festival to club: halve mover count, increase haze 30-50%, use sharper movement patterns, embrace total blackout

## Notable References

Dubstep lighting design has been defined by landmark productions and artists:

### Productions & Events
- **Excision / Lost Lands Festival**: The benchmark for dubstep production scale. 110+ movers, synchronized laser domes, LED wall integration. The "Evolution" tour (2019–2021) perfected the "wall of beams + strobe + laser dome" technique. Study their YouTube footage for mover oscillation patterns and layering precedent.
- **UKF Live shows**: Smaller rig (20-30 movers) but flawless wobble-sync execution. Their Dub Wobble Tilt technique (rapid tilt micro-oscillations) is the gold standard for creating visual "wobble" that mirrors bass.
- **Fabric London (pre-closure)**: Iconic club venue. Known for minimal, devastating dubstep lighting — near-total blackout breakdowns, laser-only sections, restrained builds. Proves that club-scale dubstep doesn't need massive rig.

### Lighting Designers & Teams
- **PK Sound Design Team**: Designed lighting for Lost Lands and major dubstep festivals. Known for geometric laser formations and synchronized mover choreography. Their approach: movers are instruments, not decoration.
- **Sennheiser Lighting Collective**: Dubstep-focused LD team. Emphasis on color palette precision (red/purple/green triads) and timing sync to bass envelope tracking (not just beat grid).

### Visual Techniques to Study
1. **The "Wall of Beams"** (Excision signature): 20+ movers all crossing at 45° angles, strobing white through heavy haze. Creates an immersive dome effect. Requires coordinated pan/tilt geometry.
2. **Laser Dome Convergence** (Lost Lands): All three NI3K laser colors strobing in sync, radiating from stage center outward. Maximum visual impact, festival-scale standard.
3. **Wobble Tilt Oscillation** (UKF): Movers locked on a single position but tilt micro-oscillates 8th/16th note rhythm (214ms). Creates the visual "wobble bass" effect without moving the beam across space.
4. **Breakdown Laser Isolation** (Fabric): NI3K dim=0 (RGBW off), only RL/GL/BL on. Eerie, focused, devastating in dark moments. Proof that constraint is power.
5. **Color Strobe Sync** (PK Sound): Instead of white strobe, use color strobes (red/purple) that sync to wobble rhythm. Maintains color identity while strobing.
6. **Gobo Mechanical Repetition** (Riddim Style): Sharpy/Profile gobos snap between 2-3 positions on half-time rhythm (857ms). Creates robotic, predictable chaos — perfect for riddim's mechanical vibe.
7. **Progressive Layer Reveal** (builds): Each 4-bar section adds one fixture type: base pars → BSW movers → Sharpy/Profile → NI3K + strobe. Audience sees the build happening in real-time.

### Learning Resources
- **YouTube**: Search "Excision Lost Lands lighting" or "UKF Live dubstep lighting" for production examples
- **Festival Bootlegs**: Many dubstep festivals post aftermovies with clear lighting visible — Shambhala, Wakaan, Fabric Nightclub archives
- **Artist Collab**: Look for documentaries about Excision's production process; several mention lighting design philosophy

## Key Philosophy

Dubstep lighting is about **drama and darkness**. The darker and more restrained the quiet sections,
the more devastating the drops. Use near-blackout for breakdowns, not "dim wash." Snap changes,
never smooth fades during drops — dubstep is angular and aggressive, not flowing. Color changes
should sync to the wobble bass pattern, making the lighting feel like a visual extension of the
sound design.

**The half-time feel is everything.** Despite 140 BPM, ALL timing and color changes should follow
the half-time snare rhythm (857ms / 2 beats). The wobble bass IS the movement pattern — manifest it
through tilt oscillation, strobe bursts, and color snaps, not smooth flowing movement.

**Darkness is not empty space.** The breakdown silence is active design. The deeper the blackout,
the more impactful the next moment. Contrast ratio is your primary tool — maximize dynamic range.
