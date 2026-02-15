# Lorn - Acid Rain (Skeler Remix) — Show Design Notes

## Overview
- **BPM**: 115
- **Duration**: ~4:33 (131 bars)
- **Genre**: Dark electronic / wave
- **Generator**: `generators/Lorn - Acid Rain (Skeler Remix).py`
- **Output**: `shows/Lorn - Acid Rain (Skeler Remix).qxw`
- **Run Order**: SingleShot
- **Analysis**: `songs-data/Lorn - Acid Rain (Skeler Remix).json`

## Creative Brief
- False calm intro: cool blue wash that corrupts over 3 intro sections
- Distinct solo chapters: each with unique movement pattern and personality
- Predatory hunting: slow stalk punctuated by violent snaps
- Mixed snap accents: strobes, color flashes, and silence (3 types)
- Break: eerie isolation (single fixture, unsettling movement)
- Lasers: punctuation marks at transitions + sustained during break
- Static fixtures: counter-rhythm against movers (4BAR alternating patterns)
- Outro: echo of the false calm, darker and emptier

## Color Palettes

### False Calm (Intro 1)
| Name | RGB | Usage |
|------|-----|-------|
| Calm Blue | (40, 80, 180) | Serene opening wash |
| Calm Teal | (20, 100, 140) | Subtle secondary |

### Corruption (Intro 2-3)
| Name | RGB | Usage |
|------|-----|-------|
| Sick Green | (60, 140, 20) | Colors going wrong |
| Sick Amber | (180, 100, 10) | Warmth invading |
| Bruise Purple | (90, 10, 120) | Fully corrupt |

### Dark Aggressive (Solo Chapters)
| Name | RGB | Usage |
|------|-----|-------|
| Blood Red | (180, 0, 0) | Primary aggression |
| Deep Red | (120, 0, 10) | Secondary/accent |
| Void Blue | (0, 10, 80) | Chapters 2, 5 |
| Poison Green | (0, 100, 20) | Chapter 3: Erratic |
| Cold White | (200, 200, 220) | Strobe flash accents |
| Violet | (100, 0, 180) | Chapter 2, 4, 6 |
| Dark Cyan | (0, 80, 100) | Chapters 3, 5 |

### Outro
| Name | RGB | Usage |
|------|-----|-------|
| Dead Blue | (15, 30, 60) | Corrupted memory |
| Dead Teal | (8, 40, 50) | Fading to nothing |

### Mover Color Mapping
BSW → Sharpy mapping: WHITE→WHITE, RED→RED, BLUE→BLUE, GREEN→GREEN, MAG→PURPLE, TEAL→TEAL, ORANGE→ORANGE, YELLOW→YELLOW, PINK→PINK

BSW → Profile mapping: WHITE→WHITE, RED→RED, BLUE→BLUE, GREEN→GREEN, MAG→PINK, TEAL→TEAL, ORANGE→ORANGE, YELLOW→YELLOW, PINK→PINK

## Fixture Roles
- **All 3 Movers**: Predatory hunting vocabulary — creeping, snapping, lunging, crossing.
- **4BAR (ID 2)**: Counter-rhythm patterns. chase_a/chase_b alternate odd/even pars. bar_sweep_lr does single-par sweeps. Creates visual push-pull against mover movement.
- **Missyee 1+2 (ID 5, 6)**: Often split — one on, one off. Creates directional feel that shifts with mover positions.
- **NI3K (ID 3)**: Laser punctuation at transitions. Break section has slow laser strobes for eeriness. Chapter 7 gets all lasers for maximum chaos. Halo matches section palette.

## Movement Vocabulary

### Position Library (12 positions)
- Center: S_C (153,0), B_C (7,19), P_C (0,123)
- Far Left: S_FAR_L (80,15), B_FAR_L (80,30), P_FAR_L (60,100)
- Far Right: S_FAR_R (220,15), B_FAR_R (200,5), P_FAR_R (200,100)
- High: S_HIGH (153,40), B_HIGH (7,50), P_HIGH (0,80)
- Low: S_LOW (153,245), B_LOW (7,5), P_LOW (0,160)
- Cross (swap sides): S_CROSS (80,10), B_CROSS (200,10), P_CROSS (180,100)
- Wide: S_WIDE (220,20), B_WIDE (80,30), P_WIDE (50,90)
- Audience: S_AUD (153,230), B_AUD (7,0), P_AUD (0,150)

### Movement Patterns by Chapter
- **Chapter 1 (Stalk)**: Slow creep to far positions → violent SNAP to center → creep opposite direction → SNAP again
- **Chapter 2 (Sweeps)**: Wide sweeping across room. Prisms on. Silent converge snaps (no strobe, just sudden position change).
- **Chapter 3 (Erratic Whip)**: Fast unpredictable — high/low scatter, cross snaps. Gobos on. Ends with strobe burst aimed at audience.
- **Chapter 4 (Lockstep)**: All 3 movers hit positions in UNISON. Coordinated aggression. Laser stab entry.
- **Chapter 5 (Renewed Hunt)**: Return to stalking but more aggressive. Low prowl / high lunge pattern. Cyan strobe snaps.
- **Chapter 6 (Final Push)**: Dual prisms on all movers. Left/right prism assault alternating. NI3K tilts spread.
- **Chapter 7 (Unhinged)**: Everything at once. Maximum aggression. Full send left/right alternating, ends with white obliteration.

## Section-by-Section Breakdown

### Intro 1: False Calm (bars 1-9, 2 scenes)
- Serene blue wash. Movers positioned but subdued.
- Gentle frost (200) on all movers, soft NI3K blue halo.
- 5-bar + 4-bar smooth crossfades.

### Intro 2: Corruption Begins (bars 10-18, 2 scenes)
- Colors shift sickly: teal→green→amber.
- Pars split to contrasting sick colors (pairs pattern).
- NI3K halo shifts cyan→yellow.

### Intro 3: Fully Corrupt (bars 19-27, 3 scenes)
- Movement gets twitchy. Colors wrong.
- Bruise purple dominates. Movers start jumping positions.
- **Laser stab** at transition into solo (red laser only, 1 bar).

### Chapter 1: The Stalk (bars 28-36, 5 steps using 4 scenes)
- Slow deliberate creep right → **STROBE SNAP** to center → creep left → **RED FLASH SNAP** to cross positions → resume creep
- 4BAR: alternating chase_a/chase_b patterns
- Gobos on Sharpy (G1_3) and BSW (G1_2)
- 3 snap accent types demonstrated: strobe burst, color flash, position-only

### Chapter 2: Cross-Room Sweeps (bars 37-52, 6 steps using 4 scenes)
- Wide Left → Cross Center → **SILENT SNAP converge** → Wide Right → Cross Center → **SILENT SNAP**
- Prisms spinning on all movers (Sharpy prism1=128, BSW prism=80)
- NI3K laser strobe (red+blue) on converge snaps
- 4BAR: gradient patterns

### Chapter 3: Erratic Whip (bars 53-63, 7 steps using 4 scenes)
- Fast scatter: high/low/cross, unpredictable
- Poison green palette. Gobos on (G1_4, G1_5).
- Single-par 4BAR sweep (bar_sweep_lr)
- Ends with **STROBE BURST** aimed at audience (S_AUD, B_AUD, P_AUD). All lasers ON.

### Break: Eerie Isolation (bars 64-71, 4 steps using 4 scenes)
- Hard cut to blackout. Then only BSW active.
- BSW: gobo2 rotating, frosted, slowly creeping through 3 positions
- All other fixtures dead. One dim missyee alternating.
- NI3K: very dim, slow laser strobes (red+blue, then green, then all 3)

### Chapter 4: Lockstep Assault (bars 72-86, 9 steps using 5 scenes)
- **Laser stab** entry from break (all 3 lasers ON)
- All movers move in UNISON: All Right → All Left → Violet Converge → All Wide
- Blood red palette with violet snap accents
- 4BAR chase patterns alternating. NI3K red halo.

### Chapter 5: Renewed Hunt (bars 87-98, 5 steps using 3 scenes)
- Return to stalking: Low Prowl (slow) → **Cyan Strobe** snap → High Lunge (slow) → **Cyan Strobe** snap → Low Prowl
- Dark cyan/void blue palette. Gobos on.
- NI3K cyan halo, green+blue lasers on snap moments.

### Chapter 6: Final Push (bars 99-106, 4 steps using 2 scenes)
- Left/right alternating prism assaults
- DUAL prisms on Sharpy (prism1 + prism2 both 128)
- BSW prism=200. Profile prism=120.
- Violet/Blood Red alternating. NI3K tilts spread (30/90/50 → 90/30/70).

### Chapter 7: Unhinged (bars 107-116, 8 steps using 3 scenes)
- Maximum aggression. Everything at once.
- Full Send Left → Full Send Right → **WHITE OBLITERATION** (repeat with decreasing bar count: 2+2+0.5 → 1.5+1.5+0.5 → 1+1)
- Accelerating pace creates increasing panic.
- All lasers ON. NI3K tilts auto-rotating (130-170 range). Prisms + gobos on all movers.

### Outro: Echo of the Calm (bars 117-131, 4 steps using 4 scenes)
- Return to blue wash but darker, emptier.
- Dead Blue/Dead Teal palette. Heavy frost (200-255).
- Everything dim (40→25→10→0). Slow 6+5+3+1 bar crossfades.

## Key Techniques
- **Dark helpers with fixed strobe**: `dark_sharpy()`, `dark_bsw()`, `dark_profile()` keep shutter/strobe at "open" values (SHARPY_OPEN, BSW_SHUT_OPEN, PROFILE_STROBE_OFF) to avoid crossfade artifacts.
- **3 snap accent types**: Strobe burst (Ch1 Snap Center), color flash (Ch1 Snap Cross), silent position (Ch2 Snap Silent). Variety prevents audience from anticipating hits.
- **Counter-rhythm 4BAR**: chase_a/chase_b, bar_sweep_lr, gradient patterns create visual tension against mover movement.
- **Isolation break**: Single fixture (BSW) with gobo2 rotation + frost creates unsettling focal point before explosive Chapter 4.
- **Accelerating repetition**: Chapter 7 repeats a 3-scene pattern (L/R/White) at decreasing durations (2+2+0.5 → 1.5+1.5+0.5 → 1+1) for increasing panic.

## Custom VC Layout
- ▶ ACID RAIN (toggle, red, 470×100) — starts main chaser
- BLACKOUT (toggle, red, 470×80)

## Stats
- 39 scenes (+ blackout), 59 chaser steps
- Total: ~273s (131 bars), target ~263s track length
