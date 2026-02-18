# ai-qlc-ld

AI-assisted lighting design with QLC+. Uses Claude as a lighting designer to create DMX show files — programming fixtures, building musically-synced chasers, generating busking workspaces, and producing complete QLC+ workspace files from song analysis data.

## How It Works

There are two main workflows: **busking** (live, improvised) and **song-synced shows** (pre-programmed).

### Busking (Live Lighting)

For real-time lighting control during DJ sets. Claude generates a QLC+ workspace with layered controls — color palettes, position presets, movement effects, strobes, and special moments — all organized in the Virtual Console for on-the-fly operation.

1. Set up a venue (plot → patch → focus-positions)
2. Pick a genre (or create one)
3. Optionally pick a mood to shape the feel
4. Generate the busking workspace

### Song-Synced Shows

For pre-programmed shows synced to a specific track. Just name a song (or say "pick one") and Claude handles the rest.

1. Drop audio files in `songs/`
2. Tell Claude which song to analyze (or ask it to pick an unanalyzed one)
3. Claude runs `./analyze.sh`, reviews the analysis data, and asks about creative direction
4. Claude writes a Python generator, produces the `.qxw`, and validates it
5. Load the generated `.qxw` file in QLC+ and hit play

## Skills

Skills are specialized instructions that guide Claude through specific tasks. They chain together in a dependency order — each skill produces files that downstream skills consume.

### Venue Setup (run once per venue)

| Step | Skill | Creates | Depends On |
|------|-------|---------|------------|
| 1 | **plot** | `venue/<name>/plot.md` | — (starting point) |
| 2 | **patch** | `venue/<name>/patch.md` | plot.md |
| 3 | **focus-positions** | `venue/<name>/focus-positions.md` | plot.md + patch.md |

**plot** places fixtures in 3D space — room dimensions, fixture types, XYZ coordinates, orientations. Just describe where things go ("Sharpy back left, up high") and Claude converts to coordinates.

**patch** assigns DMX addresses, fixture IDs, and channel modes from the plot.

**focus-positions** defines named pan/tilt targets (like "DSL", "Ceiling Hit", "DJ Booth") for every mover, so shows and busking workspaces can reference positions by name instead of raw DMX values.

### Content Definition (run as needed)

| Skill | Creates | Purpose |
|-------|---------|---------|
| **genres** | `genres/<genre>.md` | Color palettes, timing presets, movement conventions, strobe/laser/gobo rules |
| **moods** | `moods/<mood>.md` | Abstract modifiers that shape how a genre's values get applied |

**Genres** define concrete lighting values for an EDM subgenre — specific colors (with per-fixture wheel mappings), BPM-calibrated timing, per-section energy profiles, and effect conventions. Available: drum-and-bass, dubstep, house, techno, trance.

**Moods** define abstract modifiers — color filtering, intensity scaling, movement speed, effect density, timing adjustments. They never specify DMX values directly; they modify what the genre provides. A mood applied to different genres produces different concrete results but the same emotional character.

Available moods — emotional states: dark, ethereal, aggressive, hypnotic, euphoric, melancholic, chaotic, intimate. Energy levels: chill, building, peak, comedown.

### Generation

| Skill | Creates | Reads |
|-------|---------|-------|
| **busking** | `venue/<name>/shows/Busking-<Genre>.qxw` | patch + focus-positions + genre + mood |
| **song-analysis** | analysis JSON + show generator + `.qxw` | song audio + venue files + genre + mood |

**busking** generates a complete Virtual Console layout for live operation: color pair buttons (Solo Frame), position presets (Solo Frame), movement chasers, intensity sliders, strobe/flash buttons, and special moment buttons (blackout, whiteout, lasers, prism, etc.).

**song-analysis** is the entry point for song-synced shows. Finds a song (or picks an unanalyzed one), runs the Docker analysis pipeline, presents a summary of BPM/structure/energy, then gathers creative direction and builds the show generator.

### How Genre + Mood Combine

Genre provides the raw material (specific colors, ms timing, DMX channel values). Mood applies filters and multipliers (prefer cool colors, dim to 60%, slow movement 0.5x, no strobe). The busking skill reads both files and applies the mood's modifiers to the genre's values.

Example: "Ethereal" mood + DnB genre = DnB's blue/cyan palette with slower movements, longer fades, no strobes. Same "Ethereal" + House = house's teal/blue palette with even smoother fades and minimal effects.

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

## CI Command

Run the full test suite with:

```bash
./ci.sh
```

This runs all `unittest` test files under `tests/` via discovery.

The analysis pipeline runs two stages in a single pass:

1. **allin1** — BPM, beat/downbeat timestamps, song structure segments (intro, verse, chorus, break, etc.), and demucs source separation
2. **Feature extraction** — per-stem (bass, drums, vocals, other) energy envelopes and onset timestamps, frequency band energy (sub-bass through high), spectral centroid/flux, and onset strength

Results land in `songs-data/` as JSON. Onset timestamps give you the exact time of every individual note/hit per stem — during a quiet breakdown, you get timestamps for each piano or synth note, which generators can map directly to light cues.

## Project Structure

```
├── showlib.py              # Show generator library (fixtures, colors, timing, XML)
├── venue/                  # Venue directories (shows, generators, plots per venue)
│   └── home-studio/
│       ├── plot.md         # Fixture positions in 3D space
│       ├── patch.md        # DMX patch (IDs, addresses, modes)
│       ├── focus-positions.md  # Named focus positions (pan/tilt per mover)
│       ├── shows/          # Generated .qxw workspace files
│       │   ├── Template-Base.qxw  # Auto-generated from plot.md
│       │   └── notes/      # Show design notes (one .md per show)
│       └── generators/     # Per-song generator scripts
├── genres/                 # EDM subgenre lighting definitions (one .md per genre)
├── moods/                  # Mood modifier definitions (one .md per mood)
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

Generator scripts live in `venue/<name>/generators/` and are named to match their song file. Each one imports `showlib` and writes output to the venue's `shows/` directory:

```python
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
from showlib import *

scenes = [
    scene("Blackout", *blackout_all()),
    scene("Blue Wash",
        sharpy(pan=153, tilt=0, dim=200, frost=180),   # pan/tilt from focus-positions.md
        bsw(pan=7, tilt=19, color=BSW_BLUE, dim=180),  # pan/tilt from focus-positions.md
        profile(pan=0, tilt=123, dim=150),              # pan/tilt from focus-positions.md
        fourbar_solid(0, 40, 180),
        *miss_both(0, 60, 140),
        ni3k(r=20, g=40, b=160, halo=H_BLU),
    ),
]

chaser = make_chaser("Main", [0, 1], [hold(115), smooth(115, 4)])
write_workspace(os.path.join(VENUE_DIR, "shows", "My-Show.qxw"), scenes, [chaser], bpm=115)
```

Run from the project root:

```bash
python3 "venue/home-studio/generators/Lorn - Acid Rain (Skeler Remix).py"
```

### showlib.py Provides

**Fixture helpers** with safe defaults and correct channel maps: `sharpy()`, `bsw()`, `profile()`, `fourbar()`, `fourbar_solid()`, `fourbar_pairs()`, `fourbar_gradient()`, `miss1()`, `miss2()`, `miss_both()`, `ni3k()`

**Color constants** for RGB fixtures: `RED`, `GREEN`, `BLUE`, `WHITE`, `CYAN`, `MAGENTA`, `YELLOW`, `AMBER`, `PURPLE`, `TEAL`, `PINK`, `ORANGE`, `WARM`, `COOL`, `OFF`

**BSW color wheel / gobos / shutter**, **Sharpy shutter**, **NI3K halo / lasers**: named constants matching actual DMX values

**Timing helpers**: `bpm_to_ms()`, `smooth()`, `snap()`, `hold()`

**Genre templates**: `structure_dnb()`, `structure_melodic_house()`, `structure_dubstep()`, `structure_party()`

**Venue template**: `generate_venue_template(venue_dir, bpm)` — reads a venue's `plot.md` and generates a `Template-Base.qxw` with only the fixtures placed in that venue

## Shows (venue/home-studio)

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
