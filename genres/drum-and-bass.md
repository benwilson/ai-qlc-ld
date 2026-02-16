# Genre: Drum & Bass

## Overview

Drum & Bass is characterized by fast breakbeats (170–180 BPM), heavy sub-bass, and dramatic
contrasts between rolling grooves and explosive drops. Lighting should match this intensity
arc — restrained and atmospheric during breakdowns, building through rolls, then unleashing
everything on the drop.

## BPM Range

- Typical: 170–180 BPM
- Common: 174 BPM
- Time signature: 4/4 (but feels double-time due to breakbeat patterns)

## Energy Profile

DnB has the most extreme contrast between sections of any EDM genre. Drops are peak energy,
breakdowns can be near-silent. The lighting should mirror this dynamic range.

| Section | Energy | Duration | Lighting Character |
|---------|--------|----------|--------------------|
| Intro | Low–Medium | 8–16 bars | Atmospheric wash, minimal movement, establish palette |
| Build | Medium–High | 8–16 bars | Ramp intensity, add fixtures, accelerate strobe/movement |
| Drop | Peak | 16–32 bars | FULL SEND — all fixtures, fast movement, strobes, lasers |
| Rolling Bass | High | 8–16 bars | Sustained energy, rhythmic chases, less chaotic than drop |
| Breakdown | Low | 4–16 bars | Strip to minimal — single color wash, slow sweep, near-dark |
| Second Build | Medium–High | 8–16 bars | Rebuild tension, layer effects progressively |
| Second Drop | Peak+ | 16–32 bars | Even bigger than first — different palette, more effects |

## Color Palette

### Primary Colors (use most often)
- **Deep Blue** (0, 0, 255) / BSW Blue / Sharpy Blue — the signature DnB color, cold and aggressive
- **Red** (255, 0, 0) / BSW Red / Sharpy Red — high energy, danger, intensity
- **White** (255, 255, 255) / BSW White / Sharpy White — impact, strobes, drops

### Accent Colors (use for contrast and variety)
- **Purple** (128, 0, 255) / Sharpy Purple — dark, moody, good for breakdowns
- **Cyan** (0, 255, 255) / BSW Teal / Sharpy Teal — cold but lighter than blue, rolling sections
- **Amber** (255, 128, 0) / Sharpy Amber — warmth for melodic sections, contrast with blues

### Two-Color Pairs (primary busking combos)
| Combo Name | Color A | Color B | Best For |
|------------|---------|---------|----------|
| Classic DnB | Deep Blue | Red | Drops, high energy |
| Ice | Deep Blue | White | Clean drops, strobes |
| Neon Night | Purple | Cyan | Rolling bass, mid-energy |
| Fire & Ice | Red | Cyan | Builds, contrast moments |
| Midnight | Purple | Deep Blue | Breakdowns, atmosphere |
| Blood Moon | Red | Amber | Dark, aggressive drops |
| Whiteout | White | Red | Maximum impact drops |

### Avoid
- Pastels and warm tones as primary palette (too soft for DnB energy)
- Green as a primary color (reads as "nature" rather than "aggressive")
- Yellow as a primary color (too cheerful)

## Movement Conventions

### Drop Movement
- Fast mover sweeps timed to downbeats (L→R or R→L across 2–4 beats)
- Split movers: Sharpy and BSW crossing to opposite sides on the drop hit
- Profile punching downstage on snare accents
- NI3K head rotation at maximum speed
- Position changes every 1–2 beats during peak energy

### Rolling Bass Movement
- Smooth 2–4 bar sweeps (movers flowing rather than snapping)
- Figure-8 or circular patterns on movers
- Gentle left-right oscillation
- NI3K slow rotation creating ambient texture

### Breakdown Movement
- Static or very slow drift (8+ bar sweeps)
- Movers converge to center or ceiling hit
- Minimal position changes — let the stillness contrast with the drops

### Build Movement
- Accelerating sweep speed (start at 4-bar, end at 1-beat by drop)
- Movers gradually spreading from center to wide
- NI3K ramping from static to rotation

## Timing Presets

| Preset | FadeIn (ms) | Hold (ms) | Use |
|--------|-------------|-----------|-----|
| DnB Snap | 50 | 1329 | Drop color changes (1 bar) |
| DnB Fast Snap | 50 | 295 | Drop accents (1 beat) |
| DnB Strobe | 0 | 86 | 1/4 beat strobe effect |
| DnB Roll 2bar | 2759 | 0 | Rolling bass smooth fade (2 bars) |
| DnB Roll 4bar | 5517 | 0 | Extended smooth sweep (4 bars) |
| DnB Breathe | 11034 | 0 | Breakdown slow fade (8 bars) |
| DnB Beat Step | 0 | 345 | Beat-synced chase (1 beat hold) |
| DnB Half Beat | 0 | 172 | Half-beat chase for energy |

## Strobe Conventions

- **On drops**: White or single-color strobe, 1/8 or 1/16 note speed, 2–4 bars maximum
- **On builds**: Accelerating strobe (start slow, increase to fast over 4–8 bars)
- **Blackout + strobe**: Brief blackout (1–2 beats) followed by strobe hit for maximum impact
- **Never**: Sustained strobe through an entire section — it loses impact
- **Fixture strobes**: Use Sharpy ch6 strobe (64–120) and BSW ch16 strobe (20–128) for
  beam-only strobes while pars hold steady. This creates depth.

## Laser Conventions

- **Drops only**: NI3K lasers on during drops, off during everything else
- **Build reveal**: Bring lasers in at the last 2–4 bars of a build for anticipation
- **Color**: Match or contrast with the mover color palette
- **Strobe lasers**: Use for the biggest moments only — laser strobe during the peak of drop 2

## Gobo & Prism Conventions

- **Drops**: Tight gobos + prism spinning creates chaotic, energetic beams
- **Rolling**: Open gobo (clean beam) with optional slow prism rotation
- **Breakdowns**: Open gobo, no prism — clean and simple
- **Builds**: Add gobo partway through, add prism in final bars before drop

## Par Behavior

- **Drops**: `par_wash()` all same color for maximum unity, or `par_pairs()` alternating with beat
- **Rolling**: `par_gradient()` for subtle depth
- **Breakdowns**: `par_wash()` at low intensity, single color
- **Builds**: Progressive `par_chase()` speeding up, or pars lighting one at a time

## Key Philosophy

DnB lighting is about **contrast and restraint**. The drops hit hardest when the breakdowns
are dark. Save your biggest effects (lasers, prism strobes, audience blinder) for the most
important moment. As Ed Warren says: "Hit the beat, the off beat. Wait for the last possible
moment. Save something for the next drop."
