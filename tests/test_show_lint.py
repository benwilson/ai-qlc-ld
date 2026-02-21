#!/usr/bin/env python3
"""Tests for show linting (Part 1), beat reactivity (Part 2), and scene helpers (Part 3)."""

import unittest

from showlib import (
    # Part 1: Lint
    validate_show, DEFAULT_LINT, _scene_ch,
    # Part 2: Reactivity
    REACTIVITY_BARS, reactivity_to_bars,
    # Part 3: Helpers
    mover_look, par_look, ni3k_look,
    # Core
    scene, make_chaser, hold, snap, smooth, bpm_to_ms,
    sharpy, bsw, profile, fourbar_solid, miss1, miss2, ni3k,
    dark_sharpy, dark_bsw, dark_profile, dark_ni3k, blackout_all,
    # Constants
    FX_SHARPY, FX_BSW, FX_PROFILE, FX_NI3K, FX_4BAR, FX_MISS1, FX_MISS2,
    SHARPY_OPEN, BSW_SHUT_OPEN, PROFILE_STROBE_OFF,
    H_OFF, H_BLU, H_CYN, LASER_OFF, LASER_ON,
    SHARPY_BLUE, BSW_BLUE, PROF_BLUE,
    WHITE, BLUE, CYAN, OFF,
)


# Fake focus position tuples for testing (7-tuple per position)
FAKE_POS = {
    "DSC": (158, 6, 179, 27, 64, 145, 128),
    "C":   (153, 0, 177, 19, 0, 123, 128),
    "SL":  (100, 10, 120, 25, 30, 130, 80),
}

BPM = 128


def _good_scene(name, pos="DSC"):
    """A lively scene: all movers active, pars on, NI3K visible."""
    p = FAKE_POS[pos]
    return scene(name,
        sharpy(pan=p[0], tilt=p[1], dim=200),
        bsw(pan=p[2], tilt=p[3], dim=180),
        profile(pan=p[4], tilt=p[5], dim=150),
        fourbar_solid(*BLUE, master=200),
        miss1(*CYAN, master=100),
        miss2(*CYAN, master=100),
        ni3k(pan=p[6], dim=160, r=0, g=200, b=255),
    )


def _solo_scene(name, pos="DSC"):
    """Only Sharpy active; BSW + Profile dark."""
    p = FAKE_POS[pos]
    return scene(name,
        sharpy(pan=p[0], tilt=p[1], dim=200),
        dark_bsw(pan=p[2], tilt=p[3]),
        dark_profile(pan=p[4], tilt=p[5]),
        fourbar_solid(*BLUE, master=200),
        miss1(*CYAN, master=100),
        miss2(*CYAN, master=100),
        ni3k(pan=p[6], dim=160, r=0, g=200, b=255),
    )


# =========================================================================
# Part 1: Post-generation show linting
# =========================================================================

class TestSceneCh(unittest.TestCase):
    def test_extracts_known_channel(self):
        sc = _good_scene("test")
        self.assertEqual(_scene_ch(sc, FX_SHARPY, 7), 200)  # dim

    def test_returns_none_for_missing_fixture(self):
        sc = scene("empty", fourbar_solid(*BLUE))
        self.assertIsNone(_scene_ch(sc, FX_SHARPY, 7))

    def test_returns_none_for_missing_channel(self):
        sc = _good_scene("test")
        self.assertIsNone(_scene_ch(sc, FX_SHARPY, 99))


class TestValidateShow(unittest.TestCase):

    def test_clean_show_no_warnings(self):
        scenes_list = [
            _good_scene("S0", "DSC"),
            _good_scene("S1", "SL"),
            _good_scene("S2", "C"),
            _good_scene("S3", "DSC"),
        ]
        ch = make_chaser("Main", [0, 1, 2, 3],
                         [hold(BPM, 1)] * 4, path="Test")
        warnings = validate_show(scenes_list, [ch], bpm=BPM)
        self.assertEqual(warnings, [])

    def test_solo_mover_warning(self):
        scenes_list = [_solo_scene(f"S{i}") for i in range(4)]
        ch = make_chaser("Main", [0, 1, 2, 3],
                         [hold(BPM, 1)] * 4, path="Test")
        warnings = validate_show(scenes_list, [ch], bpm=BPM)
        solo_warnings = [w for w in warnings if w.startswith("SOLO_MOVER")]
        self.assertTrue(len(solo_warnings) > 0, f"Expected SOLO_MOVER, got: {warnings}")

    def test_solo_mover_short_run_ok(self):
        """2 solo steps (at the limit) should NOT warn."""
        scenes_list = [
            _solo_scene("S0"),
            _solo_scene("S1"),
            _good_scene("S2", "C"),
            _good_scene("S3", "SL"),
        ]
        ch = make_chaser("Main", [0, 1, 2, 3],
                         [hold(BPM, 1)] * 4, path="Test")
        warnings = validate_show(scenes_list, [ch], bpm=BPM)
        solo_warnings = [w for w in warnings if w.startswith("SOLO_MOVER")]
        self.assertEqual(solo_warnings, [])

    def test_static_pos_warning(self):
        """All movers at same position for 6 steps should warn."""
        scenes_list = [_good_scene(f"S{i}", "DSC") for i in range(6)]
        ch = make_chaser("Main", list(range(6)),
                         [hold(BPM, 1)] * 6, path="Test")
        warnings = validate_show(scenes_list, [ch], bpm=BPM)
        static_warnings = [w for w in warnings if w.startswith("STATIC_POS")]
        self.assertTrue(len(static_warnings) > 0, f"Expected STATIC_POS, got: {warnings}")

    def test_static_pos_movement_ok(self):
        """Alternating positions should not warn."""
        scenes_list = [
            _good_scene("S0", "DSC"),
            _good_scene("S1", "SL"),
            _good_scene("S2", "C"),
            _good_scene("S3", "DSC"),
        ]
        ch = make_chaser("Main", [0, 1, 2, 3],
                         [hold(BPM, 1)] * 4, path="Test")
        warnings = validate_show(scenes_list, [ch], bpm=BPM)
        static_warnings = [w for w in warnings if w.startswith("STATIC_POS")]
        self.assertEqual(static_warnings, [])

    def test_long_step_warning(self):
        """A step > 2.5 bars should produce LONG_STEP."""
        scenes_list = [_good_scene("S0"), _good_scene("S1", "SL")]
        ch = make_chaser("Main", [0, 1],
                         [hold(BPM, 3), hold(BPM, 1)], path="Test")
        warnings = validate_show(scenes_list, [ch], bpm=BPM)
        long_warnings = [w for w in warnings if w.startswith("LONG_STEP")]
        self.assertTrue(len(long_warnings) > 0, f"Expected LONG_STEP, got: {warnings}")

    def test_long_step_within_limit_ok(self):
        scenes_list = [_good_scene("S0"), _good_scene("S1", "SL")]
        ch = make_chaser("Main", [0, 1],
                         [hold(BPM, 2), hold(BPM, 2)], path="Test")
        warnings = validate_show(scenes_list, [ch], bpm=BPM)
        long_warnings = [w for w in warnings if w.startswith("LONG_STEP")]
        self.assertEqual(long_warnings, [])

    def test_par_inactive_warning(self):
        """Steps with all pars off for >4 steps should warn."""
        def _par_off_scene(name, pos="DSC"):
            p = FAKE_POS[pos]
            return scene(name,
                sharpy(pan=p[0], tilt=p[1], dim=200),
                bsw(pan=p[2], tilt=p[3], dim=180),
                profile(pan=p[4], tilt=p[5], dim=150),
                fourbar_solid(0, 0, 0, master=0),
                miss1(0, 0, 0, master=0),
                miss2(0, 0, 0, master=0),
                ni3k(pan=p[6], dim=160),
            )
        scenes_list = [_par_off_scene(f"S{i}") for i in range(6)]
        ch = make_chaser("Main", list(range(6)),
                         [hold(BPM, 1)] * 6, path="Test")
        warnings = validate_show(scenes_list, [ch], bpm=BPM)
        par_warnings = [w for w in warnings if w.startswith("PAR_OFF")]
        self.assertTrue(len(par_warnings) > 0, f"Expected PAR_OFF, got: {warnings}")

    def test_ni3k_absent_warning(self):
        """NI3K dark for >25% of steps should warn."""
        def _ni3k_off_scene(name, pos="DSC"):
            p = FAKE_POS[pos]
            return scene(name,
                sharpy(pan=p[0], tilt=p[1], dim=200),
                bsw(pan=p[2], tilt=p[3], dim=180),
                profile(pan=p[4], tilt=p[5], dim=150),
                fourbar_solid(*BLUE, master=200),
                miss1(*CYAN, master=100),
                miss2(*CYAN, master=100),
                dark_ni3k(pan=p[6]),
            )
        # 4 out of 5 steps with NI3K dark = 80% > 25%
        scenes_list = [
            _ni3k_off_scene("S0"),
            _ni3k_off_scene("S1"),
            _ni3k_off_scene("S2"),
            _ni3k_off_scene("S3"),
            _good_scene("S4", "SL"),
        ]
        ch = make_chaser("Main", list(range(5)),
                         [hold(BPM, 1)] * 5, path="Test")
        warnings = validate_show(scenes_list, [ch], bpm=BPM)
        ni3k_warnings = [w for w in warnings if w.startswith("NI3K_OFF")]
        self.assertTrue(len(ni3k_warnings) > 0, f"Expected NI3K_OFF, got: {warnings}")

    def test_custom_lint_thresholds(self):
        """Custom lint dict should override defaults."""
        scenes_list = [_solo_scene(f"S{i}") for i in range(4)]
        ch = make_chaser("Main", [0, 1, 2, 3],
                         [hold(BPM, 1)] * 4, path="Test")
        # Raise solo threshold so 4 steps is OK
        warnings = validate_show(scenes_list, [ch], bpm=BPM,
                                  lint={"solo_mover_max_run": 10})
        solo_warnings = [w for w in warnings if w.startswith("SOLO_MOVER")]
        self.assertEqual(solo_warnings, [])

    def test_empty_chaser_no_crash(self):
        warnings = validate_show([], [], bpm=BPM)
        self.assertEqual(warnings, [])

    def test_none_chasers_no_crash(self):
        warnings = validate_show([], None, bpm=BPM)
        self.assertEqual(warnings, [])


# =========================================================================
# Part 2: Beat reactivity conversion
# =========================================================================

class TestReactivityToBars(unittest.TestCase):

    def test_known_values(self):
        self.assertEqual(reactivity_to_bars("beat"), 0.25)
        self.assertEqual(reactivity_to_bars("2beat"), 0.5)
        self.assertEqual(reactivity_to_bars("bar"), 1)
        self.assertEqual(reactivity_to_bars("2bar"), 2)
        self.assertEqual(reactivity_to_bars("4bar"), 4)

    def test_unknown_returns_default(self):
        self.assertEqual(reactivity_to_bars("unknown"), 2)
        self.assertEqual(reactivity_to_bars(""), 2)

    def test_reactivity_bars_dict_complete(self):
        self.assertEqual(len(REACTIVITY_BARS), 5)


# =========================================================================
# Part 3a: mover_look() helper
# =========================================================================

class TestMoverLook(unittest.TestCase):

    def test_returns_three_fixtures(self):
        result = mover_look("DSC", FAKE_POS)
        self.assertEqual(len(result), 3)
        ids = [r[0] for r in result]
        self.assertIn(FX_SHARPY, ids)
        self.assertIn(FX_BSW, ids)
        self.assertIn(FX_PROFILE, ids)

    def test_position_from_tuples(self):
        result = mover_look("SL", FAKE_POS, dims=(200, 180, 150))
        sharpy_data = [r for r in result if r[0] == FX_SHARPY][0]
        ch_map = dict(sharpy_data[1])
        self.assertEqual(ch_map[0], 100)  # SL sharpy pan
        self.assertEqual(ch_map[1], 10)   # SL sharpy tilt

    def test_solo_dims(self):
        """dims=(200, 0, 0) should still return all 3 fixtures."""
        result = mover_look("DSC", FAKE_POS, dims=(200, 0, 0))
        self.assertEqual(len(result), 3)
        bsw_data = [r for r in result if r[0] == FX_BSW][0]
        ch_map = dict(bsw_data[1])
        self.assertEqual(ch_map[17], 0)  # BSW dim = 0

    def test_prism_enabled(self):
        result = mover_look("DSC", FAKE_POS, prism=True)
        sharpy_data = [r for r in result if r[0] == FX_SHARPY][0]
        ch_map = dict(sharpy_data[1])
        self.assertEqual(ch_map[11], 128)  # prism1

    def test_custom_strobes(self):
        result = mover_look("DSC", FAKE_POS, strobes=(0, 0, 0))
        sharpy_data = [r for r in result if r[0] == FX_SHARPY][0]
        ch_map = dict(sharpy_data[1])
        self.assertEqual(ch_map[6], 0)  # sharpy strobe closed

    def test_fallback_to_C(self):
        """Unknown pos_key should fall back to 'C'."""
        result = mover_look("NONEXISTENT", FAKE_POS)
        sharpy_data = [r for r in result if r[0] == FX_SHARPY][0]
        ch_map = dict(sharpy_data[1])
        self.assertEqual(ch_map[0], 153)  # C sharpy pan

    def test_default_strobes_are_open(self):
        result = mover_look("DSC", FAKE_POS)
        sharpy_data = [r for r in result if r[0] == FX_SHARPY][0]
        bsw_data = [r for r in result if r[0] == FX_BSW][0]
        prof_data = [r for r in result if r[0] == FX_PROFILE][0]
        self.assertEqual(dict(sharpy_data[1])[6], SHARPY_OPEN)
        self.assertEqual(dict(bsw_data[1])[16], BSW_SHUT_OPEN)
        self.assertEqual(dict(prof_data[1])[1], PROFILE_STROBE_OFF)

    def test_colors_applied(self):
        result = mover_look("DSC", FAKE_POS,
                            colors=(SHARPY_BLUE, BSW_BLUE, PROF_BLUE))
        sharpy_data = [r for r in result if r[0] == FX_SHARPY][0]
        self.assertEqual(dict(sharpy_data[1])[8], SHARPY_BLUE)  # colormacro

    def test_usable_in_scene(self):
        """mover_look output should unpack into scene() with *."""
        s = scene("test", *mover_look("DSC", FAKE_POS))
        self.assertEqual(len(s["fixtures"]), 3)


# =========================================================================
# Part 3b: par_look() helper
# =========================================================================

class TestParLook(unittest.TestCase):

    def test_solid_returns_three(self):
        result = par_look("solid", BLUE)
        self.assertEqual(len(result), 3)
        ids = [r[0] for r in result]
        self.assertIn(FX_4BAR, ids)
        self.assertIn(FX_MISS1, ids)
        self.assertIn(FX_MISS2, ids)

    def test_pairs_mode(self):
        result = par_look("pairs", BLUE, CYAN, master=200)
        self.assertEqual(len(result), 3)

    def test_gradient_mode(self):
        result = par_look("gradient", BLUE, CYAN)
        self.assertEqual(len(result), 3)

    def test_chase_returns_three(self):
        for i in range(6):
            result = par_look("chase", WHITE, beat_idx=i)
            self.assertEqual(len(result), 3)

    def test_chase_active_fixture_is_bright(self):
        """beat_idx=0 should have P1 at full brightness."""
        result = par_look("chase", (200, 200, 200), beat_idx=0)
        fourbar_data = [r for r in result if r[0] == FX_4BAR][0]
        ch_map = dict(fourbar_data[1])
        self.assertEqual(ch_map[3], 200)  # P1 Red = full
        self.assertEqual(ch_map[6], 50)   # P2 Red = quarter

    def test_chase_missyee_active(self):
        """beat_idx=4 should activate miss1."""
        result = par_look("chase", (200, 100, 0), beat_idx=4)
        m1_data = [r for r in result if r[0] == FX_MISS1][0]
        ch_map = dict(m1_data[1])
        self.assertEqual(ch_map[1], 200)  # Red = full

    def test_chase_missyee2_active(self):
        """beat_idx=5 should activate miss2."""
        result = par_look("chase", (200, 100, 0), beat_idx=5)
        m2_data = [r for r in result if r[0] == FX_MISS2][0]
        ch_map = dict(m2_data[1])
        self.assertEqual(ch_map[1], 200)  # Red = full

    def test_miss_color_override(self):
        result = par_look("solid", BLUE, miss_color=CYAN, miss_master=50)
        m1_data = [r for r in result if r[0] == FX_MISS1][0]
        ch_map = dict(m1_data[1])
        self.assertEqual(ch_map[0], 50)   # master
        self.assertEqual(ch_map[1], 0)    # R (CYAN = 0,255,255)
        self.assertEqual(ch_map[2], 255)  # G

    def test_usable_in_scene(self):
        """par_look output should unpack into scene() with *."""
        s = scene("test", *par_look("solid", BLUE))
        self.assertEqual(len(s["fixtures"]), 3)


# =========================================================================
# Part 3c: ni3k_look() helper
# =========================================================================

class TestNi3kLook(unittest.TestCase):

    def test_returns_single_tuple(self):
        result = ni3k_look("DSC", FAKE_POS)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], FX_NI3K)

    def test_static_tilt(self):
        result = ni3k_look("DSC", FAKE_POS, tilt_values=(30, 60, 90))
        ch_map = dict(result[1])
        self.assertEqual(ch_map[1], 30)
        self.assertEqual(ch_map[2], 60)
        self.assertEqual(ch_map[3], 90)

    def test_spread_tilt(self):
        result = ni3k_look("DSC", FAKE_POS, tilt_mode="spread")
        ch_map = dict(result[1])
        self.assertEqual(ch_map[1], 40)
        self.assertEqual(ch_map[2], 64)
        self.assertEqual(ch_map[3], 88)

    def test_spin_tilt(self):
        result = ni3k_look("DSC", FAKE_POS, tilt_mode="spin")
        ch_map = dict(result[1])
        self.assertEqual(ch_map[1], 160)
        self.assertEqual(ch_map[2], 180)
        self.assertEqual(ch_map[3], 200)

    def test_lasers_on(self):
        result = ni3k_look("DSC", FAKE_POS, lasers=True)
        ch_map = dict(result[1])
        self.assertEqual(ch_map[14], LASER_ON)
        self.assertEqual(ch_map[15], LASER_ON)
        self.assertEqual(ch_map[16], LASER_ON)

    def test_lasers_off_by_default(self):
        result = ni3k_look("DSC", FAKE_POS)
        ch_map = dict(result[1])
        self.assertEqual(ch_map[14], LASER_OFF)

    def test_position_from_tuples(self):
        result = ni3k_look("SL", FAKE_POS)
        ch_map = dict(result[1])
        self.assertEqual(ch_map[0], 80)  # SL ni3k pan

    def test_usable_in_scene(self):
        """ni3k_look output should be usable directly in scene() (no * unpack)."""
        s = scene("test", ni3k_look("DSC", FAKE_POS))
        self.assertEqual(len(s["fixtures"]), 1)
        self.assertEqual(s["fixtures"][0][0], FX_NI3K)


# =========================================================================
# Integration: all three helpers in one scene
# =========================================================================

class TestCombinedHelpers(unittest.TestCase):

    def test_full_scene_with_all_helpers(self):
        """All three helpers compose into a single scene with all 7 fixtures."""
        s = scene("Full Look",
            *mover_look("DSC", FAKE_POS,
                        colors=(SHARPY_BLUE, BSW_BLUE, PROF_BLUE),
                        dims=(230, 200, 150)),
            *par_look("solid", CYAN, master=220),
            ni3k_look("DSC", FAKE_POS, rgb=CYAN, dim=160,
                      halo=H_CYN, tilt_mode="spin"),
        )
        ids = [f[0] for f in s["fixtures"]]
        self.assertEqual(len(ids), 7)
        for fx in [FX_BSW, FX_4BAR, FX_NI3K, FX_PROFILE, FX_MISS1, FX_MISS2, FX_SHARPY]:
            self.assertIn(fx, ids)


if __name__ == "__main__":
    unittest.main()
