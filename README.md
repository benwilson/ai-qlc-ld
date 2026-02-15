# ai-qlc-ld

AI-assisted lighting design with QLC+. Uses Claude as a lighting designer to create DMX show files — programming fixtures, building musically-synced chasers, and generating complete QLC+ workspace files from song analysis data.

## How It Works

1. Drop audio files in `songs/`
2. Run `./analyze.sh` to extract BPM, beats, downbeats, and song structure via [all-in-one](https://github.com/mir-aidj/all-in-one)
3. Write a Python generator script that uses `showlib.py` to build scenes and chasers synced to the song structure
4. Load the generated `.qxw` file in QLC+ and hit play

## Setup

**Software:** QLC+ 5.0.1, outputting ArtNet to `10.0.0.7` on Universe 1.

**Song analysis** requires Docker:

```bash
# First run builds the image automatically (~5 min on Apple Silicon)
./analyze.sh

# Or analyze a specific file
./analyze.sh "Artist - Title.flac"
```

Results land in `songs-data/` as JSON with BPM, beat timestamps, downbeat timestamps, and labeled song segments (intro, verse, chorus, solo, break, outro, etc.).

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
├── fixtures/               # QLC+ fixture definitions (.qxf)
├── songs/                  # Audio files for analysis
├── songs-data/             # Analysis output (JSON)
├── references/             # QLC+ format documentation
├── analyze.sh              # Song analysis wrapper (Docker)
├── Dockerfile              # allin1 Docker image
└── DOCKERFILE.md           # Docker build notes and pitfalls
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

## Docker Image (allin1)

The `Dockerfile` builds a CPU-only image for [all-in-one](https://github.com/mir-aidj/all-in-one) music structure analysis. It runs natively on Apple Silicon (ARM64) and x86_64 Linux. See `DOCKERFILE.md` for build details, dependency pinning, and pitfalls.

Tested on: Apple M1 Pro (MacBook Pro 18,3), Docker Desktop for Mac.
