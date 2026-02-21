#!/usr/bin/env python3
"""Validate portability constraints for research-gated generators.

Scope:
- Any generator that calls require_research_brief(...) is treated as
  phrase/research workflow compliant and must also load venue focus positions
  through showlib.load_focus_position_tuples(...).
- Generators using phrase planner selection must build creative context via
  showlib.build_creative_context(...) and pass creative_directives into
  pick_phrase_technique(...) / pick_phrase_technique_candidates(...).
"""

from __future__ import annotations

from pathlib import Path
import re


def assert_condition(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def is_research_gated_generator(text: str) -> bool:
    return "require_research_brief(" in text


def uses_phrase_planner(text: str) -> bool:
    return "pick_phrase_technique(" in text or "pick_phrase_technique_candidates(" in text


def validate_generator(path: Path, text: str) -> None:
    assert_condition(
        "venue_dir=VENUE_DIR" in text,
        f"{path}: require_research_brief should pass venue_dir=VENUE_DIR",
    )
    assert_condition(
        "load_focus_position_tuples(" in text,
        f"{path}: must use load_focus_position_tuples for venue-portable position mapping",
    )
    # Guard against reintroducing venue-specific absolute assumptions.
    assert_condition(
        "venue/home-studio" not in text,
        f"{path}: hardcoded venue path found; use VENUE_DIR/project_root resolution",
    )
    # POS should be loaded, not static literal assignment.
    assert_condition(
        re.search(r"^\s*POS\s*=\s*{", text, flags=re.MULTILINE) is None,
        f"{path}: static POS dict found; use load_focus_position_tuples",
    )
    if uses_phrase_planner(text):
        assert_condition(
            "build_creative_context(" in text,
            f"{path}: phrase planners must call build_creative_context from showlib",
        )
        assert_condition(
            "creative_directives=" in text,
            f"{path}: phrase planners must pass creative_directives into pick_phrase_technique",
        )
        assert_condition(
            "brand_tokens=" in text,
            f"{path}: phrase planners must pass brand_tokens into pick_phrase_technique",
        )


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    gen_dir = root / "venue"
    if not gen_dir.exists():
        print("No venue directory found.")
        return 1

    checked = 0
    for py_path in sorted(gen_dir.glob("*/generators/*.py")):
        text = py_path.read_text(encoding="utf-8")
        if not is_research_gated_generator(text):
            continue
        validate_generator(py_path, text)
        checked += 1

    if checked == 0:
        print("No research-gated generators found.")
        return 1

    print(f"Portability validation passed for {checked} research-gated generator(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
