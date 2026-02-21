---
title: "fix: Segment-Driven Lighting Reactivity"
type: fix
date: 2026-02-21
revision: 5 (implementation-ready)
---

# fix: Segment-Driven Lighting Reactivity

## Overview

Generated shows lack visual distinction between song segments. A viewer should **immediately** see a shift when the song moves from intro to verse, verse to drop, drop to breakdown. Currently the scaffold template dispatches sections to `build_low/mid/high` based on energy thresholds, but those builders produce subtly similar output — overlapping dimmer ranges, similar position patterns, identical PAR/NI3K treatment. Energy data maps only to dimmer via `e2d()`, leaving color, frost, prism, lasers, halo, strobe, position sweep, and PAR mode as hardcoded constants.

## Problem Statement

### What's broken

1. **Energy only drives dimmer.** The `atmo()` helper takes an `energy` param but only uses it for `e2d(energy, lo, hi)` dimmer calculations. Frost, color selection, prism, lasers, halo, strobe, NI3K tilt mode, and position sweep pattern are all hardcoded per builder, not energy-proportional.

2. **Section builders overlap.** The visual delta between `build_low`, `build_mid`, and `build_high` is subtle:
   - `build_low`: DSC only, frost=220, no halo, BASE_COLOR pars, missyees off
   - `build_mid`: SWEEP_TIGHT, frost=160, H_BLU halo, ACCENT pars, DIM missyees
   - `build_high`: SWEEP_WIDE, frost=140-60*e, H_CYN halo, prism if e>0.7
   - A viewer can't tell when verse becomes chorus.

3. **Color is binary, not energy-scaled.** Color decisions are threshold-based (`vocal_present → gold, else → indigo`) rather than using the research brief's palette tiers (base/accent/hit) mapped to energy.

4. **Effects never activate in scaffold.** Lasers, strobe, and prism are all off or gated behind extremely high thresholds. The NI3K is effectively invisible below e=0.5. The scaffold produces safe but lifeless output.

5. **Technique dimensions are metadata-only.** The phrase planner assigns `dimensions.intensity`, `dimensions.effect_density`, plus `relationship`, `timing`, and `mover_pattern` to each technique, but only `beat_reactivity` reaches the scene factory. Everything else is used for candidate scoring only.

### Evidence

From the Children generator analysis:
- `build_low` dimmer range: Sharpy 18-42, BSW 12-28, Par 24-56
- `build_high` dimmer range: Sharpy 100-200, BSW 80-180, Par 80-180
- The difference is real but **all other dimensions are nearly identical** between the two

From a serialized `drop` technique (via `_serialize_planned_phrase_technique()`):
```json
"dimensions": {"intensity": "peak", "effect_density": "high"},
"relationship": "unison",
"timing": {"mover_beats": 4, "par_beats": 2, "par_style": "chase"},
"mover_pattern": {"base_route": "R035", "transforms": ["mirror", "phase_shift"]}
```
But the scaffold template only reads `beat_reactivity` — all other fields are ignored.

## Proposed Solution

### Architecture: Two-layer split (policy + rendering)

Instead of a single "god function," split into two layers:

1. **`resolve_phrase_style()`** — pure policy. Takes phrase + energy + technique and returns a style dict with all visual parameters resolved to concrete values. No fixture assembly, no scene creation. This is where phrase-rules.json defaults, technique overrides, and energy scaling all merge.

2. **`render_phrase_scene()`** — fixture assembly. Takes the resolved style dict + position + palette and calls `mover_look()`, `par_look()`, `ni3k_look()` to produce a `scene()`. Pure wiring, no policy decisions.

The scaffold template calls both in sequence. Custom generators can call `resolve_phrase_style()` and then override specific values before passing to `render_phrase_scene()`.

```
technique data ──┐
                 ├──→ resolve_phrase_style() ──→ style dict ──→ render_phrase_scene() ──→ scene()
phrase + energy ─┘                                    ↑
                                                 palette + pos
```

### Design principle: Planner is the single source of truth

The phrase planner already owns phrase classification and technique selection. `resolve_phrase_style()` reads planner output — it does NOT duplicate policy. `PHRASE_DEFAULTS` provides fallback ranges only when no technique is available (e.g., unit tests, manual calls).

The planner's technique dict carries:
- `dimensions.intensity` / `dimensions.effect_density` → modulate dimmer, frost, effect gates
- `relationship` → via existing `mover_family_from_phrase()` → mover coordination mode
- `timing.par_beats` / `timing.par_style` → via existing `par_mode_from_phrase_timing()` → PAR mode
- `mover_pattern.transforms` → position sweep style (mirror/expand → wide, compress → tight)
- `beat_reactivity` → step size (already wired)

### Design principle: Brief constrains, energy selects

The research brief defines a color world but stores **prose**, not fixture values. Generators must define concrete palettes. `build_phrase_palette()` is a convenience for structuring the palette dict — the generator author fills in the actual RGB and color-wheel values based on the brief's color story.

Energy selects which tier is active:
- `energy < 0.35` → `palette["base"]`
- `0.35 <= energy < 0.65` → `palette["accent"]`
- `energy >= 0.65` → `palette["hit"]`

### Phrase Visual Defaults

Each phrase class has a defined visual signature. These are **fallback defaults** that `resolve_phrase_style()` uses when no technique is provided:

| Dimension | intro | verse_groove | build | drop | breakdown | outro |
|-----------|-------|-------------|-------|------|-----------|-------|
| **Dimmer range** | 15-80 | 40-160 | 60-200 | 150-255 | 20-100 | 10-60 |
| **Frost** | 200-240 | 160-200 | 120-180 | 80-140 | 180-240 | 200-240 |
| **Prism** | off | off | e>0.7, last 4 bars | on if e>0.5 | off | off |
| **Lasers** | off | off | off | e>0.75, song>50% | off | off |
| **Halo** | off | base color | accent color | hit color | off/subtle | fading |
| **Strobe** | off | off | last 2 bars, slow | e>0.8 | off | off |
| **NI3K dim** | 0-30 | 15-80 | 40-120 | 100-200 | 10-50 | 0-25 |
| **NI3K tilt** | static | static | spread | spin | static | static |
| **Position** | DSC only | tight sweep | converging | wide sweep | park DSC | simplifying |
| **Par mode** | solid | pairs | gradient | chase | solid | solid |
| **Color tier** | base only | base/accent | accent/hit | hit | base | base, dimming |
| **Missyee** | off | dim base | accent | full hit | dim | off |

When a technique IS provided, its fields override these defaults (see Phase 3).

## Implementation

### Phase 1: `resolve_phrase_style()` + `PHRASE_DEFAULTS` in showlib.py

**File: `showlib.py`**

Add module-level constants:

```python
# Bridge planner PAR modes (blink*/fade*) to par_look() modes (solid/pairs/gradient/chase)
PLANNER_TO_PAR_LOOK = {
    "blink1": "chase", "blink2": "chase", "blink4": "chase",
    "fade4": "gradient", "fade8": "solid",
}
```

Add `PHRASE_DEFAULTS` — fallback ranges only, not a policy engine:

```python
PHRASE_DEFAULTS = {
    "intro":        {"dim": (15, 80),   "frost": (200, 240), "prism_gate": None,
                     "laser_gate": None, "strobe_gate": None, "halo_tier": "off",
                     "ni3k_dim": (0, 30), "ni3k_tilt": "static",
                     "pos_style": "static", "par_mode": "solid", "miss": "off"},
    "verse_groove": {"dim": (40, 160),  "frost": (160, 200), "prism_gate": None,
                     "laser_gate": None, "strobe_gate": None, "halo_tier": "base",
                     "ni3k_dim": (15, 80), "ni3k_tilt": "static",
                     "pos_style": "tight", "par_mode": "pairs", "miss": "dim"},
    "build":        {"dim": (60, 200),  "frost": (120, 180), "prism_gate": 0.7,
                     "laser_gate": None, "strobe_gate": 0.85, "halo_tier": "accent",
                     "ni3k_dim": (40, 120), "ni3k_tilt": "spread",
                     "pos_style": "converge", "par_mode": "gradient", "miss": "accent"},
    "drop":         {"dim": (150, 255), "frost": (80, 140),  "prism_gate": 0.5,
                     "laser_gate": 0.75, "strobe_gate": 0.8, "halo_tier": "hit",
                     "ni3k_dim": (100, 200), "ni3k_tilt": "spin",
                     "pos_style": "wide", "par_mode": "chase", "miss": "full"},
    "breakdown":    {"dim": (20, 100),  "frost": (180, 240), "prism_gate": None,
                     "laser_gate": None, "strobe_gate": None, "halo_tier": "off",
                     "ni3k_dim": (10, 50), "ni3k_tilt": "static",
                     "pos_style": "static", "par_mode": "solid", "miss": "off"},
    "outro":        {"dim": (10, 60),   "frost": (200, 240), "prism_gate": None,
                     "laser_gate": None, "strobe_gate": None, "halo_tier": "off",
                     "ni3k_dim": (0, 25), "ni3k_tilt": "static",
                     "pos_style": "static", "par_mode": "solid", "miss": "off"},
}
```

Add `resolve_phrase_style()` — pure policy, returns a flat dict of resolved values:

```python
def resolve_phrase_style(phrase, energy, technique=None,
                         song_progress=0.5, bars_left=None):
    """Resolve phrase + energy + technique into concrete visual parameters.

    Args:
        phrase: One of the 6 phrase classes from classify_phrase()
        energy: 0.0-1.0 RMS energy for this step
        technique: Optional serialized PlannedTechnique dict
        song_progress: 0.0-1.0 position in song (for laser gating)
        bars_left: Bars remaining in current section (for end-of-section effects).
                   None means unknown — disables "last N bars" behaviors.

    Returns:
        dict with resolved keys: dim, frost, prism, lasers, strobe, halo_tier,
        ni3k_dim, ni3k_tilt, pos_style, par_mode, miss_level, color_tier
    """
    vis = PHRASE_DEFAULTS.get(phrase, PHRASE_DEFAULTS["verse_groove"])

    # --- Base ranges from phrase defaults ---
    dim_lo, dim_hi = vis["dim"]
    frost_lo, frost_hi = vis["frost"]
    ni3k_lo, ni3k_hi = vis["ni3k_dim"]
    prism_gate = vis["prism_gate"]
    laser_gate = vis["laser_gate"]
    strobe_gate = vis["strobe_gate"]
    pos_style = vis["pos_style"]
    par_mode = vis["par_mode"]

    # --- Technique overrides (planner is source of truth) ---
    if technique:
        dims = technique.get("dimensions", {})
        intensity = dims.get("intensity", "medium")
        density = dims.get("effect_density", "low")

        # Intensity: boost dimmer floor
        boost = {"low": 0.0, "medium": 0.0, "rising": 0.15, "peak": 0.25}
        dim_lo += int((dim_hi - dim_lo) * boost.get(intensity, 0))

        # Effect density: lower activation thresholds
        if density in ("high", "peak"):
            if prism_gate is not None:
                prism_gate *= 0.8
            if strobe_gate is not None:
                strobe_gate *= 0.85

        # Relationship → mover family → dim ratio between movers
        rel = technique.get("relationship", "")
        mover_family = "geometric"  # default
        if rel:
            mover_family = mover_family_from_phrase(phrase, rel, energy, energy)
            # family drives relative brightness between movers in render_phrase_scene()

        # Timing → PAR mode (bridge planner modes to par_look() modes)
        # par_mode_from_phrase_timing() returns blink1/blink2/blink4/fade4/fade8
        # par_look() accepts solid/pairs/gradient/chase
        # PLANNER_TO_PAR_LOOK (module-level constant) bridges them
        t_timing = technique.get("timing", {})
        par_beats = t_timing.get("par_beats", 4)
        par_style = t_timing.get("par_style", "solid")
        if par_beats and par_style:
            planner_mode = par_mode_from_phrase_timing(par_beats, par_style, phrase, 0)
            par_mode = PLANNER_TO_PAR_LOOK.get(planner_mode, par_mode)

        # Mover pattern → position style
        # Route IDs are abstract (R001, R011, etc.) — no semantic sweep names.
        # Map by route number range + transforms to sweep style:
        #   - Routes with "mirror"/"phase_shift" transforms → wide (opposing motion)
        #   - Routes with "compress" → tight
        #   - Routes with "expand"/"fan_out" → wide
        #   - Default: phrase default pos_style stands
        mp = technique.get("mover_pattern", {})
        transforms = mp.get("transforms", [])
        if transforms:
            if any(t in ("mirror", "phase_shift", "expand") for t in transforms):
                pos_style = "wide"
            elif "compress" in transforms:
                pos_style = "tight"

    # --- Resolve concrete values from energy ---
    dim = int(dim_lo + (dim_hi - dim_lo) * energy)
    frost = int(frost_hi - (frost_hi - frost_lo) * energy)
    ni3k_dim = int(ni3k_lo + (ni3k_hi - ni3k_lo) * energy)

    prism = (prism_gate is not None and energy > prism_gate)
    lasers = (laser_gate is not None and energy > laser_gate
              and song_progress > 0.5)
    strobe = (strobe_gate is not None and energy > strobe_gate)

    # End-of-section effects (only when bars_left is known)
    if bars_left is not None:
        if phrase == "build" and bars_left <= 4 and prism_gate is not None:
            prism = True  # prism enters in last 4 bars of build
        if phrase == "build" and bars_left <= 2 and strobe_gate is not None:
            strobe = True  # strobe in last 2 bars of build

    # Color tier from energy
    if energy >= 0.65:
        color_tier = "hit"
    elif energy >= 0.35:
        color_tier = "accent"
    else:
        color_tier = "base"

    return {
        "dim": dim, "frost": frost, "prism": prism, "lasers": lasers,
        "strobe": strobe, "halo_tier": vis["halo_tier"],
        "ni3k_dim": ni3k_dim, "ni3k_tilt": vis["ni3k_tilt"],
        "pos_style": pos_style, "par_mode": par_mode,
        "miss_level": vis["miss"], "color_tier": color_tier,
        "mover_family": mover_family if technique else (
            "atmospheric" if phrase in ("intro", "breakdown", "outro") else "geometric"
        ),
    }
```

### Phase 2: `render_phrase_scene()` in showlib.py

**File: `showlib.py`**

Pure fixture assembly — takes a resolved style dict and produces a `scene()`:

```python
def render_phrase_scene(name, style, pos_key, pos_tuples, palette,
                        beat_idx=0, path=""):
    """Assemble a scene from a resolved style dict + palette.

    Args:
        name: Scene name
        style: Dict from resolve_phrase_style()
        pos_key: Position name for movers
        pos_tuples: Dict from load_focus_position_tuples()
        palette: Dict with "base", "accent", "hit" tiers
        beat_idx: Step counter for chase cycling
        path: QLC+ function tree folder
    """
    tier = palette[style["color_tier"]]

    # Mover strobe values
    if style["strobe"]:
        s_strobe, b_shutter = SHARPY_STROBE_MED, BSW_SHUT_STROBE_SLOW
    else:
        s_strobe, b_shutter = SHARPY_OPEN, BSW_SHUT_OPEN

    # Halo color from tier
    halo_map = {"off": H_OFF, "base": H_BLU, "accent": H_CYN,
                "hit": H_RGB, "fading": H_OFF}
    halo = halo_map.get(style["halo_tier"], H_OFF)

    # Missyee level
    miss_map = {"off": (0, NOTHING), "dim": (60, tier.get("miss_rgb", NOTHING)),
                "accent": (150, tier.get("miss_rgb", NOTHING)),
                "full": (255, tier.get("miss_rgb", NOTHING))}
    miss_master, miss_color = miss_map.get(style["miss_level"], (0, NOTHING))

    # Mover dim ratios from family (set by resolve_phrase_style)
    # family_from_phrase_and_relationship() returns: atmospheric, geometric, snap
    family = style.get("mover_family", "geometric")
    FAMILY_RATIOS = {
        "atmospheric": (0.8, 0.7, 0.5),     # soft, even, subdued — intro/breakdown/outro
        "geometric":   (1.0, 0.85, 0.6),    # balanced, structured — verse/build
        "snap":        (1.0, 0.6, 0.6),     # sharpy dominant, punchy — drop/high-energy
    }
    sr, br, pr = FAMILY_RATIOS.get(family, (1.0, 0.85, 0.6))

    return scene(name,
        *mover_look(pos_key, pos_tuples,
                    colors=(tier.get("sharpy", 0), tier.get("bsw", 0),
                            tier.get("profile", 0)),
                    dims=(int(style["dim"] * sr), int(style["dim"] * br),
                          int(style["dim"] * pr)),
                    frost=(style["frost"], min(255, style["frost"])),
                    prism=style["prism"], focus=128,
                    strobes=(s_strobe, b_shutter, PROFILE_STROBE_OFF)),
        *par_look(style["par_mode"], tier.get("par_rgb", NOTHING),
                  master=int(style["dim"] * 0.8),
                  miss_color=miss_color, miss_master=miss_master,
                  beat_idx=beat_idx),
        ni3k_look(pos_key, pos_tuples,
                  rgb=tier.get("ni3k_rgb", NOTHING), dim=style["ni3k_dim"],
                  halo=halo, lasers=style["lasers"],
                  tilt_mode=style["ni3k_tilt"]),
        path=path)
```

Convenience wrapper combining both layers:

```python
def phrase_scene(name, phrase, energy, pos_key, pos_tuples, palette,
                 technique=None, song_progress=0.5, bars_left=None,
                 beat_idx=0, path="", **overrides):
    """Build a complete scene driven by phrase type and energy level.

    Combines resolve_phrase_style() + render_phrase_scene().
    **overrides apply to the resolved style dict before rendering.
    """
    style = resolve_phrase_style(phrase, energy, technique=technique,
                                 song_progress=song_progress,
                                 bars_left=bars_left)
    style.update(overrides)
    return render_phrase_scene(name, style, pos_key, pos_tuples, palette,
                               beat_idx=beat_idx, path=path)
```

### Phase 3: `build_phrase_palette()` convenience helper

**File: `showlib.py`**

Generators provide concrete color values (the brief stores prose, not DMX values). This helper structures them into the 3-tier format that `render_phrase_scene()` expects:

```python
def build_phrase_palette(base_rgb, accent_rgb, hit_rgb,
                         sh_base=0, sh_accent=0, sh_hit=0,
                         bsw_base=0, bsw_accent=0, bsw_hit=0,
                         pf_base=0, pf_accent=0, pf_hit=0):
    """Build a 3-tier palette dict for phrase_scene().

    Generator authors define concrete colors from the research brief's
    color story. This helper structures them for energy-tier selection.
    """
    return {
        "base":   {"sharpy": sh_base, "bsw": bsw_base, "profile": pf_base,
                   "par_rgb": base_rgb, "miss_rgb": base_rgb, "ni3k_rgb": base_rgb},
        "accent": {"sharpy": sh_accent, "bsw": bsw_accent, "profile": pf_accent,
                   "par_rgb": accent_rgb, "miss_rgb": accent_rgb, "ni3k_rgb": accent_rgb},
        "hit":    {"sharpy": sh_hit, "bsw": bsw_hit, "profile": pf_hit,
                   "par_rgb": hit_rgb, "miss_rgb": hit_rgb, "ni3k_rgb": hit_rgb},
    }
```

### Phase 4: Position sweep with venue filtering

**File: `showlib.py`**

```python
SWEEP_PATTERNS = {
    "static":   ["DSC"],
    "tight":    ["SL", "C", "SR", "C"],
    "converge": ["USL", "DSL", "DSC", "DSR", "USR", "DSC"],
    "wide":     ["USL", "DSR", "USR", "DSL", "DSC", "USC"],
}

def pick_sweep_position(pos_style, step_idx, pos_tuples):
    """Return a position key from the sweep pattern for this step.

    Filters pattern to positions that exist in pos_tuples.
    Falls back to first available position if none match.
    """
    pattern = SWEEP_PATTERNS.get(pos_style, SWEEP_PATTERNS["tight"])
    available = [k for k in pattern if k in pos_tuples]
    if not available:
        available = list(pos_tuples.keys())[:1] or ["DSC"]
    return available[step_idx % len(available)]
```

### Phase 5: Update scaffold template — incremental swap

**File: `scripts/show_workflow.py`** — `_generator_template()`

**Incremental approach:** Keep `build_low`, `build_mid`, `build_high` as the dispatch names but swap their internals to use `resolve_phrase_style()` + `render_phrase_scene()`. This preserves the expected edit points for generators while gaining all the visual differentiation.

The scaffold template changes:

1. **Add PALETTE definition** at the top of the template (alongside existing color constants):

```python
PALETTE = build_phrase_palette(
    base_rgb=BASE_COLOR, accent_rgb=ACCENT_COLOR, hit_rgb=HIT_COLOR,
    sh_base=SH_BASE, sh_accent=SH_ACCENT, sh_hit=SH_ACCENT,
    bsw_base=BSW_BASE_C, bsw_accent=BSW_ACC_C, bsw_hit=BSW_ACC_C,
    pf_base=PF_BASE_C, pf_accent=PF_ACC_C, pf_hit=PF_ACC_C,
)
```

2. **Replace `atmo()` with `resolve_phrase_style()` + `render_phrase_scene()`** inside each builder. Builders call the two-step API (not the convenience `phrase_scene()`) because they need the resolved `style["pos_style"]` for position selection before rendering. Example for `build_low`:

```python
def build_low(sec):
    """Low energy: intro/breakdown/outro — phrase-aware scene factory."""
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 4

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        energy = avg_energy(e_rms, t, next_t)
        bars_here = max(0.25, (next_t - t) / bar)
        bars_remaining = max(0, (t_end - next_t) / bar)
        # Step-relative progress: where this step sits in the whole song
        progress = t / max(1.0, beats[-1])

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        phrase = technique.get("phrase", "intro")

        # Resolve style first, then use resolved pos_style for sweep
        style = resolve_phrase_style(phrase, energy, technique=technique,
                                      song_progress=progress,
                                      bars_left=bars_remaining)
        pos_key = pick_sweep_position(style["pos_style"], n, POS)

        sid = cached(f"low_{sec['idx']}_{n}", lambda: render_phrase_scene(
            f"{sec['name']} {n}", style, pos_key, POS, PALETTE,
            beat_idx=n, path=folder))

        br = technique.get("beat_reactivity") or {}
        step_bars = reactivity_to_bars(br.get("mover_min", "4bar"))
        steps.append((sid, timing))
        t = next_t
        n += 1
```

Same pattern for `build_mid` (default phrase="verse_groove") and `build_high` (default phrase="drop"). Each builder:
- Calls `resolve_phrase_style()` to get the style dict (reads technique, applies policy)
- Uses `style["pos_style"]` with `pick_sweep_position()` for position (not raw technique data)
- Uses step-relative `t / beats[-1]` for `song_progress` (not section-constant)
- Passes resolved `style` to `render_phrase_scene()` for fixture assembly

3. **Remove `atmo()` from the template** — it's no longer needed since the resolve+render pair replaces it.

4. **Add imports** to the template header:
```python
from showlib import (phrase_scene, build_phrase_palette,
                     pick_sweep_position, resolve_phrase_style,
                     render_phrase_scene, PLANNER_TO_PAR_LOOK, ...)
```

### Phase 6: Tests

**File: `tests/test_phrase_scene.py`** (new)

```python
# test_resolve_returns_dict — resolve_phrase_style() returns dict with all required keys
# test_phrase_signatures_differ — each of 6 phrases at same energy=0.5 produces
#     different dim, frost, par_mode, pos_style, ni3k_tilt
# test_energy_scales_dimensions — energy=0.2 vs 0.8 in same phrase differs in
#     dim, frost, color_tier, ni3k_dim
# test_drop_activates_effects — drop at e=0.85 has prism=True, strobe=True, halo="hit"
# test_intro_is_minimal — intro at e=0.2 has prism=False, lasers=False, strobe=False
# test_palette_tier_selection — e<0.35 → "base", 0.35-0.65 → "accent", >0.65 → "hit"
# test_technique_dimensions_modulate — technique with intensity="peak" raises dim floor
# test_technique_par_mode_bridge — planner blink2 maps to par_look "chase", fade8 to "solid"
# test_technique_transforms_override — technique with mirror transform → pos_style "wide"
# test_mover_family_in_style — relationship "counterpoint" → mover_family in returned dict
# test_bars_left_prism_build — build phrase with bars_left=3 and prism_gate activates prism
# test_bars_left_none_safe — bars_left=None doesn't crash, disables end-of-section effects
# test_laser_song_progress_gate — lasers only active when song_progress > 0.5
# test_render_returns_scene_dict — render_phrase_scene() returns dict with "name", "path", "fixtures"
# test_phrase_scene_convenience — phrase_scene() matches resolve + render manually
# test_sweep_filters_to_available — pick_sweep_position only returns keys in pos_tuples
# test_palette_helper — build_phrase_palette() returns correct 3-tier structure
```

**File: `tests/test_phrase_scene_integration.py`** (new)

```python
# test_scaffold_generates_and_runs — scaffold a test song, exec the generator,
#     assert .qxw exists, all 3 validators pass
# test_different_sections_produce_different_scenes — generate a show, extract
#     scene data from intro vs drop sections, assert >= 5 differing dimensions
```

## Acceptance Criteria

- [x] `resolve_phrase_style()` exists in showlib.py and returns a complete style dict
- [x] `render_phrase_scene()` exists and produces a scene dict from a style dict + palette
- [x] `phrase_scene()` exists as the convenience wrapper
- [x] At identical energy (e.g., 0.6), `resolve_phrase_style("intro", ...)` and `resolve_phrase_style("drop", ...)` differ in at least 5 keys
- [x] Energy at 0.2 vs 0.8 within the same phrase produces different dim, frost, color_tier, and effect activation
- [x] Technique `dimensions` modulate dimmer floor and effect thresholds
- [x] Technique `timing` drives PAR mode via `par_mode_from_phrase_timing()` → `PLANNER_TO_PAR_LOOK` bridge
- [x] Technique `mover_pattern.transforms` drive position sweep style (mirror/expand → wide, compress → tight)
- [x] `bars_left` parameter enables end-of-section prism and strobe in builds
- [x] Scaffold template `build_low/mid/high` use `resolve_phrase_style()` + `render_phrase_scene()` internally (preserving builder names for generator customization)
- [x] `pick_sweep_position()` filters to positions available in the venue
- [x] Drop sections activate prism, strobe, lasers (gated), halo in hit color, wide sweeps, chase pars
- [x] Intro/outro sections are minimal: static DSC, high frost, no effects, base color, dim pars
- [x] Build sections escalate toward drop: converging positions, prism in last 4 bars, strobe in last 2 bars
- [x] Breakdown sections are a clear visual reset: park DSC, high frost, base color, pars solid
- [x] Lasers only in drops, only in second half of song, only at e>0.75
- [x] All existing tests pass (180 total, 42 new)
- [x] All 3 validators pass
- [x] Regenerated Children show runs clean (120 scenes, XML valid, 6 intentional lint warnings)

## Deferred to Follow-Up

These were in the original plan but add state complexity before the baseline is validated:

- **Same-phrase repetition cycling** (rep_cycle parameter, color swaps, PAR mode toggles) — add after confirming baseline phrase differentiation works
- **Strobe governor state machine** (max 2 bars continuous, 4-bar cooldown) — needs explicit state tracking across calls; add after baseline is solid
- **Brief-to-palette automation** — currently briefs store prose; automatic color extraction would need a color-name-to-DMX mapping. Generators define palettes manually for now.

## Files to Modify

| File | Changes |
|------|---------|
| `showlib.py` | Add `PHRASE_DEFAULTS`, `resolve_phrase_style()`, `render_phrase_scene()`, `phrase_scene()`, `build_phrase_palette()`, `pick_sweep_position()`, `SWEEP_PATTERNS` |
| `scripts/show_workflow.py` | Update template: add PALETTE + imports, swap `build_low/mid/high` internals to use `resolve_phrase_style()` + `render_phrase_scene()`, remove `atmo()` |
| `tests/test_phrase_scene.py` (new) | ~16 unit tests for resolve/render/convenience/sweep/palette |
| `tests/test_phrase_scene_integration.py` (new) | 2 integration tests: scaffold+generate end-to-end, section visual differentiation |

## Dependencies & Risks

- **Existing generators are not affected.** All new functions are additive. `atmo()` remains in showlib.py for hand-written generators. Only the scaffold template changes.
- **PALETTE definition is per-generator.** Generator authors define concrete colors from the brief. `build_phrase_palette()` structures them but doesn't generate values.
- **Position keys are venue-filtered.** `pick_sweep_position()` filters patterns to available positions via `pos_tuples`. Falls back to first available if none match. No KeyError risk.
- **Technique dict is optional.** When None (unit tests, manual calls), `resolve_phrase_style()` uses `PHRASE_DEFAULTS` — still produces distinct per-phrase output.

## References

- `showlib.py:417-457` — existing `mover_look()`
- `showlib.py:460-506` — existing `par_look()`
- `showlib.py:507-560` — existing `ni3k_look()`
- `showlib.py:1727-1770` — `_serialize_planned_phrase_technique()` (full technique dict shape)
- `showlib.py:1773-1808` — existing `mover_family_from_phrase()`, `par_mode_from_phrase_timing()`
- `scripts/show_workflow.py:294-408` — scaffold template `atmo()` + `build_low/mid/high`
- `scripts/show_workflow.py:410-494` — scaffold dispatch loop + transition insertion
- `qlc_runtime/phrase_planner.py:296-319` — `classify_phrase()` mapping
- `references/data/phrase-rules.json` — technique pools and beat_reactivity per phrase
- `docs/solutions/logic-errors/scaffold-song-sync-drift-additive-transitions.md` — timing offset rule
- `docs/solutions/logic-errors/scene-timing-count-mismatch-showlib-20260220.md` — transition contract
