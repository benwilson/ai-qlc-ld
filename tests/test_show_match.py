#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

from qlc_runtime.show_match import (
    index_shows,
    match_show_for_media,
    normalize_show_stem,
)


class ShowMatchTests(unittest.TestCase):
    def test_normalize_show_stem_collapses_whitespace_and_case(self):
        self.assertEqual(normalize_show_stem("  My   SHOW  "), "my show")

    def test_index_and_match_exact_stem(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            show_path = root / "Track Name.qxw"
            show_path.write_text("<Workspace/>")

            index = index_shows(root)
            matched = match_show_for_media("Track Name.mp3", index)
            self.assertEqual(matched, show_path)

    def test_match_missing_raises(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "Existing.qxw").write_text("<Workspace/>")
            index = index_shows(root)
            with self.assertRaises(ValueError):
                match_show_for_media("Missing Song.flac", index)

    def test_duplicate_stems_raise(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "dup.qxw").write_text("<Workspace/>")
            nested = root / "nested"
            nested.mkdir()
            (nested / "Dup.qxw").write_text("<Workspace/>")
            with self.assertRaises(ValueError):
                index_shows(root)


if __name__ == "__main__":
    unittest.main()
