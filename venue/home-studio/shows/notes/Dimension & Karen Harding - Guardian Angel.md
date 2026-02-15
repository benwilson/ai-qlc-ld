# Dimension & Karen Harding - Guardian Angel — Show Design Notes (v2)

## Overview
- **BPM**: 174
- **Duration**: ~3:48 (165 bars including cool down)
- **Genre**: Drum & Bass (euphoric/liquid)
- **Generator**: `generators/Dimension & Karen Harding - Guardian Angel.py`
- **Output**: `shows/Dimension & Karen Harding - Guardian Angel.qxw`
- **Run Order**: SingleShot
- **Analysis**: `songs-data/Dimension & Karen Harding - Guardian Angel.json`
- **Version**: v2 — rebuilt with techniques from Fixin's, Acid Rain, and PhatAdam shows

## v2 Changes from v1
1. **Focus-positions grid**: Replaced 7 custom positions with 9-point stage grid (DSL, DSC, DSR, SL, C, SR, USL, USC, USR) + specials (CEIL, AUD, WALL, DJ) from `focus-positions.md`
2. **NI3K atmosphere mode**: Quiet sections (ambient, verses, bridge) now use subtle RGBW glow + palette-matched halo instead of total darkness. NI3K contributes ambient light.
3. **BSW gobo escalation**: Progressive gobo staircase across drops: none (Drop 1) → G1_3 (Drop 2) → G1_4 (Triple #1) → G1_5 (Triple #2/3)
4. **Laser strobe tease**: Builds ramp LASER_STROBE_SLOW → LASER_STROBE_MED → LASER_ON instead of binary off→on
5. **White downbeat blast**: Triple #3 fires white on beat 1 of every bar (16 blasts) with alternating strobe
6. **Prime-number tilt math**: `beat * 7 % 37`, `beat * 11 % 29`, `beat * 13 % 31` for more chaotic NI3K rotation patterns vs v1's simple modulo
7. **Cool down section**: 4-bar smooth fade replaces v1's 2-bar snap-to-black. Movers frost up, dim down, NI3K returns to soft atmosphere.
8. **Mover strobe ramp**: Build sections (V1B, V2B) ramp mover strobe from open → SLOW → MED in final bars
9. **Audience Blinder position**: POS_BIG sequence includes AUD for brief blinder hits during Triple #3

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

### NI3K Halo Mapping (v2)
| Palette Color | Halo Value |
|---------------|-----------|
| Ice Blue | H_BLU |
| Pure White | H_RGB |
| Gold | H_YEL |
| Soft Teal | H_CYN |

## Fixture Roles
- **All 3 Movers**: Unified movement from focus-positions grid. Forward-facing only. Color-matched to palette. Frosted and slow during breakdowns, clean and snappy during drops.
- **4BAR (ID 2) + Missyee 1+2 (ID 5, 6)**: Dynamic wash unit — fades out in quiet parts, goes crazy during builds. Drops mix wash/pairs/chase on rotating 4-bar cycles. Triple #3 is chase + white downbeat blasts.
- **NI3K (ID 3)**: Dual-mode fixture:
  - **Quiet sections** (ambient, verses, bridge): Atmosphere mode — subtle RGBW glow matching palette color, halo synced, dim 30-96. Lasers strobe-teased in builds.
  - **Drops**: Laser-only mode — dim=0, no RGBW, no halo. High tilt rotation (160-247 range via prime-number math). Laser color builds section by section.

## Movement Positions (v2: Focus-positions grid)

### 9-Point Stage Grid
| Key | Sharpy (pan,tilt) | BSW (pan,tilt) | Profile (pan,tilt) | Description |
|-----|-------------------|----------------|-------------------|-------------|
| C | 153, 0 | 7, 19 | 0, 123 | Center floor |
| DSC | 153, 9 | 7, 10 | 0, 136 | Downstage center (near audience) |
| USC | 153, 0 | 7, 27 | 0, 109 | Upstage center (near DJ) |
| SL | 90, 0 | 79, 19 | 29, 123 | Stage left |
| SR | 220, 0 | 0, 19 | 0, 123 | Stage right |
| DSL | 90, 9 | 79, 10 | 29, 136 | Downstage left |
| DSR | 220, 9 | 0, 10 | 0, 136 | Downstage right |
| USL | 90, 0 | 79, 27 | 29, 109 | Upstage left |
| USR | 220, 0 | 0, 27 | 0, 109 | Upstage right |

### Special Positions
| Key | Description | Usage |
|-----|-------------|-------|
| CEIL | Ceiling hit — all beams up | Sweeps, atmospheric moments |
| AUD | Audience blinder — brief only! | Triple #3 accent hits |
| WALL | Par wall highlight | Not used in this show |
| DJ | DJ booth spotlight | Not used in this show |

### Position Sequences
- **POS_SWEEP** (8): C, SL, CEIL, SR, DSC, USL, C, DSR — dreamy sweep for breakdowns
- **POS_DROP** (8): C, SL, SR, DSL, DSR, CEIL, DSC, C — standard drop movement
- **POS_WIDE** (8): DSL, DSR, USL, USR, DSC, SL, SR, DSR — widest moves for Triple #2
- **POS_BIG** (16): Full 16-position cycle including AUD — maximum variety for Triple #3

## Gobo Staircase (v2)
| Section | BSW Gobo | Notes |
|---------|----------|-------|
| Drop 1 | None (open) | Clean beams, first chorus |
| Drop 2 | G1_3 | First gobo texture, beam breakup |
| Triple #1 | G1_4 | Escalating complexity |
| Triple #2 | G1_5 | + prisms = maximum beam texture |
| Triple #3 | G1_5 | + dual prisms, same gobo as T2 |

## NI3K Laser Progression (v2: with strobe tease)
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
- NI3K: **v2: Subtle blue atmosphere** — dim 0→35, halo appears at bar 3. Was dark in v1.
- Timing: 4-beat holds. Pre-beat atmosphere.

### Verse 1A (bars 9-20, 12 steps @ 4-beat)
- Pars: **Gradients** cycling ETHEREAL_3 pairs, master 30→184 (fading in gently)
- Movers: Slowly appearing (dim 0→198). Frosted (180). Pure white. Gentle position shifts (C→SL→SR→CEIL→C).
- NI3K: **v2: Halo tracks palette** — dim 30→96, halo color-matches current palette. Was dark in v1.
- Timing: 4-beat holds. Vocals enter.

### Verse 1B (bars 21-32, 24 steps @ 2-beat)
- Pars: **Escalating patterns** — gradient (bars 1-4) → pairs (bars 5-8) → chase (bars 9-12). Master 140→250.
- Movers: Brightening (180→246), frost reducing (160→6). Sweeping through POS_SWEEP.
- **v2: Mover strobe ramp** in last 2 bars (SHARPY_STROBE_SLOW building).
- **v2: Blue laser strobe tease** in last 4 bars (LASER_STROBE_SLOW → MED).
- Timing: 2-beat steps. Momentum building to drop.

### Drop 1 (bars 33-48, 64 steps @ 1-beat)
- Pars: **Wash + pairs alternating** every 2 bars, ETHEREAL_4 cycle. White solid on strobe accents.
- Movers: Full brightness. Color snaps every beat. Reposition every bar via POS_DROP.
- Strobe accent: Beat 1 every 4 bars (SHARPY_STROBE_MED + BSW_SHUT_STROBE_FAST).
- NI3K: Blue laser ON. **v2: Prime tilt math** (beat*7%37, beat*11%29, beat*13%31). Pan 200.
- Timing: Beat-by-beat instant snaps.

### Bridge (bars 49-64, 8 steps @ 2-bar smooth)
- Pars: **Fading out** — master 80→10 (near-dark by end).
- Movers: Frosted (200), dim 180. Slow continuous sweeps. Gold/blue/white/teal.
- NI3K: **v2: Atmosphere mode** — dim 60, halo tracks palette, blue laser ON. Provides warm underglow.
- Timing: 2-bar smooth crossfades. Dreamy, flowing.

### Drop 2 (bars 65-88, 96 steps @ 1-beat)
- Pars: **Rotating patterns** every 4 bars: wash → pairs → chase cycle. White solid on strobe accents.
- Movers: Full brightness. **v2: BSW gobo G1_3** for beam texture. Wider positions (POS_DROP + POS_WIDE + POS_DROP cycle).
- Strobe accent: Beat 1 every 4 bars (SHARPY_STROBE_FAST + BSW_SHUT_STROBE_FAST).
- NI3K: Blue + green lasers. **v2: Prime tilt math**. Pan 200-210.
- Timing: Beat-by-beat instant snaps.

### Verse 2A (bars 89-104, 8 steps @ 2-bar smooth)
- Pars: **Whisper-level** — master 15→50. Barely visible. Soft wash, smooth crossfades.
- Movers: Frosted (200), dim 160. Luxurious sweeps through v2a_sweep positions.
- NI3K: **v2: Atmosphere mode** — dim 50, halo tracks palette, green laser only. Warm ambient glow.
- Timing: 2-bar smooth crossfades. Maximum luxury.

### Verse 2B (bars 105-112, 16 steps @ 2-beat)
- Pars: **Rocket launch build** — gradient (bars 1-3) → pairs (bars 4-6) → chase (bars 7-8). Master 50→253.
- Movers: Brightening (180→243), frost reducing (150→10). **v2: Strobe ramp** in last 2 bars.
- NI3K: **v2: Green laser sustains, blue laser strobe tease** in last 4 bars (LASER_STROBE_SLOW → MED). Atmosphere mode with halo.
- Timing: 2-beat steps. Building back toward drops.

### Triple #1 (bars 113-128, 64 steps @ 1-beat)
- Staircase Level 1: Strong but not maxed. Clean beams.
- Pars: **Wash + pairs** alternating every 2 bars. ETHEREAL_4.
- Movers: Full brightness. No prisms. **v2: BSW gobo G1_4**. POS_DROP positions.
- NI3K: Blue + green lasers. **v2: Prime tilt math**. Pan 205.
- Timing: Beat-by-beat snaps.

### Triple #2 (bars 129-144, 64 steps @ 1-beat)
- Staircase Level 2: Add prisms + gobos, wider movement, all 3 lasers.
- Pars: **Rotating patterns** — wash (4 bars) → chase (4 bars) → pairs (4 bars) → chase. White on strobe accents.
- Movers: Prisms spinning (Sharpy prism1=128 @200, BSW prism=80 @180, Profile prism=60). **v2: BSW gobo G1_5**. POS_WIDE positions.
- Strobe accent: Beat 1 every 4 bars.
- NI3K: ALL 3 lasers ON. **v2: Prime tilt math — widest range**. Pan 215.
- Timing: Beat-by-beat snaps.

### Triple #3 (bars 145-160, 64 steps @ 1-beat)
- Staircase Level 3: EVERYTHING MAXED. Full blowout.
- Pars: **v2: White downbeat blast** on beat 1 of every bar (16 blasts!). Chase on other beats. Alternating strobe every 2 bars.
- Movers: DUAL prisms (Sharpy prism1+prism2=128 @200, BSW prism=128 @200, Profile prism=120). **v2: BSW gobo G1_5**. POS_BIG 16-position cycle **including AUD blinder**.
- NI3K: ALL 3 lasers. Pan 220. **v2: Prime tilt math — maximum range** (175-247).
- Timing: Beat-by-beat snaps.

### Cool Down (v2: replaces 2-bar snap-to-black)
- **4 steps**: 1-bar smooth crossfades converging to center.
- Movers: Dim 120→15, frost 150→225 (re-frosting), returning to C.
- Pars: Master 100→10 (fading).
- NI3K: Returns to atmosphere mode — dim 50→5, halo fading, no lasers.
- Final blackout: 4-beat hold.

## Key Techniques
- **Scene deduplication**: `add_scene()` with `scene_cache` prevents duplicate scenes. 433 unique, 0 reuses (every beat is unique due to prime tilt math).
- **Dual NI3K modes**: `mk_ni3k_atmo()` for quiet sections (RGBW+halo), `mk_ni3k_laser()` for drops (lasers only). v1 only had laser mode.
- **Prime-number tilt math**: `beat * P % M` where P and M are different primes per-head creates pseudo-random rotation that never repeats within a section.
- **Laser strobe tease**: Build sections ramp LASER_STROBE_SLOW → MED before drops snap to LASER_ON. Creates anticipation.
- **White downbeat blast**: Triple #3 fires white on beat 1 of every bar for maximum visual punch (technique from Fixin's generator).
- **Gobo staircase**: Progressive BSW gobo escalation (none → G1_3 → G1_4 → G1_5) adds beam texture complexity alongside prism staircase.
- **Focus-positions grid**: Uses standardized 9-point stage grid from focus-positions.md instead of ad-hoc positions. More positions = more variety.
- **Mover strobe ramp**: Build sections ramp mover strobe SLOW → MED in final bars for tension.
- **Cool down section**: Proper breathing-out fade replaces abrupt blackout.

## Custom VC Layout
- ▶ GUARDIAN ANGEL (toggle, ice blue #96C8FF, 470×100)
- BLACKOUT (toggle, red, 470×80)

## Stats
- 433 unique scenes (0 reuses), 433 chaser steps
- Total: 227.7s (165.1 bars), target ~224s (162 bars + 3s cool down)
