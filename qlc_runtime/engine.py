#!/usr/bin/env python3
import time
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from qlc_runtime.model import (
    ChaserFunction,
    ChaserStep,
    SceneFunction,
    WorkspaceModel,
)


STOPPED = "stopped"
TIMEOUT = "timeout"
COMPLETED = "completed"


@dataclass
class RunResult:
    reason: str
    last_frame: bytes
    steps_executed: int = 0


def make_blackout_frame() -> bytes:
    return bytes(512)


def interpolate_frame(start: bytes, end: bytes, alpha: float) -> bytes:
    alpha = max(0.0, min(1.0, float(alpha)))
    out = bytearray(512)
    for i in range(512):
        out[i] = int(round(start[i] + (end[i] - start[i]) * alpha))
    return bytes(out)


def apply_scene_to_frame(
    frame: bytes,
    scene: SceneFunction,
    workspace: WorkspaceModel,
    universe: int,
) -> bytes:
    out = bytearray(frame)
    for fixture_id, ch_map in scene.fixture_values.items():
        fixture = workspace.fixtures.get(fixture_id)
        if fixture is None or fixture.universe != universe:
            continue
        for channel, value in ch_map.items():
            abs_channel = fixture.address + channel
            if 0 <= abs_channel < 512:
                out[abs_channel] = max(0, min(255, int(value)))
    return bytes(out)


def _is_per_step(mode: str) -> bool:
    return str(mode or "").casefold() == "perstep"


def resolve_step_timing(chaser: ChaserFunction, step: ChaserStep) -> Tuple[int, int, int]:
    fade_in = step.fade_in if _is_per_step(chaser.speed_modes.fade_in) else chaser.speed_fade_in
    hold = step.hold if _is_per_step(chaser.speed_modes.duration) else chaser.speed_duration
    fade_out = step.fade_out if _is_per_step(chaser.speed_modes.fade_out) else chaser.speed_fade_out
    return max(0, int(fade_in)), max(0, int(hold)), max(0, int(fade_out))


def run_function(
    workspace: WorkspaceModel,
    function_id: int,
    universe: int,
    sender,
    fps: int = 40,
    max_seconds: Optional[float] = None,
    should_stop: Optional[Callable[[], bool]] = None,
    on_step: Optional[Callable[[int, int, int, int, str], None]] = None,
) -> RunResult:
    if fps <= 0:
        raise ValueError("fps must be > 0")
    fn = workspace.functions.get(function_id)
    if fn is None:
        raise ValueError(f"Function ID {function_id} not found")

    tick_s = 1.0 / float(fps)
    start_time = time.monotonic()
    current = make_blackout_frame()

    def stop_reason() -> Optional[str]:
        if should_stop is not None and should_stop():
            return STOPPED
        if max_seconds is not None and (time.monotonic() - start_time) >= max_seconds:
            return TIMEOUT
        return None

    def run_phase(
        start_frame: bytes,
        end_frame: bytes,
        duration_ms: int,
        interpolate: bool,
    ) -> Optional[str]:
        phase_s = max(0.0, duration_ms / 1000.0)
        phase_start = time.monotonic()
        next_tick = phase_start

        while True:
            reason = stop_reason()
            if reason is not None:
                return reason
            now = time.monotonic()
            elapsed = now - phase_start
            if elapsed >= phase_s:
                break
            if now < next_tick:
                time.sleep(max(0.0, next_tick - now))
                continue

            if interpolate and phase_s > 0:
                frame = interpolate_frame(start_frame, end_frame, elapsed / phase_s)
            else:
                frame = end_frame
            sender.send(frame)
            next_tick += tick_s
            if next_tick < now - (tick_s * 2):
                next_tick = now + tick_s

        sender.send(end_frame)
        return None

    if isinstance(fn, SceneFunction):
        target = apply_scene_to_frame(current, fn, workspace, universe)
        if on_step is not None:
            on_step(0, 0, 0, 0, fn.name)
        while True:
            reason = stop_reason()
            if reason is not None:
                return RunResult(reason=reason, last_frame=target, steps_executed=1)
            sender.send(target)
            time.sleep(tick_s)

    if not isinstance(fn, ChaserFunction):
        raise ValueError(
            f"Unsupported function type for execution: {type(fn).__name__} (ID {function_id})"
        )

    if not fn.steps:
        raise ValueError(f"Chaser {fn.id} has no steps")

    run_order = (fn.run_order or "SingleShot").casefold()
    step_idx = 0
    direction = 1
    steps_executed = 0

    while True:
        reason = stop_reason()
        if reason is not None:
            return RunResult(reason=reason, last_frame=current, steps_executed=steps_executed)

        step = fn.steps[step_idx]
        scene_fn = workspace.functions.get(step.function_id)
        if not isinstance(scene_fn, SceneFunction):
            raise ValueError(
                f"Chaser {fn.id} step {step.number} targets unsupported function ID "
                f"{step.function_id}"
            )

        fade_ms, hold_ms, _fade_out_ms = resolve_step_timing(fn, step)
        if on_step is not None:
            on_step(step_idx, fade_ms, hold_ms, steps_executed, scene_fn.name)

        target = apply_scene_to_frame(current, scene_fn, workspace, universe)
        reason = run_phase(current, target, fade_ms, interpolate=True)
        if reason is not None:
            return RunResult(reason=reason, last_frame=current, steps_executed=steps_executed)
        current = target

        if hold_ms > 0:
            reason = run_phase(current, current, hold_ms, interpolate=False)
            if reason is not None:
                return RunResult(reason=reason, last_frame=current, steps_executed=steps_executed)

        steps_executed += 1

        if run_order == "singleshot":
            if step_idx >= len(fn.steps) - 1:
                return RunResult(reason=COMPLETED, last_frame=current, steps_executed=steps_executed)
            step_idx += 1
        elif run_order == "loop":
            step_idx = (step_idx + 1) % len(fn.steps)
        elif run_order == "pingpong":
            if len(fn.steps) == 1:
                step_idx = 0
            elif direction == 1 and step_idx == len(fn.steps) - 1:
                direction = -1
                step_idx -= 1
            elif direction == -1 and step_idx == 0:
                direction = 1
                step_idx += 1
            else:
                step_idx += direction
        else:
            # Unknown run order: behave like SingleShot for safety.
            if step_idx >= len(fn.steps) - 1:
                return RunResult(reason=COMPLETED, last_frame=current, steps_executed=steps_executed)
            step_idx += 1

