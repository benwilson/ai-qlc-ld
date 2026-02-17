# Show Notes: Busking-Techno

## Overview
- **Type**: Busking / looping show — high energy techno
- **Venue**: Home Studio
- **Genre**: Techno (128 BPM)
- **Duration**: 10 minutes (320 bars), loops continuously
- **Generator**: `venue/home-studio/generators/Busking-Techno.py`
- **Design goal**: Beat-synced blinking — lights snap to new positions/colors every beat during high-energy sections

## VC Layout

### Master Controls
| Button | Function | Color |
|--------|----------|-------|
| FULL SHOW | 10-min sequence through all 9 sections, loops | Green |
| BLACKOUT | All fixtures off | Red |

### Section Triggers (all loop independently)
| Button | Bars | Duration | Beat Timing | Character |
|--------|------|----------|-------------|-----------|
| OPENING | 32 | 60s | 4-bar hold | Single red beam pulsing in darkness |
| TENSION BUILD | 32 | 60s | 8-bar smooth | Fixtures added one by one, converging |
| GROOVE LOCK | 48 | 90s | 1-beat snap | White/Red alternation on every beat |
| FILTER BUILD | 16 | 30s | 2-beat snap | Full white ↔ dim red industrial pulse |
| RELEASE 1 | 48 | 90s | 1-beat snap | 8 geometric positions cycling on beat |
| STRIP BACK | 16 | 30s | 4-bar smooth | Remove fixtures back to single beam |
| SECOND BUILD | 32 | 60s | 2-beat snap | Cold Steel palette building up |
| RELEASE 2 | 64 | 120s | 1-beat snap | PEAK — lasers + prisms + spinning NI3K |
| OUTRO | 32 | 60s | 8-bar smooth | Fade to single dim red beam |

## Color Palette
Strictly minimal per techno conventions — max 2 colors at any time:
- **White** (255, 255, 255) — industrial, stark, signature techno
- **Deep Red** (200, 0, 0) — Berghain aesthetic
- **Cool Blue** (0, 0, 200) — cold, late-night (Second Build + Release 2)
- **Black/Off** — darkness is a design element; used liberally

### Two-Color Pairs Used
- **Berghain** (Red/White) — Opening through Release 1, Outro
- **Cold Steel** (Blue/White) — Second Build through Release 2
- **Industrial** (White/Off) — Filter Build

## Custom Extrapolated Positions
10 new positions calculated by interpolating/extrapolating from verified focus-positions.md:

| Name | Description | Used In |
|------|-------------|---------|
| SPLIT_W | Maximum divergence — Sharpy far left, BSW far right | Release 2 |
| CROSS | X-pattern — Sharpy aims right, BSW aims left | Release 1, 2 |
| Q_LEFT | Midpoint between SL and C | Groove Lock |
| Q_RIGHT | Midpoint between SR and C | Groove Lock |
| NW_LEFT | Between SL and Sweep Far Left | Release 1 |
| NW_RIGHT | Between SR and Sweep Far Right | Release 1 |
| BACK_CRN | Sharpy at USL, BSW at USR, Profile at USC | Release 1, 2 |
| FRT_SPR | Sharpy at DSL, BSW at DSR, Profile at DSC | Release 1 |
| MID_CEIL | Halfway between C and Ceiling | (available) |
| DEEP_DS | Extrapolated past DSC toward audience | Release 2 |

## Beat-Sync Technique
The "blinking" effect comes from chaser step timing, NOT fixture strobe channels:
- **1-beat hold** (469ms at 128 BPM): Scenes snap-change on every beat
- **2-beat hold** (938ms): Scenes change on every other beat
- **4-bar hold** (7500ms): Slow pulse for low-energy sections
- Fixture strobe channels stay at "open" (Sharpy=252, BSW=8) — the rhythm comes from the chaser, not the strobe

This means every beat produces a completely different look (different position, different color, different fixture emphasis) creating a relentless machine-like pulse.

## Fixture Roles
- **Sharpy + BSW**: Lead movers — snap between positions on the beat, cross beams in haze
- **Profile**: Front-facing accent — follows the geometric pattern from the audience side
- **4BAR + Missyees**: Color wash layer — alternate opposite color from movers (white when movers are red, red when movers are white)
- **NI3K**: Atmosphere — dim halo matching mood; in Release 2: red laser only (single color per techno convention), tilt heads set to forward rotation values (160-180) for spinning motion

## Laser Usage
Per techno convention: minimal, single color (red only), static beams.
- Lasers OFF for all sections except Release 2
- Release 2: Red laser only (rl=LASER_ON, gl/bl=LASER_OFF) for the Berghain aesthetic
- NI3K tilt heads use forward rotation mode (values 160-180) during Release 2 for dramatic spinning beam patterns

## Energy Arc
```
Energy
  ▲
  │                              ████████████████████
  │                    ████      █ RELEASE 2 (PEAK) █
  │          ████████  █FLT█    ██████████████████████
  │    ████  █GROOVE█  ████   ██
  │    █TNS█ █ LOCK █       ██2B█
  │  ██████  ████████      █████
  │ █OPEN█              █STRP█           ████████
  │ ██████              ██████            █ OUTRO █
  │                                       ████████
  └──────────────────────────────────────────────────► Time
   0    1    2    3    4    5    6    7    8    9   10 min
```

## Usage Tips
- FULL SHOW for set-and-forget 10 minutes of techno lighting
- Section triggers loop independently — hold GROOVE LOCK as long as the DJ is in a groove
- The show builds from near-darkness to maximum intensity — respect the arc
- STRIP BACK is your reset button mid-set to rebuild tension
- RELEASE 2 is the peak — save it for the biggest moment
- The 1-beat timing in section chasers is faster than in the full show (which uses 1-bar timing for manageability) — tap a section trigger for the most intense beat-locked effect
