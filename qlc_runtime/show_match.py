#!/usr/bin/env python3
import re
import unicodedata
from pathlib import Path
from typing import Dict


_WHITESPACE = re.compile(r"\s+")


def normalize_show_stem(raw: str) -> str:
    text = unicodedata.normalize("NFC", str(raw or ""))
    text = _WHITESPACE.sub(" ", text).strip().casefold()
    return text


def _media_to_stem(media_name: str) -> str:
    basename = Path(str(media_name or "")).name
    stem = Path(basename).stem if basename else ""
    return stem or basename


def index_shows(shows_dir: Path) -> Dict[str, Path]:
    root = Path(shows_dir)
    if not root.exists():
        raise ValueError(f"Shows directory does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"Shows path is not a directory: {root}")

    index: Dict[str, Path] = {}
    collisions = {}

    for path in sorted(root.rglob("*.qxw")):
        key = normalize_show_stem(path.stem)
        if not key:
            continue
        if key in index:
            collisions.setdefault(key, [index[key]])
            collisions[key].append(path)
            continue
        index[key] = path

    if collisions:
        key, paths = sorted(collisions.items(), key=lambda item: item[0])[0]
        rendered = ", ".join(str(p) for p in sorted(paths))
        raise ValueError(f"Ambiguous show stem {key!r}: {rendered}")

    return index


def match_show_for_media(media_name: str, show_index: Dict[str, Path]) -> Path:
    stem = _media_to_stem(media_name)
    key = normalize_show_stem(stem)
    if key in show_index:
        return show_index[key]
    raise ValueError(f"No .qxw show matched media {media_name!r} (normalized stem {key!r})")
