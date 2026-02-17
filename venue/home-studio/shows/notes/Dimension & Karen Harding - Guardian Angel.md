# Dimension & Karen Harding - Guardian Angel — Show Design Notes (v3)

## Overview
- **BPM**: 174
- **Duration**: ~3:48 (165 bars including cool down)
- **Genre**: Drum & Bass (euphoric/liquid)
- **Generator**: `generators/Dimension & Karen Harding - Guardian Angel.py`
- **Output**: `shows/Dimension & Karen Harding - Guardian Angel.qxw`
- **Run Order**: SingleShot
- **Analysis**: `songs-data/Dimension & Karen Harding - Guardian Angel.json`
- **Version**: v3 — all positions hardware-verified, specials integrated

## v3 Changes from v2
1. **Hardware-verified positions**: ALL 9 area positions + specials now use values confirmed on the actual rig. The v2 calculated values were completely wrong (e.g., SL Sharpy calc=90 vs verified=170).
2. **7-tuple format**: Position tuples now include NI3K pan as 7th element: `(sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt, ni3k_pan)`.
3. **Room collapse**: SL=DSL=USL and SR=DSR=USR — room too small for depth to matter on sides. Only centerline positions (C, DSC, USC) vary with depth.
4. **Verified specials**: DJ Booth, Disco Ball, Center Ceiling all use hardware-verified pan/tilt values.
5. **Cross position (X)**: Built from verified SL/SR — Sharpy aims SR side, BSW aims SL side, Profile at center.
6. **NI3K position-aware**: `mk_ni3k_laser()` and `mk_ni3k_atmo()` now look up NI3K pan from position dict (was hardcoded at 128/200/etc).
7. **Position sequences redesigned**: Specials integrated at musically meaningful moments — Disco Ball in sweeps/bridge, Center Ceiling in builds/drops, DJ Booth in intimate verses, Cross in drop accents.

## Creative Brief
- Theme: Angels, heaven, clouds, feeling a rush
- Palette: Ethereal & pure — white, gold, ice blue, soft teal. Clean and restrained.
- Every little sound pops — beat-level scene changes in all drops
- Breakdowns: wide, sweeping, luxurious slow continuous mover sweeps with smooth crossfades
- Movers: NEVER point behind themselves — always forward, left, right, up, down
- Pars (4BAR + both Missyees): Always cohesive and uniform — wash for unity, gradient/pairs for texture, chase for builds
- NI3K: Subtle RGBW atmosphere in quiet sections (halo color-matched to palette), lasers-only in drops
- Laser progression: blue only → blue+green → all 3 by final drops
- Triple drop staircase: each successive drop adds prisms, gobos, wider movement, more lasers, faster strobes

## Color Palette
| Name | RGB | Usage |
|------|-----|-------|
| Ice Blue | (150, 200, 255) | Primary — heavenly cool wash |
| Pure White | (255, 255, 255) | Accents, strobe flashes, climax |
| Gold | (255, 200, 80) | Warmth — breakdowns, contrast |
| Soft Teal | (100, 255, 200) | Secondary — ethereal shimmer |

### Color Rotation Sets
- **ETHEREAL_3**: Ice Blue → Pure White → Soft Teal (low-energy sections)
- **ETHEREAL_4**: Ice Blue → Pure White → Gold → Soft Teal (drops, full cycle)

### Mover Color Mapping
| Palette Color | BSW | Sharpy | Profile |
|---------------|-----|--------|---------|
| Ice Blue | BSW_BLUE | SHARPY_BLUE | PROF_BLUE |
| Pure White | BSW_WHITE | SHARPY_WHITE | PROF_WHITE |
| Gold | BSW_YELLOW | SHARPY_AMBER | PROF_YELLOW |
| Soft Teal | BSW_TEAL | SHARPY_TEAL | PROF_TEAL |

### NI3K Halo Mapping
| Palette Color | Halo Value |
|---------------|-----------|
| Ice Blue | H_BLU |
| Pure White | H_RGB |
| Gold | H_YEL |
| Soft Teal | H_CYN |

## Fixture Roles
- **All 3 Movers**: Unified movement from verified focus-positions grid. Forward-facing only. Color-matched to palette. Frosted and slow during breakdowns, clean and snappy during drops.
- **4BAR (ID 2) + Missyee 1+2 (ID 5, 6)**: Dynamic wash unit — fades out in quiet parts, goes crazy during builds. Drops mix wash/pairs/chase on rotating 4-bar cycles. Triple #3 is chase + white downbeat blasts.
- **NI3K (ID 3)**: Dual-mode fixture:
  - **Quiet sections** (ambient, verses, bridge): Atmosphere mode — subtle RGBW glow matching palette color, halo synced, dim 30-96. Lasers strobe-teased in builds.
  - **Drops**: Laser-only mode — dim=0, no RGBW, no halo. High tilt rotation (160-247 range via prime-number math). Laser color builds section by section. Pan varies per position.

## Movement Positions (v3: All Hardware-Verified)

### Position Values
| Key | Sharpy (pan,tilt) | BSW (pan,tilt) | Profile (pan,tilt) | NI3K pan | Verified |
|-----|-------------------|----------------|-------------------|----------|----------|
| C | 153, 0 | 7, 19 | 0, 123 | 128 | Yes |
| SL | 170, 0 | 189, 29 | 50, 165 | 80 | Yes |
| SR | 149, 5 | 170, 23 | 110, 145 | 176 | Yes |
| DSC | 158, 6 | 179, 27 | 64, 145 | 128 | Yes |
| USC | 157, 0 | 181, 21 | 52, 136 | 128 | Yes |
| DJ | 142, 3 | 196, 25 | 95, 107 | 128 | Yes |
| DISCO | 144, 34 | 170, 56 | 154, 168 | 128 | Yes |
| CEIL | 158, 73 | 180, 86 | 91, 30 | 128 | Yes |
| X | 149, 5 | 189, 29 | 0, 123 | 128 | Composite |
| AUD | 153, 15 | 7, 5 | 0, 155 | 128 | No (calc) |

Notes: DSL=SL, DSR=SR, USL=SL, USR=SR (room too small for depth on sides). NI3K pan for SL (80) and SR (176) are calculated, not hardware-verified.

### Position Sequences (v3: with specials)
- **POS_SWEEP** (8): C, SL, DISCO, SR, DSC, DJ, CEIL, DSR — dreamy sweep featuring specials
- **POS_DROP** (8): C, SL, SR, X, DSC, CEIL, DSR, C — standard drop movement with cross + ceiling
- **POS_WIDE** (8): DSL, DSR, USL, USR, X, DISCO, CEIL, DSR — widest moves + specials for Triple #2
- **POS_BIG** (16): Full 16-position cycle including DISCO, CEIL, DJ, X, AUD — maximum variety for Triple #3

## Gobo Staircase
| Section | BSW Gobo | Notes |
|---------|----------|-------|
| Drop 1 | None (open) | Clean beams, first chorus |
| Drop 2 | G1_3 | First gobo texture, beam breakup |
| Triple #1 | G1_4 | Escalating complexity |
| Triple #2 | G1_5 | + prisms = maximum beam texture |
| Triple #3 | G1_5 | + dual prisms, same gobo as T2 |

## NI3K Laser Progression (with strobe tease)
| Section | Red Laser | Green Laser | Blue Laser | NI3K Mode | Notes |
|---------|-----------|-------------|------------|-----------|-------|
| Ambient + V1A | OFF | OFF | OFF | Atmosphere | Subtle RGBW glow building |
| Verse 1B (last 4 bars) | OFF | OFF | STROBE_SLOW→MED | Atmosphere | Blue laser strobe tease |
| Drop 1 | OFF | OFF | ON | Laser-only | Single blue laser — first reveal |
| Bridge | OFF | OFF | ON | Atmosphere | Blue laser, subtle RGBW glow |
| Drop 2 | OFF | ON | ON | Laser-only | Blue + green — expanding |
| Verse 2A | OFF | ON | OFF | Atmosphere | Green only — different feel |
| Verse 2B (last 4 bars) | OFF | ON | STROBE_SLOW→MED | Atmosphere | Blue laser strobe tease back in |
| Triple #1 | OFF | ON | ON | Laser-only | Blue + green — strong |
| Triple #2 | ON | ON | ON | Laser-only | All 3 — full spread |
| Triple #3 | ON | ON | ON | Laser-only | All 3 — maximum rotation |
| Cool Down | OFF | OFF | OFF | Atmosphere | Fading RGBW glow, no lasers |

## Section-by-Section Breakdown

### Ambient Intro (bars 1-8, 8 steps @ 4-beat)
- Pars: **Nearly off** — master 0→35 (first bar is blackout, barely a glow by bar 8)
- Movers: Dark (dim=0). Positioned at center.
- NI3K: Subtle blue atmosphere — dim 0→35, halo appears at bar 3.
- Timing: 4-beat holds. Pre-beat atmosphere.

### Verse 1A (bars 9-20, 12 steps @ 4-beat)
- Pars: **Gradients** cycling ETHEREAL_3 pairs, master 30→184 (fading in gently)
- Movers: Slowly appearing (dim 0→198). Frosted (180). Pure white. v3: Position sequence includes DJ Booth and CEIL for intimate variety.
- NI3K: Halo tracks palette — dim 30→96, halo color-matches current palette. Pan tracks mover position.
- Timing: 4-beat holds. Vocals enter.

### Verse 1B (bars 21-32, 24 steps @ 2-beat)
- Pars: **Escalating patterns** — gradient (bars 1-4) → pairs (bars 5-8) → chase (bars 9-12). Master 140→250.
- Movers: Brightening (180→246), frost reducing (160→6). Sweeping through POS_SWEEP (v3: includes DISCO and CEIL).
- Mover strobe ramp in last 2 bars (SHARPY_STROBE_SLOW building).
- Blue laser strobe tease in last 4 bars (LASER_STROBE_SLOW → MED).
- Timing: 2-beat steps. Momentum building to drop.

### Drop 1 (bars 33-48, 64 steps @ 1-beat)
- Pars: **Wash + pairs alternating** every 2 bars, ETHEREAL_4 cycle. White solid on strobe accents.
- Movers: Full brightness. Color snaps every beat. POS_DROP (v3: includes X cross + CEIL).
- Strobe accent: Beat 1 every 4 bars (SHARPY_STROBE_MED + BSW_SHUT_STROBE_FAST).
- NI3K: Blue laser ON. Prime tilt math (beat*7%37, beat*11%29, beat*13%31). Pan tracks position.
- Timing: Beat-by-beat instant snaps.

### Bridge (bars 49-64, 8 steps @ 2-bar smooth)
- Pars: **Fading out** — master 80→10 (near-dark by end).
- Movers: Frosted (200), dim 180. Slow continuous sweeps. Gold/blue/white/teal.
- v3: Sweep features DISCO and DJ — ethereal disco ball reflections + DJ booth intimacy.
- NI3K: Atmosphere mode — dim 60, halo tracks palette, blue laser ON. Pan tracks position.
- Timing: 2-bar smooth crossfades. Dreamy, flowing.

### Drop 2 (bars 65-88, 96 steps @ 1-beat)
- Pars: **Rotating patterns** every 4 bars: wash → pairs → chase cycle. White solid on strobe accents.
- Movers: Full brightness. BSW gobo G1_3 for beam texture. POS_DROP + POS_WIDE + POS_DROP cycle (v3: includes specials).
- Strobe accent: Beat 1 every 4 bars (SHARPY_STROBE_FAST + BSW_SHUT_STROBE_FAST).
- NI3K: Blue + green lasers. Prime tilt math. Pan tracks position.
- Timing: Beat-by-beat instant snaps.

### Verse 2A (bars 89-104, 8 steps @ 2-bar smooth)
- Pars: **Whisper-level** — master 15→50. Barely visible. Soft wash, smooth crossfades.
- Movers: Frosted (200), dim 160. v3: Sweep includes DISCO and DJ for ethereal variety.
- NI3K: Atmosphere mode — dim 50, halo tracks palette, green laser only. Pan tracks position.
- Timing: 2-bar smooth crossfades. Maximum luxury.

### Verse 2B (bars 105-112, 16 steps @ 2-beat)
- Pars: **Rocket launch build** — gradient (bars 1-3) → pairs (bars 4-6) → chase (bars 7-8). Master 50→253.
- Movers: Brightening (180→243), frost reducing (150→10). Strobe ramp in last 2 bars.
- NI3K: Green laser sustains, blue laser strobe tease in last 4 bars (LASER_STROBE_SLOW → MED). Atmosphere mode with halo.
- Timing: 2-beat steps. Building back toward drops.

### Triple #1 (bars 113-128, 64 steps @ 1-beat)
- Staircase Level 1: Strong but not maxed. Clean beams.
- Pars: **Wash + pairs** alternating every 2 bars. ETHEREAL_4.
- Movers: Full brightness. No prisms. BSW gobo G1_4. POS_DROP positions (v3: with X + CEIL).
- NI3K: Blue + green lasers. Prime tilt math. Pan tracks position.
- Timing: Beat-by-beat snaps.

### Triple #2 (bars 129-144, 64 steps @ 1-beat)
- Staircase Level 2: Add prisms + gobos, wider movement, all 3 lasers.
- Pars: **Rotating patterns** — wash (4 bars) → chase (4 bars) → pairs (4 bars) → chase. White on strobe accents.
- Movers: Prisms spinning. BSW gobo G1_5. POS_WIDE positions (v3: includes DISCO + CEIL).
- Strobe accent: Beat 1 every 4 bars.
- NI3K: ALL 3 lasers ON. Prime tilt math — widest range. Pan tracks position.
- Timing: Beat-by-beat snaps.

### Triple #3 (bars 145-160, 64 steps @ 1-beat)
- Staircase Level 3: EVERYTHING MAXED. Full blowout.
- Pars: White downbeat blast on beat 1 of every bar (16 blasts!). Chase on other beats. Alternating strobe every 2 bars.
- Movers: DUAL prisms. BSW gobo G1_5. POS_BIG 16-position cycle (v3: includes DISCO, CEIL, DJ, X, AUD).
- NI3K: ALL 3 lasers. Pan tracks position. Prime tilt math — maximum range (175-247).
- Timing: Beat-by-beat snaps.

### Cool Down (4 steps @ 1-bar smooth)
- Movers: Dim 120→15, frost 150→225 (re-frosting), returning to C.
- Pars: Master 100→10 (fading).
- NI3K: Returns to atmosphere mode — dim 50→5, halo fading, no lasers.
- Final blackout: 4-beat hold.

## Key Techniques
- **Scene deduplication**: `add_scene()` with `scene_cache` prevents duplicate scenes. 433 unique, 0 reuses (every beat is unique due to prime tilt math + position-aware NI3K pan).
- **Dual NI3K modes**: `mk_ni3k_atmo()` for quiet sections (RGBW+halo), `mk_ni3k_laser()` for drops (lasers only). Both now position-aware for NI3K pan.
- **Prime-number tilt math**: `beat * P % M` where P and M are different primes per-head creates pseudo-random rotation that never repeats within a section.
- **Laser strobe tease**: Build sections ramp LASER_STROBE_SLOW → MED before drops snap to LASER_ON. Creates anticipation.
- **White downbeat blast**: Triple #3 fires white on beat 1 of every bar for maximum visual punch.
- **Gobo staircase**: Progressive BSW gobo escalation (none → G1_3 → G1_4 → G1_5) adds beam texture complexity alongside prism staircase.
- **Hardware-verified positions**: All positions confirmed on the actual rig, eliminating the geometric calculation errors from v1/v2.
- **Special position integration**: Disco Ball, Center Ceiling, DJ Booth, and Cross positions appear at musically meaningful moments (bridge sweeps, drop accents, intimate verses).
- **Mover strobe ramp**: Build sections ramp mover strobe SLOW → MED in final bars for tension.
- **Cool down section**: Proper breathing-out fade replaces abrupt blackout.

## Custom VC Layout
- ▶ GUARDIAN ANGEL (toggle, ice blue #96C8FF, 470×100)
- BLACKOUT (toggle, red, 470×80)

## Stats
- 433 unique scenes (0 reuses), 433 chaser steps
- Total: 227.7s (165.1 bars), target ~224s (162 bars + 3s cool down)
