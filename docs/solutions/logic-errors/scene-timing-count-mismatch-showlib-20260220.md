---
module: showlib
date: 2026-02-20
problem_type: logic_error
component: service_object
symptoms:
  - "make_chaser() assertion failure: len(scene_ids) != len(timing)"
  - "4 of 21 transition factory functions returned mismatched scene/timing counts"
  - "freeze_burst and freeze_hold returned 1 scene + 2 timing entries"
  - "slow_dissolve and chase_cancel returned 0 scenes + 1 timing entry"
root_cause: logic_error
resolution_type: code_fix
severity: high
tags: [make-chaser, scene-timing-contract, transition-factories, showlib]
---

# Troubleshooting: Transition Scene Factories Violate make_chaser() Contract

## Problem
When implementing 21 transition scene factory functions for `build_transition_scenes()`, 4 factories returned mismatched `(scenes, timing)` tuple lengths, violating `make_chaser()`'s assertion that `len(scene_ids) == len(timing)`.

## Environment
- Module: showlib.py (Python show generator library)
- Affected Component: `build_transition_scenes()` dispatcher and `_transition_*` factory functions
- Date: 2026-02-20

## Symptoms
- `freeze_burst`: returned 1 scene + 2 timing entries (extra "snap back" timing with no scene)
- `freeze_hold`: returned 1 scene + 2 timing entries (extra "hold" timing with no scene)
- `slow_dissolve`: returned 0 scenes + 1 timing entry (conceptually "just fade" with no concrete scene)
- `chase_cancel`: returned 0 scenes + 1 timing entry (conceptually "just stop" with no scene)

## What Didn't Work

**Attempted Solution 1:** Initial implementations modeled transitions conceptually rather than mechanically.
- **Why it failed:** `freeze_burst` was designed as "hold previous scene, then snap" — but the "hold" phase isn't a new scene, it's the previous scene naturally continuing. The factory tried to express this as 1 scene + 2 timing entries, which breaks the contract. Similarly, `slow_dissolve` was conceptualized as "just crossfade the existing scene down" with 0 scenes, but `make_chaser()` needs at least 1 scene per timing entry.

## Solution

Every factory must return `len(scenes) == len(timing)`. If a transition conceptually has a "hold" or "fade" phase, materialize it as a concrete scene.

**Code changes:**

```python
# Before (broken) - freeze_burst: 1 scene + 2 timing
def _transition_freeze_burst(bpm, dur, **kw):
    ms = _beat_ms(bpm, dur)
    hold_ms = ms // 2
    burst_ms = ms - hold_ms
    scenes = [scene("TR:freeze_burst", *blackout_all())]  # 1 scene
    timing = [(0, hold_ms), (0, burst_ms)]                 # 2 timing entries!
    return scenes, timing

# After (fixed) - freeze_burst: 1 scene + 1 timing
def _transition_freeze_burst(bpm, dur, **kw):
    ms = _beat_ms(bpm, dur)
    scenes = [scene("TR:freeze_burst", *blackout_all())]
    timing = [(0, ms)]  # The "freeze" is the previous scene holding naturally
    return scenes, timing
```

```python
# Before (broken) - slow_dissolve: 0 scenes + 1 timing
def _transition_slow_dissolve(bpm, dur, **kw):
    ms = _beat_ms(bpm, dur)
    scenes = []          # 0 scenes!
    timing = [(ms, 0)]   # 1 timing entry
    return scenes, timing

# After (fixed) - slow_dissolve: 1 scene + 1 timing
def _transition_slow_dissolve(bpm, dur, **kw):
    ms = _beat_ms(bpm, dur)
    scenes = [scene("TR:slow_dissolve",
                     fourbar_solid(*OFF), *miss_both(*OFF),
                     dark_sharpy(), dark_bsw(), dark_profile(), dark_ni3k())]
    timing = [(ms, 0)]  # Smooth crossfade INTO the dim scene
    return scenes, timing
```

## Why This Works

1. **Root cause:** `make_chaser()` builds a QLC+ `<Chaser>` where each `<Step>` references one scene ID and has its own FadeIn/Hold timing. The assertion `len(scene_ids) == len(timing)` is fundamental — every timing entry needs a scene to transition to/from.

2. **The fix:** Rather than modeling transitions as abstract concepts ("hold then burst"), model them as concrete scene sequences. A "freeze" effect is just the previous scene continuing — the factory doesn't need to produce a "hold" step because that's inherent in the chaser's sequential execution. A "dissolve" needs a dim target scene to crossfade into.

3. **Design principle:** Transition factories must think in terms of "what new scenes do I insert into the chaser?" not "what lighting effect do I want?" Every conceptual phase that isn't a new scene is either handled by the previous scene's natural hold or by the chaser's FadeIn crossfade.

## Prevention

- **Contract test:** The test suite includes `test_build_transition_scenes_contract` which iterates all 21 types and asserts `len(scenes) == len(timing)` for each. Run this after adding any new transition type.
- **Mental model:** When writing a new `_transition_*` factory, count your scenes and timing entries before returning. They must match.
- **Minimum 1 scene:** Every factory must return at least 1 scene + 1 timing entry. There's no such thing as a "0-scene transition" — if the transition does nothing visible, it still needs a concrete blackout or dim scene.

## Related Issues

No related issues documented yet.
