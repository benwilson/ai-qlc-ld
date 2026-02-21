import json
from pathlib import Path

import showlib
from qlc_runtime.venue_profile import (
    SCHEMA_VERSION,
    load_and_validate_venue_profile,
    resolve_venue_profile_path,
)


ROOT = Path(__file__).resolve().parents[1]


def _sample_profile(venue_name: str = "home-studio"):
    return {
        "schema_version": SCHEMA_VERSION,
        "venue": venue_name,
        "updated_on": "2026-02-19",
        "fixture_roles": {
            "PAR_A": "Main PAR role",
            "PAR_B": "Secondary PAR role",
            "M1_BEAM": "Beam mover",
            "M2_HYBRID": "Hybrid mover",
            "M3_PROFILE": "Profile mover",
            "M4_FX": "FX role",
        },
        "zone_aliases": {
            "C": "C",
            "SL": "SL",
            "SR": "SR",
            "USL": "USL",
            "USC": "USC",
            "USR": "USR",
            "DSL": "DSL",
            "DSC": "DSC",
            "DSR": "DSR",
        },
        "special_zones": {
            "DJ_BOOTH": "DJ",
            "CENTER_CEILING": "CEIL",
        },
        "par_groups": {
            "PAR_A": ["A1", "A2", "A3", "A4"],
            "PAR_B": ["B1", "B2"],
        },
        "reference_files": [
            "venue/home-studio/plot.md",
            "venue/home-studio/focus-positions.md",
        ],
    }


def test_repo_profile_loads():
    profile = load_and_validate_venue_profile(project_root=ROOT, venue_dir="venue/home-studio")
    assert profile["venue"] == "home-studio"
    assert profile["_meta"]["profile_json"].endswith("venue/home-studio/references/creative-profile.json")


def test_profile_path_resolution(tmp_path):
    venue_dir = tmp_path / "venue" / "my-venue"
    refs_dir = venue_dir / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)

    path = resolve_venue_profile_path(project_root=tmp_path, venue_dir=venue_dir)
    assert path == refs_dir / "creative-profile.json"


def test_missing_profile_fails(tmp_path):
    venue_dir = tmp_path / "venue" / "home-studio"
    venue_dir.mkdir(parents=True, exist_ok=True)
    try:
        load_and_validate_venue_profile(project_root=tmp_path, venue_dir=venue_dir)
        assert False, "Expected missing venue profile to fail"
    except Exception as exc:
        assert "Missing venue creative profile" in str(exc)


def test_valid_profile_passes(tmp_path):
    venue_dir = tmp_path / "venue" / "home-studio"
    refs_dir = venue_dir / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)

    profile_path = refs_dir / "creative-profile.json"
    profile_path.write_text(json.dumps(_sample_profile("home-studio"), indent=2) + "\n", encoding="utf-8")

    profile = load_and_validate_venue_profile(project_root=tmp_path, venue_dir=venue_dir)
    assert profile["fixture_roles"]["PAR_A"] == "Main PAR role"
    assert profile["_meta"]["venue_dir"].endswith("venue/home-studio")


def test_showlib_wrapper_loads_profile():
    profile = showlib.load_venue_profile(project_root=str(ROOT), venue_dir="venue/home-studio")
    assert profile["venue"] == "home-studio"
