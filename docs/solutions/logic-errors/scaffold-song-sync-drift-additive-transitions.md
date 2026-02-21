---
title: "Scaffold Generator Song-Sync Drift from Additive Transitions"
date: 2026-02-20
category: logic-errors
severity: moderate
component: show-generator-scaffold
tags:
  - timing
  - transitions
  - scaffold
  - song-sync
  - qlc-plus
  - code-review
symptoms:
  - "Chaser total duration overran audio by +19-34 seconds"
  - "Freeze-style transitions degraded to generic dim/black behavior"
root_cause: "Transition scenes were appended as additive chaser steps without borrowing time from adjacent sections"
resolution: "Offset section start time by transition duration; pass last_scene to freeze transitions; reduce final blackout"
files_modified:
  - scripts/show_workflow.py
---

# Scaffold Generator Song-Sync Drift from Additive Transitions

## Problem

After upgrading `_generator_template()` in `scripts/show_workflow.py` from a 2-scene stub to a full phrase-aware template, a Codex code review identified that generated shows overran audio duration by +19-34 seconds. This broke the "song-synced" expectation where the chaser should complete in approximately the same time as the track.

A secondary issue: freeze-style transitions (freeze_decay, freeze_burst, freeze_hold) degraded to generic dim/black instead of holding the prior look.

## Investigation

The timing simulation across 10 real `songs-data` files showed consistent overrun. Two compounding causes:

1. **Additive transitions**: `plan_segment_transition()` + `build_transition_scenes()` inserted extra chaser steps between sections. Each transition adds 1-4 beats. With ~14 segment boundaries at ~1s average = ~14s of additive time.
2. **Fixed final blackout**: `hold(BPM, 2)` appended a 2-bar hold (~3.8s at 125 BPM) unconditionally.
3. **Missing `last_scene`**: `build_transition_scenes()` was called without the `last_scene` parameter, so freeze factories couldn't hold/decay the prior look.

## Root Cause

Transitions were purely additive — they didn't borrow time from adjacent sections. The section builders used analysis timestamps (`sec["start"]` to `sec["end"]`) to generate steps, and transition steps were inserted on top of that. Total chaser duration = section durations + transition durations + final blackout, which always exceeded song duration.

## Solution

### Fix 1: Transitions borrow time from next section

Track transition duration and offset the next section's start time forward:

```python
trans_offset_s = 0.0
for ts, tt in zip(t_scenes, t_timing):
    idx = len(scenes)
    scenes.append(ts)
    steps.append((idx, tt))
    trans_offset_s += (tt[0] + tt[1]) / 1000.0

# Offset section start so transitions borrow time, not add it
build_sec = sec
if trans_offset_s > 0:
    build_sec = {**sec, "start": sec["start"] + trans_offset_s}

# Dispatch builder with adjusted section
build_high(build_sec)  # fewer steps = compensates for transition time
```

The section builder starts later and produces fewer steps, exactly compensating for the transition's duration. Per-step energy lookups remain accurate because they use the actual time window of each step.

### Fix 2: Reduce final blackout

```python
# Before: 2-bar hold (~3.8s at 125 BPM)
steps.append((0, hold(BPM, 2)))

# After: short snap (~1s)
steps.append((0, snap(BPM, 0.5, fade_ms=100)))
```

### Fix 3: Track and pass last_scene

```python
last_scene_dict = None

for i, sec in enumerate(SECTIONS):
    # ... transitions use last_scene_dict ...
    t_scenes, t_timing = build_transition_scenes(
        trans, BPM, pos_tuples=POS, palette=ACCENT_COLOR,
        last_scene=last_scene_dict,
    )

    # ... build section ...

    # Capture last scene for next iteration's transitions
    if steps:
        last_scene_dict = scenes[steps[-1][0]]
```

### Result

Duration drift reduced from +9.3% (250.3s) to +2.6% (234.9s) for a 229s target. The remaining ~6s comes from `max(1, ...)` bar rounding on very short segments.

## Not Fixed (Intentional)

**Hard-indexing analysis data** (`data["energy"]["sub_bass"]` instead of `.get()`): All 14 existing generators use this pattern. The analysis pipeline guarantees complete schema. Silent degradation to empty arrays would produce generators that run but generate garbage (zero energy = phrase classification fails silently). Fail-loud is correct here.

## Prevention

1. **Time accounting rule**: Transitions between fixed-time sections must borrow time, not add it. Track `trans_offset_s` and offset the next section's start.

2. **Duration assertion**: After computing total_ms, compare to target:
   ```python
   target_ms = beats[-1] * 1000
   drift_pct = abs(total_ms - target_ms) / target_ms
   if drift_pct > 0.05:
       print(f"WARNING: Duration drift {drift_pct:.1%} exceeds 5% threshold")
   ```

3. **Optional parameter audit**: When calling functions with optional kwargs that affect behavior (`last_scene`, `palette`, etc.), verify whether omitting them degrades functionality silently. Freeze transitions without `last_scene` degrade to black — no error, just wrong output.

4. **Template testing**: Scaffold templates that generate code should be tested by running the generated code against real data, not just checking syntax validity.

## Related

- [Scene-Timing Count Mismatch](./scene-timing-count-mismatch-showlib-20260220.md) — related transition contract: `len(scenes) == len(timing)`
- `.claude/CLAUDE.md` "Transition Scene Contract" section — documents the `make_chaser()` assertion
- `docs/plans/2026-02-20-feat-dramatic-transitions-and-beat-sync-plan.md` — feature plan for the 21 transition types
