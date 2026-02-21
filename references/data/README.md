# Reference Data Layer

This directory is the canonical machine-readable layer for lighting generation.
It contains venue-agnostic catalogs only.

## Canonical Files

- `coordination-techniques.json`: `INT-001..INT-###` PAR/mover interaction techniques.
- `palettes.json`: `P-001..P-048` palette catalog and palette rules.
- `designers.json`: `LD-001..LD-###` designer study set + prompt template.
- `designer-techniques.json`: `DTP-001..` technical designer packs (mover/chase ideas + anti-rules).
- `phrase-rules.json`: phrase-aware mapping, fill handling, contrast rules, mover-pattern grammar, uniqueness constraints, builder template.
- `manifest.json`: catalog registry + counts.

Venue-specific machine data lives under:
- `venue/<name>/references/creative-profile.json`

Runtime memory (generated automatically when `show_key` is used):
- `references/data/designer-pack-memory.json` (cross-show pack cooldown state)

## Source of Truth

- Human creative source: `references/creativity.md`
- Machine source: files in this folder
- Venue machine source: `venue/<name>/references/creative-profile.json`

For automation, parse this folder first. Use `references/creativity.md` for extended rationale and examples.
Then apply the selected venue profile as a hard mapping layer.

## Sync + Validate

```bash
python3 references/data/sync_from_creativity.py
python3 references/data/validate_data.py
python3 references/data/validate_venue_profiles.py
python3 references/data/validate_generator_portability.py
```

## Expansion Rules

- Keep ID ranges sequential and unique by family (`INT`, `P`, `LD`).
- Add new entries in `references/creativity.md`, then regenerate JSON.
- Keep venue mappings out of `references/creativity.md`; store them in `venue/<name>/references/`.
- Never edit generated catalog JSON manually unless doing one-off emergency fixes.
- Run validation after every update before generating shows.
