---
title: Dramatic Segment Transitions and Perceivable Beat Sync
type: feat
date: 2026-02-20
---

# Dramatic Segment Transitions and Perceivable Beat Sync

## Overview

Two connected problems in algorithmically-generated shows:

1. **Segment transitions are invisible** — The phrase planner guarantees 2+ visual dimensions change on phrase boundaries, but this is a *safety net*, not a *creative engine*. A drop might get a different mover route and par timing than the build before it, but there's no transition *event* — no blackout, no flash, no freeze-then-burst. Hand-crafted generators (Guardian Angel) produce electric transitions; algorithmic generators (Loyalty, Space) produce competent but workmanlike ones.

2. **Beat sync isn't perceivable** — Some generators respond at beat level (Lorn, PhatAdam), others operate at bar level (Loyalty). The phrase planner assigns timing recipes but doesn't enforce minimum beat reactivity. A viewer watching a Loyalty-generated show might not perceive any relationship between the music and the lights during verse sections.

Both problems compound: if the audience can't feel the beat AND can't see the section change, the show looks random.

## Problem Statement

### Transitions Today

The contrast enforcement system (`phrase_planner._enforce_phrase_contrast()`) guarantees:
- 2+ of {position, rhythm, color, intensity, effect_density} differ on phrase change
- If the natural candidate doesn't hit 2 dims, it force-adds transforms and retimes pars

What it does NOT do:
- Insert a *transition event* (blackout, flash, freeze, strobe burst) at the boundary
- Score how *visually dramatic* the change is (same route with different transform = "changed" but subtle)
- Escalate effects across the show (laser/strobe/gobo progression)
- Control transition *style* (snap vs crossfade vs strobe-burst at the exact boundary moment)

### Beat Sync Today

Timing recipes in `phrase-rules.json` define mover and par timing per phrase, but:
- No **minimum** beat reactivity per phrase class — a drop could theoretically get a 4-bar mover cycle
- No layered timing guarantee — movers and pars could run at the same granularity (looks flat)
- No energy-reactive granularity — timing is phrase-based, not energy-based
- PAR intensity/color changes at bar level look *static* to viewers; need beat-level or accent-level changes in high-energy sections

### Variety Today

Designer packs + technique cooldown prevent exact repetition, but:
- Transitions use the same mechanism every time (contrast enforcement)
- No vocabulary of distinct transition *types* that rotate across shows
- Beat reactivity is generator-dependent, not planner-enforced

## Proposed Solution

### Layer 1: Transition Events (phrase_planner.py + phrase-rules.json)

Add a **transition event system** that inserts 1-4 beat "bridge" moments at segment boundaries. These are distinct from the techniques on either side — they're punctuation marks between paragraphs.

**New data in `phrase-rules.json`:**
```json
"transition_events": {
  "pools": {
    "low_to_low": ["dead_air", "slow_dissolve"],
    "low_to_mid": ["color_swap", "position_snap", "par_ladder"],
    "low_to_high": ["blackout_slingshot", "white_flash", "strobe_burst"],
    "high_to_low": ["freeze_decay", "pulse_to_glow", "dim_dissolve"],
    "high_to_high": ["color_inversion", "stutter_gate", "chase_cancel"],
    "mid_to_high": ["compression_snap", "ladder_build", "par_convergence"],
    "mid_to_mid": ["color_swap", "position_snap", "slow_dissolve"],
    "same_to_same": ["slow_dissolve", "color_swap", "position_snap"],
    "build_to_drop": ["blackout_slingshot", "white_flash", "freeze_burst", "stutter_resolve"],
    "end_of_show": ["fade_to_black", "freeze_hold"]
  },
  "event_schema": {
    "blackout_slingshot": {
      "duration_beats": 1,
      "description": "Full cut to black for 1 beat, then snap return with all beams",
      "fixtures": "all",
      "exit_style": "snap"
    },
    "white_flash": {
      "duration_beats": 1,
      "description": "All fixtures flash white for 1 beat, then snap to new palette",
      "fixtures": "all",
      "exit_style": "snap"
    },
    "freeze_decay": {
      "duration_beats": 4,
      "description": "Hold last frame, fade pars to 20% over 2 beats, movers crossfade to DSC over 4 beats",
      "fixtures": "all",
      "exit_style": "smooth"
    },
    "color_inversion": {
      "duration_beats": 1,
      "description": "Swap warm/cool across all fixtures on beat 1",
      "fixtures": "pars+movers",
      "exit_style": "snap"
    },
    "stutter_gate": {
      "duration_beats": 2,
      "description": "Rapid on/off strobing at 1/4 beat for 2 beats, then hold",
      "fixtures": "pars",
      "exit_style": "snap"
    },
    "dead_air": {
      "duration_beats": 2,
      "description": "Dim all to 10-20% for 2 beats, no movement",
      "fixtures": "all",
      "exit_style": "smooth"
    },
    "pulse_to_glow": {
      "duration_beats": 4,
      "description": "Rhythmic par pulse decays from beat-level to static over 4 beats",
      "fixtures": "pars",
      "exit_style": "smooth"
    },
    "slow_dissolve": {
      "duration_beats": 4,
      "description": "4-beat crossfade between old and new looks, no hard edge",
      "fixtures": "all",
      "exit_style": "smooth"
    },
    "fade_to_black": {
      "duration_beats": 4,
      "description": "All fixtures smooth fade to black over 4 beats",
      "fixtures": "all",
      "exit_style": "smooth"
    },
    "freeze_hold": {
      "duration_beats": 4,
      "description": "Hold last frame for 2 beats, then fade to black over 2 beats",
      "fixtures": "all",
      "exit_style": "smooth"
    }
  },
  "cooldown": 3,
  "variety_rule": "no same transition type within 3 segment boundaries"
}
```

**New method in `PhraseAwarePlanner`:**
```python
def plan_transition(self, prev_phrase, next_phrase, prev_energy, next_energy,
                    segment_index, recent_transitions, show_key) -> TransitionEvent:
    """Select a transition event for a segment boundary.

    Returns TransitionEvent with: type, duration_beats, fixture_targets,
    exit_style, and the scenes/timing needed to render it.
    """
```

**New in showlib.py:**
```python
def plan_segment_transition(prev_phrase, next_phrase, prev_energy, next_energy, ...) -> dict
# Wrapper that returns serialized TransitionEvent

# Scene helpers for each transition type:
def transition_blackout_slingshot(bpm, pos_tuples) -> list[dict]  # returns 1-2 scenes
def transition_white_flash(bpm) -> list[dict]
def transition_freeze_decay(bpm, last_scene, target_pos) -> list[dict]
def transition_color_inversion(bpm, current_palette) -> list[dict]
def transition_stutter_gate(bpm, par_color) -> list[dict]
def transition_dead_air(bpm) -> list[dict]
# etc.
```

**Generator usage pattern:**
```python
for seg_idx, segment in enumerate(segments):
    # At EVERY segment boundary, insert transition (not just phrase changes)
    if seg_idx > 0:
        transition = plan_segment_transition(
            prev_phrase, phrase, prev_energy, energy,
            segment_index=seg_idx, total_segments=len(segments), ...)
        transition_scenes = build_transition_scenes(
            transition, bpm, POS, palette, last_scene)
        scenes.extend(transition_scenes)
        chaser_steps.extend(transition_timing)

    # Then build the segment's content as before
    for bar in range(segment_bars):
        technique = pick_phrase_technique(...)
        # ... build bar scenes

# End-of-show transition
end_transition = plan_segment_transition(
    phrase, None, energy, 0.0, segment_index=len(segments),
    total_segments=len(segments), end_of_show=True, ...)
scenes.extend(build_transition_scenes(end_transition, bpm, POS, palette, last_scene))
```

### Layer 2: Beat Reactivity Minimums (phrase-rules.json + phrase_planner.py)

Add **minimum beat reactivity** per phrase class to ensure perceivable sync.

**New data in `phrase-rules.json`:**
```json
"beat_reactivity": {
  "intro":        {"par_min": "2bar", "mover_min": "4bar", "accent_layer": "none"},
  "verse_groove": {"par_min": "2beat", "mover_min": "2bar", "accent_layer": "bar_downbeat"},
  "build":        {"par_min": "beat", "mover_min": "bar", "accent_layer": "beat"},
  "drop":         {"par_min": "beat", "mover_min": "bar", "accent_layer": "sub_beat"},
  "breakdown":    {"par_min": "bar", "mover_min": "4bar", "accent_layer": "none"},
  "outro":        {"par_min": "2bar", "mover_min": "4bar", "accent_layer": "none"}
}
```

Where:
- `par_min` = minimum granularity of par color/intensity changes
- `mover_min` = minimum granularity of mover position changes
- `accent_layer` = what additional per-beat accents are required:
  - `none` = no accents needed
  - `bar_downbeat` = visible accent on beat 1 of each bar (dimmer bump, color snap, or strobe hit)
  - `beat` = visible accent every beat (par intensity pulse, color rotation, position micro-shift)
  - `sub_beat` = sub-beat accents allowed (strobe packets, 1/4-beat par flashes)

**Changes to `PlannedTechnique`:**
Add fields to the returned technique dict:
```python
"beat_reactivity": {
    "par_min": "beat",
    "mover_min": "bar",
    "accent_layer": "beat",
    "accent_type": "par_intensity_pulse"  # chosen from pool
}
```

**Accent type pools** (chosen per-show for variety):
- `par_intensity_pulse` — PAR master bumps 20% on each beat then decays
- `par_color_snap` — PAR hue shifts slightly on each beat (within palette)
- `mover_micro_shift` — Mover pan/tilt adjusts ±2-5 values per beat (subtle but perceivable)
- `strobe_hit` — Brief strobe flash on beat 1 only
- `dimmer_breathe` — Sinusoidal dimmer modulation synced to beat

### Layer 3: Generator Template and Guidance

**Update scaffold template** (`scripts/show_workflow.py`) to include:

```python
# === SEGMENT BOUNDARY: Insert transition at EVERY boundary ===
if seg_idx > 0:
    transition = plan_segment_transition(
        prev_phrase=prev_phrase, next_phrase=phrase,
        prev_energy=prev_rms, next_energy=rms,
        segment_index=seg_idx, total_segments=len(segments),
        recent_transitions=recent_transitions,
        show_key=SONG_STEM, project_root=PROJECT_ROOT)
    # Build transition scenes via dispatcher
    t_scenes = build_transition_scenes(transition, bpm, POS, palette, last_scene)
    scenes.extend(t_scenes)
    chaser_steps.extend(transition_timing(transition, bpm))
    recent_transitions.append(transition["type"])

# === BEAT SYNC: Apply reactivity minimum ===
technique = pick_phrase_technique(...)
reactivity = technique["beat_reactivity"]
# Par scenes must change at least every reactivity["par_min"]
# Movers must change at least every reactivity["mover_min"]
# If accent_layer != "none", add accent scenes between main scenes
```

**Update `skills/qlc-show-workflow/SKILL.md`** with:
- Requirement to call `plan_segment_transition()` at every phrase boundary
- Requirement to read and enforce `beat_reactivity` from technique
- Guidance on layered timing (movers slower than pars, accents on top)

**Update `.claude/CLAUDE.md` Lessons Learned** with:
- "Every segment boundary needs a transition event, not just a technique change"
- "Beat sync must be perceivable: par changes at beat level in drops, accent layer on top"
- "Layered timing: movers at bar/2bar, pars at beat/2beat, accents on downbeats"

## Acceptance Criteria

### Transitions
- [x] `phrase-rules.json` has `transition_events` section with pools and event schemas
- [x] `PhraseAwarePlanner.plan_transition()` method exists and returns `TransitionEvent`
- [x] showlib.py has `plan_segment_transition()` wrapper and `build_transition_scenes()` dispatcher
- [x] Scene helpers exist for each transition type (blackout_slingshot, white_flash, freeze_decay, etc.)
- [x] Transition cooldown prevents same type within 3 boundaries
- [x] Transition pools are phrase-pair-aware (build→drop gets different options than verse→verse)
- [x] Same-phrase boundaries (verse→verse) trigger transitions via `same_to_same` pool
- [x] Transition duration capped at 25% of shorter adjacent segment
- [x] At least 8 distinct transition types + 2 end-of-show types implemented
- [x] Show-level escalation: first-half transitions exclude most dramatic options
- [ ] Generator scaffold template calls `plan_segment_transition()` at ALL segment boundaries
- [x] Pool exhaustion handled gracefully (relaxed cooldown with warning)

### Beat Sync
- [x] `phrase-rules.json` has `beat_reactivity` section with per-phrase minimums
- [x] `PlannedTechnique` includes `beat_reactivity` fields
- [x] At least 5 accent type options exist for variety across shows
- [x] Drops and builds have beat-level par reactivity minimum
- [x] Breakdowns and intros have coarser reactivity (no over-animation)

### Variety
- [x] Different shows hitting the same phrase pair get different transition types (cooldown + randomized pool selection)
- [x] Accent types rotate per-show (not always the same beat sync pattern)
- [x] Transition events are musically appropriate (high-energy transitions for build→drop, subtle for verse→verse)

### Quality
- [x] Existing tests pass (`python3 -m pytest tests/`)
- [x] New tests for `plan_transition()` covering: pool selection, cooldown enforcement, all phrase pairs, same-phrase boundaries, duration capping, escalation
- [x] New tests for beat reactivity: verify technique output includes reactivity fields
- [ ] New `validate_beat_reactivity()` function checks generated chasers meet par_min/mover_min
- [x] Validate scripts pass: `validate_data.py`, `validate_venue_profiles.py`
- [x] `validate_data.py` updated to accept new `transition_events` and `beat_reactivity` schema fields

## Technical Considerations

### Transition Duration vs. Chaser Timing
Transition events consume 1-4 beats at segment boundaries. The generator must account for this when calculating total chaser duration — the transition beats come from the *previous* section's bar allocation (last 1-4 beats become transition), not added on top.

### Backwards Compatibility
Existing generators that don't call `plan_segment_transition()` continue to work — transitions are additive, not required. But new generators from the scaffold template will include them by default.

### Energy Classification
Transition pools are keyed by energy level pair (low/mid/high), not phrase name. This means `classify_phrase()` output needs to be mapped to energy:
- low: intro, breakdown, outro
- mid: verse_groove
- high: build, drop

The `build_to_drop` pool is a special case because it's the most emotionally important transition in EDM and deserves its own curated pool.

### Accent Layer Performance
Sub-beat accents (1/4-beat par flashes) in drops could produce many scenes. If a 32-bar drop at 128 BPM with 1/4-beat accents = 512 accent scenes. Dedup caching should handle this if accent patterns repeat, but worth monitoring scene count.

## Design Decisions (from SpecFlow analysis)

### D1: Same-phrase segment boundaries
Progressive house/techno songs often have verse→verse or drop→drop boundaries where the phrase class doesn't change but the musical section does. These currently get NO transition.

**Decision**: Trigger transitions on *segment index change*, not just *phrase class change*. Same-phrase boundaries use a `same_to_same` pool with subtle transitions (slow_dissolve, color_swap, position_snap). The generator pattern becomes:
```python
if seg_idx > 0:  # not: "and phrase != prev_phrase"
    transition = plan_segment_transition(...)
```

### D2: build_to_drop pool priority
The `build_to_drop` pool is phrase-name-keyed while others are energy-keyed. When a build→drop transition is detected, the phrase-specific pool takes priority over the energy-based `high_to_high` pool.

**Priority order**: phrase-pair-specific pool (e.g., `build_to_drop`) → energy-pair pool (e.g., `high_to_high`) → fallback `same_to_same`.

### D3: Transition duration safety
A 4-beat transition in a 2-bar (8-beat) segment consumes 50% of the segment.

**Rule**: Transition duration capped at 25% of the *shorter* adjacent segment. If the cap forces a 1-beat maximum but the chosen transition needs 4 beats, fall back to a shorter transition from the same pool.

### D4: Transition-contrast interaction
Transitions and contrast enforcement solve related but different problems. Contrast enforcement ensures the *content* on either side differs; transitions insert *punctuation* between them.

**Rule**: Transitions run BEFORE contrast enforcement. The transition event is independent — it doesn't count toward the 2-dimension contrast requirement. Contrast enforcement still applies to the pre/post technique pair.

### D5: Show-level transition escalation
First and last drops shouldn't get identical transitions. The show should build in spectacle.

**Rule**: `plan_transition()` receives `segment_index` and `total_segments`. Transitions in the back half of the show can access the full pool; transitions in the first half exclude the most dramatic options (strobe_burst, freeze_burst). The `build_to_drop` pool is exempt — those are always dramatic.

### D6: `build_transition()` dispatcher
Every generator shouldn't need its own match/case for transition types.

**Rule**: `showlib.py` provides a single `build_transition_scenes(transition, bpm, pos_tuples, palette, last_scene)` dispatcher that routes to the correct scene helper based on `transition["type"]`. Generators call this one function.

### D7: Beat reactivity is advisory with validation
The phrase planner returns `beat_reactivity` fields in the technique dict. Generators are expected to honor them. Enforcement is via a post-generation validator, not runtime assertion.

**Rule**: Add `validate_beat_reactivity(chaser_steps, technique_sequence)` to the validation pipeline. It checks that par scene changes meet the minimum granularity for each phrase. This catches violations at build time, not runtime.

### D8: Song ending
The last segment needs an exit transition (not just a hard stop).

**Rule**: Add `end_of_show` to the transition pools. Options: `fade_to_black` (4-beat smooth dimdown), `freeze_hold` (hold last frame, 2-beat decay). Applied after the last segment's content, before the final blackout.

## Dependencies & Risks

- **Risk**: Transition scenes add to total chaser step count. For 10-segment songs with 2-4 beat transitions each, that's 20-40 extra steps — manageable.
- **Risk**: Beat-level par changes in long drops produce many scenes. Mitigated by dedup cache and repeating accent patterns.
- **Risk**: Pool exhaustion — small pools (2 options) with cooldown=3 may starve if many boundaries share the same energy pair. Mitigated by allowing cooldown to relax (wrap around) when pool is exhausted, with a warning logged.
- **Dependency**: `phrase-rules.json` schema change requires updating `validate_data.py` to accept new fields.
- **Dependency**: New showlib.py functions need test coverage before generators can use them.

## References

### Internal
- Contrast enforcement: `qlc_runtime/phrase_planner.py:1094-1144` (`_enforce_phrase_contrast`)
- Phrase rules: `references/data/phrase-rules.json`
- FX/transition concepts: `references/creativity.md` Section 12.3 (EDM-033..EDM-045)
- Coordination techniques: `references/data/coordination-techniques.json`
- Best transition example: `venue/home-studio/generators/` Guardian Angel generator
- Best beat sync example: `venue/home-studio/generators/` Lorn generator
- Scaffold template: `scripts/show_workflow.py`
