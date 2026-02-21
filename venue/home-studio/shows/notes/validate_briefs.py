#!/usr/bin/env python3
"""Validate research briefs for this venue (or all venues)."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
DEFAULT_VENUE = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from qlc_runtime.research_gate import load_and_validate_brief, validate_all_briefs


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate research briefs")
    parser.add_argument(
        "--venue",
        default=str(DEFAULT_VENUE.relative_to(ROOT)),
        help="Venue directory relative to project root",
    )
    parser.add_argument(
        "--all-venues",
        action="store_true",
        help="Validate briefs across all venue/*/shows/notes folders",
    )
    parser.add_argument("--song", default=None, help="Validate only one song title")
    args = parser.parse_args()

    if args.song:
        try:
            brief = load_and_validate_brief(
                song_title=args.song,
                project_root=ROOT,
                venue_dir=args.venue,
            )
        except Exception as exc:
            print(f"FAIL: {args.song}: {exc}")
            return 1
        print(f"OK: {args.song}")
        print(f"  brief: {brief['_meta']['brief_json']}")
        return 0

    results = validate_all_briefs(
        ROOT,
        venue_dir=None if args.all_venues else args.venue,
    )
    if not results:
        print("No research briefs found.")
        return 1

    failures = 0
    for song_title, ok, message in results:
        prefix = "OK" if ok else "FAIL"
        print(f"{prefix}: {song_title}: {message}")
        if not ok:
            failures += 1

    if failures:
        print(f"\n{failures} brief(s) failed validation.")
        return 1

    print("\nAll briefs valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
