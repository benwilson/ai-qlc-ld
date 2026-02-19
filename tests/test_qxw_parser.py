#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

from qlc_runtime.model import ChaserFunction, SceneFunction
from qlc_runtime.parser import parse_workspace
from tests.qxw_samples import write_sample_qxw


class QxwParserTests(unittest.TestCase):
    def test_parse_workspace_extracts_core_runtime_data(self):
        with tempfile.TemporaryDirectory() as td:
            qxw = Path(td) / "sample.qxw"
            write_sample_qxw(qxw)
            ws = parse_workspace(str(qxw))

        self.assertEqual(ws.artnet_ip, "127.0.0.1")
        self.assertEqual(ws.artnet_universe, 0)
        self.assertIn(1, ws.fixtures)
        self.assertIn(0, ws.functions)
        self.assertIn(2, ws.functions)
        self.assertEqual(len(ws.buttons), 1)
        self.assertEqual(ws.buttons[0].caption, "FULL SHOW")

        self.assertIsInstance(ws.functions[0], SceneFunction)
        scene = ws.functions[0]
        self.assertEqual(scene.fixture_values[1][0], 0)
        self.assertEqual(scene.fixture_values[1][1], 0)
        self.assertEqual(scene.fixture_values[1][2], 0)

        self.assertIsInstance(ws.functions[2], ChaserFunction)
        chaser = ws.functions[2]
        self.assertEqual(chaser.run_order, "Loop")
        self.assertEqual(chaser.speed_modes.fade_in, "PerStep")
        self.assertEqual(chaser.speed_modes.duration, "PerStep")
        self.assertEqual(len(chaser.steps), 2)
        self.assertEqual(chaser.steps[1].function_id, 1)
        self.assertEqual(chaser.steps[1].hold, 25)


if __name__ == "__main__":
    unittest.main()

