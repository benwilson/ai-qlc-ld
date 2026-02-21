#!/usr/bin/env python3
"""Validate the home-studio creative profile."""

from __future__ import annotations

from pathlib import Path
import sys

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
VENUE_DIR = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from qlc_runtime.venue_profile import load_and_validate_venue_profile


def main() -> int:
    try:
        profile = load_and_validate_venue_profile(project_root=ROOT, venue_dir=VENUE_DIR)
    except Exception as exc:
        print(f"FAIL: {VENUE_DIR.name}: {exc}")
        return 1

    print(f"OK: {VENUE_DIR.name}")
    print(f"  profile: {profile['_meta']['profile_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
