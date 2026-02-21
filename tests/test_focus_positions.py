import json
from pathlib import Path

from qlc_runtime.focus_positions import load_focus_position_tuples


ROOT = Path(__file__).resolve().parents[1]


def _sample_profile(venue_name: str = "sample-venue"):
    return {
        "schema_version": 1,
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
            "PAR_WALL": "PAR_WALL",
            "DANCE_FLOOR": "DANCE",
            "DISCO_BALL": "DISCO",
            "CENTER_CEILING": "CEIL",
        },
        "par_groups": {
            "PAR_A": ["A1", "A2", "A3", "A4"],
            "PAR_B": ["B1", "B2"],
        },
        "reference_files": [
            "venue/sample-venue/plot.md",
            "venue/sample-venue/focus-positions.md",
        ],
    }


def test_home_studio_focus_positions_load():
    positions = load_focus_position_tuples(project_root=ROOT, venue_dir="venue/home-studio")
    for key in ("C", "DSC", "DJ", "CEIL", "PAR_WALL", "DISCO", "X"):
        assert key in positions
        assert len(positions[key]) == 7


def test_focus_positions_parse_specials_and_composites(tmp_path):
    venue_dir = tmp_path / "venue" / "sample-venue"
    refs_dir = venue_dir / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "creative-profile.json").write_text(
        json.dumps(_sample_profile("sample-venue"), indent=2) + "\n",
        encoding="utf-8",
    )

    focus_text = """# Focus Positions

### Center (C)
| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 100 | 10 | Yes |
| BSW (ID 1) | 120 | 20 | Yes |
| Profile (ID 4) | 140 | 30 | Yes |
| NI3K (ID 3) | 150 | — | Yes |

### Stage Right (SR)
| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 101 | 11 | Yes |
| BSW (ID 1) | 121 | 21 | Yes |
| Profile (ID 4) | 141 | 31 | Yes |
| NI3K (ID 3) | 151 | — | Yes |

### Downstage Left (DSL)
| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 102 | 12 | Yes |
| BSW (ID 1) | 122 | 22 | Yes |
| Profile (ID 4) | 142 | 32 | Yes |
| NI3K (ID 3) | 152 | — | Yes |

### DJ Booth
| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 103 | 13 | Yes |
| BSW (ID 1) | 123 | 23 | Yes |
| Profile (ID 4) | 143 | 33 | Yes |
| NI3K (ID 3) | 153 | — | Yes |
"""
    (venue_dir / "focus-positions.md").write_text(focus_text, encoding="utf-8")

    positions = load_focus_position_tuples(project_root=tmp_path, venue_dir=venue_dir)
    assert positions["DJ"] == (103, 13, 123, 23, 143, 33, 153)
    assert positions["X"] == (101, 11, 122, 22, 140, 30, 150)


def test_focus_positions_fails_fast_on_malformed_pan_tilt_section(tmp_path):
    venue_dir = tmp_path / "venue" / "sample-venue"
    refs_dir = venue_dir / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "creative-profile.json").write_text(
        json.dumps(_sample_profile("sample-venue"), indent=2) + "\n",
        encoding="utf-8",
    )

    # Center section includes a Pan/Tilt table but is missing Profile rows.
    malformed = """# Focus Positions

### Center (C)
| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 100 | 10 | Yes |
| BSW (ID 1) | 120 | 20 | Yes |
"""
    (venue_dir / "focus-positions.md").write_text(malformed, encoding="utf-8")

    try:
        load_focus_position_tuples(project_root=tmp_path, venue_dir=venue_dir)
        assert False, "Expected malformed Pan/Tilt section to raise"
    except Exception as exc:
        assert "Invalid focus-position section" in str(exc)
