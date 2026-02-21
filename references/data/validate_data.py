#!/usr/bin/env python3
"""Validate machine-readable lighting reference catalogs."""

from __future__ import annotations

import json
import re
from pathlib import Path

CREATIVITY_BANNED_PATTERNS = (
    r"venue\/home-studio\/",
    r"venue\/[a-zA-Z0-9_-]+\/(plot|patch|focus-positions)\.md",
    r"borrow_for_this_rig",
    r"Project Rig Abstraction \(Home Studio\)",
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def assert_condition(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def assert_sequential(prefix: str, ids: list[str], start: int, end: int) -> None:
    expected = [f"{prefix}-{i:03d}" for i in range(start, end + 1)]
    assert_condition(ids == expected, f"{prefix} ID range mismatch: expected {expected[0]}..{expected[-1]}")


def validate_coordination(data: dict) -> set[str]:
    techniques = data["techniques"]
    ids = [row["id"] for row in techniques]
    assert_condition(len(ids) == len(set(ids)), "Duplicate technique IDs found")
    assert_condition(len(ids) >= 60, "Technique catalog unexpectedly small; expected at least INT-001..INT-060")
    assert_sequential("INT", ids, 1, len(ids))

    allowed_relationships = {"unison", "counterpoint", "inclusion"}
    allowed_groups = {"unison_cohesion", "counterpoint", "inclusion"}

    for row in techniques:
        assert_condition(row["relationship"] in allowed_relationships, f"Invalid relationship: {row['id']}")
        assert_condition(row["group"] in allowed_groups, f"Invalid group: {row['id']}")
        assert_condition("movers=" in row["timing_recipe"], f"Missing movers timing: {row['id']}")
        assert_condition("pars=" in row["timing_recipe"], f"Missing PAR timing: {row['id']}")

    return set(ids)


def validate_palettes(data: dict) -> set[str]:
    palettes = data["palettes"]
    ids = [row["id"] for row in palettes]
    assert_condition(len(ids) == len(set(ids)), "Duplicate palette IDs found")
    assert_sequential("P", ids, 1, 48)

    for row in palettes:
        assert_condition(len(row.get("hex", [])) >= 3, f"Palette missing hex triplet: {row['id']}")
        for token in row["hex"]:
            assert_condition(bool(re.fullmatch(r"#[0-9A-Fa-f]{6}", token)), f"Invalid hex token {token} in {row['id']}")

    selection_ids = set()
    for values in data["selection_rules"]["by_energy"].values():
        selection_ids.update(values)

    invalid = sorted(selection_ids - set(ids))
    assert_condition(not invalid, f"Unknown palette IDs in selection_rules: {invalid}")

    return set(ids)


def validate_designers(data: dict) -> set[str]:
    designers = data["designers"]
    ids = [row["id"] for row in designers]
    assert_condition(len(ids) == len(set(ids)), "Duplicate designer IDs found")
    assert_condition(len(ids) >= 15, "Designer catalog unexpectedly small; expected at least LD-001..LD-015")
    assert_sequential("LD", ids, 1, len(ids))

    template = data["prompt_template"]
    assert_condition(len(template.get("input", [])) >= 3, "Designer prompt template input is incomplete")
    assert_condition(len(template.get("output", [])) >= 3, "Designer prompt template output is incomplete")

    return set(ids)


def validate_designer_techniques(data: dict, valid_ld_ids: set[str]) -> set[str]:
    packs = data.get("packs", [])
    assert_condition(isinstance(packs, list) and packs, "designer-techniques.json has no packs")

    ids = [str(row.get("id", "")) for row in packs]
    assert_condition(len(ids) == len(set(ids)), "Duplicate designer technique pack IDs found")
    assert_sequential("DTP", ids, 1, len(ids))

    model = data.get("selection_model", {})
    assert_condition(isinstance(model, dict), "designer-techniques selection_model must be an object")
    dominant_range = model.get("dominant_pack_count_range", [])
    assert_condition(
        isinstance(dominant_range, list) and len(dominant_range) >= 2,
        "designer-techniques dominant_pack_count_range must be [min,max]",
    )
    assert_condition(int(dominant_range[0]) >= 1, "dominant pack min must be >=1")
    assert_condition(int(dominant_range[1]) >= int(dominant_range[0]), "dominant pack max must be >= min")
    assert_condition(int(model.get("contrast_pack_count", 0)) >= 1, "contrast_pack_count must be >=1")
    assert_condition(int(model.get("pack_cooldown_shows", 0)) >= 1, "pack_cooldown_shows must be >=1")

    allowed_phrases = {"intro", "verse_groove", "build", "drop", "breakdown", "outro"}
    allowed_transforms = {"mirror", "invert", "phase_shift", "expand", "compress", "reverse"}
    allowed_modes = {"blink1", "blink2", "blink4", "fade4", "fade8"}
    allowed_relationships = {"unison", "counterpoint", "inclusion"}

    for row in packs:
        pack_id = row.get("id", "<unknown>")
        ld_id = str(row.get("ld_id", ""))
        assert_condition(ld_id in valid_ld_ids, f"{pack_id} references unknown ld_id: {ld_id}")

        for key in ("name", "focus"):
            assert_condition(bool(str(row.get(key, "")).strip()), f"{pack_id} missing {key}")

        phrase_targets = row.get("phrase_targets", [])
        assert_condition(isinstance(phrase_targets, list) and phrase_targets, f"{pack_id} phrase_targets must be a non-empty list")
        invalid_phrases = sorted(set(phrase_targets) - allowed_phrases)
        assert_condition(not invalid_phrases, f"{pack_id} has invalid phrase_targets: {invalid_phrases}")

        transforms = row.get("preferred_transforms", [])
        assert_condition(isinstance(transforms, list) and transforms, f"{pack_id} preferred_transforms missing")
        invalid_transforms = sorted(set(transforms) - allowed_transforms)
        assert_condition(not invalid_transforms, f"{pack_id} invalid preferred_transforms: {invalid_transforms}")

        modes = row.get("preferred_par_modes", [])
        assert_condition(isinstance(modes, list) and modes, f"{pack_id} preferred_par_modes missing")
        invalid_modes = sorted(set(modes) - allowed_modes)
        assert_condition(not invalid_modes, f"{pack_id} invalid preferred_par_modes: {invalid_modes}")

        rels = row.get("preferred_relationships", [])
        assert_condition(isinstance(rels, list) and rels, f"{pack_id} preferred_relationships missing")
        invalid_rels = sorted(set(rels) - allowed_relationships)
        assert_condition(not invalid_rels, f"{pack_id} invalid preferred_relationships: {invalid_rels}")

        anti_rules = row.get("anti_rules", [])
        assert_condition(isinstance(anti_rules, list) and len(anti_rules) >= 2, f"{pack_id} must have at least 2 anti_rules")

    return set(ids)


def validate_phrase_rules(data: dict, valid_int_ids: set[str], valid_palette_ids: set[str]) -> None:
    phrase_map = data["phrase_map"]
    expected_keys = {"intro", "verse_groove", "build", "drop", "breakdown", "outro"}
    assert_condition(set(phrase_map.keys()) == expected_keys, "Phrase map keys mismatch")

    for name, section in phrase_map.items():
        for field in ("mover_mode", "par_mode", "coordination_pool"):
            assert_condition(field in section, f"Missing {field} in phrase {name}")
        pool = set(section["coordination_pool"])
        invalid = sorted(pool - valid_int_ids)
        assert_condition(not invalid, f"Unknown coordination IDs in phrase {name}: {invalid}")

    uniqueness = data["uniqueness_constraints"]
    for field in (
        "no_same_mover_route_within",
        "no_same_par_pattern_within",
        "no_same_palette_within",
        "include_density_peak_per_song",
        "mandatory_reset_after_peak",
    ):
        assert_condition(field in uniqueness, f"Missing uniqueness constraint: {field}")

    contrast = data.get("contrast_rules", {})
    assert_condition(isinstance(contrast, dict), "contrast_rules must be an object")
    assert_condition(
        int(contrast.get("min_changed_dimensions_on_phrase_change", 0)) >= 2,
        "contrast_rules.min_changed_dimensions_on_phrase_change must be >=2",
    )
    assert_condition(
        int(contrast.get("candidate_plan_count", 0)) >= 3,
        "contrast_rules.candidate_plan_count must be >=3",
    )
    contrast_dims = contrast.get("dimensions", [])
    assert_condition(isinstance(contrast_dims, list) and len(contrast_dims) >= 5, "contrast_rules.dimensions is incomplete")
    for dim in ("position", "rhythm", "color", "intensity", "effect_density"):
        assert_condition(dim in contrast_dims, f"contrast_rules.dimensions missing '{dim}'")

    grammar = data.get("mover_pattern_grammar", {})
    assert_condition(isinstance(grammar, dict), "mover_pattern_grammar must be an object")
    transforms = grammar.get("transforms", [])
    assert_condition(isinstance(transforms, list), "mover_pattern_grammar.transforms must be a list")
    for token in ("mirror", "invert", "phase_shift", "expand", "compress", "reverse"):
        assert_condition(token in transforms, f"mover_pattern_grammar.transforms missing '{token}'")
    assert_condition(
        bool(str(grammar.get("base_route_source", "")).strip()),
        "mover_pattern_grammar.base_route_source must be set",
    )

    template = data["show_builder_template"]
    required_steps = [f"step_{n}" for n in range(1, 8)]
    for step in required_steps:
        assert_condition(step in template, f"Missing show builder template field: {step}")

    palette_refs = set(re.findall(r"P-\d{3}", " ".join(template.values())))
    invalid_palettes = sorted(palette_refs - valid_palette_ids)
    assert_condition(not invalid_palettes, f"Unknown palette refs in show builder template: {invalid_palettes}")

    # --- transition_events ---
    te = data.get("transition_events")
    if te is not None:
        assert_condition(isinstance(te, dict), "transition_events must be an object")

        energy_map = te.get("energy_map", {})
        assert_condition(isinstance(energy_map, dict), "transition_events.energy_map must be an object")
        allowed_energy = {"low", "mid", "high"}
        for phrase_key, energy_val in energy_map.items():
            assert_condition(phrase_key in expected_keys, f"energy_map has unknown phrase: {phrase_key}")
            assert_condition(energy_val in allowed_energy, f"energy_map[{phrase_key}] has invalid energy: {energy_val}")

        pools = te.get("pools", {})
        assert_condition(isinstance(pools, dict) and pools, "transition_events.pools must be a non-empty object")

        schema = te.get("event_schema", {})
        assert_condition(isinstance(schema, dict) and schema, "transition_events.event_schema must be a non-empty object")

        all_pool_types = set()
        for pool_key, pool_list in pools.items():
            assert_condition(isinstance(pool_list, list) and pool_list, f"transition pool {pool_key} must be a non-empty list")
            for t_type in pool_list:
                assert_condition(t_type in schema, f"transition type {t_type!r} in pool {pool_key!r} not found in event_schema")
                all_pool_types.add(t_type)

        allowed_fixtures = {"all", "pars", "movers", "pars+movers"}
        allowed_exit = {"snap", "smooth"}
        for t_name, t_def in schema.items():
            assert_condition(isinstance(t_def, dict), f"event_schema[{t_name}] must be an object")
            assert_condition(isinstance(t_def.get("duration_beats"), int) and t_def["duration_beats"] >= 1,
                             f"event_schema[{t_name}].duration_beats must be int >= 1")
            assert_condition(t_def.get("fixtures") in allowed_fixtures,
                             f"event_schema[{t_name}].fixtures must be one of {allowed_fixtures}")
            assert_condition(t_def.get("exit_style") in allowed_exit,
                             f"event_schema[{t_name}].exit_style must be one of {allowed_exit}")

        assert_condition(isinstance(te.get("cooldown"), int) and te["cooldown"] >= 1,
                         "transition_events.cooldown must be int >= 1")
        assert_condition(len(schema) >= 10, f"Expected at least 10 transition types, got {len(schema)}")

    # --- beat_reactivity ---
    br = data.get("beat_reactivity")
    if br is not None:
        assert_condition(isinstance(br, dict), "beat_reactivity must be an object")
        allowed_granularity = {"beat", "2beat", "bar", "2bar", "4bar"}
        allowed_accent = {"none", "bar_downbeat", "beat", "sub_beat"}
        for phrase_key in expected_keys:
            assert_condition(phrase_key in br, f"beat_reactivity missing phrase: {phrase_key}")
            entry = br[phrase_key]
            assert_condition(entry.get("par_min") in allowed_granularity,
                             f"beat_reactivity[{phrase_key}].par_min invalid: {entry.get('par_min')}")
            assert_condition(entry.get("mover_min") in allowed_granularity,
                             f"beat_reactivity[{phrase_key}].mover_min invalid: {entry.get('mover_min')}")
            assert_condition(entry.get("accent_layer") in allowed_accent,
                             f"beat_reactivity[{phrase_key}].accent_layer invalid: {entry.get('accent_layer')}")

    # --- accent_type_pools ---
    atp = data.get("accent_type_pools")
    if atp is not None:
        assert_condition(isinstance(atp, list) and len(atp) >= 5,
                         f"accent_type_pools must have at least 5 entries, got {len(atp) if isinstance(atp, list) else 'non-list'}")


def validate_manifest(manifest: dict, counts: dict[str, int]) -> None:
    assert_condition(manifest["counts"] == counts, "Manifest counts do not match catalog data")
    required_catalogs = {
        "coordination_techniques",
        "palettes",
        "designers",
        "designer_techniques",
        "phrase_rules",
    }
    assert_condition(set(manifest["catalogs"].keys()) == required_catalogs, "Manifest catalog keys mismatch")


def validate_creativity_is_venue_agnostic(creativity_text: str) -> None:
    for pattern in CREATIVITY_BANNED_PATTERNS:
        assert_condition(
            re.search(pattern, creativity_text) is None,
            f"references/creativity.md contains venue-specific token matching: {pattern}",
        )


def main() -> None:
    data_dir = Path(__file__).resolve().parent
    creativity_path = data_dir.parent / "creativity.md"

    coordination = load_json(data_dir / "coordination-techniques.json")
    palettes = load_json(data_dir / "palettes.json")
    designers = load_json(data_dir / "designers.json")
    designer_techniques = load_json(data_dir / "designer-techniques.json")
    phrase_rules = load_json(data_dir / "phrase-rules.json")
    manifest = load_json(data_dir / "manifest.json")
    creativity_text = creativity_path.read_text(encoding="utf-8")

    int_ids = validate_coordination(coordination)
    palette_ids = validate_palettes(palettes)
    ld_ids = validate_designers(designers)
    validate_designer_techniques(designer_techniques, ld_ids)
    validate_phrase_rules(phrase_rules, int_ids, palette_ids)
    validate_creativity_is_venue_agnostic(creativity_text)

    counts = {
        "coordination_techniques": len(coordination["techniques"]),
        "palettes": len(palettes["palettes"]),
        "designers": len(designers["designers"]),
        "designer_techniques": len(designer_techniques["packs"]),
        "phrase_buckets": len(phrase_rules["phrase_map"]),
    }
    validate_manifest(manifest, counts)

    print("Validation passed:")
    print(f"- coordination techniques: {counts['coordination_techniques']}")
    print(f"- palettes: {counts['palettes']}")
    print(f"- designers: {counts['designers']}")
    print(f"- designer techniques: {counts['designer_techniques']}")
    print(f"- phrase buckets: {counts['phrase_buckets']}")
    print("- creativity.md venue-agnostic check: passed")


if __name__ == "__main__":
    main()
