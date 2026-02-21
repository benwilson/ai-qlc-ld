#!/usr/bin/env python3
"""Research brief enforcement for show generation.

Each song generator must load an approved research brief that captures:
- artist branding/style
- song-title-inspired motifs
- source citations with recency
- final creative thesis

Briefs are stored per venue under:
  venue/<venue-name>/shows/notes/<song-slug>.json
"""

from __future__ import annotations

from datetime import date, datetime
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple

SCHEMA_VERSION = 1
MIN_SOURCE_COUNT = 5
MIN_RECENT_SOURCE_COUNT = 2
RECENT_WINDOW_YEARS = 3

REQUIRED_SOURCE_CATEGORIES = {
    "artist_branding",
    "song_specific",
    "visual_reference",
}


def slugify_song(song_title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", str(song_title).strip().lower())
    return slug.strip("_") or "untitled_song"


def _resolve_venue_dir(project_root: Path, venue_dir: Optional[str | Path]) -> Path:
    if venue_dir:
        vdir = Path(venue_dir)
        if not vdir.is_absolute():
            vdir = project_root / vdir
        vdir = vdir.resolve()
        if vdir.name == "notes" and vdir.parent.name == "shows":
            return vdir.parent.parent
        if vdir.name == "shows":
            return vdir.parent
        return vdir

    venue_root = project_root / "venue"
    candidates: List[Path] = []
    if venue_root.exists():
        for row in sorted(venue_root.iterdir()):
            if row.is_dir():
                candidates.append(row)
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise ValueError("No venue directories found under project_root/venue")
    raise ValueError("Multiple venue directories found; pass venue_dir explicitly.")


def resolve_brief_dir(
    project_root: str | Path,
    venue_dir: Optional[str | Path] = None,
) -> Path:
    root = Path(project_root)
    resolved_venue = _resolve_venue_dir(root, venue_dir)
    return resolved_venue / "shows" / "notes"


def resolve_brief_paths(
    project_root: str | Path,
    song_title: str,
    venue_dir: Optional[str | Path] = None,
) -> Tuple[Path, Path]:
    brief_dir = resolve_brief_dir(project_root=project_root, venue_dir=venue_dir)
    base = slugify_song(song_title)
    return brief_dir / f"{base}.json", brief_dir / f"{base}.md"


def _default_stub(song_title: str) -> Dict[str, Any]:
    year = date.today().year
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "draft",
        "song_title": song_title,
        "artist": "TODO",
        "research_date": str(date.today()),
        "thesis": "TODO: One-sentence creative thesis tied to artist brand + song title motifs.",
        "artist_branding": {
            "summary": "TODO",
            "visual_cues": [
                "TODO",
                "TODO",
                "TODO",
            ],
            "do_not_copy": [
                "TODO: Avoid direct cloning of signature set pieces.",
            ],
        },
        "song_title_inspiration": {
            "keywords": ["TODO", "TODO"],
            "motifs": [
                "TODO: geometry motif",
                "TODO: color motif",
                "TODO: movement motif",
            ],
        },
        "visual_direction": {
            "color_story": "TODO",
            "motion_story": "TODO",
            "staging_story": "TODO",
        },
        "style_constraints": {
            "must_include": [
                "TODO",
            ],
            "avoid": [
                "TODO",
            ],
        },
        "brand_alignment_score": 0,
        "sources": [
            {
                "title": "TODO",
                "url": "https://example.com",
                "year": year,
                "category": "artist_branding",
                "note": "TODO",
            },
            {
                "title": "TODO",
                "url": "https://example.com",
                "year": year,
                "category": "song_specific",
                "note": "TODO",
            },
            {
                "title": "TODO",
                "url": "https://example.com",
                "year": year,
                "category": "visual_reference",
                "note": "TODO",
            },
            {
                "title": "TODO",
                "url": "https://example.com",
                "year": year,
                "category": "artist_branding",
                "note": "TODO",
            },
            {
                "title": "TODO",
                "url": "https://example.com",
                "year": year,
                "category": "visual_reference",
                "note": "TODO",
            },
        ],
    }


def _default_markdown(song_title: str) -> str:
    return f"""# Research Brief: {song_title}

Status: `draft`

## Artist Branding
- Summary: TODO
- Visual cues:
  - TODO
  - TODO
  - TODO

## Song Title Inspiration
- Keywords: TODO, TODO
- Motifs:
  - Geometry: TODO
  - Color: TODO
  - Motion: TODO

## Creative Thesis
- TODO

## Sources
- TODO (add at least {MIN_SOURCE_COUNT}, including at least {MIN_RECENT_SOURCE_COUNT} from the last {RECENT_WINDOW_YEARS} years)
"""


def _write_stub_if_missing(json_path: Path, md_path: Path, song_title: str) -> None:
    if json_path.exists():
        return
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(_default_stub(song_title), indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    if not md_path.exists():
        md_path.write_text(_default_markdown(song_title), encoding="utf-8")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _require_nonempty_text(obj: Dict[str, Any], key: str, context: str) -> str:
    value = str(obj.get(key, "")).strip()
    _require(bool(value), f"Missing {context}.{key}")
    return value


def _require_nonempty_list(obj: Dict[str, Any], key: str, context: str, min_len: int = 1) -> List[Any]:
    value = obj.get(key)
    _require(isinstance(value, list), f"{context}.{key} must be a list")
    _require(len(value) >= min_len, f"{context}.{key} must have at least {min_len} item(s)")
    return value


def _validate_date(text: str) -> None:
    try:
        d = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("research_date must be YYYY-MM-DD") from exc
    _require(d <= date.today(), "research_date cannot be in the future")


def _validate_sources(sources: List[Dict[str, Any]]) -> None:
    _require(len(sources) >= MIN_SOURCE_COUNT, f"At least {MIN_SOURCE_COUNT} sources required")

    current_year = date.today().year
    recent_cutoff = current_year - RECENT_WINDOW_YEARS

    recent_count = 0
    categories = set()

    for i, src in enumerate(sources):
        _require(isinstance(src, dict), f"sources[{i}] must be an object")
        title = _require_nonempty_text(src, "title", f"sources[{i}]")
        _ = title
        url = _require_nonempty_text(src, "url", f"sources[{i}]")
        _require(url.startswith("http://") or url.startswith("https://"), f"sources[{i}].url must start with http:// or https://")

        year = src.get("year")
        _require(isinstance(year, int), f"sources[{i}].year must be an integer")
        _require(1900 <= year <= current_year + 1, f"sources[{i}].year looks invalid")
        if year >= recent_cutoff:
            recent_count += 1

        category = _require_nonempty_text(src, "category", f"sources[{i}]")
        categories.add(category)

    _require(
        recent_count >= MIN_RECENT_SOURCE_COUNT,
        f"Need at least {MIN_RECENT_SOURCE_COUNT} recent source(s) from {recent_cutoff}+",
    )
    missing_categories = sorted(REQUIRED_SOURCE_CATEGORIES - categories)
    _require(
        not missing_categories,
        f"Missing required source categories: {missing_categories}",
    )


def load_and_validate_brief(
    song_title: str,
    project_root: str | Path,
    venue_dir: Optional[str | Path] = None,
    brief_json_path: Optional[str | Path] = None,
    brief_md_path: Optional[str | Path] = None,
    create_stub_if_missing: bool = True,
) -> Dict[str, Any]:
    root = Path(project_root)

    if brief_json_path is None:
        json_path, md_path = resolve_brief_paths(root, song_title, venue_dir=venue_dir)
    else:
        json_path = Path(brief_json_path)
        if not json_path.is_absolute():
            json_path = root / json_path
        md_path = json_path.with_suffix(".md")

    if brief_md_path is not None:
        md_path = Path(brief_md_path)
        if not md_path.is_absolute():
            md_path = root / md_path

    if create_stub_if_missing:
        _write_stub_if_missing(json_path, md_path, song_title)
    elif not json_path.exists():
        raise ValueError(f"Missing research brief: {json_path}")

    raw = json_path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in research brief: {json_path}") from exc

    _require(isinstance(data, dict), "Research brief root must be an object")

    _require(data.get("schema_version") == SCHEMA_VERSION, f"schema_version must be {SCHEMA_VERSION}")
    status = str(data.get("status", "")).strip().lower()
    _require(status == "approved", "Research brief status must be 'approved'")

    brief_song = _require_nonempty_text(data, "song_title", "brief")
    _require(brief_song == song_title, f"song_title mismatch (expected: {song_title})")

    _require_nonempty_text(data, "artist", "brief")
    research_date = _require_nonempty_text(data, "research_date", "brief")
    _validate_date(research_date)

    thesis = _require_nonempty_text(data, "thesis", "brief")
    _require(len(thesis) >= 24, "thesis is too short")

    branding = data.get("artist_branding")
    _require(isinstance(branding, dict), "artist_branding must be an object")
    _require_nonempty_text(branding, "summary", "artist_branding")
    _require_nonempty_list(branding, "visual_cues", "artist_branding", min_len=3)
    _require_nonempty_list(branding, "do_not_copy", "artist_branding", min_len=1)

    title_inspo = data.get("song_title_inspiration")
    _require(isinstance(title_inspo, dict), "song_title_inspiration must be an object")
    _require_nonempty_list(title_inspo, "keywords", "song_title_inspiration", min_len=2)
    _require_nonempty_list(title_inspo, "motifs", "song_title_inspiration", min_len=3)

    visual = data.get("visual_direction")
    _require(isinstance(visual, dict), "visual_direction must be an object")
    _require_nonempty_text(visual, "color_story", "visual_direction")
    _require_nonempty_text(visual, "motion_story", "visual_direction")
    _require_nonempty_text(visual, "staging_story", "visual_direction")

    constraints = data.get("style_constraints")
    _require(isinstance(constraints, dict), "style_constraints must be an object")
    _require_nonempty_list(constraints, "must_include", "style_constraints", min_len=1)
    _require_nonempty_list(constraints, "avoid", "style_constraints", min_len=1)

    score = data.get("brand_alignment_score")
    _require(isinstance(score, (int, float)), "brand_alignment_score must be numeric")
    _require(0 <= score <= 5, "brand_alignment_score must be between 0 and 5")
    _require(score >= 3, "brand_alignment_score must be >= 3 for approved briefs")

    sources = data.get("sources")
    _require(isinstance(sources, list), "sources must be a list")
    _validate_sources(sources)

    data["_meta"] = {
        "brief_json": str(json_path),
        "brief_md": str(md_path),
        "slug": slugify_song(song_title),
        "venue_notes_dir": str(json_path.parent),
    }
    return data


def validate_all_briefs(
    project_root: str | Path,
    venue_dir: Optional[str | Path] = None,
) -> List[Tuple[str, bool, str]]:
    root = Path(project_root)

    brief_dirs: List[Path] = []
    if venue_dir is not None:
        brief_dirs.append(resolve_brief_dir(root, venue_dir=venue_dir))
    else:
        venue_root = root / "venue"
        if venue_root.exists():
            for row in sorted(venue_root.iterdir()):
                notes_dir = row / "shows" / "notes"
                if row.is_dir() and notes_dir.exists():
                    brief_dirs.append(notes_dir)

    if not brief_dirs:
        return []

    results: List[Tuple[str, bool, str]] = []
    for brief_dir in brief_dirs:
        resolved_venue = brief_dir.parent.parent
        for json_path in sorted(brief_dir.glob("*.json")):
            song_title = json_path.stem
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    song_title = str(data.get("song_title", "")).strip() or json_path.stem
                load_and_validate_brief(
                    song_title=song_title,
                    project_root=root,
                    venue_dir=resolved_venue,
                    brief_json_path=json_path,
                    brief_md_path=json_path.with_suffix(".md"),
                    create_stub_if_missing=False,
                )
                results.append((song_title, True, "ok"))
            except Exception as exc:  # pragma: no cover - reporting path
                results.append((song_title, False, str(exc)))
    return results
