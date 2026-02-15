# ai-qlc-ld

AI-assisted lighting design with QLC+. Uses Claude as a lighting designer to create DMX show files — programming fixtures, building musically-synced chasers, and generating complete QLC+ workspace files from song analysis data.

## How It Works

1. Drop audio files in `songs/`
2. Run `./analyze.sh` to analyze tracks — extracts BPM, beats, song structure, per-stem energy envelopes, onset timestamps, and spectral dynamics
3. Write a Python generator script that uses `showlib.py` to build scenes and chasers synced to the analysis data
4. Load the generated `.qxw` file in QLC+ and hit play

## Setup

**Software:** QLC+ 5.0.1, outputting ArtNet to `10.0.0.7` on Universe 1.

**Song analysis** requires Docker:

```bash
# First run builds the image automatically (~5 min on Apple Silicon)
./analyze.sh

# Or analyze a specific file
./analyze.sh "Artist - Title.flac"

# Keep demucs WAV stems after analysis
./analyze.sh --keep-stems "Artist - Title.flac"
```

The analysis pipeline runs two stages in a single pass:

1. **allin1** — BPM, beat/downbeat timestamps, song structure segments (intro, verse, chorus, break, etc.), and demucs source separation
2. **Feature extraction** — per-stem (bass, drums, vocals, other) energy envelopes and onset timestamps, frequency band energy (sub-bass through high), spectral centroid/flux, and onset strength

Results land in `songs-data/` as JSON. Onset timestamps give you the exact time of every individual note/hit per stem — during a quiet breakdown, you get timestamps for each piano or synth note, which generators can map directly to light cues.

## Fixtures

| Fixture | ID | DMX Address | Type |
|---------|-----|-------------|------|
| Generic BSW 3-in-1 | 1 | 145–164 | Moving Head (20ch) |
| Chauvet 4BAR | 2 | 1–15 | 4-par RGB bar (15ch) |
| Generic Nausea Inducer 3000 | 3 | 241–259 | Flower/laser/halo (19ch) |
| Generic Profile Knockoff | 4 | 193–206 | Moving Head spot (14ch) |
| Missyee 36 RGB LED #1 | 5 | 49–55 | RGB par (7ch) |
| Missyee 36 RGB LED #2 | 6 | 57–63 | RGB par (7ch) |
| Generic Sharpy Knockoff | 8 | 97–114 | Moving Head beam (18ch) |

## Project Structure

```
├── showlib.py              # Show generator library (fixtures, colors, timing, XML)
├── generators/             # Per-song generator scripts
│   ├── Lorn - Acid Rain (Skeler Remix).py
│   └── gen_deep_currents.py
├── shows/                  # Generated .qxw workspace files
│   ├── Template-Base.qxw   # Blank starting point
│   └── ...
├── venue/                  # Venue fixture plots (physical positions in 3D space)
│   └── home-studio/plot.md # Current rig layout
├── fixtures/               # QLC+ fixture definitions (.qxf)
├── songs/                  # Audio files for analysis
├── songs-data/             # Analysis output (JSON — structure + energy + onsets)
├── references/             # QLC+ format documentation
├── analyze.sh              # Analysis pipeline wrapper (Docker)
├── pipeline.py             # Docker entrypoint — orchestrates allin1 + feature extraction
├── extract_features.py     # Stem energy envelopes + onset detection (librosa)
├── Dockerfile              # Analysis pipeline Docker image
└── dockerfile.md           # Docker build notes, output format, and pitfalls
```

## Writing a Show Generator

Generator scripts live in `generators/` and are named to match their song file. Each one imports `showlib` and builds scenes programmatically:

```python
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from showlib import *

scenes = [
    scene("Blackout", *blackout_all()),
    scene("Blue Wash",
        sharpy(pan=153, tilt=0, dim=200, frost=180),
        bsw(pan=7, tilt=19, color=BSW_BLUE, dim=180),
        profile(pan=0, tilt=123, dim=150),
        fourbar_solid(0, 40, 180),
        *miss_both(0, 60, 140),
        ni3k(r=20, g=40, b=160, halo=H_BLU),
    ),
]

chaser = make_chaser("Main", [0, 1], [hold(115), smooth(115, 4)])
write_workspace("shows/My-Show.qxw", scenes, [chaser], bpm=115)
```

Run from the project root:

```bash
python3 "generators/Lorn - Acid Rain (Skeler Remix).py"
```

### showlib.py Provides

**Fixture helpers** with safe defaults and correct channel maps: `sharpy()`, `bsw()`, `profile()`, `fourbar()`, `fourbar_solid()`, `fourbar_pairs()`, `fourbar_gradient()`, `miss1()`, `miss2()`, `miss_both()`, `ni3k()`

**Color constants** for RGB fixtures: `RED`, `GREEN`, `BLUE`, `WHITE`, `CYAN`, `MAGENTA`, `YELLOW`, `AMBER`, `PURPLE`, `TEAL`, `PINK`, `ORANGE`, `WARM`, `COOL`, `OFF`

**BSW color wheel / gobos / shutter**, **Sharpy shutter**, **NI3K halo / lasers**: named constants matching actual DMX values

**Timing helpers**: `bpm_to_ms()`, `smooth()`, `snap()`, `hold()`

**Movement presets**: `movers_center()`, `movers_spread()`, `movers_cross()`

**Genre templates**: `structure_dnb()`, `structure_melodic_house()`, `structure_dubstep()`, `structure_party()`

## Shows

| Show | BPM | Description |
|------|-----|-------------|
| Lorn - Acid Rain (Skeler Remix) | 115 | Song-synced — false calm → corruption → predatory hunting → eerie isolation → lockstep assault → echo |
| PhatAdam - Never Cared Enough | 133 | Song-synced — neon pop palette, building choruses, strobe buildup, climax with strobes + lasers |
| Deep Currents | 128 | 2-min loop — cool/deep palette, leader/follower movers, NI3K dramatic reveals |

## Analysis Pipeline (Docker)

The `Dockerfile` builds a CPU-only image that combines [all-in-one](https://github.com/mir-aidj/all-in-one) (structure/beats), [demucs](https://github.com/facebookresearch/demucs) (source separation), and [librosa](https://librosa.org/) (feature extraction). Demucs runs once — allin1 uses it for structure analysis, and the stems are reused for feature extraction before being cleaned up.

Tuned for electronic music (house, DnB, dubstep): frequency bands target sub-bass (20–80Hz) through highs (2k+), and onset detection parameters are calibrated per stem type (sensitive for synth/piano, sustained for bass, transient for drums).

Runs natively on Apple Silicon (ARM64) and x86_64 Linux. See `dockerfile.md` for build details, dependency pinning, output format, and pitfalls.

Tested on: Apple M1 Pro (MacBook Pro 18,3), Docker Desktop for Mac.
