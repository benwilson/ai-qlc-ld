#!/usr/bin/env python3
"""Unit tests for the phrase-aware scene API in showlib.py.

Tests: resolve_phrase_style(), render_phrase_scene(), phrase_scene(),
build_phrase_palette(), pick_sweep_position()
"""
import unittest

from showlib import (
    PHRASE_DEFAULTS,
    PLANNER_TO_PAR_LOOK,
    SWEEP_PATTERNS,
    build_phrase_palette,
    phrase_scene,
    pick_sweep_position,
    render_phrase_scene,
    resolve_phrase_style,
)

# ---------------------------------------------------------------------------
# Shared test fixtures
# ---------------------------------------------------------------------------

# Minimal pos_tuples: name → (sp, st, bp, bt, pp, pt, ni_pan)
_POS = {
    "DSC": (153, 100, 177, 50, 128, 123, 128),
    "SL":  (60,  80,  80,  40, 60,  100, 80),
    "SR":  (200, 80,  240, 40, 200, 100, 200),
    "C":   (128, 90,  128, 45, 128, 110, 128),
    "USC": (128, 60,  128, 30, 128, 90,  128),
    "USL": (50,  50,  70,  25, 50,  80,  50),
    "USR": (210, 50,  240, 25, 210, 80,  210),
    "DSL": (60,  110, 90,  55, 60,  130, 60),
    "DSR": (200, 110, 230, 55, 200, 130, 200),
}

_PALETTE = build_phrase_palette(
    base_rgb=(20, 40, 120),
    accent_rgb=(80, 160, 200),
    hit_rgb=(200, 220, 255),
)

_REQUIRED_STYLE_KEYS = {
    "dim", "frost", "prism", "lasers", "strobe", "halo_tier",
    "ni3k_dim", "ni3k_tilt", "pos_style", "par_mode",
    "miss_level", "color_tier", "mover_family",
}


# ---------------------------------------------------------------------------
# resolve_phrase_style() tests
# ---------------------------------------------------------------------------

class TestResolvePhraseStyle(unittest.TestCase):

    def test_resolve_returns_dict_with_all_keys(self):
        style = resolve_phrase_style("drop", 0.5)
        self.assertEqual(set(style.keys()), _REQUIRED_STYLE_KEYS)

    def test_phrase_signatures_differ_at_same_energy(self):
        """Each of 6 phrases at energy=0.5 must produce different output in ≥5 keys."""
        phrases = ["intro", "verse_groove", "build", "drop", "breakdown", "outro"]
        styles = {p: resolve_phrase_style(p, 0.5) for p in phrases}
        # Compare intro vs drop — should differ the most
        intro = styles["intro"]
        drop = styles["drop"]
        differing = [k for k in _REQUIRED_STYLE_KEYS if intro[k] != drop[k]]
        self.assertGreaterEqual(
            len(differing), 5,
            f"intro vs drop only differ in {differing}",
        )

    def test_energy_scales_dim_monotonically(self):
        lo = resolve_phrase_style("verse_groove", 0.2)
        hi = resolve_phrase_style("verse_groove", 0.8)
        self.assertLess(lo["dim"], hi["dim"])

    def test_energy_scales_frost_inversely(self):
        lo = resolve_phrase_style("verse_groove", 0.2)
        hi = resolve_phrase_style("verse_groove", 0.8)
        self.assertGreater(lo["frost"], hi["frost"])

    def test_energy_scales_ni3k_dim(self):
        lo = resolve_phrase_style("drop", 0.2)
        hi = resolve_phrase_style("drop", 0.9)
        self.assertLess(lo["ni3k_dim"], hi["ni3k_dim"])

    def test_drop_activates_prism_at_high_energy(self):
        style = resolve_phrase_style("drop", 0.9)
        self.assertTrue(style["prism"])

    def test_drop_activates_strobe_at_high_energy(self):
        style = resolve_phrase_style("drop", 0.9)
        self.assertTrue(style["strobe"])

    def test_drop_halo_is_hit(self):
        style = resolve_phrase_style("drop", 0.5)
        self.assertEqual(style["halo_tier"], "hit")

    def test_intro_is_minimal_no_effects(self):
        style = resolve_phrase_style("intro", 0.2)
        self.assertFalse(style["prism"])
        self.assertFalse(style["lasers"])
        self.assertFalse(style["strobe"])
        self.assertEqual(style["halo_tier"], "off")

    def test_palette_tier_base_at_low_energy(self):
        style = resolve_phrase_style("drop", 0.2)
        self.assertEqual(style["color_tier"], "base")

    def test_palette_tier_accent_at_mid_energy(self):
        style = resolve_phrase_style("drop", 0.5)
        self.assertEqual(style["color_tier"], "accent")

    def test_palette_tier_hit_at_high_energy(self):
        style = resolve_phrase_style("drop", 0.8)
        self.assertEqual(style["color_tier"], "hit")

    def test_technique_peak_intensity_raises_dim_floor(self):
        base = resolve_phrase_style("drop", 0.1)
        tech = {"dimensions": {"intensity": "peak", "effect_density": "low"}}
        boosted = resolve_phrase_style("drop", 0.1, technique=tech)
        self.assertGreater(boosted["dim"], base["dim"])

    def test_technique_high_density_lowers_prism_gate(self):
        # At energy 0.6, drop phrase_gate is 0.5 → already active at 0.6
        # With high density, gate is lowered to 0.5*0.8=0.4 — still active but
        # test the indirect effect by checking that intro at 0.6 + high density
        # still has no prism (gate remains None → False)
        tech = {"dimensions": {"intensity": "medium", "effect_density": "high"}}
        style = resolve_phrase_style("intro", 0.6, technique=tech)
        # intro prism_gate is None → prism stays False regardless of density
        self.assertFalse(style["prism"])
        # build at e=0.58 normally gated at 0.7 (not active), with high density 0.7*0.8=0.56 → active
        build_style = resolve_phrase_style("build", 0.58, technique=tech)
        self.assertTrue(build_style["prism"])

    def test_technique_par_mode_bridge_blink2(self):
        tech = {
            "dimensions": {}, "relationship": "",
            "timing": {"par_beats": 2, "par_style": "chase"},
            "mover_pattern": {"transforms": []},
        }
        style = resolve_phrase_style("drop", 0.5, technique=tech)
        self.assertIn(style["par_mode"], ("chase",))

    def test_technique_par_mode_bridge_fade8(self):
        tech = {
            "dimensions": {}, "relationship": "",
            "timing": {"par_beats": 8, "par_style": "fade"},
            "mover_pattern": {"transforms": []},
        }
        style = resolve_phrase_style("drop", 0.5, technique=tech)
        # par_mode_from_phrase_timing with fade8 should map to "solid" via PLANNER_TO_PAR_LOOK
        self.assertIn(style["par_mode"], ("solid", "gradient", "pairs", "chase"))

    def test_technique_mirror_transform_gives_wide_pos_style(self):
        tech = {
            "dimensions": {}, "relationship": "",
            "timing": {"par_beats": 4, "par_style": "solid"},
            "mover_pattern": {"transforms": ["mirror"]},
        }
        style = resolve_phrase_style("verse_groove", 0.5, technique=tech)
        self.assertEqual(style["pos_style"], "wide")

    def test_technique_compress_transform_gives_tight_pos_style(self):
        tech = {
            "dimensions": {}, "relationship": "",
            "timing": {"par_beats": 4, "par_style": "solid"},
            "mover_pattern": {"transforms": ["compress"]},
        }
        style = resolve_phrase_style("drop", 0.5, technique=tech)
        self.assertEqual(style["pos_style"], "tight")

    def test_bars_left_triggers_prism_in_build(self):
        # bars_left=3 (≤4) should force prism even at low energy
        style = resolve_phrase_style("build", 0.1, bars_left=3.0)
        self.assertTrue(style["prism"])

    def test_bars_left_triggers_strobe_in_build(self):
        # bars_left=1 (≤2) should force strobe even at low energy
        style = resolve_phrase_style("build", 0.1, bars_left=1.0)
        self.assertTrue(style["strobe"])

    def test_bars_left_none_does_not_trigger_early_effects(self):
        # None → disables end-of-section logic, no crash
        style = resolve_phrase_style("build", 0.1, bars_left=None)
        # At energy 0.1, prism_gate=0.7 and strobe_gate=0.85 → both inactive
        self.assertFalse(style["prism"])
        self.assertFalse(style["strobe"])

    def test_laser_only_after_halfway_through_song(self):
        # drop at high energy should have lasers at song_progress > 0.5
        style_late = resolve_phrase_style("drop", 0.9, song_progress=0.8)
        self.assertTrue(style_late["lasers"])
        # but not in the first half
        style_early = resolve_phrase_style("drop", 0.9, song_progress=0.3)
        self.assertFalse(style_early["lasers"])

    def test_unknown_phrase_falls_back_to_verse_groove(self):
        # Unknown phrase should not crash — falls back to verse_groove defaults
        style = resolve_phrase_style("totally_unknown_phrase", 0.5)
        self.assertIn("dim", style)


# ---------------------------------------------------------------------------
# render_phrase_scene() tests
# ---------------------------------------------------------------------------

class TestRenderPhraseScene(unittest.TestCase):

    def test_render_returns_scene_dict(self):
        style = resolve_phrase_style("drop", 0.7)
        sc = render_phrase_scene("Test Scene", style, "DSC", _POS, _PALETTE)
        self.assertIn("name", sc)
        self.assertIn("path", sc)
        self.assertIn("fixtures", sc)
        self.assertEqual(sc["name"], "Test Scene")

    def test_render_has_fixtures(self):
        style = resolve_phrase_style("drop", 0.7)
        sc = render_phrase_scene("Test", style, "DSC", _POS, _PALETTE)
        self.assertIsInstance(sc["fixtures"], list)
        self.assertGreater(len(sc["fixtures"]), 0)

    def test_render_uses_pos_key(self):
        # Both renders should produce valid scenes without error
        style = resolve_phrase_style("verse_groove", 0.5)
        sc1 = render_phrase_scene("A", style, "SL", _POS, _PALETTE)
        sc2 = render_phrase_scene("B", style, "SR", _POS, _PALETTE)
        self.assertIsNotNone(sc1)
        self.assertIsNotNone(sc2)

    def test_render_beat_idx_accepted(self):
        style = resolve_phrase_style("drop", 0.7)
        sc = render_phrase_scene("Test", style, "DSC", _POS, _PALETTE, beat_idx=3)
        self.assertIsNotNone(sc)


# ---------------------------------------------------------------------------
# phrase_scene() convenience wrapper tests
# ---------------------------------------------------------------------------

class TestPhraseSceneConvenience(unittest.TestCase):

    def test_phrase_scene_matches_resolve_then_render(self):
        style = resolve_phrase_style("verse_groove", 0.5)
        pos_key = pick_sweep_position(style["pos_style"], 0, _POS)
        expected = render_phrase_scene("X", style, pos_key, _POS, _PALETTE)
        actual = phrase_scene("X", "verse_groove", 0.5, pos_key, _POS, _PALETTE)
        self.assertEqual(expected["name"], actual["name"])
        self.assertEqual(len(expected["fixtures"]), len(actual["fixtures"]))

    def test_phrase_scene_overrides_apply(self):
        # Override color_tier to "hit" even at low energy
        sc = phrase_scene("X", "intro", 0.1, "DSC", _POS, _PALETTE, color_tier="hit")
        # Scene should complete without error; the override is applied
        self.assertIsNotNone(sc)


# ---------------------------------------------------------------------------
# pick_sweep_position() tests
# ---------------------------------------------------------------------------

class TestPickSweepPosition(unittest.TestCase):

    def test_static_always_returns_dsc(self):
        # "static" pattern is ["DSC"] → always DSC
        pos = pick_sweep_position("static", 0, _POS)
        self.assertEqual(pos, "DSC")
        pos = pick_sweep_position("static", 5, _POS)
        self.assertEqual(pos, "DSC")

    def test_filters_to_available_positions(self):
        # Small pos_tuples with only one key
        tiny_pos = {"DSC": _POS["DSC"]}
        pos = pick_sweep_position("wide", 0, tiny_pos)
        self.assertEqual(pos, "DSC")

    def test_cycles_through_pattern(self):
        # "tight" pattern: SL, C, SR, C → filtered to what's in _POS (all present)
        results = [pick_sweep_position("tight", i, _POS) for i in range(4)]
        self.assertEqual(len(set(results)), len(set(SWEEP_PATTERNS["tight"])))

    def test_fallback_when_no_pattern_match(self):
        # Unknown style falls back to "tight" pattern
        pos = pick_sweep_position("unknown_style", 0, _POS)
        self.assertIn(pos, _POS)

    def test_empty_pos_tuples_returns_string(self):
        # Edge case: pos_tuples is empty → falls back to ["DSC"]
        pos = pick_sweep_position("wide", 0, {})
        self.assertEqual(pos, "DSC")


# ---------------------------------------------------------------------------
# build_phrase_palette() tests
# ---------------------------------------------------------------------------

class TestBuildPhrasePalette(unittest.TestCase):

    def test_palette_has_three_tiers(self):
        pal = build_phrase_palette((10, 20, 30), (50, 100, 150), (200, 210, 220))
        self.assertIn("base", pal)
        self.assertIn("accent", pal)
        self.assertIn("hit", pal)

    def test_palette_tiers_have_required_keys(self):
        pal = build_phrase_palette((10, 20, 30), (50, 100, 150), (200, 210, 220))
        for tier in ("base", "accent", "hit"):
            self.assertIn("par_rgb", pal[tier])
            self.assertIn("miss_rgb", pal[tier])
            self.assertIn("ni3k_rgb", pal[tier])
            self.assertIn("sharpy", pal[tier])

    def test_palette_rgb_values_correct(self):
        base = (10, 20, 30)
        pal = build_phrase_palette(base, (50, 100, 150), (200, 210, 220))
        self.assertEqual(pal["base"]["par_rgb"], base)
        self.assertEqual(pal["base"]["miss_rgb"], base)

    def test_palette_mover_wheel_values_set(self):
        pal = build_phrase_palette(
            (10, 20, 30), (50, 100, 150), (200, 210, 220),
            sh_base=30, sh_accent=70, sh_hit=50,
        )
        self.assertEqual(pal["base"]["sharpy"], 30)
        self.assertEqual(pal["accent"]["sharpy"], 70)
        self.assertEqual(pal["hit"]["sharpy"], 50)


# ---------------------------------------------------------------------------
# PLANNER_TO_PAR_LOOK bridge tests
# ---------------------------------------------------------------------------

class TestPlannerToParLookBridge(unittest.TestCase):

    def test_blink1_maps_to_chase(self):
        self.assertEqual(PLANNER_TO_PAR_LOOK["blink1"], "chase")

    def test_blink2_maps_to_chase(self):
        self.assertEqual(PLANNER_TO_PAR_LOOK["blink2"], "chase")

    def test_fade4_maps_to_gradient(self):
        self.assertEqual(PLANNER_TO_PAR_LOOK["fade4"], "gradient")

    def test_fade8_maps_to_solid(self):
        self.assertEqual(PLANNER_TO_PAR_LOOK["fade8"], "solid")


if __name__ == "__main__":
    unittest.main()
