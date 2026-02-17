# PhatAdam - Never Cared Enough — Show Design Notes

## Overview
- **BPM**: 133
- **Duration**: ~2:28 (82 bars)
- **Genre**: Happy / upbeat electronic
- **Generator**: `generators/PhatAdam - Never Cared Enough.py`
- **Output**: `shows/PhatAdam - Never Cared Enough.qxw`
- **Run Order**: SingleShot
- **Analysis**: `songs-data/PhatAdam - Never Cared Enough.json`
- **Version**: v3 — Verified Focus Positions

## v3 Changes from v2
- ALL mover positions now use hardware-verified values from `focus-positions.md`
- Added specials: DJ Booth, Disco Ball, Center Ceiling
- Cross position ("X") built from verified SL/SR values (Sharpy→SR, BSW→SL = visible crossing beams)
- NI3K pan now varies per position (was fixed at 128 in v2)
- Position sequences redesigned to feature specials at musically meaningful moments
- Break section reimagined: DJ Booth → Center Ceiling → Center (spatial build matches energy build)

## Creative Brief
- EVERYTHING to the beat: pars snap on every beat (or 2/4 in slower sections)
- 4BAR + Missyees = unified wash unit (Missyees extend the 4BAR chase/pattern)
- Par patterns rotate per section: chase → pairs → solid → alternating
- Movers reposition every 4 beats, color/effect changes every beat
- Neon pop palette: hot pink, electric blue, vivid green, magenta, yellow, orange
- Strobe accents on chorus downbeats and big moments
- NI3K halo: beat-synced in verses/tease, hardware jump mode in choruses
- All timing: FadeIn=0 instant snaps for maximum punch
- **Special positions used intentionally**: Disco Ball for surprise reveals, Center Ceiling for dramatic upward beams in builds, DJ Booth for performer spotlight moments

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
- **All 3 Movers**: Repositioned per bar, color changes per beat. All move together from shared position library. Now using hardware-verified positions.
- **4BAR (ID 2)**: Part of unified wash unit. 4 par patterns: chase (single par cycling), pairs (P1+P3 vs P2+P4), solid (all same), alternating.
- **Missyee 1+2 (ID 5, 6)**: Extend 4BAR patterns — alternate on even/odd beats for chase, split for pairs, both on for solid.
- **NI3K (ID 3)**: Halo color-matched to current beat color. "sync" mode = individual color. "jump_fast/med/slow" = hardware color jump effect. Pan now tracks mover positions. Tilts increasingly active through choruses. All lasers in Climax only.

## Movement Positions (9 named positions — ALL VERIFIED)
| Key | Sharpy | BSW | Profile | NI3K Pan | Description |
|-----|--------|-----|---------|----------|-------------|
| C | 153, 0 | 7, 19 | 0, 123 | 128 | Center (verified) |
| SL | 170, 0 | 189, 29 | 50, 165 | 80 | Stage Left (verified) |
| SR | 149, 5 | 170, 23 | 110, 145 | 176 | Stage Right (verified) |
| DSC | 158, 6 | 179, 27 | 64, 145 | 128 | Downstage Center (verified) |
| USC | 157, 0 | 181, 21 | 52, 136 | 128 | Upstage Center (verified) |
| DJ | 142, 3 | 196, 25 | 95, 107 | 128 | DJ Booth (verified) |
| DISCO | 144, 34 | 170, 56 | 154, 168 | 128 | Disco Ball (verified) |
| CEIL | 158, 73 | 180, 86 | 91, 30 | 128 | Center Ceiling (verified) |
| X | 149, 5 | 189, 29 | 0, 123 | 128 | Cross (Sharpy→SR, BSW→SL) |

### Position Sequences
- **POS_DANCE** (8): C, SL, SR, DSC, X, USC, DISCO, C — standard party movement with disco ball surprise
- **POS_WIDE** (8): DSC, X, CEIL, SL, DISCO, SR, DJ, X — wider moves featuring all specials
- **POS_BIG** (16): Full cycle through every position — maximum variety for Chorus 3

## Section-by-Section Breakdown

### Tease (bars 1-8, 8 steps)
- Par chase pattern, building from dim (master 60→200)
- Movers dark (dim=0) at Center. Soft NI3K (dim 40→136).
- 4 neon colors cycling. Each step = 1 bar (4 beats).

### Opens Up (bars 9-16, 16 steps)
- Pairs pattern with complementary colors (c1 + c1 offset by 3)
- Movers fade in (dim 60→252) through: C → SL → SR → USC → C → SL → SR → DSC
- Introduces width (SL/SR) and depth (USC/DSC). Building toward the dance floor.
- Each step = 2 beats. 6-color rotation.

### Full Party (bars 17-24, 32 steps)
- Chase pattern on EVERY BEAT — this is where it kicks in
- Movers follow POS_DANCE: C, SL, SR, DSC, X, USC, **DISCO**, C
- **Bar 7: Disco Ball surprise** — first time movers aim upward, unexpected visual
- All at full brightness (dim=255). 4-color rotation.

### Chorus 1 (bars 25-33, 36 steps)
- Every beat. Chase + solid hits.
- **Strobe accent**: beat 1 of every other bar (SHARPY_STROBE_FAST + BSW_SHUT_STROBE_FAST + par_solid)
- **Bar 5: DJ Booth** — performer spotlight mid-chorus
- NI3K jump_med mode. Tilts start moving (50-95 range).
- Positions: C, SL, SR, DSC, DJ, X, USC, DSC, C

### Verse (bars 34-40, 14 steps)
- Pull back. Pairs every 2 beats (softer).
- Movers frosted (frost=150), dimmer (dim=140).
- Gentle movement: C → SL → SR → C (position changes every 8 beats).
- NI3K beat-synced (dim=100).

### Break: Strobe Build (bars 41-48, 19 steps)
- **Bars 1-3**: DJ Booth focus — performer in the spotlight as energy builds. Slow strobe (SHARPY_STROBE_SLOW). Par solid, building master.
- **Bars 4-5**: Center Ceiling — beams reach upward as tension peaks. Medium strobe. Par chase.
- **Bars 6-8**: Center convergence — all beams snap to center as energy explodes. Fast strobe, NI3K jump_fast. 6-color cycle.
- Spatial journey: intimate DJ spot → upward expansion → center convergence.

### Chorus 2 (bars 49-58, 40 steps)
- Every beat. 6-color cycle. Prisms on all movers.
- Sharpy prism1=128 (rotating at 200). BSW prism=80. Profile prism=60.
- **Strobe accent**: beat 1 every other bar
- Features Disco Ball + Center Ceiling in POS_WIDE rotation
- NI3K jump_fast. Tilts dancing (varying per beat).

### Chorus 3 (bars 59-73, 60 steps)
- Maximum variety. Every beat. ALL 9 positions used via POS_BIG.
- **Alternating par patterns** every 2 bars: chase vs pairs
- **Strobe accent**: beat 1 every 4 bars (less frequent but harder hitting)
- Heavier prisms: Sharpy prism1=128, BSW prism=128, Profile prism=80
- POS_BIG features every position including DJ, DISCO, CEIL for full spatial range.

### Climax (bars 74-82, 36 steps)
- **ALL strobes** on every beat. **ALL 3 lasers** ON permanently.
- par_solid hits every beat (maximum impact).
- All prisms maxed. NI3K tilts auto-rotating (160, 140, 180).
- **Position sequence**: C, DISCO, X, CEIL, DSC, DISCO, SL, SR, CEIL
- Disco Ball + Center Ceiling featured twice each — lasers + disco ball reflections + upward beams = maximum spectacle.

### End
- Single beat blackout (scene 0).

## Key Techniques
- **Scene deduplication**: `add_scene()` with `scene_cache` prevents duplicate scenes. 252 unique from 262 steps (10 reuses).
- **Unified par builder**: `par_chase()`, `par_pairs()`, `par_solid()` return 4BAR + both Missyees as a group.
- **Color wheel mapping dicts**: `BSW_FOR`, `SHARPY_FOR`, `PROF_FOR`, `HALO_FOR` translate RGB tuples to fixture-specific color values.
- **Mover builder**: `mkvrs(pos_key, color)` builds all 3 movers from a position name + color, auto-mapping to each fixture's color wheel. Now unpacks 7-tuple (includes NI3K pan).
- **NI3K position tracking**: `mkni()` now takes `pos_key` and reads NI3K pan from the position dict, so the NI3K tracks mover positions instead of staying fixed at center.
- **Strobe buildup**: Break section demonstrates accelerating tempo (4→2→1 beat) with corresponding strobe speed increase (SLOW→MED→FAST) AND spatial expansion (DJ→CEIL→C).
- **Special position dramaturgy**: Specials introduced at specific narrative moments — Disco Ball as a Full Party surprise, DJ Booth for performer focus during builds, Center Ceiling for upward expansion before drops.

## Custom VC Layout
- ▶ NEVER CARED ENOUGH (toggle, hot pink #FF1488, 470×100)
- BLACKOUT (toggle, red, 470×80)

## Stats
- 252 unique scenes (10 reuses), 262 chaser steps
- Total: 148.4s (82.2 bars), target ~148s
