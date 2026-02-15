# Lorn - Acid Rain (Skeler Remix) — Show Design Notes (v3 Data-Driven)

## Overview
- **BPM**: 115
- **Duration**: ~4:42 (282s generated, ~263s track)
- **Genre**: Dark electronic / wave
- **Generator**: `generators/Lorn - Acid Rain (Skeler Remix).py` (v3 — fully data-driven)
- **Output**: `shows/Lorn - Acid Rain (Skeler Remix).qxw`
- **Run Order**: SingleShot
- **Analysis**: `songs-data/Lorn - Acid Rain (Skeler Remix).json`

## Creative Brief
- **Every bass hit** triggers a visible reaction (strobe snap, color flash, position converge)
- **Quiet sections**: individual synth/piano onsets fire single fixtures, rotating which mover leads
- **Energy curves** drive dimmer levels, frost (inverse of energy), prism/gobo activation
- **4BAR + Missyees** snap colors on every beat (beat-reactive, alternating primary/accent)
- **NI3K** halo follows segment palette, lasers reserved for peak sub-bass moments (>0.8)
- **Movers** react to overall energy: low energy = center/tight, high = extreme positions
- **Color palette** shifts per segment (cool → corrupt → aggressive → eerie → assault → echo)

## Architecture: Data-Driven Generation

Unlike v1/v2 which hand-crafted every scene, v3 reads the analysis JSON and generates scenes dynamically:

1. **Energy at each beat** drives dimmer, frost, prism activation, position selection
2. **Per-stem onsets** trigger individual light cues (bass → converge snap, synth → single-fixture spot)
3. **Segment type** determines strategy: sparse, building, melodic, peak, or outro
4. **Scene caching** (`get_or_create_scene()`) prevents duplicate scenes in the workspace

### Section Strategies
- **Sparse** (quiet intros, break): Walk through individual onset timestamps. Each synth note fires one fixture, rotating lead between Sharpy/BSW/Profile. Gaps between notes hold darkness.
- **Building** (intro with energy): 2-bar chunks. Bass hits within get snap reactions, otherwise smooth crossfade.
- **Melodic** (solos): 1-2 bar steps based on energy. Bass hits get strobe snaps. Prism/gobo activate above energy thresholds.
- **Peak** (choruses): 2-beat steps for maximum reactivity. Every bass hit = strobe snap. Prisms and gobos always on. Lasers when sub-bass > 0.8.
- **Outro**: 3-bar chunks, progressively darker. Forced dimmer decay from 120 → 0. Ends with blackout crossfade.

## Color Palettes

### Per-Segment Mapping (14 segments)
| Seg | Time | Label | Primary RGB | Accent RGB | Mover Color | Halo |
|-----|------|-------|-------------|------------|-------------|------|
| 0 | 0:00 | start | Calm Blue (40,80,180) | Calm Teal (20,100,140) | Blue | Blue |
| 1 | 0:00–0:19 | intro | Calm Blue | Calm Teal | Blue | Blue |
| 2 | 0:19–0:37 | intro | Calm Teal | Sick Green (60,140,20) | Teal | Cyan |
| 3 | 0:37–0:56 | intro | Sick Green | Bruise Purple (90,10,120) | Green | Green |
| 4 | 0:56–1:23 | solo | Blood Red (180,0,0) | Deep Red (120,0,10) | Red | Red |
| 5 | 1:23–1:35 | solo | Violet (100,0,180) | Blood Red | Magenta | Pink |
| 6 | 1:35–1:52 | chorus | Cold White (200,200,220) | Blood Red | White | RGB |
| 7 | 1:52–2:08 | solo | Dark Cyan (0,80,100) | Void Blue (0,10,80) | Teal | Cyan |
| 8 | 2:08–2:32 | break | Eerie Dim (10,5,30) | Black (0,0,0) | Blue | Off |
| 9 | 2:32–3:01 | solo | Deep Red | Poison Green (0,100,20) | Red | Red |
| 10 | 3:01–3:25 | solo | Violet | Dark Cyan | Magenta | Pink |
| 11 | 3:25–3:43 | solo | Blood Red | Violet | Red | Red |
| 12 | 3:43–4:02 | chorus | Cold White | Blood Red | White | RGB |
| 13 | 4:02–4:23 | outro | Dead Blue (15,30,60) | Dead Teal (8,40,50) | Blue | Blue |

## Fixture Roles

### Movers (Sharpy ID 8, BSW ID 1, Profile ID 4)
- **Position**: Selected from 10-position vocabulary based on energy level + beat index for variety
- **Dimmer**: Direct map from RMS energy (40–255)
- **Frost**: Inverse of energy (high energy = sharp beams, low = soft wash)
- **Prism**: Activates when RMS > 0.7 (or forced in peak sections)
- **Gobo**: BSW G1_3 when RMS > 0.5 and alternating beats
- **Strobe**: Only on bass hit accent scenes in peak sections

### 4BAR (ID 2) + Missyees (ID 5, 6)
- **Beat-reactive**: Colors alternate between primary/accent on even/odd beats
- **4BAR uses pairs pattern**: Pars 1+3 = one color, Pars 2+4 = other color, swaps each beat
- **Missyees split**: Miss1 = primary on even beats, Miss2 = accent on odd beats
- **Accent scenes**: All go cold white for bass hit impact
- **Master**: Direct map from RMS energy

### NI3K (ID 3)
- **RGBW**: Follows segment primary color
- **Halo**: Matches segment palette
- **Lasers**: OFF by default. Only activate in peak sections when sub-bass > 0.8
- **Dimmer**: Energy-driven

## Movement Vocabulary (10 Positions)

| # | Name | Sharpy | BSW | Profile |
|---|------|--------|-----|---------|
| 0 | Center | 153,0 | 7,19 | 0,123 |
| 1 | Spread Left | 220,15 | 80,30 | 60,100 |
| 2 | Spread Right | 80,15 | 200,5 | 200,100 |
| 3 | Cross | 80,10 | 200,10 | 180,100 |
| 4 | Wide | 220,20 | 80,30 | 50,90 |
| 5 | High | 153,40 | 7,50 | 0,80 |
| 6 | Low/Audience | 153,245 | 7,5 | 0,160 |
| 7 | Tight Cluster | 130,20 | 40,10 | 35,110 |
| 8 | All Right | 200,30 | 200,25 | 200,95 |
| 9 | All Left | 100,30 | 100,25 | 100,95 |

### Position Selection Logic
- RMS < 0.15: Center or Tight Cluster (alternating)
- RMS 0.15–0.4: Spread Left/Right, Cross, Tight (cycling)
- RMS 0.4–0.7: Wide, High, Low, Cross, All Right/Left (cycling)
- RMS > 0.7: Wide, Low, All Right/Left, High, Cross (cycling)

## Section-by-Section Breakdown

### Seg 1: Silent Start (0:00, ~0 bars)
- Click/silence. Skipped (duration < 0.1s).

### Seg 1: Quiet Intro (0:00–0:19, 9 bars, rms=0.09)
- **Strategy**: Sparse — 27 synth onsets trigger individual fixtures
- Each piano/synth note lights one mover (rotating Sharpy→BSW→Profile)
- Dark gaps between notes. NI3K blue halo barely visible.
- No bass, no drums — pure ambient triggers.

### Seg 2: Building Intro (0:19–0:37, 9 bars, rms=0.44)
- **Strategy**: Building — 2-bar chunks, 7 bass hits get snap reactions
- Colors shift to teal/sick green. Energy starting to build.
- Bass hits (7 total) trigger accent scenes with white flash.

### Seg 3: Corrupt Intro (0:37–0:56, 9 bars, rms=0.41)
- **Strategy**: Building — 48 melody onsets, 10 bass hits
- Sick green/bruise purple palette. Dense melodic activity.
- Drums enter (23 onsets). Movers start moving more.

### Seg 4: First Solo (0:56–1:23, 13 bars, rms=0.57)
- **Strategy**: Melodic — 1.5-bar steps, blood red palette
- 12 bass hits trigger converge-center snaps with strobe on peaks > 0.7
- Prism activates on high-energy moments. Gobos when > 0.5.

### Seg 5: Melodic Climax (1:23–1:35, 6 bars, rms=0.60)
- **Strategy**: Melodic — 1.5-bar steps, violet/blood red
- Continued high energy. Prism and gobo active most of the time.

### Seg 6: First Chorus (1:35–1:52, 8 bars, rms=0.61, peak=1.00)
- **Strategy**: Peak — 2-beat steps for maximum reactivity
- Cold white/blood red palette. Strobes on every bass hit (8 total).
- Prisms + gobos always on. Lasers when sub-bass > 0.8.
- **This is the absolute peak energy of the track** (rms peak = 1.00).

### Seg 7: Post-Chorus Solo (1:52–2:08, 8 bars, rms=0.60)
- **Strategy**: Melodic — dark cyan/void blue palette
- Still high energy, movers reactive. 11 bass hits with snaps.

### Seg 8: The Break (2:08–2:32, 11 bars, rms=0.39)
- **Strategy**: Sparse — only 4 melody onsets + 10 bass hits
- Eerie dim palette (10,5,30). NI3K halo off.
- Individual onsets fire single fixtures. Long dark gaps between events.
- Minimal drum activity (6 hits) — mostly silence.

### Seg 9: Extended Solo (2:32–3:01, 14 bars, rms=0.28)
- **Strategy**: Melodic — 2-bar steps (lower energy)
- Deep red/poison green. Sub-bass present but energy moderate.
- 47 melody onsets drive varied looks. 11 bass snaps.

### Seg 10: Synth Exploration (3:01–3:25, 12 bars, rms=0.34)
- **Strategy**: Melodic — 2-bar steps, violet/dark cyan
- Building energy. Drums returning (7 hits).

### Seg 11: Heavy Build (3:25–3:43, 9 bars, rms=0.66)
- **Strategy**: Melodic — 1-bar steps (high energy)
- Blood red/violet. 77 drum hits, 14 bass hits.
- Prism and gobo nearly constant. Strobe snaps on peaks.

### Seg 12: Final Chorus (3:43–4:02, 9 bars, rms=0.64, peak=0.87)
- **Strategy**: Peak — 2-beat steps
- Cold white/blood red. 90 drum hits, 15 bass hits.
- Maximum strobe, prism, gobo. Lasers on sub-bass peaks.

### Seg 13: Outro (4:02–4:23, 10 bars, rms=0.23)
- **Strategy**: Outro — 3-bar chunks, progressive fade
- Dead blue/dead teal. Forced dimmer decay 120→0.
- Heavy frost (200). Movers return to center.

### Seg 14: Silence (4:23–4:33, 5 bars, rms=0.00)
- **Strategy**: Outro — final blackout crossfade

## Key Techniques
- **Scene caching**: `get_or_create_scene(key, create_fn)` prevents duplicate scenes when similar energy levels produce identical looks. 162 scenes total, 149 unique.
- **Per-onset triggering**: In sparse sections, each synth timestamp from the analysis JSON fires a dedicated scene with a single lead fixture.
- **Energy-driven everything**: Dimmers, frost, prism activation, gobo activation, position selection, and master levels all derive from the beat-indexed energy arrays.
- **Bass hit convergence**: Every bass onset during a step window triggers a converge-center snap — all movers aim center simultaneously.
- **Forced outro decay**: Outro ignores energy data and forces progressively lower dimmers based on position within the section (0%→100% progress = 120→0 dimmer).

## Custom VC Layout
- ▶ ACID RAIN (toggle, dark red #880000, 470×100) — starts main chaser
- BLACKOUT (toggle, red #FF0000, 470×80)

## Stats
- 162 scenes (+ blackout = scene 0), 163 chaser steps
- 149 unique scene fingerprints (13 legitimate duplicates from similar energy levels)
- Total generated duration: 282s (target ~263s track length)
- Analysis data: 509 beats, 15 segments, 113 bass / 369 drum / 65 vocal / 256 other onsets
