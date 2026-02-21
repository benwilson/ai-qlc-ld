#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from pathlib import Path

import showlib
from qlc_runtime.phrase_planner import (
    BeatReactivity,
    CONTRAST_DIMENSIONS,
    PHRASE_CLASSES,
    MOVER_TRANSFORM_TOKENS,
    PhraseAwarePlanner,
    TransitionEvent,
    family_from_phrase_and_relationship,
    parse_timing_recipe,
    par_mode_from_timing,
)


ROOT = Path(__file__).resolve().parents[1]


class PhrasePlannerCoreTests(unittest.TestCase):

    def test_loads_and_has_all_phrase_pools(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        self.assertEqual(set(planner.phrase_pools.keys()), set(PHRASE_CLASSES))
        for phrase in PHRASE_CLASSES:
            self.assertTrue(planner.phrase_pools[phrase])
        self.assertGreaterEqual(len(planner.designer_packs), 10)

    def test_phrase_classification_uses_expected_buckets(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        self.assertEqual(planner.classify_phrase("intro", rms=0.1, sub=0.1, high=0.1, progress=0.02), "intro")
        self.assertEqual(planner.classify_phrase("verse", rms=0.4, sub=0.3, high=0.3, progress=0.3), "verse_groove")
        self.assertEqual(planner.classify_phrase("chorus", rms=0.8, sub=0.7, high=0.4, progress=0.5), "drop")
        self.assertEqual(planner.classify_phrase("break", rms=0.2, sub=0.2, high=0.2, progress=0.6), "breakdown")
        self.assertEqual(planner.classify_phrase("outro", rms=0.1, sub=0.1, high=0.1, progress=0.95), "outro")
        self.assertEqual(planner.classify_phrase("inst", rms=0.78, sub=0.66, high=0.35, progress=0.4), "drop")
        self.assertEqual(planner.classify_phrase("inst", rms=0.22, sub=0.18, high=0.15, progress=0.55), "breakdown")

    def test_pick_technique_is_enforced_by_phrase_pool(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        phrase = "build"
        planned = planner.pick_technique(phrase=phrase, segment_index=3, global_bar=28)
        self.assertIn(planned.technique_id, planner.phrase_pools[phrase])
        self.assertIn(planned.relationship, {"unison", "counterpoint", "inclusion"})
        self.assertGreaterEqual(planned.timing.mover_beats, 1)
        self.assertGreaterEqual(planned.timing.par_beats, 1)
        self.assertTrue(planned.mover_pattern.base_route.startswith("R"))
        self.assertTrue(set(planned.mover_pattern.transforms).issubset(set(MOVER_TRANSFORM_TOKENS)))
        self.assertGreaterEqual(planned.candidate_count, 3)
        self.assertEqual(planned.candidate_rank, 1)
        self.assertGreaterEqual(planned.score.total, 0.0)
        self.assertLessEqual(planned.score.total, 1.0)
        self.assertIn(planned.designer_role, {"dominant", "contrast", "none"})
        if planned.designer_pack_id:
            self.assertTrue(planned.designer_ld_id.startswith("LD-"))

    def test_pick_technique_balances_without_forcing_full_uniqueness(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        pool = planner.phrase_pools["drop"]
        usage = {tech_id: 10 for tech_id in pool}
        usage[pool[-1]] = 0
        planned = planner.pick_technique(
            phrase="drop", segment_index=0, global_bar=0,
            usage=usage, recent=[pool[0], pool[1]], cooldown=2,
        )
        self.assertEqual(planned.technique_id, pool[-1])
        planned = planner.pick_technique(
            phrase="drop", segment_index=0, global_bar=0,
            usage=None, recent=[pool[0]], cooldown=1,
        )
        if len(pool) > 1:
            self.assertNotEqual(planned.technique_id, pool[0])

    def test_planner_generates_three_scored_candidates_and_picks_top(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        show_key = "unit_test_song"
        candidates = planner.plan_candidates(
            phrase="drop", segment_index=5, global_bar=44,
            candidate_count=3, show_key=show_key,
        )
        self.assertEqual(len(candidates), 3)
        self.assertEqual([row.candidate_rank for row in candidates], [1, 2, 3])
        self.assertGreaterEqual(candidates[0].score.total, candidates[1].score.total)
        self.assertGreaterEqual(candidates[1].score.total, candidates[2].score.total)
        picked = planner.pick_technique(
            phrase="drop", segment_index=5, global_bar=44,
            candidate_count=3, show_key=show_key,
        )
        self.assertEqual(picked.technique_id, candidates[0].technique_id)
        self.assertEqual(picked.designer_pack_id, candidates[0].designer_pack_id)

    def test_select_show_designer_packs_returns_dominant_and_contrast(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        selected = planner.select_show_designer_packs(
            show_key="designer_pack_test",
            brand_tokens=["melodic", "techno", "space"],
            pack_usage={"DTP-001": 3},
            pack_recent=["DTP-001", "DTP-002"],
            pack_cooldown=2,
        )
        self.assertTrue(selected["dominant"])
        self.assertGreaterEqual(len(selected["dominant"]), 1)
        self.assertLessEqual(len(selected["dominant"]), 2)
        self.assertIsNotNone(selected["contrast"])

    def test_creative_directives_influence_candidate_scoring(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        show_key = "creative_directive_test"
        neutral = planner.plan_candidates(
            phrase="drop", segment_index=6, global_bar=48,
            show_key=show_key, candidate_count=3,
        )
        constrained = planner.plan_candidates(
            phrase="drop", segment_index=6, global_bar=48,
            show_key=show_key, candidate_count=3,
            creative_directives={
                "must_include": ["PAR behavior cycling fade/chase at 1, 2, or 4 beats"],
                "avoid": ["continuous rainbow cycling"],
                "do_not_copy": ["signature set pieces"],
                "direction_notes": ["lane-based beam architecture with center reunions"],
                "brand_alignment_score": 4.5,
            },
        )
        self.assertGreaterEqual(neutral[0].score.creative_fit, 0.0)
        self.assertGreaterEqual(constrained[0].score.creative_fit, 0.0)
        self.assertNotEqual(constrained[0].score.total, neutral[0].score.total)

    def test_phrase_change_contrast_enforces_two_dimension_changes(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        first = planner.pick_technique(phrase="intro", segment_index=0, global_bar=0)
        second = planner.pick_technique(
            phrase="drop", segment_index=1, global_bar=8,
            previous=first, candidate_count=3,
        )
        self.assertGreaterEqual(len(second.changed_dimensions), 2)
        self.assertTrue(set(second.changed_dimensions).issubset(set(CONTRAST_DIMENSIONS)))

    def test_timing_and_mode_helpers(self):
        timing = parse_timing_recipe("movers=4b, pars=1b chase")
        self.assertEqual(timing.mover_beats, 4)
        self.assertEqual(timing.par_beats, 1)
        self.assertEqual(timing.par_style, "chase")
        self.assertEqual(par_mode_from_timing(timing=timing, phrase="drop", seg_bar_idx=0), "blink1")
        timing = parse_timing_recipe("movers=4b, pars=4b fade")
        self.assertIn(par_mode_from_timing(timing=timing, phrase="intro", seg_bar_idx=0), {"fade4", "fade8"})

    def test_family_mapping_helpers(self):
        self.assertEqual(family_from_phrase_and_relationship("intro", "unison", rms=0.2, sub=0.2), "atmospheric")
        self.assertEqual(family_from_phrase_and_relationship("drop", "inclusion", rms=0.8, sub=0.7), "snap")
        self.assertIn(
            family_from_phrase_and_relationship("verse_groove", "counterpoint", rms=0.6, sub=0.4),
            {"snap", "geometric"},
        )


class ShowlibWrapperTests(unittest.TestCase):

    @patch("showlib._record_designer_pack_usage_once")
    def test_wrappers_expose_phrase_planner(self, _mock_record):
        phrase = showlib.classify_phrase(
            segment_label="chorus", rms=0.82, sub=0.71, high=0.33,
            progress=0.56, project_root=str(ROOT),
        )
        self.assertEqual(phrase, "drop")
        technique = showlib.pick_phrase_technique(
            phrase=phrase, segment_index=4, global_bar=40, project_root=str(ROOT),
        )
        self.assertEqual(technique["phrase"], "drop")
        self.assertTrue(technique["id"].startswith("INT-"))
        self.assertGreaterEqual(technique["timing"]["par_beats"], 1)
        self.assertGreaterEqual(technique["candidate_count"], 3)
        self.assertIn("mover_pattern", technique)
        self.assertIn("score", technique)
        self.assertIn("creative_fit", technique["score"])
        self.assertIn("designer_pack", technique)
        self.assertEqual(set(technique["dimensions"].keys()), set(CONTRAST_DIMENSIONS))
        candidates = showlib.pick_phrase_technique_candidates(
            phrase=phrase, segment_index=4, global_bar=40, project_root=str(ROOT),
        )
        self.assertGreaterEqual(len(candidates), 3)
        self.assertEqual(candidates[0]["candidate_rank"], 1)
        packs = showlib.pick_show_designer_packs(
            show_key="wrapper_show_test",
            brand_tokens=["dark", "melodic", "space"],
            project_root=str(ROOT),
        )
        self.assertTrue(packs["dominant"])
        self.assertIsNotNone(packs["contrast"])

    def test_build_creative_context_uses_full_brief(self):
        brief = {
            "artist": "Daniel Portman",
            "song_title": "Loyalty",
            "thesis": "Center returns represent loyalty through disciplined geometry.",
            "artist_branding": {
                "summary": "Progressive-house control with clean beam lanes.",
                "visual_cues": ["Dark base states", "Symmetry", "Lane architecture"],
                "do_not_copy": ["Avoid direct cloning of signature stage objects."],
            },
            "song_title_inspiration": {
                "keywords": ["loyalty", "return"],
                "motifs": ["Center reunions", "4-beat route discipline"],
            },
            "visual_direction": {
                "color_story": "Steel-indigo to white crest.",
                "motion_story": "4-beat quantized routes with inclusion bursts.",
                "staging_story": "PAR anchor with mover lead narration.",
            },
            "style_constraints": {
                "must_include": ["PAR fade/chase 1,2,4 beats", "Inclusion phrases"],
                "avoid": ["Continuous rainbow cycling"],
            },
            "brand_alignment_score": 4.2,
        }
        context = showlib.build_creative_context(brief, song_stem="Daniel Portman - Loyalty")
        self.assertTrue(context["brand_tokens"])
        directives = context["creative_directives"]
        self.assertTrue(directives["must_include"])
        self.assertTrue(directives["avoid"])
        self.assertTrue(directives["do_not_copy"])
        self.assertTrue(directives["direction_notes"])
        self.assertGreater(directives["brand_alignment_weight"], 0.0)


class TransitionEventTests(unittest.TestCase):

    def test_plan_transition_returns_event_for_phrase_boundary(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        event = planner.plan_transition(
            prev_phrase="build", next_phrase="drop",
            prev_energy=0.7, next_energy=0.9,
            segment_index=5, total_segments=10,
            show_key="transition_test",
        )
        self.assertIsNotNone(event)
        self.assertIsInstance(event, TransitionEvent)
        self.assertEqual(event.pool_key, "build_to_drop")
        self.assertGreaterEqual(event.duration_beats, 1)
        self.assertIn(event.fixtures, {"all", "pars", "movers", "pars+movers"})
        self.assertIn(event.exit_style, {"snap", "smooth"})
        self.assertFalse(event.end_of_show)

    def test_plan_transition_end_of_show(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        event = planner.plan_transition(
            prev_phrase="outro", next_phrase=None,
            prev_energy=0.2, next_energy=0.0,
            segment_index=10, total_segments=10,
            show_key="end_test", end_of_show=True,
        )
        self.assertIsNotNone(event)
        self.assertEqual(event.pool_key, "end_of_show")
        self.assertTrue(event.end_of_show)
        self.assertIn(event.transition_type, {"fade_to_black", "freeze_hold"})

    def test_plan_transition_respects_cooldown(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        events = []
        for i in range(6):
            e = planner.plan_transition(
                prev_phrase="verse_groove", next_phrase="build",
                prev_energy=0.5, next_energy=0.7,
                segment_index=i, total_segments=12,
                recent_transitions=[ev.transition_type for ev in events],
                show_key="cooldown_test",
            )
            self.assertIsNotNone(e)
            events.append(e)
        types = {e.transition_type for e in events}
        self.assertGreaterEqual(len(types), 2, f"Expected variety, got only: {types}")

    def test_plan_transition_duration_capping(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        event = planner.plan_transition(
            prev_phrase="intro", next_phrase="verse_groove",
            prev_energy=0.2, next_energy=0.5,
            segment_index=1, total_segments=10,
            show_key="cap_test",
            prev_segment_beats=4, next_segment_beats=4,
        )
        self.assertIsNotNone(event)
        self.assertLessEqual(event.duration_beats, 1)

    def test_plan_transition_escalation_restriction(self):
        """First-half transitions should not get escalation_restricted types."""
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        restricted = {"strobe_burst", "freeze_burst", "stutter_resolve"}
        for i in range(20):
            event = planner.plan_transition(
                prev_phrase="verse_groove", next_phrase="verse_groove",
                prev_energy=0.5, next_energy=0.5,
                segment_index=1, total_segments=20,
                show_key=f"escalation_test_{i}",
            )
            if event is not None:
                self.assertNotIn(
                    event.transition_type, restricted,
                    f"Got restricted type {event.transition_type} in first half",
                )

    def test_plan_transition_deterministic(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        results = set()
        for _ in range(5):
            event = planner.plan_transition(
                prev_phrase="build", next_phrase="drop",
                prev_energy=0.7, next_energy=0.9,
                segment_index=3, total_segments=8,
                show_key="deterministic_test",
            )
            results.add(event.transition_type)
        self.assertEqual(len(results), 1, "Same inputs should produce same output")

    def test_energy_from_phrase(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        self.assertEqual(planner._energy_from_phrase("intro"), "low")
        self.assertEqual(planner._energy_from_phrase("verse_groove"), "mid")
        self.assertEqual(planner._energy_from_phrase("build"), "high")
        self.assertEqual(planner._energy_from_phrase("drop"), "high")
        self.assertEqual(planner._energy_from_phrase("breakdown"), "low")
        self.assertEqual(planner._energy_from_phrase("outro"), "low")

    def test_select_pool_key_priority(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        te = planner._phrase_rules.get("transition_events", {})
        pools = te.get("pools", {})
        self.assertEqual(planner._select_pool_key("build", "drop", pools), "build_to_drop")
        self.assertEqual(planner._select_pool_key("intro", "verse_groove", pools), "low_to_mid")
        self.assertIn(planner._select_pool_key("drop", "drop", pools), pools)


class BeatReactivityTests(unittest.TestCase):

    def test_get_beat_reactivity_returns_correct_values(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        br = planner.get_beat_reactivity("drop", show_key="br_test")
        self.assertIsInstance(br, BeatReactivity)
        self.assertEqual(br.par_min, "beat")
        self.assertEqual(br.mover_min, "bar")
        self.assertEqual(br.accent_layer, "sub_beat")
        self.assertNotEqual(br.accent_type, "")

        br_intro = planner.get_beat_reactivity("intro", show_key="br_test")
        self.assertEqual(br_intro.par_min, "2bar")
        self.assertEqual(br_intro.mover_min, "4bar")
        self.assertEqual(br_intro.accent_layer, "none")
        self.assertEqual(br_intro.accent_type, "")

    def test_beat_reactivity_on_planned_technique(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        planned = planner.pick_technique(
            phrase="drop", segment_index=3, global_bar=16, show_key="br_plan_test",
        )
        self.assertIsNotNone(planned.beat_reactivity)
        self.assertEqual(planned.beat_reactivity.par_min, "beat")
        self.assertEqual(planned.beat_reactivity.mover_min, "bar")

    def test_beat_reactivity_accent_varies_by_show_key(self):
        planner = PhraseAwarePlanner.from_project_defaults(str(ROOT))
        accents = set()
        for i in range(20):
            br = planner.get_beat_reactivity("drop", show_key=f"variety_{i}")
            accents.add(br.accent_type)
        self.assertGreaterEqual(len(accents), 2, f"Expected accent variety, got: {accents}")

    @patch("showlib._record_designer_pack_usage_once")
    def test_beat_reactivity_in_serialized_technique(self, _mock_record):
        technique = showlib.pick_phrase_technique(
            phrase="build", segment_index=2, global_bar=8,
            show_key="serialize_test", project_root=str(ROOT),
        )
        br = technique.get("beat_reactivity")
        self.assertIsNotNone(br)
        self.assertEqual(br["par_min"], "beat")
        self.assertEqual(br["mover_min"], "bar")
        self.assertEqual(br["accent_layer"], "beat")
        self.assertNotEqual(br["accent_type"], "")


class ShowlibTransitionTests(unittest.TestCase):

    def test_plan_segment_transition(self):
        t = showlib.plan_segment_transition(
            prev_phrase="build", next_phrase="drop",
            prev_energy=0.7, next_energy=0.9,
            segment_index=5, total_segments=10,
            show_key="showlib_test", project_root=str(ROOT),
        )
        self.assertIsNotNone(t)
        self.assertEqual(t["pool_key"], "build_to_drop")
        self.assertTrue(t["type"])
        self.assertGreaterEqual(t["duration_beats"], 1)
        self.assertIn(t["exit_style"], {"snap", "smooth"})

    def test_build_transition_scenes_contract(self):
        """Every transition type returns matching scene/timing lists."""
        from showlib import _TRANSITION_FACTORIES
        for t_type in _TRANSITION_FACTORIES:
            transition = {"type": t_type, "duration_beats": 2, "exit_style": "snap"}
            scenes, timing = showlib.build_transition_scenes(
                transition, bpm=128, palette=(0, 100, 255),
            )
            self.assertEqual(
                len(scenes), len(timing),
                f"{t_type}: scenes={len(scenes)} != timing={len(timing)}",
            )
            for s in scenes:
                self.assertIn("name", s)
            for fade_in, hold_val in timing:
                self.assertGreaterEqual(fade_in, 0)
                self.assertGreaterEqual(hold_val, 0)

    def test_build_transition_scenes_none_returns_empty(self):
        scenes, timing = showlib.build_transition_scenes(None, bpm=128)
        self.assertEqual(scenes, [])
        self.assertEqual(timing, [])

    def test_build_transition_scenes_unknown_type_falls_back(self):
        transition = {"type": "nonexistent_fancy_transition", "duration_beats": 1, "exit_style": "snap"}
        scenes, timing = showlib.build_transition_scenes(transition, bpm=128)
        self.assertEqual(len(scenes), 1)
        self.assertEqual(len(timing), 1)


if __name__ == "__main__":
    unittest.main()
