---
name: song-analysis
description: >
  Analyze songs and launch show creation. Finds a user-specified song (or picks an
  unanalyzed one), runs the analysis pipeline via ./analyze.sh, reviews the results,
  and transitions into show creation. Use this skill when the user wants to analyze
  a song, create a show for a song, mentions a specific track name, says "analyze,"
  "new show," "light this track," "pick a song," or drops a new audio file into songs/.
---

# Song Analysis

Analyze audio files and launch show creation. This skill is the bridge between raw
audio and a finished QLC+ show — it handles finding the song, running analysis, reviewing
the data, and handing off to the show creation workflow.

## When to Use

- User says "analyze," "analyze this song," "run analysis," or "analyze all"
- User names a specific track ("let's do a show for Acid Rain")
- User says "pick a song" or "what hasn't been analyzed yet"
- User says "new show," "create a show," "light this track," or "make a show for..."
- User drops a new audio file into `songs/`
- User wants to re-analyze a track (maybe with `--keep-stems`)

## Prerequisites

- **Docker** must be running on the host machine. The analysis pipeline runs inside
  a Docker container. If the image doesn't exist, `analyze.sh` builds it automatically
  (~5 min first run on Apple Silicon).
- **Venue** must be set up (plot + patch + focus-positions) before show creation can
  begin. Analysis doesn't require a venue, but the show creation handoff does.

## Workflow

### Step 1: Find the Song

There are three entry points:

#### A. User specifies a song
Match the user's description to a file in `songs/`. Use fuzzy matching — "acid rain"
should match `Lorn - Acid Rain (Skeler Remix).flac`. If multiple files match, list
them and ask which one.

If the file isn't in `songs/`, tell the user to drop it there first.

#### B. User says "pick one" or "what's next"
List songs in `songs/` that don't have a corresponding JSON in `songs-data/` (compare
filenames without extensions). If all songs have results, list them with their analysis
status and whether they have an existing show generator.

Present the options:

```
Unanalyzed songs:
  - New Track.flac (no analysis data)

Analyzed but no show:
  - Some Other Track.flac (analyzed, no generator)

Complete (has show):
  - Lorn - Acid Rain (Skeler Remix).flac (analyzed + generator + show)
```

#### C. User says "analyze all"
Run `./analyze.sh` with no arguments — it auto-skips songs with existing results.

### Step 2: Check Existing Analysis

Before running analysis, check if `songs-data/<stem>.json` already exists (where
`<stem>` is the filename without extension).

- **If it exists**: Tell the user the analysis is already done. Show the key stats
  (BPM, duration, segment count, stem onset counts). Ask if they want to re-analyze
  or proceed to show creation.
- **If it doesn't exist**: Proceed to Step 3.

### Step 3: Run Analysis

Run the analysis pipeline:

```bash
./analyze.sh "filename.ext"
```

This runs inside Docker and takes approximately:
- 1-3 minutes for a typical 3-5 minute track on Apple Silicon
- Longer on first run (Docker image build)

**Important**: The analyze.sh script must be run from the project root directory.
The script auto-detects the songs/ and songs-data/ directories relative to itself.

If the user wants to keep stems for manual review:
```bash
./analyze.sh --keep-stems "filename.ext"
```

After analysis completes, verify the output JSON exists in `songs-data/`.

### Step 4: Review Analysis Results

Read the JSON from `songs-data/<stem>.json` and present a human-readable summary:

```
Analysis complete for "Artist - Track"

  BPM: 174
  Duration: 3:42 (222 beats, 55 bars)
  First beat: 2.1s (1.5 bars of silence before music)

  Song structure (8 sections):
    0:00 - 0:28  intro       (7 bars, low energy)
    0:28 - 0:56  verse       (7 bars, building)
    0:56 - 1:25  chorus      (7 bars, high energy)
    ...

  Energy signature:
    Sub-bass peak: 0.92 (during chorus sections)
    Drums most active: 305 onsets (every beat + fills)
    Melodic hits (other): 186 onsets
    Vocals: 28 onsets (sparse — instrumental-heavy track)

  Key moments:
    Likely drop at 0:56 (sub-bass jumps from 0.1 → 0.85)
    Energy peak at 2:10 (RMS = 0.94)
    Breakdown at 1:25 (RMS drops to 0.12)
```

To build this summary:

1. **BPM**: Read `bpm` field. Check for half-time detection — if BPM is under 90 and
   the genre is EDM, it's likely half-time (actual BPM = reported × 2). Flag this.
2. **Duration**: Calculate from last beat timestamp. Count total beats and bars (beats ÷ 4).
3. **Pre-beat silence**: `beats[0]` tells you when music actually starts. If > 2s,
   note this — the generator needs to account for it.
4. **Song structure**: List each segment with start/end times converted to mm:ss,
   duration in bars, and rough energy level based on RMS at that section's beats.
5. **Energy signature**: Peak values from `energy.sub_bass`, `energy.rms`, stem onset
   counts from `stems.*.onset_count`.
6. **Key moments**: Scan for drops (sub-bass jumps > 0.5 between adjacent beats),
   energy peaks (highest RMS values), breakdowns (RMS drops > 0.5).

### Step 5: Transition to Show Creation

After presenting the analysis summary, transition to the **qlc-show-workflow** pipeline:

1. **Which venue?** (list available venues from `venue/` subdirectories)
2. Run scaffold: `python3 scripts/show_workflow.py scaffold --song "<Artist - Song>" --venue <dir>`
3. Follow the qlc-show-workflow pipeline (see `skills/qlc-show-workflow/SKILL.md`):
   - Fill research brief (artist branding, song motifs, thesis, 5+ sources) → set status=approved
   - Validate brief
   - Build phrase-aware generator using `require_research_brief()`, `build_creative_context()`, `classify_phrase()`, `pick_phrase_technique()`
   - Generate .qxw
   - Validate invariants

Creative direction now comes from research briefs + the phrase planner + designer packs,
not from genre/mood .md files. Genre and mood files are still used by the **busking** skill
for live improvised lighting.

## Analysis Data Reference

The JSON output contains these key fields (see `dockerfile.md` for full format):

| Field | Type | Description |
|-------|------|-------------|
| `bpm` | int | Detected BPM (may be half-time for some genres) |
| `beats` | float[] | Timestamp (seconds) of every beat |
| `downbeats` | float[] | Timestamp of every bar start (beat 1) |
| `beat_positions` | int[] | Which beat in bar (1-4) for each beat |
| `segments` | object[] | Song sections: `{start, end, label}` |
| `energy.sub_bass` | float[] | Sub-bass (20-80Hz) energy per beat, 0.0-1.0 |
| `energy.bass` | float[] | Bass (80-250Hz) energy per beat |
| `energy.low_mid` | float[] | Low-mid (250-500Hz) energy per beat |
| `energy.mid` | float[] | Mid (500-2kHz) energy per beat |
| `energy.high` | float[] | High (2k+) energy per beat |
| `energy.rms` | float[] | Overall loudness per beat |
| `dynamics.spectral_centroid` | float[] | Brightness (Hz) per beat |
| `dynamics.spectral_flux` | float[] | Spectral change rate per beat |
| `dynamics.onset_strength` | float[] | Impact of each beat, 0.0-1.0 |
| `stems.bass.energy` | float[] | Bass stem energy per beat |
| `stems.bass.onsets` | float[] | Bass note timestamps (seconds) |
| `stems.drums.energy` | float[] | Drums stem energy per beat |
| `stems.drums.onsets` | float[] | Drum hit timestamps |
| `stems.vocals.energy` | float[] | Vocals stem energy per beat |
| `stems.vocals.onsets` | float[] | Vocal onset timestamps |
| `stems.other.energy` | float[] | Other (synths/melody) energy per beat |
| `stems.other.onsets` | float[] | Melodic hit timestamps |

### Half-Time BPM Detection

The allin1 analyzer sometimes reports half-time BPM for genres with strong half-time
feel (dubstep, some trap, some DnB). Signs of half-time misdetection:

- BPM is 60-90 for a track that's clearly EDM
- Beats array has roughly half the expected number of entries
- Sub-bass energy patterns repeat every 2 "beats" instead of every 4

When this happens, note it in the analysis summary and use `bpm × 2` for timing
calculations in the generator. The beat timestamps are still correct — they're just
spaced at half-bars instead of beats.

## Important Notes

- **Docker is required** — analysis cannot run without it. If Docker isn't available,
  tell the user and explain the setup.
- **analyze.sh runs from the project root** — don't cd into songs/ first.
- **The analysis JSON is the source of truth** for timing in generators. Don't
  approximate — use the actual beat timestamps and segment boundaries.
- **Always check for pre-beat silence** — if `beats[0]` is significantly after 0.0s,
  the generator needs to handle those silent bars as a dark/ambient intro.
- **Show notes are mandatory** — always create `venue/<name>/shows/notes/<Song>.md`
  before or alongside the generator. This documents creative decisions for future edits.
- **Read existing show notes** before modifying an existing show — they capture palette
  choices, fixture roles, and section breakdowns that should be preserved unless the
  user explicitly wants changes.
- **Filename matching** — the generator, show, and notes files should all use the same
  name as the song file (minus the audio extension). This keeps everything findable.
