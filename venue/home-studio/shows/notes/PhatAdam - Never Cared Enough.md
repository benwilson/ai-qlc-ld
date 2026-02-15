# PhatAdam - Never Cared Enough — Show Design Notes

## Overview
- **BPM**: 134
- **Duration**: ~2:28 (82 bars)
- **Genre**: Happy / upbeat electronic
- **Generator**: `generators/PhatAdam - Never Cared Enough.py`
- **Output**: `shows/PhatAdam - Never Cared Enough.qxw`
- **Run Order**: SingleShot
- **Analysis**: `songs-data/PhatAdam - Never Cared Enough.json`

## Creative Brief
- EVERYTHING to the beat: pars snap on every beat (or 2/4 in slower sections)
- 4BAR + Missyees = unified wash unit (Missyees extend the 4BAR chase/pattern)
- Par patterns rotate per section: chase → pairs → solid → alternating
- Movers reposition every 4 beats, color/effect changes every beat
- Neon pop palette: hot pink, electric blue, vivid green, magenta, yellow, orange
- Strobe accents on chorus downbeats and big moments
- NI3K halo: beat-synced in verses/tease, hardware jump mode in choruses
- All timing: FadeIn=0 instant snaps for maximum punch

## Color Palette
| Name | RGB | Usage |
|------|-----|-------|
| Hot Pink | (255, 20, 100) | Primary neon |
| Electric Blue | (0, 100, 255) | Primary neon |
| Vivid Green | (0, 255, 80) | Primary neon |
| Neon Magenta | (255, 0, 200) | Primary neon |
| Neon Yellow | (255, 220, 0) | Extended palette (6-color) |
| Neon Orange | (255, 100, 0) | Extended palette (6-color) |
| Bright White | (255, 255, 255) | Flash accents |

### Color Rotation Sets
- **NEON_4**: Hot Pink → Electric Blue → Vivid Green → Neon Magenta (verses, basic sections)
- **NEON_6**: All 6 colors (choruses, high-energy sections)

### Mover Color Mapping
Each neon RGB color maps to the closest match on each fixture's color wheel:

| Neon Color | BSW | Sharpy | Profile | NI3K Halo |
|------------|-----|--------|---------|-----------|
| Hot Pink | BSW_PINK | SHARPY_PINK | PROF_PINK | H_PNK |
| Electric Blue | BSW_BLUE | SHARPY_BLUE | PROF_BLUE | H_BLU |
| Vivid Green | BSW_GREEN | SHARPY_GREEN | PROF_GREEN | H_GRN |
| Neon Magenta | BSW_MAG | SHARPY_PURPLE | PROF_PINK | H_PNK |
| Neon Yellow | BSW_YELLOW | SHARPY_YELLOW | PROF_YELLOW | H_YEL |
| Neon Orange | BSW_ORANGE | SHARPY_ORANGE | PROF_ORANGE | H_RED |
| Bright White | BSW_WHITE | SHARPY_WHITE | PROF_WHITE | H_RGB |

## Fixture Roles
- **All 3 Movers**: Repositioned per bar, color changes per beat. All move together from shared position library.
- **4BAR (ID 2)**: Part of unified wash unit. 4 par patterns: chase (single par cycling), pairs (P1+P3 vs P2+P4), solid (all same), alternating.
- **Missyee 1+2 (ID 5, 6)**: Extend 4BAR patterns — alternate on even/odd beats for chase, split for pairs, both on for solid.
- **NI3K (ID 3)**: Halo color-matched to current beat color. "sync" mode = individual color. "jump_fast/med/slow" = hardware color jump effect. Tilts increasingly active through choruses. All lasers in Climax only.

## Movement Positions (7 named positions)
| Key | Sharpy | BSW | Profile | Description |
|-----|--------|-----|---------|-------------|
| C | 153, 0 | 7, 19 | 0, 123 | Center |
| L | 100, 10 | 80, 25 | 50, 110 | Left |
| R | 210, 10 | 190, 10 | 200, 110 | Right |
| W | 220, 20 | 80, 30 | 50, 90 | Wide spread |
| H | 153, 40 | 7, 50 | 0, 80 | High |
| A | 153, 230 | 7, 0 | 0, 150 | Audience |
| X | 80, 5 | 200, 15 | 200, 130 | Cross (swapped) |

### Position Sequences
- **POS_DANCE** (8): C, L, R, W, X, H, A, C — standard party movement
- **POS_WIDE** (8): W, X, A, H, W, L, R, X — wider, more extreme
- **POS_BIG** (16): Full cycle through all positions — maximum variety

## Section-by-Section Breakdown

### Tease (bars 1-8, 8 steps)
- Par chase pattern, building from dim (master 60→200)
- Movers dark (dim=0). Soft NI3K (dim 40→136).
- 4 neon colors cycling. Each step = 1 bar (4 beats).

### Opens Up (bars 9-16, 16 steps)
- Pairs pattern with complementary colors (c1 + c1 offset by 3)
- Movers fade in (dim 60→252) following POS_DANCE sequence
- Each step = 2 beats. 6-color rotation.

### Full Party (bars 17-24, 32 steps)
- Chase pattern on EVERY BEAT — this is where it kicks in
- Movers reposition every bar, color changes every beat
- All at full brightness (dim=255). 4-color rotation.

### Chorus 1 (bars 25-33, 36 steps)
- Every beat. Chase + solid hits.
- **Strobe accent**: beat 1 of every other bar (SHARPY_STROBE_FAST + BSW_SHUT_STROBE_FAST + par_solid)
- NI3K jump_med mode. Tilts start moving (50-85 range).
- Positions follow POS_DANCE + "X".

### Verse (bars 34-40, 14 steps)
- Pull back. Pairs every 2 beats (softer).
- Movers frosted (frost=150), dimmer (dim=140).
- Position changes every 8 beats (very slow).
- NI3K beat-synced (dim=100).

### Break: Strobe Build (bars 41-48, 19 steps)
- Accelerating rate: 4 beats → 2 beats → 1 beat
- Bars 1-3 (3 steps): par_solid, movers slow strobe (SHARPY_STROBE_SLOW)
- Bars 4-5 (4 steps): par_chase, medium strobe
- Bars 6-8 (12 steps): par_chase every beat, fast strobe, NI3K jump_fast
- Colors escalate: Pink → Blue → Magenta → 4-cycle → 6-cycle

### Chorus 2 (bars 49-58, 40 steps)
- Every beat. 6-color cycle. Prisms on all movers.
- Sharpy prism1=128 (rotating at 200). BSW prism=80. Profile prism=60.
- **Strobe accent**: beat 1 every other bar
- NI3K jump_fast. Tilts dancing (varying per beat).
- Positions follow POS_WIDE.

### Chorus 3 (bars 59-73, 60 steps)
- Maximum variety. Every beat.
- **Alternating par patterns** every 2 bars: chase vs pairs
- **Strobe accent**: beat 1 every 4 bars (less frequent but harder hitting)
- Heavier prisms: Sharpy prism1=128, BSW prism=128, Profile prism=80
- Positions follow POS_BIG (16-position cycle).
- NI3K tilts varied per-beat (7 different patterns).

### Climax (bars 74-82, 36 steps)
- **ALL strobes** on every beat. **ALL 3 lasers** ON permanently.
- par_solid hits every beat (maximum impact).
- All prisms maxed. NI3K tilts auto-rotating (160, 140, 180).
- NI3K jump_fast halo.
- Positions follow POS_DANCE + "X".

### End
- Single beat blackout (scene 0).

## Key Techniques
- **Scene deduplication**: `add_scene()` with `scene_cache` prevents duplicate scenes. 252 unique from 262 steps (10 reuses).
- **Unified par builder**: `par_chase()`, `par_pairs()`, `par_solid()` return 4BAR + both Missyees as a group.
- **Color wheel mapping dicts**: `BSW_FOR`, `SHARPY_FOR`, `PROF_FOR`, `HALO_FOR` translate RGB tuples to fixture-specific color values.
- **Mover builder**: `mkvrs(pos_key, color)` builds all 3 movers from a position name + color, auto-mapping to each fixture's color wheel.
- **Strobe buildup**: Break section demonstrates accelerating tempo (4→2→1 beat) with corresponding strobe speed increase (SLOW→MED→FAST).

## Custom VC Layout
- ▶ NEVER CARED ENOUGH (toggle, hot pink #FF1488, 470×100)
- BLACKOUT (toggle, red, 470×80)

## Stats
- 252 unique scenes (10 reuses), 262 chaser steps
- Total: 148.4s (82.2 bars), target ~148s
