# Workflow Checklist

Use these commands from project root.

## 1) Pick Song

```bash
python3 scripts/show_workflow.py next --venue venue/home-studio
```

Or target one song directly:

```bash
python3 scripts/show_workflow.py scaffold --song "Artist - Song" --venue venue/home-studio
```

## 2) Complete Research Brief

Brief files:
- `venue/<name>/shows/notes/<song-slug>.json`
- `venue/<name>/shows/notes/<song-slug>.md`

Required focus:
- artist branding and visual language
- song-title-driven motifs
- citations and recency
- final creative thesis

Validate:

```bash
python3 venue/home-studio/shows/notes/validate_briefs.py --song "Artist - Song" --venue venue/home-studio
```

## 3) Build Generator

Generator path:
- `venue/<name>/generators/<Artist - Song>.py`

Keep these calls:
- `require_research_brief(..., venue_dir=VENUE_DIR)`
- `load_focus_position_tuples(...)`
- phrase planning APIs from `showlib.py`
- `build_creative_context(...)` with planner calls receiving both `brand_tokens` and `creative_directives`

## 4) Render Show

```bash
python3 "venue/home-studio/generators/Artist - Song.py"
```

Expected output:
- `venue/home-studio/shows/Artist - Song.qxw`

## 5) Validate Portability

```bash
python3 references/data/validate_data.py
python3 references/data/validate_venue_profiles.py
python3 references/data/validate_generator_portability.py
```

## Definition Of Done

- Brief exists and validates as approved.
- Generator exists and uses venue-portable mapping.
- `.qxw` is generated in target venue.
- Validation scripts pass.
