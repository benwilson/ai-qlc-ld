#!/usr/bin/env python3
"""Venue creativity profile loading and validation.

The global creativity layer is venue-agnostic. Venue-specific mappings live at:
  venue/<venue-name>/references/creative-profile.json
"""

from __future__ import annotations

from datetime import date, datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SCHEMA_VERSION = 1
REQUIRED_ROLES = (
    "PAR_A",
    "PAR_B",
    "M1_BEAM",
    "M2_HYBRID",
    "M3_PROFILE",
    "M4_FX",
)
REQUIRED_BASE_ZONES = (
    "C",
    "SL",
    "SR",
    "USL",
    "USC",
    "USR",
    "DSL",
    "DSC",
    "DSR",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _require_nonempty_text(obj: Dict[str, Any], key: str, context: str) -> str:
    value = str(obj.get(key, "")).strip()
    _require(bool(value), f"Missing {context}.{key}")
    return value


def _require_nonempty_dict(obj: Dict[str, Any], key: str, context: str) -> Dict[str, Any]:
    value = obj.get(key)
    _require(isinstance(value, dict), f"{context}.{key} must be an object")
    _require(bool(value), f"{context}.{key} must not be empty")
    return value


def _require_nonempty_list(obj: Dict[str, Any], key: str, context: str) -> List[Any]:
    value = obj.get(key)
    _require(isinstance(value, list), f"{context}.{key} must be a list")
    _require(bool(value), f"{context}.{key} must not be empty")
    return value


def _validate_date(text: str) -> None:
    try:
        d = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("updated_on must be YYYY-MM-DD") from exc
    _require(d <= date.today(), "updated_on cannot be in the future")


def _resolve_venue_dir(project_root: Path, venue_dir: Optional[str | Path]) -> Path:
    if venue_dir:
        vdir = Path(venue_dir)
        if not vdir.is_absolute():
            vdir = project_root / vdir
        vdir = vdir.resolve()
        if vdir.name == "references":
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


def resolve_venue_profile_path(
    project_root: str | Path,
    venue_dir: Optional[str | Path] = None,
) -> Path:
    root = Path(project_root)
    resolved_venue = _resolve_venue_dir(root, venue_dir)
    return resolved_venue / "references" / "creative-profile.json"


def load_and_validate_venue_profile(
    project_root: str | Path,
    venue_dir: Optional[str | Path] = None,
) -> Dict[str, Any]:
    profile_path = resolve_venue_profile_path(project_root=project_root, venue_dir=venue_dir)
    if not profile_path.exists():
        raise ValueError(f"Missing venue creative profile: {profile_path}")

    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in venue creative profile: {profile_path}") from exc

    _require(isinstance(data, dict), "Venue creative profile root must be an object")
    _require(data.get("schema_version") == SCHEMA_VERSION, f"schema_version must be {SCHEMA_VERSION}")

    venue_name = _require_nonempty_text(data, "venue", "profile")
    _validate_date(_require_nonempty_text(data, "updated_on", "profile"))

    fixture_roles = _require_nonempty_dict(data, "fixture_roles", "profile")
    missing_roles = [role for role in REQUIRED_ROLES if role not in fixture_roles]
    _require(not missing_roles, f"fixture_roles missing required role(s): {missing_roles}")
    for role, value in fixture_roles.items():
        _require(bool(str(value).strip()), f"fixture_roles.{role} must be non-empty text")

    zone_aliases = _require_nonempty_dict(data, "zone_aliases", "profile")
    missing_zones = [zone for zone in REQUIRED_BASE_ZONES if zone not in zone_aliases]
    _require(not missing_zones, f"zone_aliases missing required zone(s): {missing_zones}")
    for zone, value in zone_aliases.items():
        _require(bool(str(value).strip()), f"zone_aliases.{zone} must be non-empty text")

    special_zones = _require_nonempty_dict(data, "special_zones", "profile")
    for zone, value in special_zones.items():
        _require(bool(str(zone).strip()), "special_zones keys must be non-empty")
        _require(bool(str(value).strip()), f"special_zones.{zone} must be non-empty text")

    par_groups = _require_nonempty_dict(data, "par_groups", "profile")
    for key in ("PAR_A", "PAR_B"):
        _require(key in par_groups, f"par_groups missing {key}")
        heads = _require_nonempty_list(par_groups, key, "par_groups")
        for head in heads:
            _require(bool(str(head).strip()), f"par_groups.{key} contains empty head token")

    reference_files = _require_nonempty_list(data, "reference_files", "profile")
    for idx, rel_path in enumerate(reference_files):
        text = str(rel_path).strip()
        _require(bool(text), f"reference_files[{idx}] is empty")

    resolved_venue = profile_path.parents[1]
    _require(
        venue_name == resolved_venue.name,
        f"profile.venue mismatch (expected {resolved_venue.name}, got {venue_name})",
    )

    data["_meta"] = {
        "profile_json": str(profile_path),
        "venue_dir": str(resolved_venue),
    }
    return data


def validate_all_venue_profiles(project_root: str | Path) -> List[Tuple[str, bool, str]]:
    root = Path(project_root)
    venue_root = root / "venue"
    if not venue_root.exists():
        return []

    results: List[Tuple[str, bool, str]] = []
    for venue_dir in sorted(venue_root.iterdir()):
        if not venue_dir.is_dir():
            continue
        try:
            load_and_validate_venue_profile(project_root=root, venue_dir=venue_dir)
            results.append((venue_dir.name, True, "ok"))
        except Exception as exc:  # pragma: no cover - reporting path
            results.append((venue_dir.name, False, str(exc)))
    return results
