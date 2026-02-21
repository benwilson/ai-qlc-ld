#!/usr/bin/env python3
"""Validate venue creative profiles under venue/*/references/creative-profile.json."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from qlc_runtime.venue_profile import validate_all_venue_profiles


def main() -> int:
    results = validate_all_venue_profiles(project_root=ROOT)
    if not results:
        print("No venue profiles found.")
        return 1

    failures = 0
    for venue_name, ok, message in results:
        prefix = "OK" if ok else "FAIL"
        print(f"{prefix}: {venue_name}: {message}")
        if not ok:
            failures += 1

    if failures:
        print(f"\n{failures} venue profile(s) failed validation.")
        return 1

    print("\nAll venue profiles valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
