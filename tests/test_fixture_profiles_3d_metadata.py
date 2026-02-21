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
        self.assertEqual(_head_channels(missyee_mode), [1, 2, 3])

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


if __name__ == "__main__":
    unittest.main()
