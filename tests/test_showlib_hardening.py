#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

from showlib import (
    FIXTURE_DEFS,
    STAGE_POSITIONS,
    dark_bsw,
    dark_ni3k,
    dark_profile,
    dark_sharpy,
    generate_venue_template,
    hold,
    make_chaser,
    scene,
    write_workspace,
)


def _channel_map(fixture):
    _, channels = fixture
    return dict(channels)


class ShowlibHardeningTests(unittest.TestCase):
    def test_dark_helpers_respect_zero_position_values(self):
        self.assertEqual(_channel_map(dark_sharpy(pan=0, tilt=0))[0], 0)
        self.assertEqual(_channel_map(dark_sharpy(pan=0, tilt=0))[1], 0)

        self.assertEqual(_channel_map(dark_bsw(pan=0, tilt=0))[0], 0)
        self.assertEqual(_channel_map(dark_bsw(pan=0, tilt=0))[2], 0)

        self.assertEqual(_channel_map(dark_profile(pan=0, tilt=0))[2], 0)
        self.assertEqual(_channel_map(dark_profile(pan=0, tilt=0))[3], 0)

        self.assertEqual(_channel_map(dark_ni3k(pan=0))[0], 0)

    def test_write_workspace_escapes_special_xml_chars(self):
        scenes = [
            scene('A&B "Scene" <1>', dark_sharpy(), path='P&"Q"<r>')
        ]
        chasers = [
            make_chaser('Chaser & "One" <x>', [0], [hold(120, 1)], path='Path & "<c>"')
        ]
        vc_buttons = [
            {
                "caption": 'BTN & "<>"',
                "vc_id": 0,
                "func_id": 1,
                "x": 10,
                "y": 10,
                "w": 100,
                "h": 40,
                "color": "#22AA22",
                "action": "Toggle",
            }
        ]

        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "escaped.qxw"
            write_workspace(
                str(output),
                scenes,
                chasers,
                artnet_ip='10.0.0.7&unsafe"<tag>"',
                vc_buttons=vc_buttons,
            )
            xml = output.read_text()

        self.assertIn('UID="10.0.0.7&amp;unsafe&quot;&lt;tag&gt;&quot;"', xml)
        self.assertIn('Name="A&amp;B &quot;Scene&quot; &lt;1&gt;"', xml)
        self.assertIn('Path="P&amp;&quot;Q&quot;&lt;r&gt;"', xml)
        self.assertIn('Caption="BTN &amp; &quot;&lt;&gt;&quot;"', xml)

    def test_generate_venue_template_keeps_global_state_unchanged(self):
        original_defs = [dict(fx) for fx in FIXTURE_DEFS]
        original_positions = list(STAGE_POSITIONS)

        with tempfile.TemporaryDirectory() as td:
            venue_dir = Path(td)
            (venue_dir / "shows").mkdir(parents=True, exist_ok=True)
            (venue_dir / "plot.md").write_text(
                "\n".join(
                    [
                        "# Test Venue",
                        "",
                        "| Name | Type | X (m) | Y (m) | Z (m) | Orientation |",
                        "|------|------|-------|-------|-------|-------------|",
                        "| Test 4BAR | 4BAR | 2.1 | 1.4 | 0.2 | Facing audience |",
                    ]
                )
            )

            generate_venue_template(str(venue_dir), bpm=128)
            self.assertTrue((venue_dir / "shows" / "Template-Base.qxw").exists())

        self.assertEqual(original_defs, FIXTURE_DEFS)
        self.assertEqual(original_positions, STAGE_POSITIONS)


if __name__ == "__main__":
    unittest.main()
