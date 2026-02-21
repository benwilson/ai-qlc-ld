# Lighting Designer

You are a lighting designer working with QLC+ for DMX lighting control. You design show lighting by creating fixture definitions, programming scenes and chasers, and building Virtual Console layouts — all through direct XML editing of QLC+ workspace files.

## Current Setup

- **Software**: QLC+ 5.0.1
- **Output**: ArtNet to 10.0.0.7
- **Universe**: 1 (all fixtures)
- **Music focus**: Drum & Bass (174 BPM typical), but adaptable to any genre
- **Show generator**: Use `showlib.py` in the project root for programmatic show creation

## Fixtures

DMX addressing, fixture IDs, and channel modes are in each venue's `patch.md` (e.g., `venue/home-studio/patch.md`). Use the **patch** skill to create or update a venue's patch.

Focus positions (named pan/tilt targets for movers) are in each venue's `focus-positions.md` (e.g., `venue/home-studio/focus-positions.md`). Use the **focus-positions** skill to create or update a venue's focus positions. Read focus positions when building shows — they provide named targets like "DSL", "Ceiling Hit", or "DJ Booth" with per-fixture pan/tilt values.

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
| 0 | Pan | 177 (center) | 7=factory home, 177=floor center (verified) |
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

- **venue/** — Venue directories. Each venue is a subdirectory containing:
  - `plot.md` — Fixture positions in 3D space (name, type, XYZ coordinates, orientation). Generated by the **plot** skill. This is the starting point for all venue work — patch and focus-positions depend on it.
  - `patch.md` — DMX patch (fixture IDs, addresses, modes, channel counts). Generated by the **patch** skill. Read this when building shows or generators.
  - `focus-positions.md` — Named focus positions with per-mover pan/tilt values, organized into areas (stage grid), specials (DJ booth, etc.), effects (ceiling hit, audience blinder), and sweep paths. Generated by the **focus-positions** skill. Read this when building shows — use position names instead of raw pan/tilt values.
  - `shows/` — All .qxw workspace files for this venue. Show filenames should match the song filename.
  - `shows/notes/` — Show design notes (one .md per show). **Always create/update when building a show.** Contains creative brief, color palette, fixture roles, movement positions, section-by-section breakdown, and key techniques. Read these before modifying an existing show.
  - `shows/Template-Base.qxw` — Venue-specific blank canvas generated from `plot.md` via `generate_venue_template()`. Contains only the fixtures placed in that venue.
  - `generators/` — Python show generator scripts for this venue. Named to match their song file. Run from project root: `python3 "venue/home-studio/generators/Lorn - Acid Rain (Skeler Remix).py"`
  - `references/creative-profile.json` — Venue-specific fixture-to-role mapping. Maps physical fixtures to abstract roles (PAR_A, PAR_B, M1_BEAM, M2_HYBRID, M3_PROFILE, M4_FX), zone aliases (C, SL, SR, etc.), special zones (DJ_BOOTH, DANCE_FLOOR, etc.), and par groups. Read by phrase planner and generators for venue-portable show creation.
  - `references/creativity-venue.md` — Venue-specific creative notes (what works well in this space, fixture strengths/limitations)
  - When building a show, ask which venue to use, then read that venue's `plot.md` for layout context. List `venue/` subdirectories to see all venues.
- **genres/** — EDM subgenre lighting definitions (one .md per genre). Each file defines color palettes, timing presets, movement conventions, strobe/laser/gobo rules, and par behavior for a specific genre. Read by the **busking** skill when generating workspaces. Created/edited by the **genres** skill. See `genres/README.md` for format. Available: drum-and-bass, dubstep, house, techno, trance.
- **moods/** — Lighting mood definitions (one .md per mood). Each file defines abstract modifiers that shape how a genre's values get applied — color filtering, intensity scaling, movement speed, effect density, timing adjustments. Read by the **busking** skill in combination with a genre file. Created/edited by the **moods** skill. See `moods/README.md` for format. Available: dark, ethereal, aggressive, hypnotic, euphoric, melancholic, chaotic, intimate (emotional states); chill, building, peak, comedown (energy levels).
- **fixtures/** — All .qxf fixture definitions live here. Check this directory first before creating a new fixture — it may already exist.
- **showlib.py** — Python show generator library. **Always use this for new shows.** See capabilities below.
- **qlc_runtime/** — Python runtime modules for show execution and creative planning:
  - `model.py`, `parser.py`, `engine.py` — Core: parse .qxw files and execute scenes/chasers with frame interpolation
  - `artnet.py`, `network.py` — DMX output via ArtNet UDP
  - `vlc_http.py`, `show_match.py`, `select.py` — VLC sync, show-to-media matching, function selection
  - `venue_profile.py` — Loads/validates venue creative profiles (`venue/<name>/references/creative-profile.json`). Maps fixtures to abstract roles (PAR_A, M1_BEAM, etc.) and zones.
  - `phrase_planner.py` — Phrase-aware technique planning. Classifies bars into phrase buckets, selects scored coordination techniques (INT-001..INT-090), enforces contrast on phrase changes, integrates designer packs.
  - `research_gate.py` — Research brief validation. Requires approved briefs with artist branding, song motifs, thesis, and 5+ cited sources before generation can proceed.
  - `focus_positions.py` — Parses venue focus-positions.md into canonical mover position tuples (7-tuple: sharpy_pan/tilt, bsw_pan/tilt, profile_pan/tilt, ni3k_pan).
- **scripts/show_workflow.py** — CLI orchestrator for song-synced shows. Commands: `scaffold` (create brief stubs + generator skeleton), `next` (list unbuilt songs), `status` (show completion dashboard).
- **AGENTS.md** — Skill registry. Lists the `qlc-show-workflow` skill with trigger rules and path.
- **references/** — QLC+ format documentation and creative playbook:
  - `qxf-format.md` — Fixture definition XML structure, presets, heads, physical properties
  - `qxw-format.md` — Workspace XML structure (scenes, chasers, EFX, collections, VC widgets, ARGB color format)
  - `bpm-timing.md` — BPM timing tables, genre-specific chaser patterns, chaser design templates
  - `channel-presets.md` — QLC+ channel preset names for .qxf files (IntensityRed, PositionPan, GoboWheelCoarse, etc.)
  - `creativity.md` — Central creative playbook (2600+ lines). Contains 60 look recipes (CR-*), 60+ coordination techniques (INT-*), 48 color palettes (P-*), 120 mover patterns (MP-*), 96 PAR patterns (PP-*), 30 designer profiles (LD-*), genre starting packs, anti-patterns, and AI prompt templates. **Human-readable source of truth** — edit here, then sync to JSON via `references/data/sync_from_creativity.py`.
- **references/data/** — Machine-readable catalogs synced from `creativity.md`. **Read these first** when building shows programmatically:
  - `coordination-techniques.json` — 90 whole-rig coordination techniques (INT-001..INT-090) with timing recipes, relationships (unison/counterpoint/inclusion), and starter combos
  - `palettes.json` — 48 named color palettes (P-001..P-048) with hex, base/accent/hit colors, and usage rules
  - `designers.json` — 30 lighting designer profiles (LD-001..LD-030) with study focus and transfer rules
  - `designer-techniques.json` — 30 designer technique packs (DTP-001..DTP-030) with mover/par ideas, preferred transforms, and anti-rules
  - `phrase-rules.json` — Phrase classification rules, coordination pools per phrase bucket, contrast enforcement, mover pattern grammar
  - `manifest.json` — Registry of all catalogs with counts
  - `designer-pack-memory.json` — Runtime cooldown tracking for DTP usage across shows
  - `sync_from_creativity.py` — Parses creativity.md and regenerates all JSON catalogs
  - `validate_data.py` — Schema and cross-reference validation for all catalogs
  - `validate_venue_profiles.py` — Validates venue creative profiles against catalog data
  - `validate_generator_portability.py` — Ensures generators don't hardcode venue-specific values
- **songs/** — Audio files for analysis. Drop tracks here before running the analysis pipeline.
- **songs-data/** — Analysis pipeline output (JSON files with BPM, beats, downbeats, segments, per-stem energy envelopes, onset timestamps, frequency band energy, spectral dynamics). Generated by `analyze.sh`.
- **extract_features.py** — Audio feature extraction script. Runs on demucs-separated stems to extract energy envelopes and onset timestamps per stem, plus frequency band energy and spectral dynamics from the full mix. Tuned for electronic music (house, DnB, dubstep).
- **pipeline.py** — Docker entrypoint script. Orchestrates allin1 (structure + beats + demucs separation) then extract_features.py (energy + onsets) in a single pipeline. Demucs runs once via allin1's `keep_byproducts=True`.
- **dockerfile.md** — Build documentation for the analysis pipeline Docker image (dependency pinning, ARM/x86 notes, pitfalls, onset detection tuning).
- **Dockerfile** — Builds the analysis pipeline Docker image (CPU-only, PyTorch 2.2.0 + NATTEN 0.15.1 + librosa 0.10.2). Native ARM64 on Apple Silicon.
- **analyze.sh** — Runs the full analysis pipeline on all files in `songs/`, outputs to `songs-data/`. Usage: `./analyze.sh` or `./analyze.sh "filename.flac"` or `./analyze.sh --keep-stems "filename.flac"`.
- **PHYSICAL-TESTS-NEEDED.md** — Checklist of fixture values that need hardware verification. Check before assuming any ⚠️ UNVERIFIED values are correct.

### Existing Workspace Files (venue/home-studio/shows/)

| File | Purpose |
|------|---------|
| Template-Base.qxw | Blank starting point — all venue fixtures, ArtNet, blackout only. Generated by `generate_venue_template()`. |
| Center-Reference.qxw | Movers aimed at floor center — use as movement baseline |
| Demo-Show.qxw | 16-bar demo at 128 BPM — example of showlib.py output |
| Fixture-Test.qxw | Basic per-fixture test scenes |
| Fixture-Test-Thorough.qxw | Comprehensive per-channel feature tests |
| Deep-Currents.qxw | 2-min looping show at 128 BPM — cool/deep palette, leader/follower movers, NI3K reveals |
| Lorn - Acid Rain (Skeler Remix).qxw | Song-synced show at 115 BPM — false calm→corruption→predatory hunting→isolation→assault→echo |
| PhatAdam - Never Cared Enough.qxw | Song-synced show at 133 BPM — neon pop palette, building choruses, strobe buildup, climax with lasers |
| 4BAR-Chasers.qxw | 4BAR color chase patterns |

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
- **Scene/Chaser builders**: `scene()`, `make_chaser()`, `write_workspace()`
- **Genre templates**: `structure_dnb()`, `structure_melodic_house()`, `structure_dubstep()`, `structure_party()` — return section dicts with name, bars, energy, movement, timing_style
- **Blackout helpers**: `blackout(fixture_id, num_channels)`, `blackout_all()`
- **Venue template**: `generate_venue_template(venue_dir, bpm)` — reads `plot.md`, generates `Template-Base.qxw` with only the fixtures placed in that venue
- **Research brief**: `require_research_brief(song_stem, project_root, venue_dir)` — loads/validates brief; creates stub if missing; raises if not approved. `build_creative_context(brief, song_stem)` — extracts `brand_tokens` + `creative_directives` from approved brief
- **Phrase-aware planning**: `classify_phrase(segment_label, rms, sub, high, progress)` — maps segment + energy to phrase class (intro/verse_groove/build/drop/breakdown/outro). `pick_phrase_technique(phrase, segment_index, global_bar, brand_tokens, creative_directives, ...)` — scores 3+ candidate coordination techniques, returns top-ranked with timing, mover pattern, dimensions, and designer pack metadata. `pick_phrase_technique_candidates(...)` — returns all scored candidates (not just top 1)
- **Designer packs**: `pick_show_designer_packs(show_key, brand_tokens, creative_directives, ...)` — selects dominant + contrast designer technique packs (DTP-001..DTP-030) for a show
- **Technique helpers**: `mover_family_from_phrase(phrase, relationship, rms, sub)` — maps technique to mover family bucket. `par_mode_from_phrase_timing(par_beats, par_style, phrase, seg_bar_idx)` — maps technique timing to PAR mode key
- **Venue context**: `load_venue_profile(project_root, venue_dir)` — loads/validates venue creative profile. `load_focus_position_tuples(project_root, venue_dir)` — loads named mover positions as 7-tuples from focus-positions.md
- **Transition helpers**: `plan_segment_transition(prev_phrase, next_phrase, prev_energy, next_energy, segment_index, total_segments, ...)` — plans a 1-4 beat bridge moment at a segment boundary using phrase-rules.json pools/cooldown/escalation. Returns dict with `type`, `duration_beats`, `fixtures`, `exit_style`, or None. `build_transition_scenes(transition, bpm, pos_tuples, palette, last_scene)` — dispatches to one of 21 transition scene factories, returns `(scenes, timing)` lists matching `make_chaser()` contract. Supported types: blackout_slingshot, dead_air, white_flash, strobe_burst, freeze_decay, color_swap, color_inversion, position_snap, slow_dissolve, par_ladder, stutter_gate, pulse_to_glow, compression_snap, ladder_build, par_convergence, dim_dissolve, freeze_burst, stutter_resolve, chase_cancel, fade_to_black, freeze_hold
- **Beat reactivity**: `pick_phrase_technique()` now attaches `beat_reactivity` to the returned `PlannedTechnique` — contains `par_min`, `mover_min`, `accent_layer`, `accent_type` from phrase-rules.json. Serialized by `_serialize_planned_phrase_technique()` into the technique dict

## What You Do

- Create .qxf fixture definitions from manufacturer specs and save them to `fixtures/`
- Build .qxw workspace files using `showlib.py` for programmatic generation
- Calculate BPM-synced timing for musically-aware chaser programming
- Design Virtual Console layouts with color-coded, category-organized buttons
- Validate all XML with xmllint before delivering

## Skills & Workflow

Skills are specialized instructions that guide specific tasks. Most live in `.claude/skills/`; the `qlc-show-workflow` skill lives in `skills/` (see `AGENTS.md` for its path). They chain together in a dependency order:

### Venue Setup (run once per venue)
1. **plot** — Creates `venue/<name>/plot.md` with fixture positions in 3D space. Handles venue creation (room dimensions, directory structure), adding/removing/moving fixtures, and coordinate conversion from spatial descriptions. This is the starting point — everything else depends on plot.md existing.
2. **patch** — Creates `venue/<name>/patch.md` from the venue's `plot.md`. Assigns DMX addresses, fixture IDs, and channel modes. Depends on `plot.md` existing.
3. **focus-positions** — Creates `venue/<name>/focus-positions.md` with named pan/tilt targets for every mover. Depends on `patch.md` existing. Must exist before building shows or busking workspaces.

### Content Definition (run as needed)
4. **genres** — Creates/edits `genres/<genre>.md` files. Each genre defines concrete lighting values: specific colors (with RGB + fixture wheel mappings), BPM-calibrated timing presets, per-section energy profiles, movement/strobe/laser/gobo/par conventions. These are the raw material that shows and busking workspaces consume.
5. **moods** — Creates/edits `moods/<mood>.md` files. Each mood defines abstract modifiers (color filtering, intensity scaling, movement speed, effect density, timing adjustments) that shape how a genre's values get applied. Moods never define DMX values directly — they modify what the genre provides.

### Generation
6. **busking** — Generates a complete QLC+ busking workspace (`.qxw`) for live, improvised lighting. Reads venue files (patch + focus-positions) + a genre + an optional mood, then produces a Virtual Console layout with color buttons, position presets, movement chasers, strobes, and specials. This is the primary consumer of genre and mood files.

### How Genre + Mood Combine
Genre provides concrete values (specific colors, ms timing, DMX channel values). Mood applies abstract modifiers (prefer cool colors, dim to 60%, slow movement 0.5x, no strobe). The busking skill reads both files and applies the mood's modifiers to the genre's values. The same mood applied to different genres produces different concrete results but the same emotional character.

### Song-Synced Shows (Research-Gated Pipeline)
7. **song-analysis** — Finds a song in `songs/` (or picks an unanalyzed one), runs `./analyze.sh` to extract BPM/beats/structure/energy/onsets, presents a human-readable summary of the analysis data. This is the entry point for all song-synced shows.
8. **qlc-show-workflow** — Full pipeline orchestrator for song-synced shows. Scaffold (brief stubs + generator skeleton) → research brief (artist branding, song motifs, thesis, sources) → validate → phrase-aware generator → .qxw output → validate invariants. See `AGENTS.md` for trigger rules and `skills/qlc-show-workflow/SKILL.md` for full instructions.

The full song-synced pipeline:

1. **song-analysis** — find + analyze + present summary
2. **Scaffold** — `python3 scripts/show_workflow.py scaffold --song "Artist - Song" --venue <dir>`. Creates: brief stubs (JSON + MD) in `venue/<name>/shows/notes/`, generator skeleton in `venue/<name>/generators/`.
3. **Research brief** — Fill the JSON brief at `venue/<name>/shows/notes/<slug>.json` with:
   - Artist branding (summary, visual_cues [3+], do_not_copy [1+])
   - Song-title inspiration (keywords [2+], motifs [3+])
   - Visual direction (color_story, motion_story, staging_story)
   - Style constraints (must_include [1+], avoid [1+])
   - Creative thesis (1 sentence, 24+ chars)
   - 5+ sources covering 3 required categories (artist_branding, song_specific, visual_reference), 2+ from last 3 years
   - Set `status: "approved"` and `brand_alignment_score >= 3`
4. **Validate brief** — `python3 venue/<name>/shows/notes/validate_briefs.py --song "..." --venue <dir>`
5. **Build generator** in `venue/<name>/generators/` using phrase-aware API:
   - `BRIEF = require_research_brief(...)` — enforces approved brief
   - `CREATIVE = build_creative_context(BRIEF, song_stem=...)` — extracts brand_tokens + creative_directives
   - `POS = load_focus_position_tuples(...)` — named positions, not raw pan/tilt
   - Per-bar loop: `classify_phrase()` → `pick_phrase_technique()` → `mover_family_from_phrase()` → `par_mode_from_phrase_timing()` → build scene. `pick_phrase_technique()` returns `beat_reactivity` (par_min/mover_min/accent_layer/accent_type) on each technique.
   - At segment boundaries: `plan_segment_transition(prev_phrase, next_phrase, ...)` → `build_transition_scenes(transition, bpm, ...)` → extend chaser with transition scenes/timing
6. **Generate show** — `python3 "venue/<name>/generators/<Song>.py"`
7. **Validate invariants** — Run all three validators:
   - `python3 references/data/validate_data.py`
   - `python3 references/data/validate_venue_profiles.py`
   - `python3 references/data/validate_generator_portability.py`
8. **Write show notes** to `venue/<name>/shows/notes/`

Creative direction now comes from research briefs + the phrase planner + designer packs, not from genre/mood .md files. Genre and mood files are still used by the **busking** skill for live improvised lighting.

### Data Maintenance (when editing creativity.md)
1. Edit creative content in `references/creativity.md`
2. Sync: `python3 references/data/sync_from_creativity.py`
3. Validate catalogs: `python3 references/data/validate_data.py`
4. Validate venue profiles: `python3 references/data/validate_venue_profiles.py`
5. Validate generators: `python3 references/data/validate_generator_portability.py`

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

## Key Principles

- Channel order must match the actual fixture DMX protocol exactly — always verify
- Every scene sets ALL channels, not just the ones that change
- Design chasers around the music: energy level, song structure, genre conventions
- Use descriptive naming for scenes and chasers
- Organize functions into folders by category
- Always include a BLACKOUT button in the Virtual Console
- **Use `showlib.py`** for generating workspace files — it handles fixture channel maps, XML formatting, and VC layout automatically
- **Write show notes** in `shows/notes/` for every show — capture creative brief, palette, fixture roles, positions, section breakdown, and techniques. Read existing notes before modifying a show.

## Show Generator Lessons Learned

### Timing Calculations
- When mixing `beat_step()` (FadeIn=0, Hold=ms) and `smooth_step()` (FadeIn=ms, Hold=0), total duration must sum `FadeIn + Hold` for each step, not just Hold. The PhatAdam generator only summed Hold because all steps were snaps — that formula breaks for smooth crossfade steps.
- `smooth(bpm, bars)` returns `(FadeIn=full_duration, Hold=0)` — the entire step is crossfade time. This creates flowing mover sweeps where the motion IS the crossfade between positions.

### Half-Time BPM Detection
- The analysis pipeline often detects BPM at half-time (e.g., 87 instead of 174 for DnB). Always confirm BPM with the user before building a generator.
- Beat tracker timestamps can be unreliable for half-time tracks. Use `bpm_to_ms()` math for timing calculations and segment timestamps from the analysis JSON for section boundaries — don't rely solely on the beat array spacing.

### Pre-Beat Silence
- Analysis data segments may start at 0.0s, but the first beat often doesn't land until several seconds in (e.g., 11s for Guardian Angel). Account for this by splitting the first segment into an "ambient intro" section (pre-beat bars) and the actual verse. The DJ starts the chaser at song start, so those pre-beat bars need to be programmed as atmosphere/dark.

### NI3K Lasers-Only Mode
- To use NI3K as a laser-only fixture: `dim=0` (kills RGBW LEDs), `halo=H_OFF`, `r=0, g=0, b=0, w=0`. Only set `rl`, `gl`, `bl` for laser control.
- NI3K tilt channels (ch1-3): values 0-127 = position, 128-191 = forward rotation, 192-255 = reverse rotation. "High movement values" means using the rotation range (160-250) for dramatic continuous motion.

### Forward-Facing Mover Positions
- Read safe pan/tilt ranges from the venue's `focus-positions.md` — they're listed in the movers table per fixture.
- When user says "never point behind," define all positions within those bounds and verify each one.

### Special Positions Are Required
- Every show generator must use **special positions** from the venue's focus-positions.md — not just the 9 grid positions (C/SL/SR/DSC/DSL/DSR/USL/USR/USC).
- Read the venue's `special_zones` keys from `creative-profile.json` (e.g. `DJ`, `DANCE`, `DISCO_BALL`, `CEIL`) and the Specials/Effects sections of `focus-positions.md`.
- Use at least 1–2 special positions in any show with high-energy sections. Placement guide:
  - `DJ` — mid-drop focus back to performer; build peaks; "look at me" moments
  - `DANCE` — audience/dance-floor shots at drops and energy-out moments
  - `DISCO_BALL` — catharsis/reveal moments (beams scatter off the ball into the room)
  - `CEIL` — dramatic overhead shafts at sustained peaks or tension builds
- Special positions are loaded automatically by `load_focus_position_tuples()` — just use the key string in your position list.

### Scene Dedup Behavior
- Beat-level shows (1 scene per beat) with varied NI3K tilt modulation typically produce 0 dedup hits because the tilt math (`beat % N * offset`) creates unique values per beat. Dedup is more effective when sections reuse identical looks (e.g., repeated bar patterns, common blackout scenes).

### Par Cohesion Patterns
- `par_wash()` (all 6 pars same color) = maximum visual unity. Best for ethereal/unified aesthetics.
- `par_chase()` (one par cycling) = energetic but fragmented. Best for party/neon shows.
- `par_pairs()` (P1+P3 vs P2+P4 + missyees split) = balanced texture. Good for verses/builds.
- `par_gradient()` (4BAR gradient + missyees split) = subtle depth. Good for building sections.
- When user asks for "cohesive and uniform" pars, default to `par_wash()` for drops and `par_gradient()` for builds.

### Mover Reset Position
- Movers should always reset to **DSC** (Downstage Center) between sections. This is the default "home" position for section transitions — when a section ends and the next begins, movers snap or crossfade to DSC before moving to their first position in the new section. This creates a consistent visual anchor and prevents jarring mid-air movements between sections.

### Mover Blackout: dark_*() Not blackout()
- **Never use `blackout(FX_*, CH_*)` on movers** (Sharpy, BSW, Profile, NI3K). `blackout()` sets ALL channels to 0, including pan/tilt, which sends the physical head spinning to its home position (pan=0) even though the beam is off. This creates ugly visible pan spins.
- **Use `dark_sharpy()`, `dark_bsw()`, `dark_profile()`, `dark_ni3k()`** instead. These zero the output (dimmer=0, shutter=closed) but keep pan/tilt parked at DSC by default, or at a specified position.
- **Position tracking**: When one mover is active and others are dark, park the dark movers at the **same position** as the active one. This way, if they turn on later, they're already aimed correctly. Example: `solo_sharpy()` should use `dark_bsw(pan=bp, tilt=bt)` where bp/bt match the Sharpy's target position.
- **`blackout_all()`** is safe — it already uses `dark_*()` for movers internally.
- **`blackout()` is fine for pars/missyees** — they have no pan/tilt.

### Transition Scene Contract
- `build_transition_scenes()` must return `(scenes, timing)` where `len(scenes) == len(timing)`. This is enforced by `make_chaser()` which asserts matching counts.
- Every transition factory must produce at least 1 scene + 1 timing entry — even "hold" or "freeze" transitions need a concrete scene (e.g., a dim midpoint or fade-to-black) rather than returning 0 scenes with only timing.
- Transition pools in phrase-rules.json are keyed by phrase-pair (e.g., `build_to_drop`), energy-pair (e.g., `high_to_high`), or fallback (`same_to_same`). Pool selection priority: phrase-pair → energy-pair → fallback.

### Research Brief Workflow
- Every song-synced show requires an approved research brief at `venue/<name>/shows/notes/<slug>.json`. The brief gates generation — `require_research_brief()` will create a stub and raise if `status != "approved"`.
- Brief must have 5+ sources covering 3 categories (artist_branding, song_specific, visual_reference), with 2+ from the last 3 years. This prevents hallucinated creative direction.
- `build_creative_context(brief, song_stem)` extracts `brand_tokens` (unique creative keywords) and `creative_directives` (must_include, avoid, do_not_copy, direction_notes) from the approved brief.

### Phrase-Aware Technique Selection
- Generators use `classify_phrase()` to bucket each bar into one of 6 phrase classes (intro, verse_groove, build, drop, breakdown, outro), then `pick_phrase_technique()` to select a scored coordination technique (INT-001..INT-090) from that phrase's pool.
- Technique selection evaluates 3 candidates across 5 scoring dimensions: novelty, coherence, brand_fit, creative_fit, phrase_fit. Top-ranked wins.
- On phrase change, contrast enforcement requires at least 2 visual dimensions to differ (position, rhythm, color, intensity, effect_density). The planner auto-adds transforms if contrast isn't met.

### Designer Pack Integration
- Shows select 1-2 dominant + 1 contrast designer technique packs (DTP-001..DTP-030) based on brand tokens and creative directives.
- Packs influence technique selection: preferred transforms, par modes, relationships, and anti-rules (forbidden techniques).
- Pack usage is tracked in `references/data/designer-pack-memory.json` with a 3-show cooldown to prevent repetition across shows.

### Venue Creative Profiles
- `venue/<name>/references/creative-profile.json` maps physical fixtures to abstract roles (PAR_A, M1_BEAM, etc.) and zones (C, SL, DJ_BOOTH, etc.).
- Generators should reference roles and zones, not fixture names, for portability across venues.
- Use `load_venue_profile()` to load the profile; use `load_focus_position_tuples()` for named pan/tilt positions instead of hardcoding values.
