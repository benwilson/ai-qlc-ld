#!/usr/bin/env python3
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from showlib import FIXTURE_DEFS


NS = {"q": "http://www.qlcplus.org/FixtureDefinition"}
FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"
MODEL_TO_FILE = {
    "Beam Spot Wash 3 in 1": "Generic - Beam Spot Wash 3 in 1.qxf",
    "4BAR": "Chauvet-4BAR.qxf",
    "Nausea Inducer 3000": "Generic - Nausea Inducer 3000.qxf",
    "Profile Knockoff": "Generic - Profile Knockoff.qxf",
    "36 RGB LED": "Missyee - 36 RGB LED.qxf",
    "Sharpy Knockoff": "Generic - Sharpy Knockoff.qxf",
}


def _load_fixture_root(model_name: str) -> ET.Element:
    fixture_file = FIXTURES_DIR / MODEL_TO_FILE[model_name]
    return ET.parse(fixture_file).getroot()


def _find_mode(root: ET.Element, mode_name: str) -> ET.Element:
    for mode in root.findall("q:Mode", NS):
        if mode.attrib.get("Name") == mode_name:
            return mode
    raise AssertionError(f"Missing mode {mode_name!r}")


def _head_channels(mode: ET.Element) -> list[int]:
    head = mode.find("q:Head", NS)
    if head is None:
        return []
    return [int(ch.text.strip()) for ch in head.findall("q:Channel", NS)]


def _all_head_channels(mode: ET.Element) -> list[list[int]]:
    return [
        [int(ch.text.strip()) for ch in head.findall("q:Channel", NS)]
        for head in mode.findall("q:Head", NS)
    ]


class FixtureProfiles3DMetadataTests(unittest.TestCase):
    def test_active_modes_have_head_definitions(self):
        for fx in FIXTURE_DEFS:
            root = _load_fixture_root(fx["model"])
            mode = _find_mode(root, fx["mode"])
            head = mode.find("q:Head", NS)
            self.assertIsNotNone(
                head,
                msg=f"Model {fx['model']} mode {fx['mode']} is missing <Head>",
            )

    def test_bsw_heads_match_expected_for_active_modes(self):
        root = _load_fixture_root("Beam Spot Wash 3 in 1")
        mode_17 = _find_mode(root, "17 channel")
        mode_20 = _find_mode(root, "20 channel")

        self.assertEqual(
            _head_channels(mode_17),
            [0, 1, 6, 7, 8, 10, 11, 13, 14, 15],
        )
        self.assertEqual(
            _head_channels(mode_20),
            [0, 1, 2, 3, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18],
        )

    def test_mover_pan_tilt_ranges_are_nonzero_for_rendering(self):
        expected = {
            "Beam Spot Wash 3 in 1": ("540", "270"),
            "Sharpy Knockoff": ("540", "270"),
            "Profile Knockoff": ("540", "270"),
            "Nausea Inducer 3000": ("540", "0"),
        }
        for model_name, (pan_max, tilt_max) in expected.items():
            root = _load_fixture_root(model_name)
            focus = root.find("q:Physical/q:Focus", NS)
            self.assertIsNotNone(focus, msg=f"{model_name} missing Physical/Focus")
            self.assertEqual(focus.attrib.get("PanMax"), pan_max)
            self.assertEqual(focus.attrib.get("TiltMax"), tilt_max)

    def test_all_fixture_physical_sections_have_nonzero_lumens(self):
        for model_name in MODEL_TO_FILE:
            root = _load_fixture_root(model_name)
            bulb = root.find("q:Physical/q:Bulb", NS)
            self.assertIsNotNone(bulb, msg=f"{model_name} missing Physical/Bulb")
            lumens = int(bulb.attrib.get("Lumens", "0"))
            self.assertGreater(
                lumens,
                0,
                msg=f"{model_name} should provide nonzero lumens for 3D rendering",
            )

    def test_specific_head_channel_sets(self):
        sharpy_root = _load_fixture_root("Sharpy Knockoff")
        sharpy_mode = _find_mode(sharpy_root, "18 channel")
        self.assertEqual(
            _head_channels(sharpy_mode),
            [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 15, 16],
        )

        profile_root = _load_fixture_root("Profile Knockoff")
        profile_mode = _find_mode(profile_root, "14 channel")
        self.assertEqual(
            _head_channels(profile_mode),
            [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12],
        )

        ni3k_root = _load_fixture_root("Nausea Inducer 3000")
        ni3k_mode = _find_mode(ni3k_root, "19 channel")
        self.assertEqual(
            _head_channels(ni3k_mode),
            [0, 5, 6, 7, 8, 9, 10, 14, 15, 16, 17],
        )

        missyee_root = _load_fixture_root("36 RGB LED")
        missyee_mode = _find_mode(missyee_root, "7 channel")
        self.assertEqual(_head_channels(missyee_mode), [0, 1, 2, 3, 4])

        bar_root = _load_fixture_root("4BAR")
        bar_mode = _find_mode(bar_root, "15 Channel")
        self.assertEqual(
            _all_head_channels(bar_mode),
            [
                [1, 2, 3, 4, 5],
                [1, 2, 6, 7, 8],
                [1, 2, 9, 10, 11],
                [1, 2, 12, 13, 14],
            ],
        )

    def test_profile_strobe_is_open_at_zero(self):
        root = _load_fixture_root("Profile Knockoff")
        strobe = None
        for channel in root.findall("q:Channel", NS):
            if channel.attrib.get("Name") == "Strobe":
                strobe = channel
                break
        self.assertIsNotNone(strobe, msg="Profile strobe channel not found")
        self.assertNotIn("Preset", strobe.attrib)

        caps = strobe.findall("q:Capability", NS)
        self.assertEqual(len(caps), 2)
        self.assertEqual(caps[0].attrib.get("Min"), "0")
        self.assertEqual(caps[0].attrib.get("Max"), "0")
        self.assertEqual(caps[0].attrib.get("Preset"), "ShutterOpen")
        self.assertEqual(caps[1].attrib.get("Min"), "1")
        self.assertEqual(caps[1].attrib.get("Max"), "255")
        self.assertEqual(caps[1].attrib.get("Preset"), "StrobeSlowToFast")

    def test_par_strobes_have_explicit_open_at_zero(self):
        fixtures_and_channels = [
            ("4BAR", "Strobe"),
            ("36 RGB LED", "Strobe"),
        ]
        for model_name, channel_name in fixtures_and_channels:
            root = _load_fixture_root(model_name)
            channel = None
            for candidate in root.findall("q:Channel", NS):
                if candidate.attrib.get("Name") == channel_name:
                    channel = candidate
                    break
            self.assertIsNotNone(channel, msg=f"{model_name} missing {channel_name}")
            caps = channel.findall("q:Capability", NS)
            self.assertGreaterEqual(len(caps), 1, msg=f"{model_name} {channel_name} missing capabilities")
            first = caps[0]
            self.assertEqual(first.attrib.get("Min"), "0")
            self.assertEqual(first.attrib.get("Max"), "0")
            self.assertEqual(first.attrib.get("Preset"), "ShutterOpen")

    def test_bsw_active_color_slots_are_resolved_for_3d(self):
        root = _load_fixture_root("Beam Spot Wash 3 in 1")
        color = None
        for channel in root.findall("q:Channel", NS):
            if channel.attrib.get("Name") == "Color":
                color = channel
                break
        self.assertIsNotNone(color, msg="BSW color channel not found")

        expected_caps = {
            ("19", "21"): ("ColorMacro", "#ff0000"),
            ("43", "45"): ("ColorMacro", "#0000ff"),
        }
        seen = {}
        for cap in color.findall("q:Capability", NS):
            key = (cap.attrib.get("Min"), cap.attrib.get("Max"))
            if key in expected_caps:
                seen[key] = (cap.attrib.get("Preset"), cap.attrib.get("Res1"))
        self.assertEqual(
            seen,
            expected_caps,
            msg="BSW red/blue wheel slots should resolve to explicit colors in 3D",
        )


if __name__ == "__main__":
    unittest.main()
