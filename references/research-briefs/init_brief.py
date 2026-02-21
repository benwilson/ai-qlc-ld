#!/usr/bin/env python3
"""Create draft research brief stubs for songs."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from qlc_runtime.research_gate import load_and_validate_brief, resolve_brief_paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize draft research brief(s)")
    parser.add_argument(
        "--venue",
        default=None,
        help="Venue directory relative to project root (required if multiple venues exist)",
    )
    parser.add_argument("songs", nargs="+", help="Song title(s)")
    args = parser.parse_args()

    for song in args.songs:
        json_path, md_path = resolve_brief_paths(ROOT, song, venue_dir=args.venue)
        try:
            load_and_validate_brief(song_title=song, project_root=ROOT, venue_dir=args.venue)
            print(f"Already approved: {song}")
            print(f"  {json_path}")
        except Exception as exc:
            # Missing files are auto-created by load_and_validate_brief.
            if json_path.exists():
                print(f"Draft ready: {song}")
                print(f"  {json_path}")
                print(f"  {md_path}")
                print(f"  Next: fill fields, set status=approved, re-run validate.")
            else:
                print(f"Error: could not initialize brief for {song}: {exc}")
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
