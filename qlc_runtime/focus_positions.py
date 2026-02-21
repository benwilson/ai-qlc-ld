#!/usr/bin/env python3
"""Focus-position loading for venue-portable generators.

Parses venue/<name>/focus-positions.md and returns canonical mover tuples:
  (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, profile_pan, profile_tilt, ni3k_pan)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Optional, Tuple

from qlc_runtime.venue_profile import load_and_validate_venue_profile


MoverTuple = Tuple[int, int, int, int, int, int, int]


def _resolve_venue_dir(project_root: Path, venue_dir: Optional[str | Path]) -> Path:
    profile = load_and_validate_venue_profile(project_root=project_root, venue_dir=venue_dir)
    return Path(profile["_meta"]["venue_dir"])


def _heading_key(heading: str, special_zones: Dict[str, str]) -> str:
    code_match = re.search(r"\(([A-Za-z0-9_]+)\)", heading)
    if code_match:
        return code_match.group(1).strip().upper()

    normalized = re.sub(r"[^a-z0-9]+", " ", heading.lower()).strip()
    special_map = {
        "dj booth": special_zones.get("DJ_BOOTH", "DJ"),
        "par wall": special_zones.get("PAR_WALL", "PAR_WALL"),
        "dance floor": special_zones.get("DANCE_FLOOR", "DANCE"),
        "disco ball": special_zones.get("DISCO_BALL", "DISCO"),
        "center ceiling": special_zones.get("CENTER_CEILING", "CEIL"),
        "audience blinder": special_zones.get("AUDIENCE", "AUD"),
        "back wall wash": special_zones.get("BACK_WALL", "BACK_WALL"),
        "ceiling hit": special_zones.get("CENTER_CEILING", "CEIL"),
    }
    key = special_map.get(normalized)
    if key:
        return str(key).strip().upper()
    return re.sub(r"[^A-Z0-9]+", "_", heading.upper()).strip("_")


def _parse_table_row(line: str) -> Optional[Tuple[str, Optional[int], Optional[int]]]:
    if not line.startswith("|"):
        return None
    if "Fixture" in line or "---" in line:
        return None

    cells = [cell.strip() for cell in line.split("|")[1:-1]]
    if len(cells) < 3:
        return None

    fixture = cells[0].lower()
    pan = int(cells[1]) if cells[1].isdigit() else None
    tilt = int(cells[2]) if cells[2].isdigit() else None

    if "sharpy" in fixture:
        return ("sharpy", pan, tilt)
    if "bsw" in fixture:
        return ("bsw", pan, tilt)
    if "profile" in fixture:
        return ("profile", pan, tilt)
    if "ni3k" in fixture:
        return ("ni3k", pan, tilt)
    return None


def _required_tuple_components(values: Dict[str, Tuple[Optional[int], Optional[int]]], key: str) -> MoverTuple:
    missing = []
    for fixture in ("sharpy", "bsw", "profile"):
        pair = values.get(fixture)
        if pair is None or pair[0] is None or pair[1] is None:
            missing.append(fixture)
    if missing:
        raise ValueError(f"Focus position {key!r} missing fixture pan/tilt for: {missing}")

    sharpy = values["sharpy"]
    bsw = values["bsw"]
    profile = values["profile"]
    ni_pan = 128
    if "ni3k" in values and values["ni3k"][0] is not None:
        ni_pan = int(values["ni3k"][0])

    return (
        int(sharpy[0]),
        int(sharpy[1]),
        int(bsw[0]),
        int(bsw[1]),
        int(profile[0]),
        int(profile[1]),
        ni_pan,
    )


def _with_default_composites(positions: Dict[str, MoverTuple]) -> Dict[str, MoverTuple]:
    out = dict(positions)
    if "X" not in out and all(k in out for k in ("SR", "DSL", "C")):
        sr = out["SR"]
        dsl = out["DSL"]
        c = out["C"]
        out["X"] = (sr[0], sr[1], dsl[2], dsl[3], c[4], c[5], c[6])
    return out


def _with_compat_aliases(positions: Dict[str, MoverTuple]) -> Dict[str, MoverTuple]:
    out = dict(positions)
    # Keep legacy short keys usable when venues opt into longer alias labels.
    if "DISCO_BALL" in out and "DISCO" not in out:
        out["DISCO"] = out["DISCO_BALL"]
    if "DISCO" in out and "DISCO_BALL" not in out:
        out["DISCO_BALL"] = out["DISCO"]
    return out


def load_focus_position_tuples(
    project_root: str | Path,
    venue_dir: Optional[str | Path] = None,
    include_composites: bool = True,
) -> Dict[str, MoverTuple]:
    root = Path(project_root)
    venue = _resolve_venue_dir(root, venue_dir=venue_dir)
    profile = load_and_validate_venue_profile(project_root=root, venue_dir=venue)
    special_zones = profile["special_zones"]

    focus_path = venue / "focus-positions.md"
    if not focus_path.exists():
        raise ValueError(f"Missing focus positions file: {focus_path}")

    raw = focus_path.read_text(encoding="utf-8")
    sections = re.split(r"^###\s+", raw, flags=re.MULTILINE)

    positions: Dict[str, MoverTuple] = {}
    for section in sections[1:]:
        lines = section.strip().splitlines()
        if not lines:
            continue
        heading = lines[0].strip()
        lower_lines = [line.lower() for line in lines[1:]]
        has_pan_tilt_table = any(("pan" in line and "tilt" in line) for line in lower_lines)
        key = _heading_key(heading, special_zones=special_zones)

        parsed: Dict[str, Tuple[Optional[int], Optional[int]]] = {}
        for line in lines[1:]:
            row = _parse_table_row(line)
            if row is None:
                continue
            fixture, pan, tilt = row
            parsed[fixture] = (pan, tilt)

        if not parsed:
            continue

        has_numeric_pan_tilt = any(
            (pair[0] is not None or pair[1] is not None)
            for pair in parsed.values()
        )

        try:
            positions[key] = _required_tuple_components(parsed, key=key)
        except ValueError as exc:
            # Ignore non-position metadata tables, but fail fast for malformed
            # Pan/Tilt focus sections so config errors surface clearly.
            if has_pan_tilt_table and has_numeric_pan_tilt:
                raise ValueError(f"Invalid focus-position section {heading!r}: {exc}") from exc
            continue

    positions = _with_compat_aliases(positions)
    if include_composites:
        positions = _with_default_composites(positions)

    return positions
