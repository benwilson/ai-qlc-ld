#!/usr/bin/env python3
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from showlib import FIXTURE_DEFS, STAGE_POSITIONS, dark_sharpy, scene, write_workspace


WS_NS = {"w": "http://www.qlcplus.org/Workspace"}


def _single_fixture_defs(fixture_id: int) -> list[dict]:
    for fx in FIXTURE_DEFS:
        if fx["id"] == fixture_id:
            return [dict(fx)]
    raise AssertionError(f"Fixture ID {fixture_id} not found")


class ShowlibStageLayoutTests(unittest.TestCase):
    def test_write_workspace_uses_plot_positions_when_venue_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            venue = root / "venue" / "test-room"
            shows = venue / "shows"
            shows.mkdir(parents=True, exist_ok=True)

            (venue / "plot.md").write_text(
                "\n".join(
                    [
                        "# Test Room",
                        "",
                        "## Dimensions",
                        "",
                        "| | Meters |",
                        "|---|--------|",
                        "| Width (X) | 4.3 |",
                        "| Depth (Z) | 6.7 |",
                        "| Height (Y) | 4.9 |",
                        "",
                        "## Fixtures",
                        "",
                        "| Name | Type | X (m) | Y (m) | Z (m) | Orientation |",
                        "|------|------|--------|--------|--------|-------------|",
                        "| Back Left Sharpy | Sharpy Knockoff | 0.5 | 1.5 | 0.3 | Aimed at floor center |",
                    ]
                ),
                encoding="utf-8",
            )

            output = shows / "Fixture-Test.qxw"
            write_workspace(
                str(output),
                [scene("BLACKOUT", dark_sharpy())],
                [],
                fixture_defs=_single_fixture_defs(8),
            )

            workspace = ET.parse(output).getroot()
            grid = workspace.find("w:Monitor/w:Grid", WS_NS)
            self.assertIsNotNone(grid)
            self.assertEqual(grid.attrib.get("Width"), "5")
            self.assertEqual(grid.attrib.get("Height"), "5")
            self.assertEqual(grid.attrib.get("Depth"), "7")

            items = {
                int(node.attrib["ID"]): (
                    node.attrib["XPos"],
                    node.attrib["YPos"],
                    node.attrib["ZPos"],
                )
                for node in workspace.findall("w:Monitor/w:FxItem", WS_NS)
            }
            self.assertIn(8, items)
            self.assertEqual(items[8], ("3800", "1500", "300"))

    def test_write_workspace_falls_back_to_default_stage_positions(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "fallback.qxw"
            write_workspace(
                str(output),
                [scene("BLACKOUT", dark_sharpy())],
                [],
                fixture_defs=_single_fixture_defs(8),
            )

            workspace = ET.parse(output).getroot()
            grid = workspace.find("w:Monitor/w:Grid", WS_NS)
            self.assertIsNotNone(grid)
            self.assertEqual(grid.attrib.get("Width"), "5")
            self.assertEqual(grid.attrib.get("Height"), "3")
            self.assertEqual(grid.attrib.get("Depth"), "5")

            expected = next((x, y, z) for fid, x, y, z in STAGE_POSITIONS if fid == 8)
            items = {
                int(node.attrib["ID"]): (
                    node.attrib["XPos"],
                    node.attrib["YPos"],
                    node.attrib["ZPos"],
                )
                for node in workspace.findall("w:Monitor/w:FxItem", WS_NS)
            }
            self.assertEqual(items[8], expected)


if __name__ == "__main__":
    unittest.main()
