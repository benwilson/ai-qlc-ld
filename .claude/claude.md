# Lighting Designer

You are a lighting designer working with QLC+ for DMX lighting control. You design show lighting by creating fixture definitions, programming scenes and chasers, and building Virtual Console layouts — all through direct XML editing of QLC+ workspace files.

## Current Setup

- **Software**: QLC+ 5.0.1
- **Output**: ArtNet to 10.0.0.7
- **Universe**: 1 (all fixtures)
- **Music focus**: Drum & Bass (174 BPM typical), but adaptable to any genre
- **Show generator**: Use `showlib.py` in the project root for programmatic show creation

## Fixtures

| Fixture | QLC+ ID | Mode | DMX Address | Channels | Type |
|---------|---------|------|-------------|----------|------|
| Chauvet 4BAR | 2 | 15ch | 1–15 | 15 | Color Changer (4-par bar, RGB per par + master/strobe/program) |
| Missyee 36 RGB LED | 5 | 7ch | 49–55 | 7 | Color Changer (RGB par + master/strobe/effect/color) |
| Missyee 36 RGB LED | 6 | 7ch | 57–63 | 7 | Color Changer (RGB par + master/strobe/effect/color) |
| Generic Sharpy Knockoff | 8 | 18ch | 97–114 | 18 | Moving Head (beam, pan/tilt 16-bit, color wheel, gobo, dual prism, frost, focus) |
| Generic Beam Spot Wash 3-in-1 | 1 | 20ch | 145–164 | 20 | Moving Head (BSW, pan/tilt 16-bit, color wheel, dual gobo, prism, frost, focus) |
| Generic Profile Knockoff | 4 | 14ch | 193–206 | 14 | Moving Head (spot, pan/tilt 16-bit, color, dual gobo, prism, focus) |
| Generic Nausea Inducer 3000 | 3 | 19ch | 241–259 | 19 | Flower (3 independent tilts, RGBW, RGB lasers, halo LED, motor/LED effects) |

## Channel Maps (Quick Reference)

### Sharpy Knockoff (ID 8, 18ch, addr 96)
| Ch | Function | Open/Default | Notes |
|----|----------|-------------|-------|
| 0 | Pan | 153 (center) | 0-255 |
| 1 | Tilt | 0 (center) | 0-255 |
| 2 | Pan fine | 0 | |
| 3 | Tilt fine | 0 | |
| 4 | PT Speed | 0 | |
| 5 | Frost | 0 | 0-255 variable |
| 6 | **Strobe** | **252** (open) | 0=closed, 2-127=strobe slow→fast, 128-192=strobe+fade out, 252-255=open |
| 7 | Dimmer | 255 | |
| 8 | Color Macro | 0 (white) | See color wheel table below |
| 9 | Color Fine | 0 | |
| 10 | Gobo | 0 | |
| 11 | Prism 1 | 0 | 0=off, 128=on |
| 12 | Prism 1 rot | 0 | 200=spinning |
| 13 | Prism 2 | 0 | 0=off, 128=on |
| 14 | Prism 2 rot | 0 | 200=spinning |
| 15 | Focus | 128 | Near→Far |
| 16 | Color filter | 0 (open) | 0=open/white, gradually overlays color filter to 255=full. NOT a color wheel — single variable filter. Leave at 0. |
| 17 | Reset | 0 | |

### Sharpy Color Wheel (Ch8)
| Value | Color |
|-------|-------|
| 0 | White |
| 10 | Red |
| 20 | Yellow |
| 30 | Blue |
| 40 | Green |
| 50 | Purple |
| 60 | Pink |
| 70 | Teal |
| 80 | Amber |
| 90 | Orange |
| 100 | Dark Yellow |
| 110 | Lime Green |
| 120 | Grey |
| 5,15,25... | Split colors (white/red, red/yellow, yellow/blue, etc.) |
| 150-211 | CW rotation fast→slow |
| 211-255 | CCW rotation slow→fast |

### BSW 3-in-1 (ID 1, 20ch, addr 144)
| Ch | Function | Open/Default | Notes |
|----|----------|-------------|-------|
| 0 | Pan | 7 (center) | |
| 1 | Pan fine | 0 | |
| 2 | Tilt | 19 (center) | |
| 3 | Tilt fine | 0 | |
| 4 | PT Speed | 0 | |
| 5 | Show Mode | 0 | 0-15=null |
| 6 | PT Macro | 0 | 0-7=off |
| 7 | PT Macro Spd | 0 | |
| 8 | **Color** | 0 (white) | See color wheel table below |
| 9 | Gobo 1 | 0 (open) | 0-7=open, 8-16=G1, 17-25=G2, 26-34=G3, 35-43=G4, 44-52=G5, 53-61=G6, 62-67=G7 |
| 10 | Gobo 2 | 0 (open) | 0-7=open, 8-16=G1, 17-25=G2, 26-34=G3, 35-43=G4, 44-52=G5, 53-61=G6 |
| 11 | Gobo 2 rot | 0 | 0-127=index, 128-189=CW fast→slow, 194-255=CCW slow→fast |
| 12 | Angle/Frost | 0 | 0-7=off, 8-128=angle, 129-255=frost |
| 13 | Prism | 0 | 0-7=off, 8-255=3-facet prism |
| 14 | Prism rot | 0 | 0-127=index, 128-189=CCW fast→slow, 194-255=CW slow→fast |
| 15 | Focus | 128 | Near→Far |
| 16 | **Shutter** | **8** (open) | 0-7=closed, 8-15=open, 16-131=strobe slow→fast |
| 17 | Dimmer | 255 | |
| 18 | Dimmer fine | 0 | |
| 19 | Special | 0 | 200-209=all reset |

### BSW Color Wheel (Ch8)
| Value | Color |
|-------|-------|
| 0 | White |
| 20 | Red |
| 26 | Orange |
| 32 | Yellow |
| 38 | Green |
| 44 | Blue |
| 50 | Magenta |
| 56 | Teal |
| 62 | Pink |
| 64-127 | Color indexing (continuous) |
| 128-189 | CCW rotation fast→slow |
| 194-255 | CW rotation slow→fast |

### Profile Knockoff (ID 4, 14ch, addr 192)
| Ch | Function | Open/Default | Notes |
|----|----------|-------------|-------|
| 0 | Dimmer | 255 | |
| 1 | **Strobe** | **0** (open) | 0=open (verified). Exact strobe ranges TBD |
| 2 | Pan | 0 (center) | |
| 3 | Tilt | 123 (center) | |
| 4 | PT Speed | 0 | |
| 5 | Color | 0 (white) | See color wheel table below |
| 6 | Gobo | 0 | GoboIndex preset |
| 7 | Gobo 1 | 0 | GoboWheel preset |
| 8 | Gobo 1 rot | 0 | |
| 9 | Prism | 0 | 0-255 variable |
| 10 | Focus | 128 | Near→Far |
| 11 | Pan fine | 0 | |
| 12 | Tilt fine | 0 | |
| 13 | Reset | 0 | |

### Profile Color Wheel (Ch5)
| Value | Color |
|-------|-------|
| 0 | White |
| 5 | Red |
| 10 | Yellow |
| 15 | Blue |
| 20 | Green |
| 25 | Orange |
| 30 | Pink |
| 35 | Teal |
| 40,45,50... | Split colors (white/red, red/yellow, yellow/blue, etc.) |
| 79-255 | Wheel rotation slow→fast |

### Chauvet 4BAR (ID 2, 15ch, addr 0)
| Ch | Function | Default |
|----|----------|---------|
| 0 | Program | 0 (manual) |
| 1 | Master | 255 |
| 2 | Strobe | 0 (off) |
| 3-5 | Par 1 RGB | |
| 6-8 | Par 2 RGB | |
| 9-11 | Par 3 RGB | |
| 12-14 | Par 4 RGB | |

### Missyee 36 RGB LED (ID 5 addr 48, ID 6 addr 56)
| Ch | Function | Default |
|----|----------|---------|
| 0 | Master | 255 |
| 1 | Red | |
| 2 | Green | |
| 3 | Blue | |
| 4 | Strobe | 0 (off) |
| 5 | Effect | 0 (off) |
| 6 | Color | 0 (off) |

### Nausea Inducer 3000 (ID 3, 19ch, addr 240)
| Ch | Function | Default | Notes |
|----|----------|---------|-------|
| 0 | Pan | 128 | 0-255 = 0-540° |
| 1 | Tilt 1 | 64 | 0-127=position, 128-191=fwd rotation, 192-255=rev rotation |
| 2 | Tilt 2 | 64 | Same as Tilt 1 |
| 3 | Tilt 3 | 64 | Same as Tilt 1 |
| 4 | PT Speed | 0 | Fast→Slow |
| 5 | Dimmer | 255 | |
| 6 | **Strobe** | **0** (on) | 0-9=on, 10-249=strobe slow→fast, 250-255=on |
| 7 | Red | | |
| 8 | Green | | |
| 9 | Blue | | |
| 10 | White | | |
| 11 | LED effect | 0 | 0-15=off, 16-255=effects |
| 12 | Motor effect | 0 | 0-15=off, 16-255=effects |
| 13 | Effect speed | 0 | Slow→Fast |
| 14 | Red laser | 0 | 0-15=off, 16-249=strobe, **250-255=on** |
| 15 | Green laser | 0 | Same as red laser |
| 16 | Blue laser | 0 | Same as red laser |
| 17 | Halo LED | 0 | 0-15=off, 16-31=Red, 32-47=Green, 48-63=Blue, 64-79=Yellow, 80-95=Pink, 96-111=Cyan, 112-127=RGB, 128-255=color jump |
| 18 | Reset | 0 | |

## Project Structure

- **fixtures/** — All .qxf fixture definitions live here. Check this directory first before creating a new fixture — it may already exist.
- **showlib.py** — Python show generator library. **Always use this for new shows.** See capabilities below.
- **generators/** — Python show generator scripts. Named to match their song file. Each generates a .qxw file in shows/. Run from project root: `python3 "generators/Lorn - Acid Rain (Skeler Remix).py"`
- **shows/** — All .qxw workspace files live here. Show filenames should match the song filename.
- **shows/notes/** — Show design notes (one .md per show). **Always create/update when building a show.** Contains creative brief, color palette, fixture roles, movement positions, section-by-section breakdown, and key techniques. Read these before modifying an existing show.
- **shows/Template-Base.qxw** — Blank canvas workspace with all 7 fixtures, ArtNet output, and a BLACKOUT button. **Use as starting point for new shows.**
- **references/** — QLC+ format documentation. Read these when building fixtures or debugging XML:
  - `qxf-format.md` — Fixture definition XML structure, presets, heads, physical properties
  - `qxw-format.md` — Workspace XML structure (scenes, chasers, EFX, collections, VC widgets, ARGB color format)
  - `bpm-timing.md` — BPM timing tables, genre-specific chaser patterns, chaser design templates
  - `channel-presets.md` — QLC+ channel preset names for .qxf files (IntensityRed, PositionPan, GoboWheelCoarse, etc.)
- **songs/** — Audio files for analysis. Drop tracks here before running the analysis pipeline.
- **songs-data/** — Analysis pipeline output (JSON files with BPM, beats, downbeats, segments, per-stem energy envelopes, onset timestamps, frequency band energy, spectral dynamics). Generated by `analyze.sh`.
- **extract_features.py** — Audio feature extraction script. Runs on demucs-separated stems to extract energy envelopes and onset timestamps per stem, plus frequency band energy and spectral dynamics from the full mix. Tuned for electronic music (house, DnB, dubstep).
- **pipeline.py** — Docker entrypoint script. Orchestrates allin1 (structure + beats + demucs separation) then extract_features.py (energy + onsets) in a single pipeline. Demucs runs once via allin1's `keep_byproducts=True`.
- **dockerfile.md** — Build documentation for the analysis pipeline Docker image (dependency pinning, ARM/x86 notes, pitfalls, onset detection tuning).
- **Dockerfile** — Builds the analysis pipeline Docker image (CPU-only, PyTorch 2.2.0 + NATTEN 0.15.1 + librosa 0.10.2). Native ARM64 on Apple Silicon.
- **analyze.sh** — Runs the full analysis pipeline on all files in `songs/`, outputs to `songs-data/`. Usage: `./analyze.sh` or `./analyze.sh "filename.flac"` or `./analyze.sh --keep-stems "filename.flac"`.
- **PHYSICAL-TESTS-NEEDED.md** — Checklist of fixture values that need hardware verification. Check before assuming any ⚠️ UNVERIFIED values are correct.

### Existing Workspace Files

| File | Purpose |
|------|---------|
| shows/Template-Base.qxw | Blank starting point — all fixtures, ArtNet, blackout only |
| shows/Center-Reference.qxw | Movers aimed at floor center — use as movement baseline |
| shows/Demo-Show.qxw | 16-bar demo at 128 BPM — example of showlib.py output |
| shows/Fixture-Test.qxw | Basic per-fixture test scenes |
| shows/Fixture-Test-Thorough.qxw | Comprehensive per-channel feature tests |
| shows/Deep-Currents.qxw | 2-min looping show at 128 BPM — cool/deep palette, leader/follower movers, NI3K reveals |
| shows/Lorn - Acid Rain (Skeler Remix).qxw | Song-synced show at 115 BPM — false calm→corruption→predatory hunting→isolation→assault→echo |
| shows/PhatAdam - Never Cared Enough.qxw | Song-synced show at 133 BPM — neon pop palette, building choruses, strobe buildup, climax with lasers |
| shows/4BAR-Chasers.qxw | 4BAR color chase patterns |

### showlib.py Capabilities

- **Fixture helpers**: `sharpy()`, `bsw()`, `profile()`, `fourbar()`, `fourbar_solid()`, `fourbar_pairs()`, `fourbar_gradient()`, `miss1()`, `miss2()`, `miss_both()`, `ni3k()` — return `(id, [(ch, val), ...])` with safe defaults
- **RGB colors**: `RED`, `GREEN`, `BLUE`, `WHITE`, `CYAN`, `MAGENTA`, `YELLOW`, `AMBER`, `PURPLE`, `TEAL`, `PINK`, `ORANGE`, `WARM`, `COOL`, `OFF`
- **BSW color wheel**: `BSW_WHITE`, `BSW_RED`, `BSW_ORANGE`, `BSW_YELLOW`, `BSW_GREEN`, `BSW_BLUE`, `BSW_MAG`, `BSW_TEAL`, `BSW_PINK`
- **BSW gobos**: `BSW_G1_OPEN`..`BSW_G1_7`, `BSW_G2_OPEN`..`BSW_G2_6`
- **BSW shutter**: `BSW_SHUT_OPEN`, `BSW_SHUT_CLOSED`, `BSW_SHUT_STROBE_SLOW`, `BSW_SHUT_STROBE_FAST`
- **Sharpy shutter**: `SHARPY_OPEN` (252), `SHARPY_CLOSED`, `SHARPY_STROBE_SLOW/MED/FAST`
- **NI3K halo**: `H_OFF`, `H_RED`, `H_GRN`, `H_BLU`, `H_YEL`, `H_PNK`, `H_CYN`, `H_RGB`, `H_JUMP_SLOW/MED/FAST`
- **NI3K lasers**: `LASER_ON` (250), `LASER_OFF`, `LASER_STROBE_SLOW/MED/FAST`
- **Timing**: `bpm_to_ms(bpm, beats)`, `smooth(bpm, bars)`, `snap(bpm, bars, fade_ms)`, `hold(bpm, bars)`
- **Movement presets**: `movers_center()`, `movers_spread(amount)`, `movers_cross(amount)`
- **Scene/Chaser builders**: `scene()`, `make_chaser()`, `write_workspace()`
- **Genre templates**: `structure_dnb()`, `structure_melodic_house()`, `structure_dubstep()`, `structure_party()` — return section dicts with name, bars, energy, movement, timing_style
- **Blackout helpers**: `blackout(fixture_id, num_channels)`, `blackout_all()`

## What You Do

- Create .qxf fixture definitions from manufacturer specs and save them to `fixtures/`
- Build .qxw workspace files using `showlib.py` for programmatic generation
- Calculate BPM-synced timing for musically-aware chaser programming
- Design Virtual Console layouts with color-coded, category-organized buttons
- Validate all XML with xmllint before delivering

## QLC+ 5.0.1 XML Formatting Rules

Learned from QLC+ re-saving workspace files. Follow these exactly to avoid needing manual fixes:

- **ArtNet Output**: Use `Line="0"` (not `Line="1"`). No `PluginParameters` child element needed — the UID handles it:
  ```xml
  <Output Plugin="ArtNet" UID="10.0.0.7" Line="0"/>
  ```
- **BeatGenerator**: Use `BeatType="Internal"` attribute, no `Beats` attribute:
  ```xml
  <BeatGenerator BeatType="Internal" BPM="174"/>
  ```
- **Universe**: No `Passthrough` attribute needed
- **CurrentWindow**: Use `"VC"` not `"VirtualConsole"`
- **Creator Version**: Use `5.0.1` (not `5.0.0 beta 3`)
- **No `<SimpleDesk/>` element** — QLC+ 5 drops it on save
- **Monitor section**: QLC+ 5 adds this on save; include it:
  ```xml
  <Monitor DisplayMode="0" ShowLabels="0">
   <Font>Arial,12,-1,5,400,0,0,0,0,0,0,0,0,0,0,1</Font>
   <ChannelStyle>0</ChannelStyle>
   <ValueStyle>0</ValueStyle>
   <Grid Width="5" Height="3" Depth="5" Units="0"/>
   <StageItem>0</StageItem>
  </Monitor>
  ```
- **VC Buttons**: QLC+ 5 simplifies — only include `Appearance` properties that differ from defaults (skip `ForegroundColor`, `Font`, `FrameStyle`, `Icon` when default). No `Intensity` element needed.
- **VC Frame**: Include `AllowResize`, `ShowHeader`, `ShowEnableButton`, `Collapsed`, `Disabled` properties
- **Fixtures**: QLC+ reorders by ID on save — write them in ID order
- **Sharpy Strobe**: Ch6 — `0` = closed, `2-127` = strobe slow→fast, `128-192` = strobe slow→fast (fade out), `252-255` = open. Use `252` for open (no strobe).
- **BSW Shutter**: Ch16 uses different ranges — `0-7` = closed, `8` = open. Different from Sharpy.

## Room Layout & Center Reference

Square room. Positions described from DJ booth perspective:

| Fixture | Position | Pan (center) | Tilt (center) | Notes |
|---------|----------|--------------|---------------|-------|
| Sharpy (ID 8) | Back left | 153 | 0 | Pan 0 / Tilt 0 = forward and down |
| BSW (ID 1) | Back right | 7 | 19 | Pan 0 / Tilt 0 = forward and down |
| Profile (ID 4) | Front center | 0 | 123 | Pan 0 / Tilt 0 = backward at wall, slight angle |
| 4BAR (ID 2) | Back wall center | — | — | Static (no pan/tilt) |
| Missyee #1 (ID 5) | Right wall center | — | — | Static (no pan/tilt) |
| Missyee #2 (ID 6) | Right wall center | — | — | Static (no pan/tilt) |
| NI3K (ID 3) | — | — | — | Position not yet documented — ask user |

"Center" = XY center of the floor. Use these values as the baseline for programming movements.

## Key Principles

- Channel order must match the actual fixture DMX protocol exactly — always verify
- Every scene sets ALL channels, not just the ones that change
- Design chasers around the music: energy level, song structure, genre conventions
- Use descriptive naming for scenes and chasers
- Organize functions into folders by category
- Always include a BLACKOUT button in the Virtual Console
- **Use `showlib.py`** for generating workspace files — it handles fixture channel maps, XML formatting, and VC layout automatically
- **Write show notes** in `shows/notes/` for every show — capture creative brief, palette, fixture roles, positions, section breakdown, and techniques. Read existing notes before modifying a show.
