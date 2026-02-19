#!/usr/bin/env python3
import time
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

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


def _normalize_run_order(run_order: str) -> str:
    run_order_cf = (run_order or "SingleShot").casefold()
    if run_order_cf in {"singleshot", "loop", "pingpong"}:
        return run_order_cf
    return "singleshot"


def _build_step_order(run_order: str, step_count: int) -> Tuple[List[int], bool]:
    if step_count <= 0:
        return [], False
    if run_order == "loop":
        return list(range(step_count)), True
    if run_order == "pingpong":
        if step_count == 1:
            return [0], True
        return list(range(step_count)) + list(range(step_count - 2, 0, -1)), True
    return list(range(step_count)), False


@dataclass
class _ChaserStartState:
    completed: bool
    current: bytes
    order_pos: int
    fade_offset_ms: int
    hold_offset_ms: int


def _resolve_chaser_start(
    workspace: WorkspaceModel,
    chaser: ChaserFunction,
    universe: int,
    step_order: List[int],
    repeats: bool,
    start_offset_ms: int,
) -> _ChaserStartState:
    if not step_order:
        return _ChaserStartState(
            completed=True,
            current=make_blackout_frame(),
            order_pos=0,
            fade_offset_ms=0,
            hold_offset_ms=0,
        )

    current = make_blackout_frame()
    if start_offset_ms <= 0:
        return _ChaserStartState(
            completed=False,
            current=current,
            order_pos=0,
            fade_offset_ms=0,
            hold_offset_ms=0,
        )

    offset_left = max(0, int(start_offset_ms))
    order_pos = 0
    stale_steps = 0

    while offset_left > 0:
        step_idx = step_order[order_pos]
        step = chaser.steps[step_idx]
        scene_fn = workspace.functions.get(step.function_id)
        if not isinstance(scene_fn, SceneFunction):
            raise ValueError(
                f"Chaser {chaser.id} step {step.number} targets unsupported function ID "
                f"{step.function_id}"
            )

        start_frame = current
        target = apply_scene_to_frame(start_frame, scene_fn, workspace, universe)
        fade_ms, hold_ms, _fade_out_ms = resolve_step_timing(chaser, step)
        step_ms = fade_ms + hold_ms

        if step_ms <= 0:
            current = target
            if not repeats and order_pos >= len(step_order) - 1:
                return _ChaserStartState(
                    completed=True,
                    current=current,
                    order_pos=order_pos,
                    fade_offset_ms=0,
                    hold_offset_ms=0,
                )
            order_pos = (order_pos + 1) % len(step_order) if repeats else order_pos + 1
            stale_steps += 1
            if repeats and stale_steps >= len(step_order):
                return _ChaserStartState(
                    completed=False,
                    current=current,
                    order_pos=order_pos,
                    fade_offset_ms=0,
                    hold_offset_ms=0,
                )
            continue

        stale_steps = 0

        if offset_left >= step_ms:
            offset_left -= step_ms
            current = target
            if not repeats and order_pos >= len(step_order) - 1:
                return _ChaserStartState(
                    completed=True,
                    current=current,
                    order_pos=order_pos,
                    fade_offset_ms=0,
                    hold_offset_ms=0,
                )
            order_pos = (order_pos + 1) % len(step_order) if repeats else order_pos + 1
            continue

        if offset_left < fade_ms and fade_ms > 0:
            alpha = float(offset_left) / float(fade_ms)
            current = interpolate_frame(start_frame, target, alpha)
            return _ChaserStartState(
                completed=False,
                current=current,
                order_pos=order_pos,
                fade_offset_ms=int(offset_left),
                hold_offset_ms=0,
            )

        current = target
        hold_offset = max(0, int(offset_left - fade_ms))
        return _ChaserStartState(
            completed=False,
            current=current,
            order_pos=order_pos,
            fade_offset_ms=fade_ms,
            hold_offset_ms=hold_offset,
        )

    return _ChaserStartState(
        completed=False,
        current=current,
        order_pos=order_pos,
        fade_offset_ms=0,
        hold_offset_ms=0,
    )


def run_function(
    workspace: WorkspaceModel,
    function_id: int,
    universe: int,
    sender,
    fps: int = 40,
    max_seconds: Optional[float] = None,
    should_stop: Optional[Callable[[], bool]] = None,
    on_step: Optional[Callable[[int, int, int, int, str], None]] = None,
    start_offset_ms: int = 0,
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

    run_order = _normalize_run_order(fn.run_order)
    step_order, repeats = _build_step_order(run_order, len(fn.steps))
    if not step_order:
        raise ValueError(f"Chaser {fn.id} has no runnable steps")

    start_state = _resolve_chaser_start(
        workspace=workspace,
        chaser=fn,
        universe=universe,
        step_order=step_order,
        repeats=repeats,
        start_offset_ms=start_offset_ms,
    )
    if start_state.completed:
        return RunResult(reason=COMPLETED, last_frame=start_state.current, steps_executed=0)

    current = start_state.current
    order_pos = start_state.order_pos
    fade_offset_ms = start_state.fade_offset_ms
    hold_offset_ms = start_state.hold_offset_ms
    steps_executed = 0

    while True:
        reason = stop_reason()
        if reason is not None:
            return RunResult(reason=reason, last_frame=current, steps_executed=steps_executed)

        step_idx = step_order[order_pos]
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

        remaining_fade_ms = max(0, fade_ms - fade_offset_ms)
        if remaining_fade_ms > 0:
            reason = run_phase(current, target, remaining_fade_ms, interpolate=True)
            if reason is not None:
                return RunResult(reason=reason, last_frame=current, steps_executed=steps_executed)
            current = target
        else:
            current = target

        remaining_hold_ms = max(0, hold_ms - hold_offset_ms)
        if remaining_hold_ms > 0:
            reason = run_phase(current, current, remaining_hold_ms, interpolate=False)
            if reason is not None:
                return RunResult(reason=reason, last_frame=current, steps_executed=steps_executed)

        steps_executed += 1
        fade_offset_ms = 0
        hold_offset_ms = 0

        if not repeats and order_pos >= len(step_order) - 1:
            return RunResult(reason=COMPLETED, last_frame=current, steps_executed=steps_executed)
        order_pos = (order_pos + 1) % len(step_order) if repeats else order_pos + 1
