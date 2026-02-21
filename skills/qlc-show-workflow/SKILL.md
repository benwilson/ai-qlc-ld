---
name: qlc-show-workflow
description: Build and update venue-aware, song-synced QLC+ shows from songs-data with phrase-aware planning and research-gated creative direction. Use when asked to create a new show, refresh an existing generator, pick an unbuilt song, or run the full workflow (research brief, generator, .qxw output, validation) for electronic/EDM tracks.
---

# QLC Show Workflow

Use this workflow to produce repeatable, high-quality song shows with venue portability.

## Run Workflow

1. Resolve target venue and song.
2. Run scaffold:
   `python3 scripts/show_workflow.py scaffold --song "<Artist - Song>" --venue <venue-dir>`
3. If the brief is draft/missing:
   - Create/update `venue/<name>/shows/notes/<Song Name>.json` and `.md`.
   - Include artist branding, song-title motifs, creative thesis, and sources.
   - Set `status` to `approved`.
4. Validate briefs:
   `python3 venue/<name>/shows/notes/validate_briefs.py --song "<Artist - Song>" --venue <venue-dir>`
5. Build or update generator in `venue/<name>/generators/<Artist - Song>.py`:
   - Keep `require_research_brief(..., venue_dir=VENUE_DIR)`.
   - Keep venue mapping via `load_focus_position_tuples(...)` only.
   - Use phrase-aware selection (`classify_phrase`, `pick_phrase_technique`).
   - Build `CREATIVE = build_creative_context(BRIEF, song_stem=SONG_STEM)` and pass both:
     - `brand_tokens=CREATIVE["brand_tokens"]`
     - `creative_directives=CREATIVE["creative_directives"]`
   - Make PAR and mover behavior coordinated (together or call-and-response).
6. Generate show:
   `python3 "venue/<name>/generators/<Artist - Song>.py"`
7. Validate project invariants after creative data or generator edits:
   - `python3 references/data/validate_data.py`
   - `python3 references/data/validate_venue_profiles.py`
   - `python3 references/data/validate_generator_portability.py`

## Constraints

- Keep `references/creativity.md` venue-agnostic.
- Keep venue specifics in `venue/<name>/references/`.
- Do not hardcode `venue/home-studio` inside reusable runtime code.
- Do not use static mover `POS` maps in research-gated generators.

## Selection Helpers

- To pick next unbuilt songs:
  `python3 scripts/show_workflow.py next --venue <venue-dir>`
- To inspect progress:
  `python3 scripts/show_workflow.py status --venue <venue-dir>`

Read `skills/qlc-show-workflow/references/workflow-checklist.md` for command details and done criteria.
