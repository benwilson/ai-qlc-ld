#!/usr/bin/env python3
import unittest

from qlc_runtime.engine import COMPLETED, run_function
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


def _seek_workspace(run_order: str, fades_holds):
    fixtures = {1: FixtureDef(id=1, universe=0, address=0, channels=1, name="fx")}
    scenes = {
        10: SceneFunction(id=10, name="S0", path="Show", fixture_values={1: {0: 0}}),
        11: SceneFunction(id=11, name="S1", path="Show", fixture_values={1: {0: 255}}),
        12: SceneFunction(id=12, name="S2", path="Show", fixture_values={1: {0: 128}}),
    }
    steps = []
    scene_ids = [10, 11, 12]
    for idx, (fade, hold) in enumerate(fades_holds):
        steps.append(
            ChaserStep(
                number=idx,
                function_id=scene_ids[idx],
                fade_in=fade,
                hold=hold,
                fade_out=0,
            )
        )
    chaser = ChaserFunction(
        id=20,
        name="Main",
        path="Show",
        run_order=run_order,
        speed_fade_in=0,
        speed_fade_out=0,
        speed_duration=0,
        speed_modes=SpeedModes(fade_in="PerStep", fade_out="Common", duration="PerStep"),
        steps=steps,
    )
    functions = dict(scenes)
    functions[20] = chaser
    return WorkspaceModel(fixtures=fixtures, functions=functions, buttons=[])


class EngineSeekTests(unittest.TestCase):
    def test_loop_seek_into_hold_starts_on_expected_step(self):
        ws = _seek_workspace(
            run_order="Loop",
            fades_holds=[(0, 100), (0, 100)],
        )
        sender = _FakeSender()

        result = run_function(
            workspace=ws,
            function_id=20,
            universe=0,
            sender=sender,
            fps=200,
            max_seconds=0.03,
            start_offset_ms=150,
        )

        self.assertEqual(result.reason, "timeout")
        self.assertTrue(sender.frames, "expected at least one frame")
        self.assertEqual(sender.frames[0][0], 255)

    def test_pingpong_seek_picks_bounce_step(self):
        ws = _seek_workspace(
            run_order="PingPong",
            fades_holds=[(0, 100), (0, 100), (0, 100)],
        )
        sender = _FakeSender()
        seen_steps = []

        def on_step(step_idx, _fade, _hold, _count, _name):
            if not seen_steps:
                seen_steps.append(step_idx)

        run_function(
            workspace=ws,
            function_id=20,
            universe=0,
            sender=sender,
            fps=200,
            max_seconds=0.03,
            start_offset_ms=350,
            on_step=on_step,
        )

        self.assertEqual(seen_steps, [1])

    def test_singleshot_seek_past_end_is_completed(self):
        ws = _seek_workspace(
            run_order="SingleShot",
            fades_holds=[(0, 100), (0, 100)],
        )
        sender = _FakeSender()

        result = run_function(
            workspace=ws,
            function_id=20,
            universe=0,
            sender=sender,
            fps=200,
            start_offset_ms=300,
        )

        self.assertEqual(result.reason, COMPLETED)
        self.assertEqual(len(sender.frames), 0)


if __name__ == "__main__":
    unittest.main()
