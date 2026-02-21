---
title: Integrate Creative Layer Into Workflows
type: feat
date: 2026-02-20
---

# Integrate Creative Layer Into Workflows

## Overview

The codebase has gained four major new subsystems that aren't yet reflected in the workflow documentation (CLAUDE.md, skills, memory):

1. **Research Gate** (`qlc_runtime/research_gate.py`) — Enforces approved research briefs before show generation
2. **Phrase-Aware Planner** (`qlc_runtime/phrase_planner.py`) — Maps song segments to scored coordination techniques with contrast enforcement
3. **Venue Creative Profiles** (`qlc_runtime/venue_profile.py`) — Abstract fixture role mapping (PAR_A, M1_BEAM, etc.) + zone aliases
4. **Creative Data Layer** (`references/data/*.json`) — 7 machine-readable catalogs synced from `references/creativity.md`

Plus: `references/creativity.md` (2600+ line creative playbook), `scripts/show_workflow.py` (CLI orchestrator), the `qlc-show-workflow` skill, and 10+ new showlib.py wrapper functions.

**None of this is documented in CLAUDE.md or connected to the existing skill chain.** The old "Song-Synced Shows" workflow in CLAUDE.md still describes the manual genre/mood/direction gathering flow.

## Problem Statement

A new user (or AI agent) reading CLAUDE.md today would:
- Not know research briefs exist or are required
- Not know about phrase-aware planning or coordination techniques
- Not know about venue creative profiles or the data layer
- Follow the old manual workflow instead of using the scaffold/brief/validate pipeline
- Miss the new showlib.py API functions entirely
- Not know about the creativity.md playbook or the sync/validate scripts

## Proposed Solution

Update CLAUDE.md, song-analysis skill, and MEMORY.md to fully document the new architecture. No code changes — documentation and workflow integration only.

## Acceptance Criteria

- [ ] CLAUDE.md "Project Structure" section documents all new files/directories
- [ ] CLAUDE.md "showlib.py Capabilities" section lists all new API functions
- [ ] CLAUDE.md "Song-Synced Shows" pipeline reflects research-gated, phrase-aware workflow
- [ ] CLAUDE.md "Skills & Workflow" section includes qlc-show-workflow skill
- [ ] CLAUDE.md documents the data maintenance workflow (creativity.md -> sync -> validate)
- [ ] CLAUDE.md "Show Generator Lessons Learned" covers new patterns (research briefs, phrase planning, designer packs, contrast enforcement)
- [ ] Song-analysis skill hands off to qlc-show-workflow for generation
- [ ] MEMORY.md updated with new architecture knowledge
- [ ] No stale/contradictory information left in any documentation

---

## MVP

### 1. CLAUDE.md — Project Structure Updates

Add these entries to the existing "Project Structure" section:

**New top-level entries:**
- `AGENTS.md` — Skill registry. Lists the `qlc-show-workflow` skill with trigger rules.
- `scripts/show_workflow.py` — CLI orchestrator for song-synced shows. Commands: `scaffold` (create brief stubs + generator skeleton), `next` (list unbuilt songs), `status` (show completion dashboard).
- `references/creativity.md` — Central creative playbook (2600+ lines). Contains 60 look recipes (CR-*), 60 coordination techniques (INT-*), 48 color palettes (P-*), 120 mover patterns (MP-*), 96 PAR patterns (PP-*), 30 designer profiles (LD-*), genre starting packs, anti-patterns, and AI prompt templates. **Human-readable source of truth** — edit here, then sync to JSON.

**New `references/data/` section:**
- `references/data/` — Machine-readable catalogs synced from `creativity.md`:
  - `coordination-techniques.json` — 90 whole-rig coordination techniques (INT-001..INT-090) with timing recipes and starter combos
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

**Updated venue directory entry:**
Add to the existing venue bullet:
- `references/creative-profile.json` — Venue-specific fixture-to-role mapping (PAR_A, M1_BEAM, etc.), zone aliases, special zones, par groups. Consumed by phrase planner and focus position loader.
- `references/creativity-venue.md` — Venue-specific creative notes (what works well in this space, limitations)
- `references/validate_profile.py` — Profile validation script for this venue

### 2. CLAUDE.md — showlib.py Capabilities Updates

Add a new subsection after the existing capabilities list:

**Phrase-Aware Planning:**
- `classify_phrase(segment_label, rms, sub, high, progress)` — Maps segment + energy to one of 6 phrase classes: intro, verse_groove, build, drop, breakdown, outro
- `pick_phrase_technique(phrase, segment_index, global_bar, brand_tokens, creative_directives, ...)` — Scores 3+ candidate coordination techniques, returns top-ranked with timing, mover pattern, dimensions, and designer pack metadata
- `pick_phrase_technique_candidates(...)` — Returns all scored candidates (not just top 1)
- `pick_show_designer_packs(show_key, brand_tokens, creative_directives, ...)` — Selects dominant + contrast designer packs for a show
- `mover_family_from_phrase(phrase, relationship, rms, sub)` — Maps technique to mover family bucket (geometric/snap/atmospheric)
- `par_mode_from_phrase_timing(par_beats, par_style, phrase, seg_bar_idx)` — Maps technique timing to PAR mode key

**Creative Context:**
- `require_research_brief(song_stem, project_root, venue_dir)` — Loads and validates research brief; creates stub if missing; raises if not approved
- `build_creative_context(brief, song_stem)` — Extracts brand_tokens + creative_directives from approved brief
- `load_venue_profile(project_root, venue_dir)` — Loads and validates venue creative profile
- `load_focus_position_tuples(project_root, venue_dir)` — Loads named mover positions as 7-tuples from focus-positions.md

### 3. CLAUDE.md — Song-Synced Shows Pipeline Rewrite

Replace the current "Song-Synced Shows" section (steps 1-6) with the new research-gated, phrase-aware pipeline:

```
### Song-Synced Shows (Research-Gated Pipeline)

The full song-synced pipeline:

1. **song-analysis** skill — Find + analyze + present summary (unchanged)
2. **Scaffold** — Run `python3 scripts/show_workflow.py scaffold --song "..." --venue <dir>`
   Creates: brief stubs (JSON + MD) in `venue/<name>/shows/notes/`, generator skeleton in `venue/<name>/generators/`
3. **Research brief** — Fill the JSON brief with:
   - Artist branding (summary, visual_cues, do_not_copy)
   - Song-title inspiration (keywords, motifs)
   - Visual direction (color_story, motion_story, staging_story)
   - Style constraints (must_include, avoid)
   - 5+ sources (2+ recent, covering artist_branding + song_specific + visual_reference categories)
   - Set `status: "approved"` and `brand_alignment_score >= 3`
4. **Validate brief** — `python3 venue/<name>/shows/notes/validate_briefs.py --song "..." --venue <dir>`
5. **Build generator** in `venue/<name>/generators/` using phrase-aware API:
   - `BRIEF = require_research_brief(...)` — enforces approved brief
   - `CREATIVE = build_creative_context(BRIEF, song_stem=...)` — extracts brand_tokens + creative_directives
   - `POS = load_focus_position_tuples(...)` — named positions, not raw pan/tilt
   - Per-bar loop: `classify_phrase()` → `pick_phrase_technique()` → `mover_family_from_phrase()` → `par_mode_from_phrase_timing()` → build scene
6. **Generate show** — `python3 "venue/<name>/generators/<Song>.py"`
7. **Validate** — Run all three validators:
   - `python3 references/data/validate_data.py`
   - `python3 references/data/validate_venue_profiles.py`
   - `python3 references/data/validate_generator_portability.py`
8. **Write show notes** to `venue/<name>/shows/notes/`
```

### 4. CLAUDE.md — Skills & Workflow Section Updates

Add qlc-show-workflow to the "Generation" subsection:

```
7. **qlc-show-workflow** — Full pipeline orchestrator for song-synced shows.
   Scaffold (brief stubs + generator skeleton) → research brief (artist branding,
   song motifs, thesis, sources) → validate → phrase-aware generator (classify_phrase,
   pick_phrase_technique) → .qxw output → validate invariants. See `AGENTS.md` for
   trigger rules. This skill supersedes the manual genre/mood gathering in the old
   song-analysis handoff — creative direction now comes from research briefs + phrase
   planner + designer packs, not from genre/mood .md files.
```

Add a new subsection for data maintenance:

```
### Data Maintenance (when editing creativity.md)
1. Edit creative content in `references/creativity.md`
2. Sync: `python3 references/data/sync_from_creativity.py`
3. Validate catalogs: `python3 references/data/validate_data.py`
4. Validate venue profiles: `python3 references/data/validate_venue_profiles.py`
5. Validate generators: `python3 references/data/validate_generator_portability.py`
```

### 5. CLAUDE.md — Show Generator Lessons Learned Additions

Add these new lessons:

**Research Brief Workflow:**
- Every song-synced show requires an approved research brief at `venue/<name>/shows/notes/<slug>.json`. The brief gates generation — `require_research_brief()` will create a stub and raise if status != "approved".
- Brief must have 5+ sources covering 3 categories (artist_branding, song_specific, visual_reference), with 2+ from the last 3 years. This prevents hallucinated creative direction.

**Phrase-Aware Technique Selection:**
- Generators use `classify_phrase()` to bucket each bar, then `pick_phrase_technique()` to select a scored coordination technique (INT-001..INT-090) from the phrase's pool.
- Technique selection evaluates 3 candidates across 5 scoring dimensions: novelty, coherence, brand_fit, creative_fit, phrase_fit. Top-ranked wins.
- On phrase change, contrast enforcement requires at least 2 visual dimensions to differ (position, rhythm, color, intensity, effect_density). The planner auto-adds transforms if contrast isn't met.

**Designer Pack Integration:**
- Shows select 1-2 dominant + 1 contrast designer technique packs (DTP-001..DTP-030) based on brand tokens and creative directives.
- Packs influence technique selection: preferred transforms, par modes, relationships, and anti-rules (forbidden techniques).
- Pack usage is tracked in `references/data/designer-pack-memory.json` with a 3-show cooldown to prevent repetition.

**Venue Creative Profiles:**
- `venue/<name>/references/creative-profile.json` maps physical fixtures to abstract roles (PAR_A, M1_BEAM, etc.) and zones (C, SL, DJ_BOOTH, etc.).
- Generators should reference roles and zones, not fixture names, for portability across venues.

### 6. Song-Analysis Skill — Show Creation Handoff Update

Update `.claude/skills/song-analysis/SKILL.md` Step 5 to hand off to the new workflow instead of the old manual process:

Replace the current Step 5 content with a reference to qlc-show-workflow:

```
### Step 5: Transition to Show Creation

After presenting the analysis summary, transition to the **qlc-show-workflow** skill:

1. Ask which venue (list `venue/` subdirectories)
2. Run scaffold: `python3 scripts/show_workflow.py scaffold --song "<Song>" --venue <dir>`
3. Follow the qlc-show-workflow pipeline: brief → validate → generator → show → validate

The old manual genre/mood/direction gathering is replaced by:
- **Research brief** (artist branding, song motifs, thesis, sources)
- **Phrase-aware planner** (selects coordination techniques from references/data/ catalogs)
- **Designer packs** (curated lighting ideas influenced by brand tokens)

Genre and mood .md files are still used by the **busking** skill for live improvised lighting,
but song-synced shows now get their creative direction from research briefs + the phrase planner.
```

### 7. MEMORY.md Updates

Add to the existing MEMORY.md:

```
## New Architecture (2026-02-20)
- Show workflow is now research-gated: brief (JSON) must be "approved" before generator runs
- Phrase-aware planner selects coordination techniques (INT-001..INT-090) per bar
- 5 scoring dimensions: novelty, coherence, brand_fit, creative_fit, phrase_fit
- Contrast enforcement: 2+ visual dimensions must change on phrase boundaries
- Designer packs (DTP-001..DTP-030) influence technique selection with cooldown tracking
- Creative data lives in references/data/*.json, synced from references/creativity.md
- Venue creative profiles at venue/<name>/references/creative-profile.json map fixtures to abstract roles
- qlc-show-workflow skill (in skills/ not .claude/skills/) is the new show generation entry point
- song-analysis skill still handles analysis; hands off to qlc-show-workflow for generation
```

## References

### Internal References
- Current CLAUDE.md: `.claude/CLAUDE.md`
- New skill: `skills/qlc-show-workflow/SKILL.md`
- Old skill: `.claude/skills/song-analysis/SKILL.md`
- Agent registry: `AGENTS.md`
- Phrase planner: `qlc_runtime/phrase_planner.py` (1627 lines, core planning logic)
- Research gate: `qlc_runtime/research_gate.py` (397 lines, brief validation)
- Venue profile: `qlc_runtime/venue_profile.py` (181 lines, profile loading)
- Focus positions: `qlc_runtime/focus_positions.py` (176 lines, position parsing)
- Show workflow CLI: `scripts/show_workflow.py`
- Creative playbook: `references/creativity.md` (2600+ lines)
- Data catalogs: `references/data/*.json` (7 files)
- showlib.py: `showlib.py` (1473 lines, generation library)
- Venue profile example: `venue/home-studio/references/creative-profile.json`
