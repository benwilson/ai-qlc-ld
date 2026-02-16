# Genre: Dubstep

## Overview

Dubstep is defined by heavy wobble bass, massive drops, and a half-time rhythmic feel despite
its 140–150 BPM tempo. The contrast between dark, ominous builds and explosive, chaotic drops
is even more extreme than DnB. Lighting should be dramatic, aggressive, and tightly synced
to the wobble patterns.

## BPM Range

- Typical: 140–150 BPM
- Common: 140 BPM
- Time signature: 4/4 (half-time feel — snare on beat 3 creates a 70–75 BPM groove)

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
- **Red** (255, 0, 0) / BSW Red / Sharpy Red — aggression, danger, the default dubstep color
- **Purple** (128, 0, 255) / Sharpy Purple — dark, heavy, ominous
- **White** (255, 255, 255) — strobe impact, maximum brightness

### Accent Colors
- **Green** (0, 255, 0) / BSW Green / Sharpy Green — toxic, alien, good for riddim/heavy dubstep
- **Deep Blue** (0, 0, 255) / BSW Blue / Sharpy Blue — cold, oppressive atmosphere
- **Orange** (255, 64, 0) / Sharpy Orange — fire, destruction, contrast with dark palette

### Two-Color Pairs
| Combo Name | Color A | Color B | Best For |
|------------|---------|---------|----------|
| Hellfire | Red | Purple | Classic dubstep drops |
| Toxic | Green | Purple | Riddim, heavy bass |
| Inferno | Red | Orange | Maximum aggression |
| Abyss | Deep Blue | Purple | Dark breakdowns, builds |
| Whiteout | White | Red | Peak drop impact |
| Nuclear | Green | White | Alien/industrial drops |
| Void | Purple | Black (dim) | Ominous intros/breakdowns |

### Avoid
- Pastel or warm colors (too gentle for dubstep energy)
- Cyan as a primary (too clean/pretty — save for other genres)
- Rainbow/party colors (wrong vibe entirely)

## Movement Conventions

### Drop Movement
- SNAP changes, never smooth fades during drops
- Wobble-synced: color or position changes on every wobble bass hit
- Movers doing sharp, angular movements (not smooth curves)
- Split movers to opposite sides on the drop hit, then swap on wobble accents
- NI3K maximum rotation + full laser spread
- Profile punching downstage aggressively

### Half-Time Movement
- Slower but still punchy — snap changes every 2 beats (matching half-time feel)
- Heavy single-color moments with long holds
- Movers making deliberate, weighted movements (not frantic)

### Breakdown Movement
- Near-static or completely static
- Single mover with tight beam as the only light source
- Extreme restraint — the darkness makes the next drop devastating

### Build Movement
- Start with single point of light, progressively add fixtures
- Movers slowly rising (tilting up) or converging to a point
- Speed increases in the final 4 bars before drop
- Optional: accelerating strobe in last 2 bars

## Timing Presets

| Preset | FadeIn (ms) | Hold (ms) | Use |
|--------|-------------|-----------|-----|
| Dub Snap | 0 | 1714 | Drop color changes (1 bar at 140) |
| Dub Wobble | 0 | 857 | Wobble-synced changes (2 beats) |
| Dub HalfTime | 0 | 857 | Half-time accent (snare feel) |
| Dub Strobe | 0 | 107 | 1/4 beat strobe effect |
| Dub Slow Build | 6857 | 0 | 4-bar smooth build transition |
| Dub Breathe | 13714 | 0 | 8-bar breakdown fade |
| Dub Beat Step | 0 | 429 | Beat-synced chase (1 beat hold) |
| Dub Fast Hit | 0 | 214 | 1/2 beat accent for drops |

## Strobe Conventions

- **On drops**: Aggressive full-rig strobe, first 2–4 bars of every drop
- **Wobble sync**: Strobe bursts timed to wobble bass hits (not continuous)
- **Build climax**: Accelerating strobe in final 2 bars before drop, then blackout, then FULL
- **Blackout-to-strobe**: The signature dubstep move — 1 bar of total blackout, then strobe explosion
- **Color strobes**: Red or purple strobe (not just white) for sustained drop sections

## Laser Conventions

- **Drops**: All lasers full blast during drops
- **Breakdowns**: Lasers-only mode (NI3K dim=0, only lasers on) for eerie atmosphere
- **Laser strobe**: During the biggest moments — all three NI3K laser colors strobing
- **Builds**: Gradually bring in one laser color at a time in the last 4 bars

## Gobo & Prism Conventions

- **Drops**: Tight gobo + dual prism spinning = maximum chaos
- **Wobble sections**: Gobo snap changes on wobble accents
- **Breakdowns**: Single gobo projection, no rotation, static and ominous
- **Builds**: Progressive — open → gobo → gobo + prism 1 → gobo + both prisms

## Par Behavior

- **Drops**: `par_pairs()` alternating on wobble hits, or `par_wash()` in red/purple
- **Half-time**: `par_wash()` single heavy color at full intensity
- **Breakdowns**: All pars off or single par at low intensity
- **Builds**: Light pars one at a time, building from dim to full

## Key Philosophy

Dubstep lighting is about **drama and darkness**. The darker and more restrained the quiet
sections, the more devastating the drops. Use near-blackout for breakdowns, not "dim wash."
Snap changes, never smooth fades during drops — dubstep is angular and aggressive, not flowing.
Color changes should sync to the wobble bass pattern, making the lighting feel like a visual
extension of the sound design.
