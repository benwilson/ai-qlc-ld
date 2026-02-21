import json
from pathlib import Path

from qlc_runtime.research_gate import (
    SCHEMA_VERSION,
    load_and_validate_brief,
    resolve_brief_paths,
    slugify_song,
    validate_all_briefs,
)


def _approved_brief(song_title: str):
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "approved",
        "song_title": song_title,
        "artist": "Test Artist",
        "research_date": "2026-02-19",
        "thesis": "Cinematic tension and release with architecture-led motion and title-derived motifs.",
        "artist_branding": {
            "summary": "Minimal monochrome architecture with occasional warm accents.",
            "visual_cues": ["Monochrome", "Hard diagonals", "Sparse white accents"],
            "do_not_copy": ["Avoid direct duplication of signature stage objects."],
        },
        "song_title_inspiration": {
            "keywords": ["ivory", "stone", "echo"],
            "motifs": [
                "Column-like beam stacks",
                "Desaturated ivory palette accents",
                "Slow echoing 4-beat movement",
            ],
        },
        "visual_direction": {
            "color_story": "Steel blue to ivory-white crest.",
            "motion_story": "4-beat arcs with controlled inclusion bursts.",
            "staging_story": "Center spine with periodic diagonal expansions.",
        },
        "style_constraints": {
            "must_include": ["At least one macro and one micro moment per 16 bars"],
            "avoid": ["No constant full-field strobe blocks"],
        },
        "brand_alignment_score": 4,
        "sources": [
            {
                "title": "Artist Website",
                "url": "https://example.com/artist",
                "year": 2025,
                "category": "artist_branding",
                "note": "Brand language",
            },
            {
                "title": "Official Track Upload",
                "url": "https://example.com/song",
                "year": 2026,
                "category": "song_specific",
                "note": "Track context",
            },
            {
                "title": "Visual Performance Reference",
                "url": "https://example.com/visual-1",
                "year": 2024,
                "category": "visual_reference",
                "note": "Lighting language",
            },
            {
                "title": "Interview",
                "url": "https://example.com/interview",
                "year": 2023,
                "category": "artist_branding",
                "note": "Intent",
            },
            {
                "title": "Creative Review",
                "url": "https://example.com/review",
                "year": 2021,
                "category": "visual_reference",
                "note": "Historical context",
            },
        ],
    }


def test_slugify_song():
    assert slugify_song("Daniel Portman - Ivory (Extended Mix)") == "daniel_portman_ivory_extended_mix"


def test_missing_brief_creates_stub_and_fails(tmp_path):
    song_title = "New Song"
    venue_dir = "venue/home-studio"
    try:
        load_and_validate_brief(
            song_title=song_title,
            project_root=tmp_path,
            venue_dir=venue_dir,
        )
        assert False, "Expected missing/draft brief to fail validation"
    except Exception as exc:
        assert "status must be 'approved'" in str(exc)

    json_path, md_path = resolve_brief_paths(tmp_path, song_title, venue_dir=venue_dir)
    assert json_path.exists()
    assert md_path.exists()
    assert "shows/notes" in str(json_path.as_posix())


def test_approved_brief_passes(tmp_path):
    song_title = "Approved Song"
    venue_dir = "venue/home-studio"
    json_path, _ = resolve_brief_paths(tmp_path, song_title, venue_dir=venue_dir)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(_approved_brief(song_title), indent=2) + "\n", encoding="utf-8")

    brief = load_and_validate_brief(
        song_title=song_title,
        project_root=tmp_path,
        venue_dir=venue_dir,
    )
    assert brief["status"] == "approved"
    assert brief["_meta"]["slug"] == "approved_song"


def test_requires_explicit_venue_when_multiple_venues_exist(tmp_path):
    (tmp_path / "venue" / "a").mkdir(parents=True, exist_ok=True)
    (tmp_path / "venue" / "b").mkdir(parents=True, exist_ok=True)
    try:
        resolve_brief_paths(tmp_path, "Any Song")
        assert False, "Expected multiple venues without venue_dir to fail"
    except Exception as exc:
        assert "Multiple venue directories found" in str(exc)


def test_validate_all_briefs_uses_embedded_song_title_without_slug_side_effects(tmp_path):
    notes_dir = tmp_path / "venue" / "home-studio" / "shows" / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)

    payload = _approved_brief("Bar Song")
    (notes_dir / "foo.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    results = validate_all_briefs(tmp_path, venue_dir="venue/home-studio")
    assert results == [("Bar Song", True, "ok")]
    assert not (notes_dir / "bar_song.json").exists()


def test_explicit_brief_json_path_bypasses_multi_venue_resolution(tmp_path):
    notes_dir = tmp_path / "venue" / "a" / "shows" / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    (tmp_path / "venue" / "b" / "shows" / "notes").mkdir(parents=True, exist_ok=True)

    json_path = notes_dir / "custom_name.json"
    payload = _approved_brief("Custom Song")
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    brief = load_and_validate_brief(
        song_title="Custom Song",
        project_root=tmp_path,
        brief_json_path=json_path,
        create_stub_if_missing=False,
    )
    assert brief["status"] == "approved"
    assert brief["_meta"]["brief_json"] == str(json_path)
