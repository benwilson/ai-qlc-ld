#!/usr/bin/env python3
import unittest
from threading import Event

from qlc_runtime.engine import apply_scene_to_frame, interpolate_frame, run_function
from qlc_runtime.model import (
    ChaserFunction,
    ChaserStep,
    FixtureDef,
    SceneFunction,
    SpeedModes,
    WorkspaceModel,
)


class _FakeSender:
    def __init__(self):
        self.frames = []

    def send(self, frame: bytes):
        self.frames.append(bytes(frame))


def _workspace_for_engine_tests(run_order: str = "SingleShot") -> WorkspaceModel:
    fixtures = {1: FixtureDef(id=1, universe=0, address=0, channels=1, name="fx")}
    scene0 = SceneFunction(id=10, name="S0", path="Show", fixture_values={1: {0: 0}})
    scene1 = SceneFunction(id=11, name="S1", path="Show", fixture_values={1: {0: 255}})
    scene2 = SceneFunction(id=12, name="S2", path="Show", fixture_values={1: {0: 128}})
    chaser = ChaserFunction(
        id=20,
        name="Main",
        path="Show",
        run_order=run_order,
        speed_fade_in=0,
        speed_fade_out=0,
        speed_duration=0,
        speed_modes=SpeedModes(fade_in="PerStep", fade_out="Common", duration="PerStep"),
        steps=[
            ChaserStep(number=0, function_id=10, fade_in=20, hold=10),
            ChaserStep(number=1, function_id=11, fade_in=20, hold=10),
            ChaserStep(number=2, function_id=12, fade_in=20, hold=10),
        ],
    )
    functions = {
        10: scene0,
        11: scene1,
        12: scene2,
        20: chaser,
    }
    return WorkspaceModel(fixtures=fixtures, functions=functions, buttons=[])


class EngineTimingTests(unittest.TestCase):
    def test_interpolation_produces_mid_values(self):
        start = bytes([0] * 512)
        end = bytes([255] + [0] * 511)
        mid = interpolate_frame(start, end, 0.5)
        self.assertGreater(mid[0], 0)
        self.assertLess(mid[0], 255)

    def test_run_singleshot_chaser_completes(self):
        ws = _workspace_for_engine_tests(run_order="SingleShot")
        sender = _FakeSender()

        result = run_function(
            workspace=ws,
            function_id=20,
            universe=0,
            sender=sender,
            fps=200,
            max_seconds=1.0,
        )

        self.assertEqual(result.reason, "completed")
        self.assertGreaterEqual(result.steps_executed, 3)
        self.assertGreater(len(sender.frames), 3)
        # At least one in-between value should exist due to fade interpolation.
        values = {frame[0] for frame in sender.frames}
        self.assertTrue(any(0 < v < 255 for v in values))

    def test_pingpong_step_order(self):
        ws = _workspace_for_engine_tests(run_order="PingPong")
        sender = _FakeSender()
        stop = Event()
        seen = []

        def on_step(step_idx, _fade_ms, _hold_ms, _count, _scene_name):
            seen.append(step_idx)
            if len(seen) >= 5:
                stop.set()

        result = run_function(
            workspace=ws,
            function_id=20,
            universe=0,
            sender=sender,
            fps=200,
            max_seconds=1.0,
            should_stop=stop.is_set,
            on_step=on_step,
        )

        self.assertEqual(result.reason, "stopped")
        self.assertEqual(seen[:5], [0, 1, 2, 1, 0])


if __name__ == "__main__":
    unittest.main()

