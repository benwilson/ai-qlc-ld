#!/usr/bin/env python3
"""Install local fixture definitions into QLC+ user fixture directory."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Optional, Union


DEFAULT_TARGET = Path.home() / "Library/Application Support/QLC+/Fixtures"


def _fixture_sources(source_dir: Path) -> Iterable[Path]:
    return sorted(source_dir.glob("*.qxf"))


def _next_backup_path(dst: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    candidate = dst.with_name(f"{dst.name}.bak.{stamp}")
    index = 1
    while candidate.exists():
        index += 1
        candidate = dst.with_name(f"{dst.name}.bak.{stamp}.{index}")
    return candidate


def install_fixtures(
    target_dir: Union[str, Path],
    dry_run: bool = False,
    backup: bool = True,
    source_dir: Optional[Union[str, Path]] = None,
) -> Dict[str, int]:
    """Copy repo fixtures into target directory.

    Returns a summary dictionary with operation counters.
    """
    src_dir = (
        Path(source_dir)
        if source_dir is not None
        else Path(__file__).resolve().parents[1] / "fixtures"
    )
    dst_dir = Path(target_dir)

    if not src_dir.is_dir():
        raise ValueError(f"Fixture source directory does not exist: {src_dir}")

    summary = {
        "installed": 0,
        "updated": 0,
        "unchanged": 0,
        "backed_up": 0,
    }

    if not dry_run:
        dst_dir.mkdir(parents=True, exist_ok=True)

    for src in _fixture_sources(src_dir):
        dst = dst_dir / src.name
        src_bytes = src.read_bytes()

        if dst.exists():
            dst_bytes = dst.read_bytes()
            if dst_bytes == src_bytes:
                summary["unchanged"] += 1
                continue

            summary["updated"] += 1
            if backup:
                summary["backed_up"] += 1
                if not dry_run:
                    shutil.copy2(dst, _next_backup_path(dst))
        else:
            summary["installed"] += 1

        if not dry_run:
            shutil.copy2(src, dst)

    return summary


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install fixture definitions into QLC+ user fixture directory."
    )
    parser.add_argument(
        "--target",
        default=str(DEFAULT_TARGET),
        help=f"Target fixture directory (default: {DEFAULT_TARGET})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without writing files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip backup files for changed target fixtures.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    summary = install_fixtures(
        target_dir=args.target,
        dry_run=args.dry_run,
        backup=not args.no_backup,
    )

    mode = "DRY RUN" if args.dry_run else "APPLY"
    print(f"[{mode}] target={Path(args.target)}")
    print(f"  installed: {summary['installed']}")
    print(f"  updated:   {summary['updated']}")
    print(f"  unchanged: {summary['unchanged']}")
    print(f"  backed_up: {summary['backed_up']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
