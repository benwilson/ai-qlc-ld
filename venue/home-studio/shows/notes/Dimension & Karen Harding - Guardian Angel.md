# Dimension & Karen Harding - Guardian Angel — Show Design Notes

## Overview
- **BPM**: 174
- **Duration**: ~3:44 (162 bars)
- **Genre**: Drum & Bass (euphoric/liquid)
- **Generator**: `generators/Dimension & Karen Harding - Guardian Angel.py`
- **Output**: `shows/Dimension & Karen Harding - Guardian Angel.qxw`
- **Run Order**: SingleShot
- **Analysis**: `songs-data/Dimension & Karen Harding - Guardian Angel.json`

## Creative Brief
- Theme: Angels, heaven, clouds, feeling a rush
- Palette: Ethereal & pure — white, gold, ice blue, soft teal. Clean and restrained.
- Every little sound pops — beat-level scene changes in all drops
- Breakdowns: wide, sweeping, luxurious slow continuous mover sweeps with smooth crossfades
- Movers: NEVER point behind themselves — always forward, left, right, up, down
- Pars (4BAR + both Missyees): Always cohesive and uniform — all same color via par_wash
- NI3K: Lasers ONLY (no RGBW, no halo, dim=0). High movement channel values (tilt rotation 160-250, pan 180-240)
- Laser progression: blue only → blue+green → all 3 by final drops
- Triple drop staircase: each successive drop adds prisms, wider movement, more lasers, faster strobes

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

## Fixture Roles
- **All 3 Movers**: Unified movement from shared position library. Forward-facing only. Color-matched to palette. Frosted and slow during breakdowns, clean and snappy during drops.
- **4BAR (ID 2) + Missyee 1+2 (ID 5, 6)**: Dynamic wash unit — fades out in quiet parts (bridge master 80→10, V2A master 15→50), goes crazy during builds (V1B/V2B escalate gradient→pairs→chase to full master). Drops mix wash/pairs/chase on rotating 4-bar cycles. Triple #3 is full chase with solid white strobe hits.
- **NI3K (ID 3)**: Lasers only. No RGBW LEDs (dim=0), no halo (H_OFF). High movement values for dramatic rotation. Laser color builds section by section.

## Movement Positions (7 forward-facing positions)
| Key | Sharpy (pan,tilt) | BSW (pan,tilt) | Profile (pan,tilt) | Description |
|-----|-------------------|----------------|-------------------|-------------|
| C | 153, 0 | 7, 19 | 0, 123 | Center floor |
| L | 115, 8 | 65, 22 | 40, 118 | Left |
| R | 195, 8 | 190, 15 | 210, 118 | Right |
| UP | 153, 30 | 7, 42 | 0, 90 | High/ceiling |
| W | 210, 12 | 75, 25 | 45, 100 | Wide spread |
| FW | 153, 15 | 7, 28 | 0, 138 | Forward (audience) |
| X | 100, 5 | 195, 18 | 200, 125 | Cross (swapped sides) |

### Position Sequences
- **POS_SWEEP** (8): C, L, UP, R, FW, W, C, X — dreamy sweep for breakdowns
- **POS_DROP** (8): C, L, R, W, X, UP, FW, C — standard drop movement
- **POS_WIDE** (8): W, X, FW, UP, W, L, R, X — widest moves for Triple #2
- **POS_BIG** (16): Full 16-position cycle — maximum variety for Triple #3

## NI3K Laser Progression
| Section | Red Laser | Green Laser | Blue Laser | Notes |
|---------|-----------|-------------|------------|-------|
| Ambient + Verse 1 | OFF | OFF | OFF | Dark — building atmosphere |
| Drop 1 | OFF | OFF | ON | Single blue laser — first reveal |
| Bridge | OFF | OFF | ON | Blue laser, gentle movement |
| Drop 2 | OFF | ON | ON | Blue + green — expanding |
| Verse 2 | OFF | ON | OFF | Green only — different feel |
| Triple #1 | OFF | ON | ON | Blue + green — strong |
| Triple #2 | ON | ON | ON | All 3 — full spread |
| Triple #3 | ON | ON | ON | All 3 — maximum rotation |

## Section-by-Section Breakdown

### Ambient Intro (bars 1-8, 8 steps @ 4-beat)
- Pars: **Nearly off** — master 0→35 (first bar is blackout, barely a glow by bar 8)
- Movers: Dark (dim=0). Positioned at center.
- NI3K: Dark (no lasers). Building tension.
- Timing: 4-beat holds. Pre-beat atmosphere.

### Verse 1A (bars 9-20, 12 steps @ 4-beat)
- Pars: **Gradients** cycling ETHEREAL_3 pairs, master 30→184 (fading in gently)
- Movers: Slowly appearing (dim 0→198). Frosted (180). Pure white. Gentle position shifts (C→L→R→UP→C).
- NI3K: Still dark.
- Timing: 4-beat holds. Vocals enter.

### Verse 1B (bars 21-32, 24 steps @ 2-beat)
- Pars: **Escalating patterns** — gradient (bars 1-4) → pairs (bars 5-8) → chase (bars 9-12). Master 140→250. Build goes crazy.
- Movers: Brightening (180→246), frost reducing (160→6). Sweeping through POS_SWEEP positions.
- NI3K: Still dark. Building anticipation.
- Timing: 2-beat steps. Momentum building to drop.

### Drop 1 (bars 33-48, 64 steps @ 1-beat)
- Pars: **Wash + pairs alternating** every 2 bars, ETHEREAL_4 cycle. White solid on strobe accents.
- Movers: Full brightness. Color snaps every beat. Reposition every bar via POS_DROP.
- Strobe accent: Beat 1 every 4 bars (SHARPY_STROBE_MED + BSW_SHUT_STROBE_FAST).
- NI3K: Blue laser ON. Tilts rotating (160-215 range). Pan 200.
- Timing: Beat-by-beat instant snaps.

### Bridge (bars 49-64, 8 steps @ 2-bar smooth)
- Pars: **Fading out** — master 80→10 (near-dark by end). Let movers and laser carry it.
- Movers: Frosted (200), dim 180. Slow continuous sweeps through bridge_sweep positions. Gold/blue/white/teal.
- NI3K: Blue laser ON. Gentle movement (t1=165, t2=180, t3=200).
- Timing: 2-bar smooth crossfades. Dreamy, flowing.

### Drop 2 (bars 65-88, 96 steps @ 1-beat)
- Pars: **Rotating patterns** every 4 bars: wash → pairs → chase cycle. White solid on strobe accents.
- Movers: Full brightness. Wider positions (POS_DROP + POS_WIDE + POS_DROP cycle). Color every beat.
- Strobe accent: Beat 1 every 4 bars (SHARPY_STROBE_FAST + BSW_SHUT_STROBE_FAST).
- NI3K: Blue + green lasers. More aggressive tilts (160-216 range). Pan 200-210.
- Timing: Beat-by-beat instant snaps.

### Verse 2A (bars 89-104, 8 steps @ 2-bar smooth)
- Pars: **Whisper-level** — master 15→50. Barely visible. Soft wash, smooth crossfades.
- Movers: Frosted (200), dim 160. Luxurious sweeps through v2a_sweep positions.
- NI3K: Green laser only. Pan 195-219. Gentle tilts.
- Timing: 2-bar smooth crossfades. Maximum luxury.

### Verse 2B (bars 105-112, 16 steps @ 2-beat)
- Pars: **Rocket launch build** — gradient (bars 1-3) → pairs (bars 4-6) → chase (bars 7-8). Master 50→253. Goes from whisper to screaming.
- Movers: Brightening (180→243), frost reducing (150→10). Tightening through POS_SWEEP.
- NI3K: Green laser. Moderate movement.
- Timing: 2-beat steps. Building back toward drops.

### Triple #1 (bars 113-128, 64 steps @ 1-beat)
- Staircase Level 1: Strong but not maxed. Clean beams.
- Pars: **Wash + pairs** alternating every 2 bars. ETHEREAL_4.
- Movers: Full brightness. No prisms. POS_DROP positions.
- NI3K: Blue + green lasers. Moderate tilts (165-223 range). Pan 205.
- Timing: Beat-by-beat snaps.

### Triple #2 (bars 129-144, 64 steps @ 1-beat)
- Staircase Level 2: Add prisms, wider movement, all 3 lasers.
- Pars: **Rotating patterns** — wash (4 bars) → chase (4 bars) → pairs (4 bars) → chase. White on strobe accents.
- Movers: Prisms spinning (Sharpy prism1=128 @200, BSW prism=80 @180, Profile prism=60). POS_WIDE positions.
- Strobe accent: Beat 1 every 4 bars.
- NI3K: ALL 3 lasers ON. Pan 215. Active tilts (170-232 range).
- Timing: Beat-by-beat snaps.

### Triple #3 (bars 145-160, 64 steps @ 1-beat)
- Staircase Level 3: EVERYTHING MAXED. Full blowout.
- Pars: **Chase on every beat** — one par cycling with missyees alternating. Solid white hits on strobe accents (every 2 bars!).
- Movers: DUAL prisms (Sharpy prism1+prism2=128 @200, BSW prism=128 @200, Profile prism=120). POS_BIG 16-position cycle.
- Strobe accent: Beat 1 every 2 bars (double frequency vs Triple #2).
- NI3K: ALL 3 lasers. Pan 220. Fastest tilts (175-244 range).
- Timing: Beat-by-beat snaps.

### End (bars 161-162)
- Snap to blackout. Hold 2 bars.

## Key Techniques
- **Scene deduplication**: `add_scene()` with `scene_cache` prevents duplicate scenes.
- **Par dynamics**: Master fades from 0 (ambient) to 35 (intro) to 184 (verse) to 255 (drop), crashes to 10 (bridge), rebuilds 15→253 (verse 2), full 255 (triple drops). Quiet = dark, build = crazy.
- **Par pattern escalation**: Builds use gradient→pairs→chase progression to create urgency. Each pattern is more active than the last.
- **smooth_step()**: 2-bar crossfade steps for breakdowns create flowing, continuous mover sweeps without per-beat granularity.
- **Laser staircase**: NI3K laser count increases section by section (0 → B → BG → BG → G → BG → RGB → RGB).
- **Prism staircase**: Triple drops add prisms progressively (none → single → dual).
- **Forward-only positions**: All 7 positions verified to keep beams forward of each fixture.
- **NI3K rotation modes**: Tilt values 160-250 use forward/reverse rotation for dramatic laser motion.

## Custom VC Layout
- ▶ GUARDIAN ANGEL (toggle, ice blue #96C8FF, 470×100)
- BLACKOUT (toggle, red, 470×80)
