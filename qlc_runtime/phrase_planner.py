#!/usr/bin/env python3
"""Phrase-aware planning for song-data driven show generation.

This module enforces a hard mapping from song phrase classes to compatible
coordination technique pools sourced from references/data.

Creativity layers:
- mover pattern grammar transforms (mirror/invert/phase_shift/expand/compress/reverse)
- phrase-contrast hard rule (on phrase change, change >=2 visual dimensions)
- 3-candidate planning with scoring and top-candidate selection
- designer technical packs (dominant + contrast) for real-world mover/chase ideas
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
import logging
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

logger = logging.getLogger(__name__)

PHRASE_CLASSES = (
    "intro",
    "verse_groove",
    "build",
    "drop",
    "breakdown",
    "outro",
)

CONTRAST_DIMENSIONS = (
    "position",
    "rhythm",
    "color",
    "intensity",
    "effect_density",
)

MOVER_TRANSFORM_TOKENS = (
    "mirror",
    "invert",
    "phase_shift",
    "expand",
    "compress",
    "reverse",
)

PAR_MODE_TO_TIMING = {
    "blink1": (1, "chase"),
    "blink2": (2, "chase"),
    "blink4": (4, "chase"),
    "fade4": (4, "fade"),
    "fade8": (8, "fade"),
}

_LABEL_MAP = {
    "start": "intro",
    "intro": "intro",
    "verse": "verse_groove",
    "chorus": "drop",
    "break": "breakdown",
    "bridge": "build",
    "solo": "build",
    "outro": "outro",
    "end": "outro",
}

_ROUTE_RE = re.compile(r"(?:MPX-)?R(\d{3})", re.IGNORECASE)

_BRAND_TRANSFORM_HINTS = {
    "space": {"expand", "phase_shift", "mirror"},
    "cosmic": {"expand", "phase_shift", "reverse"},
    "orbital": {"phase_shift", "reverse"},
    "dark": {"invert", "compress"},
    "industrial": {"invert", "compress", "reverse"},
    "minimal": {"compress"},
    "euphoric": {"expand", "mirror"},
    "melodic": {"mirror", "phase_shift"},
    "aggressive": {"invert", "reverse"},
    "hypnotic": {"phase_shift", "compress"},
}

_TOKEN_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "from",
    "into",
    "over",
    "under",
    "across",
    "around",
    "this",
    "these",
    "those",
    "your",
    "their",
    "while",
    "where",
    "when",
    "only",
    "using",
    "avoid",
    "must",
    "include",
    "without",
    "bars",
    "beats",
}

_INTENSITY_BY_PHRASE = {
    "intro": "low",
    "verse_groove": "medium",
    "build": "rising",
    "drop": "peak",
    "breakdown": "low",
    "outro": "low",
}


@dataclass(frozen=True)
class TechniqueTiming:
    mover_beats: int
    par_beats: int
    par_style: str  # chase|fade|mixed


@dataclass(frozen=True)
class MoverPatternPlan:
    base_route: str
    transforms: Tuple[str, ...]
    phase_shift_beats: int
    signature: str


@dataclass(frozen=True)
class CandidateScore:
    novelty: float
    coherence: float
    brand_fit: float
    creative_fit: float
    phrase_fit: float
    total: float


@dataclass(frozen=True)
class DesignerTechniquePack:
    pack_id: str
    ld_id: str
    name: str
    focus: str
    phrase_targets: Tuple[str, ...]
    mover_ideas: Tuple[str, ...]
    par_ideas: Tuple[str, ...]
    preferred_transforms: Tuple[str, ...]
    preferred_par_modes: Tuple[str, ...]
    preferred_relationships: Tuple[str, ...]
    anti_rules: Tuple[str, ...]
    tags: Tuple[str, ...]


@dataclass(frozen=True)
class BeatReactivity:
    par_min: str        # beat, 2beat, bar, 2bar, 4bar
    mover_min: str      # beat, 2beat, bar, 2bar, 4bar
    accent_layer: str   # none, bar_downbeat, beat, sub_beat
    accent_type: str    # chosen from accent_type_pools, or "" if none


@dataclass(frozen=True)
class PlannedTechnique:
    phrase: str
    technique_id: str
    technique_name: str
    relationship: str
    timing: TechniqueTiming
    mover_pattern: MoverPatternPlan
    dimensions: Dict[str, str]
    designer_pack_id: str
    designer_pack_name: str
    designer_ld_id: str
    designer_role: str  # dominant|contrast|none
    designer_phrase_targeted: bool
    score: CandidateScore
    candidate_rank: int
    candidate_count: int
    changed_dimensions: Tuple[str, ...]
    contrast_enforced: bool
    beat_reactivity: Optional[BeatReactivity] = None


@dataclass(frozen=True)
class TransitionEvent:
    transition_type: str       # e.g. "blackout_slingshot"
    duration_beats: int        # 1-4
    fixtures: str              # "all", "pars", "movers", "pars+movers"
    exit_style: str            # "snap" or "smooth"
    description: str
    pool_key: str              # which pool was used (e.g. "build_to_drop")
    segment_index: int
    end_of_show: bool = False


class PhraseAwarePlanner:
    """Map song-data segments into phrase buckets and enforce technique pools."""

    def __init__(
        self,
        phrase_rules: Dict[str, Any],
        coordination_techniques: Dict[str, Any],
        designer_techniques: Optional[Dict[str, Any]] = None,
    ):
        self._phrase_rules = phrase_rules
        self._coordination = coordination_techniques
        self._designer_techniques = designer_techniques or {}

        techniques = coordination_techniques.get("techniques", [])
        if not techniques:
            raise ValueError("coordination-techniques.json has no techniques")

        self.techniques_by_id = {row["id"]: row for row in techniques}
        if len(self.techniques_by_id) != len(techniques):
            raise ValueError("Duplicate technique IDs in coordination-techniques.json")

        self.phrase_pools: Dict[str, List[str]] = {}
        phrase_map = phrase_rules.get("phrase_map", {})
        missing_phrases = [phrase for phrase in PHRASE_CLASSES if phrase not in phrase_map]
        if missing_phrases:
            raise ValueError(f"phrase-rules.json missing phrase buckets: {missing_phrases}")

        for phrase in PHRASE_CLASSES:
            pool = list(phrase_map[phrase].get("coordination_pool", []))
            if not pool:
                raise ValueError(f"No coordination pool for phrase: {phrase}")
            unknown = sorted(set(pool) - set(self.techniques_by_id.keys()))
            if unknown:
                raise ValueError(f"Unknown technique IDs in pool for {phrase}: {unknown}")
            self.phrase_pools[phrase] = pool

        contrast = phrase_rules.get("contrast_rules", {})
        self.min_changed_dimensions = max(
            2,
            int(contrast.get("min_changed_dimensions_on_phrase_change", 2)),
        )
        self.default_candidate_count = max(
            3,
            int(contrast.get("candidate_plan_count", 3)),
        )
        configured_dims = contrast.get("dimensions", [])
        if isinstance(configured_dims, list) and configured_dims:
            dims = [str(token) for token in configured_dims if str(token).strip()]
            self.contrast_dimensions = tuple(dims)  # type: ignore[assignment]
        else:
            self.contrast_dimensions = CONTRAST_DIMENSIONS

        self.designer_packs = self._parse_designer_packs(self._designer_techniques)
        self.designer_packs_by_id = {pack.pack_id: pack for pack in self.designer_packs}
        self._show_pack_cache: Dict[str, Dict[str, Any]] = {}

        model = self._designer_techniques.get("selection_model", {})
        self.default_pack_cooldown = max(1, int(model.get("pack_cooldown_shows", 3)))
        dominant_range = model.get("dominant_pack_count_range", [1, 2])
        if isinstance(dominant_range, list) and len(dominant_range) >= 2:
            low = int(dominant_range[0])
            high = int(dominant_range[1])
        else:
            low, high = 1, 2
        self.dominant_pack_min = max(1, min(low, high))
        self.dominant_pack_max = max(self.dominant_pack_min, max(low, high))
        self.contrast_pack_count = max(1, int(model.get("contrast_pack_count", 1)))

    @classmethod
    def from_project_defaults(cls, project_root: Optional[str] = None) -> "PhraseAwarePlanner":
        if project_root:
            root = Path(project_root)
        else:
            root = Path(__file__).resolve().parents[1]

        phrase_path = root / "references" / "data" / "phrase-rules.json"
        technique_path = root / "references" / "data" / "coordination-techniques.json"
        designer_pack_path = root / "references" / "data" / "designer-techniques.json"

        phrase_rules = json.loads(phrase_path.read_text(encoding="utf-8"))
        coordination = json.loads(technique_path.read_text(encoding="utf-8"))
        designer_techniques: Dict[str, Any] = {}
        if designer_pack_path.exists():
            designer_techniques = json.loads(designer_pack_path.read_text(encoding="utf-8"))
        return cls(phrase_rules, coordination, designer_techniques)

    def classify_phrase(
        self,
        segment_label: str,
        rms: float,
        sub: float,
        high: float,
        progress: float,
    ) -> str:
        """Return one of the canonical phrase classes.

        `progress` should be normalized song position in [0, 1].
        """
        label = str(segment_label or "").strip().lower()

        direct = _LABEL_MAP.get(label)
        if direct:
            return direct

        # "inst" is common in allin1 output and needs musical disambiguation.
        if label == "inst":
            return self._classify_instrumental(rms=rms, sub=sub, high=high, progress=progress)

        # Fallback for unknown labels: phase by progress + energy.
        return self._classify_unknown(rms=rms, sub=sub, high=high, progress=progress)

    def pick_technique(
        self,
        phrase: str,
        segment_index: int,
        global_bar: int,
        usage: Optional[Dict[str, int]] = None,
        recent: Optional[List[str]] = None,
        cooldown: int = 2,
        previous: Optional[Union[PlannedTechnique, Dict[str, Any]]] = None,
        brand_tokens: Optional[Sequence[str]] = None,
        candidate_count: Optional[int] = None,
        creative_directives: Optional[Dict[str, Any]] = None,
        show_key: Optional[str] = None,
        pack_usage: Optional[Dict[str, int]] = None,
        pack_recent: Optional[List[str]] = None,
        pack_cooldown: Optional[int] = None,
    ) -> PlannedTechnique:
        """Pick top scored candidate for this phrase.

        The planner always evaluates >=3 candidates and returns rank 1.
        """
        candidates = self.plan_candidates(
            phrase=phrase,
            segment_index=segment_index,
            global_bar=global_bar,
            usage=usage,
            recent=recent,
            cooldown=cooldown,
            previous=previous,
            brand_tokens=brand_tokens,
            candidate_count=candidate_count,
            creative_directives=creative_directives,
            show_key=show_key,
            pack_usage=pack_usage,
            pack_recent=pack_recent,
            pack_cooldown=pack_cooldown,
        )
        winner = candidates[0]
        # Attach beat reactivity to the winning candidate
        br = self.get_beat_reactivity(phrase, show_key=show_key or "")
        return replace(winner, beat_reactivity=br)

    def plan_candidates(
        self,
        phrase: str,
        segment_index: int,
        global_bar: int,
        usage: Optional[Dict[str, int]] = None,
        recent: Optional[List[str]] = None,
        cooldown: int = 2,
        previous: Optional[Union[PlannedTechnique, Dict[str, Any]]] = None,
        brand_tokens: Optional[Sequence[str]] = None,
        candidate_count: Optional[int] = None,
        creative_directives: Optional[Dict[str, Any]] = None,
        show_key: Optional[str] = None,
        pack_usage: Optional[Dict[str, int]] = None,
        pack_recent: Optional[List[str]] = None,
        pack_cooldown: Optional[int] = None,
    ) -> List[PlannedTechnique]:
        """Build scored candidates and return them sorted best->worst."""
        if phrase not in self.phrase_pools:
            raise ValueError(f"Unknown phrase class: {phrase}")

        n_candidates = max(1, candidate_count or self.default_candidate_count)
        if n_candidates < 3:
            n_candidates = 3

        ordered_ids = self._ordered_phrase_ids(
            phrase=phrase,
            segment_index=segment_index,
            global_bar=global_bar,
            usage=usage,
            recent=recent,
            cooldown=cooldown,
        )
        if not ordered_ids:
            raise ValueError(f"No candidate techniques available for phrase: {phrase}")

        candidate_ids: List[str] = []
        seen: set[str] = set()
        for tech_id in ordered_ids:
            if tech_id not in seen:
                seen.add(tech_id)
                candidate_ids.append(tech_id)
            if len(candidate_ids) >= n_candidates:
                break
        while len(candidate_ids) < n_candidates:
            candidate_ids.append(ordered_ids[len(candidate_ids) % len(ordered_ids)])

        previous_phrase, previous_dimensions = self._extract_previous_context(previous)
        normalized_brand = self._normalize_brand_tokens(brand_tokens)
        normalized_creative = self._normalize_creative_directives(creative_directives)
        active_packs = self._select_active_designer_packs(
            show_key=show_key,
            brand_tokens=normalized_brand,
            creative_directives=normalized_creative,
            pack_usage=pack_usage,
            pack_recent=pack_recent,
            pack_cooldown=pack_cooldown or self.default_pack_cooldown,
        )

        candidates: List[PlannedTechnique] = []
        for slot, technique_id in enumerate(candidate_ids):
            technique = self.techniques_by_id[technique_id]
            timing = parse_timing_recipe(str(technique.get("timing_recipe", "")))
            mover_pattern = self._build_mover_pattern(
                phrase=phrase,
                technique=technique,
                segment_index=segment_index,
                global_bar=global_bar,
                slot=slot,
            )
            dimensions = self._make_dimensions(
                phrase=phrase,
                relationship=str(technique.get("relationship", "unison")),
                timing=timing,
                mover_pattern=mover_pattern,
            )
            candidate = PlannedTechnique(
                phrase=phrase,
                technique_id=technique_id,
                technique_name=str(technique.get("name", "")),
                relationship=str(technique.get("relationship", "unison")),
                timing=timing,
                mover_pattern=mover_pattern,
                dimensions=dimensions,
                designer_pack_id="",
                designer_pack_name="",
                designer_ld_id="",
                designer_role="none",
                designer_phrase_targeted=False,
                score=CandidateScore(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                candidate_rank=0,
                candidate_count=len(candidate_ids),
                changed_dimensions=tuple(),
                contrast_enforced=False,
            )

            pack, role = self._pick_pack_for_candidate(
                active_packs=active_packs,
                phrase=phrase,
                segment_index=segment_index,
                global_bar=global_bar,
                slot=slot,
            )
            candidate = self._apply_designer_pack(
                candidate=candidate,
                pack=pack,
                role=role,
                segment_index=segment_index,
                global_bar=global_bar,
                slot=slot,
            )

            candidate = self._enforce_phrase_contrast(
                candidate=candidate,
                previous_phrase=previous_phrase,
                previous_dimensions=previous_dimensions,
            )
            candidate = self._score_candidate(
                candidate=candidate,
                usage=usage,
                recent=recent,
                cooldown=cooldown,
                previous_phrase=previous_phrase,
                normalized_brand_tokens=normalized_brand,
                normalized_creative=normalized_creative,
            )
            candidates.append(candidate)

        candidates.sort(
            key=lambda row: (
                row.score.total,
                row.score.phrase_fit,
                row.score.coherence,
                row.score.novelty,
            ),
            reverse=True,
        )
        ranked: List[PlannedTechnique] = []
        for idx, row in enumerate(candidates, start=1):
            ranked.append(
                replace(
                    row,
                    candidate_rank=idx,
                    candidate_count=len(candidates),
                )
            )
        return ranked

    def select_show_designer_packs(
        self,
        show_key: Optional[str] = None,
        brand_tokens: Optional[Sequence[str]] = None,
        creative_directives: Optional[Dict[str, Any]] = None,
        pack_usage: Optional[Dict[str, int]] = None,
        pack_recent: Optional[List[str]] = None,
        pack_cooldown: Optional[int] = None,
    ) -> Dict[str, Any]:
        normalized_brand = self._normalize_brand_tokens(brand_tokens)
        normalized_creative = self._normalize_creative_directives(creative_directives)
        selected = self._select_active_designer_packs(
            show_key=show_key,
            brand_tokens=normalized_brand,
            creative_directives=normalized_creative,
            pack_usage=pack_usage,
            pack_recent=pack_recent,
            pack_cooldown=pack_cooldown or self.default_pack_cooldown,
        )
        dominant = [self._pack_to_dict(pack, "dominant") for pack in selected["dominant"]]
        contrast_pack = selected["contrast"]
        contrast = self._pack_to_dict(contrast_pack, "contrast") if contrast_pack else None
        return {
            "dominant": dominant,
            "contrast": contrast,
            "show_key": selected["show_key"],
            "cooldown": selected["cooldown"],
        }

    def _ordered_phrase_ids(
        self,
        phrase: str,
        segment_index: int,
        global_bar: int,
        usage: Optional[Dict[str, int]],
        recent: Optional[List[str]],
        cooldown: int,
    ) -> List[str]:
        pool = self.phrase_pools[phrase]
        phrase_step = global_bar // 4
        base_idx = (segment_index * 11 + phrase_step * 3 + (global_bar % 4)) % len(pool)
        ordered_ids = [pool[(base_idx + offset) % len(pool)] for offset in range(len(pool))]

        # Soft anti-overuse: avoid immediate repeats from short history.
        if recent and cooldown > 0:
            blocked = set(recent[-cooldown:])
            filtered = [tech_id for tech_id in ordered_ids if tech_id not in blocked]
            if filtered:
                ordered_ids = filtered

        # Soft balancing: prioritize least used first while keeping deterministic tie-breaks.
        if usage:
            indexed = list(enumerate(ordered_ids))
            indexed.sort(key=lambda row: (usage.get(row[1], 0), row[0]))
            ordered_ids = [tech_id for _, tech_id in indexed]

        return ordered_ids

    def _build_mover_pattern(
        self,
        phrase: str,
        technique: Dict[str, Any],
        segment_index: int,
        global_bar: int,
        slot: int,
    ) -> MoverPatternPlan:
        base_route = self._extract_route_id(technique)
        route_num = int(base_route[1:])
        seed = (
            segment_index * 41
            + global_bar * 17
            + slot * 23
            + route_num * 3
        )

        base_transform_count = {
            "intro": 1,
            "verse_groove": 2,
            "build": 2,
            "drop": 3,
            "breakdown": 1,
            "outro": 1,
        }.get(phrase, 2)

        transforms: List[str] = []
        for idx in range(base_transform_count * 2):
            token = MOVER_TRANSFORM_TOKENS[(seed + idx * 2) % len(MOVER_TRANSFORM_TOKENS)]
            if token not in transforms:
                transforms.append(token)
            if len(transforms) >= base_transform_count:
                break

        phase_shift = 0
        if "phase_shift" in transforms:
            phase_shift_options = (1, 2, 4)
            phase_shift = phase_shift_options[(seed + route_num) % len(phase_shift_options)]

        signature = self._pattern_signature(base_route, tuple(transforms), phase_shift)
        return MoverPatternPlan(
            base_route=base_route,
            transforms=tuple(transforms),
            phase_shift_beats=phase_shift,
            signature=signature,
        )

    def _select_active_designer_packs(
        self,
        show_key: Optional[str],
        brand_tokens: Sequence[str],
        creative_directives: Optional[Dict[str, Any]],
        pack_usage: Optional[Dict[str, int]],
        pack_recent: Optional[List[str]],
        pack_cooldown: int,
    ) -> Dict[str, Any]:
        if not self.designer_packs:
            return {"dominant": [], "contrast": None, "show_key": show_key or "", "cooldown": pack_cooldown}

        normalized_show = self._normalize_show_key(show_key, brand_tokens)
        cache_key = normalized_show
        if cache_key in self._show_pack_cache:
            return self._show_pack_cache[cache_key]

        seed = self._stable_hash(normalized_show)
        scored: List[Tuple[float, DesignerTechniquePack]] = []
        for pack in self.designer_packs:
            score = self._score_pack_for_show(
                pack=pack,
                brand_tokens=brand_tokens,
                creative_directives=creative_directives,
                pack_usage=pack_usage,
                pack_recent=pack_recent,
                pack_cooldown=pack_cooldown,
            )
            # Tiny deterministic jitter to prevent ties.
            jitter = ((self._stable_hash(pack.pack_id + normalized_show) % 7) / 1000.0)
            scored.append((score + jitter, pack))
        scored.sort(key=lambda row: row[0], reverse=True)

        dominant_count = self.dominant_pack_min
        if self.dominant_pack_max > self.dominant_pack_min:
            dominant_count += (seed % (self.dominant_pack_max - self.dominant_pack_min + 1))
        dominant_count = min(dominant_count, len(scored))
        dominant = [pack for _, pack in scored[:dominant_count]]

        remaining = [pack for _, pack in scored[dominant_count:]]
        contrast = self._pick_contrast_pack(dominant, remaining)
        if contrast is None and dominant:
            contrast = dominant[-1]

        selected = {
            "dominant": dominant,
            "contrast": contrast,
            "show_key": normalized_show,
            "cooldown": pack_cooldown,
        }
        self._show_pack_cache[cache_key] = selected
        return selected

    def _pick_pack_for_candidate(
        self,
        active_packs: Dict[str, Any],
        phrase: str,
        segment_index: int,
        global_bar: int,
        slot: int,
    ) -> Tuple[Optional[DesignerTechniquePack], str]:
        dominant: List[DesignerTechniquePack] = list(active_packs.get("dominant") or [])
        contrast: Optional[DesignerTechniquePack] = active_packs.get("contrast")

        if not dominant and not contrast:
            return None, "none"

        targeted_dominant = [pack for pack in dominant if phrase in pack.phrase_targets]
        if targeted_dominant:
            base = targeted_dominant[(segment_index + slot + (global_bar // 8)) % len(targeted_dominant)]
        elif dominant:
            base = dominant[(segment_index + slot + (global_bar // 8)) % len(dominant)]
        else:
            base = None

        use_contrast = False
        if contrast:
            if phrase in ("build", "drop") and ((global_bar + slot) % 8 == 4):
                use_contrast = True
            elif (global_bar + slot) % 24 == 12:
                use_contrast = True

        if use_contrast and contrast:
            return contrast, "contrast"
        if base:
            return base, "dominant"
        if contrast:
            return contrast, "contrast"
        return None, "none"

    def _apply_designer_pack(
        self,
        candidate: PlannedTechnique,
        pack: Optional[DesignerTechniquePack],
        role: str,
        segment_index: int,
        global_bar: int,
        slot: int,
    ) -> PlannedTechnique:
        if pack is None:
            return candidate

        relationship = candidate.relationship
        if pack.preferred_relationships and relationship not in pack.preferred_relationships:
            idx = (segment_index + global_bar + slot) % len(pack.preferred_relationships)
            relationship = pack.preferred_relationships[idx]

        transforms = list(candidate.mover_pattern.transforms)
        preferred_transforms = [token for token in pack.preferred_transforms if token in MOVER_TRANSFORM_TOKENS]
        if preferred_transforms:
            tidx = (segment_index + global_bar + slot) % len(preferred_transforms)
            token = preferred_transforms[tidx]
            if token in transforms:
                transforms.remove(token)
            transforms.insert(0, token)
            seen: set[str] = set()
            dedup: List[str] = []
            for item in transforms:
                if item not in seen:
                    seen.add(item)
                    dedup.append(item)
            transforms = dedup[: max(2, len(candidate.mover_pattern.transforms))]

        phase_shift = candidate.mover_pattern.phase_shift_beats
        if "phase_shift" in transforms and phase_shift <= 0:
            phase_shift = (1, 2, 4)[(segment_index + global_bar + slot) % 3]

        mover_pattern = MoverPatternPlan(
            base_route=candidate.mover_pattern.base_route,
            transforms=tuple(transforms),
            phase_shift_beats=phase_shift,
            signature=self._pattern_signature(
                candidate.mover_pattern.base_route,
                tuple(transforms),
                phase_shift,
            ),
        )

        timing = candidate.timing
        if pack.preferred_par_modes:
            mode = pack.preferred_par_modes[(segment_index + global_bar + slot) % len(pack.preferred_par_modes)]
            timing = self._timing_from_pack_mode(mode=mode, base_timing=timing, phrase=candidate.phrase)

        dimensions = self._make_dimensions(
            phrase=candidate.phrase,
            relationship=relationship,
            timing=timing,
            mover_pattern=mover_pattern,
        )
        return replace(
            candidate,
            relationship=relationship,
            timing=timing,
            mover_pattern=mover_pattern,
            dimensions=dimensions,
            designer_pack_id=pack.pack_id,
            designer_pack_name=pack.name,
            designer_ld_id=pack.ld_id,
            designer_role=role,
            designer_phrase_targeted=(candidate.phrase in pack.phrase_targets),
        )

    def _timing_from_pack_mode(self, mode: str, base_timing: TechniqueTiming, phrase: str) -> TechniqueTiming:
        normalized = str(mode).strip().lower()
        if normalized not in PAR_MODE_TO_TIMING:
            return base_timing

        par_beats, par_style = PAR_MODE_TO_TIMING[normalized]
        # Keep calmer phrase classes from getting constant 1-beat chase.
        if phrase in ("intro", "breakdown", "outro") and normalized == "blink1":
            par_beats, par_style = PAR_MODE_TO_TIMING["fade4"]

        mover_beats = base_timing.mover_beats
        if phrase == "drop":
            mover_beats = min(4, max(1, mover_beats))
        elif phrase in ("intro", "outro"):
            mover_beats = max(4, mover_beats)

        return TechniqueTiming(
            mover_beats=max(1, mover_beats),
            par_beats=max(1, par_beats),
            par_style=par_style,
        )

    def _score_pack_for_show(
        self,
        pack: DesignerTechniquePack,
        brand_tokens: Sequence[str],
        creative_directives: Optional[Dict[str, Any]],
        pack_usage: Optional[Dict[str, int]],
        pack_recent: Optional[List[str]],
        pack_cooldown: int,
    ) -> float:
        corpus = " ".join(
            [
                pack.name.lower(),
                pack.focus.lower(),
                " ".join(pack.tags).lower(),
                " ".join(pack.mover_ideas).lower(),
                " ".join(pack.par_ideas).lower(),
            ]
        )

        token_hit_count = sum(1 for token in brand_tokens if token in corpus)
        token_score = token_hit_count / max(1, len(brand_tokens)) if brand_tokens else 0.55
        phrase_span_score = len(set(pack.phrase_targets)) / float(len(PHRASE_CLASSES))
        directive_bonus = self._score_pack_directive_fit(pack, creative_directives)

        usage_penalty = 0.0
        if pack_usage:
            usage_penalty = min(0.45, 0.08 * float(pack_usage.get(pack.pack_id, 0)))

        recent_penalty = 0.0
        if pack_recent and pack_cooldown > 0 and pack.pack_id in set(pack_recent[-pack_cooldown:]):
            recent_penalty = 0.40

        base = (0.52 * token_score) + (0.30 * phrase_span_score) + (0.18 * directive_bonus)
        return self._clip01(base - usage_penalty - recent_penalty)

    def _score_pack_directive_fit(
        self,
        pack: DesignerTechniquePack,
        creative_directives: Optional[Dict[str, Any]],
    ) -> float:
        directives = creative_directives or {}
        must_include: List[Tuple[str, ...]] = list(directives.get("must_include_tokens") or [])
        avoid: List[Tuple[str, ...]] = list(directives.get("avoid_tokens") or [])
        hard_avoid: List[Tuple[str, ...]] = list(directives.get("hard_avoid_tokens") or [])

        if not must_include and not avoid and not hard_avoid:
            return 0.6

        corpus_tokens = set(
            self._normalize_text_tokens(
                " ".join(
                    [
                        pack.name,
                        pack.focus,
                        " ".join(pack.tags),
                        " ".join(pack.mover_ideas),
                        " ".join(pack.par_ideas),
                        " ".join(pack.anti_rules),
                    ]
                )
            )
        )
        anti_tokens = set(self._normalize_text_tokens(" ".join(pack.anti_rules)))

        include_score = 0.6
        if must_include:
            include_score = sum(self._directive_match(tokens, corpus_tokens) for tokens in must_include) / float(
                len(must_include)
            )

        avoid_hit = 0.0
        if avoid:
            avoid_hit = sum(self._directive_match(tokens, corpus_tokens) for tokens in avoid) / float(len(avoid))
        hard_hit = 0.0
        if hard_avoid:
            hard_hit = sum(self._directive_match(tokens, corpus_tokens) for tokens in hard_avoid) / float(len(hard_avoid))

        anti_guard = 0.55
        if avoid or hard_avoid:
            guard_rows = avoid + hard_avoid
            anti_guard = sum(self._directive_match(tokens, anti_tokens) for tokens in guard_rows) / float(len(guard_rows))

        raw = (0.55 * include_score) + (0.25 * anti_guard) - (0.25 * avoid_hit) - (0.35 * hard_hit)
        return self._clip01(raw)

    def _pick_contrast_pack(
        self,
        dominant: List[DesignerTechniquePack],
        remaining: List[DesignerTechniquePack],
    ) -> Optional[DesignerTechniquePack]:
        if not remaining:
            return None
        if not dominant:
            return remaining[0]

        dominant_targets = set()
        dominant_modes = set()
        for pack in dominant:
            dominant_targets.update(pack.phrase_targets)
            dominant_modes.update(pack.preferred_par_modes)

        best_pack: Optional[DesignerTechniquePack] = None
        best_score = -1.0
        for pack in remaining:
            target_union = dominant_targets | set(pack.phrase_targets)
            if not target_union:
                target_distance = 0.0
            else:
                target_distance = len(dominant_targets.symmetric_difference(set(pack.phrase_targets))) / float(len(target_union))

            mode_union = dominant_modes | set(pack.preferred_par_modes)
            if not mode_union:
                mode_distance = 0.0
            else:
                mode_distance = len(dominant_modes.symmetric_difference(set(pack.preferred_par_modes))) / float(len(mode_union))

            score = (0.62 * target_distance) + (0.38 * mode_distance)
            if score > best_score:
                best_score = score
                best_pack = pack
        return best_pack

    def _normalize_show_key(self, show_key: Optional[str], brand_tokens: Sequence[str]) -> str:
        if show_key and str(show_key).strip():
            raw = str(show_key).strip().lower()
        elif brand_tokens:
            raw = " ".join(sorted(set(brand_tokens))).strip().lower()
        else:
            raw = "default_show"
        return re.sub(r"[^a-z0-9]+", "_", raw).strip("_") or "default_show"

    def _stable_hash(self, text: str) -> int:
        out = 0
        for char in text:
            out = (out * 131 + ord(char)) % 1000003
        return out

    def _pack_to_dict(self, pack: DesignerTechniquePack, role: str) -> Dict[str, Any]:
        return {
            "id": pack.pack_id,
            "ld_id": pack.ld_id,
            "name": pack.name,
            "focus": pack.focus,
            "role": role,
            "phrase_targets": list(pack.phrase_targets),
            "preferred_transforms": list(pack.preferred_transforms),
            "preferred_par_modes": list(pack.preferred_par_modes),
            "preferred_relationships": list(pack.preferred_relationships),
            "anti_rules": list(pack.anti_rules),
        }

    def _parse_designer_packs(self, data: Dict[str, Any]) -> List[DesignerTechniquePack]:
        packs_data = data.get("packs", [])
        if not isinstance(packs_data, list):
            return []

        packs: List[DesignerTechniquePack] = []
        for row in packs_data:
            if not isinstance(row, dict):
                continue

            pack_id = str(row.get("id", "")).strip()
            ld_id = str(row.get("ld_id", "")).strip()
            name = str(row.get("name", "")).strip()
            if not pack_id or not ld_id or not name:
                continue

            phrase_targets = tuple(
                token for token in (str(x).strip() for x in row.get("phrase_targets", [])) if token in PHRASE_CLASSES
            )
            mover_ideas = tuple(token for token in (str(x).strip() for x in row.get("mover_ideas", [])) if token)
            par_ideas = tuple(token for token in (str(x).strip() for x in row.get("par_ideas", [])) if token)
            preferred_transforms = tuple(
                token for token in (str(x).strip() for x in row.get("preferred_transforms", [])) if token in MOVER_TRANSFORM_TOKENS
            )
            preferred_par_modes = tuple(
                token for token in (str(x).strip().lower() for x in row.get("preferred_par_modes", [])) if token in PAR_MODE_TO_TIMING
            )
            preferred_relationships = tuple(
                token
                for token in (str(x).strip() for x in row.get("preferred_relationships", []))
                if token in {"unison", "counterpoint", "inclusion"}
            )
            anti_rules = tuple(token for token in (str(x).strip() for x in row.get("anti_rules", [])) if token)
            tags = tuple(token for token in (str(x).strip().lower() for x in row.get("tags", [])) if token)

            packs.append(
                DesignerTechniquePack(
                    pack_id=pack_id,
                    ld_id=ld_id,
                    name=name,
                    focus=str(row.get("focus", "")).strip(),
                    phrase_targets=phrase_targets,
                    mover_ideas=mover_ideas,
                    par_ideas=par_ideas,
                    preferred_transforms=preferred_transforms,
                    preferred_par_modes=preferred_par_modes,
                    preferred_relationships=preferred_relationships,
                    anti_rules=anti_rules,
                    tags=tags,
                )
            )

        packs.sort(key=lambda row: row.pack_id)
        return packs

    def _pattern_signature(
        self,
        base_route: str,
        transforms: Tuple[str, ...],
        phase_shift_beats: int,
    ) -> str:
        parts = [base_route]
        if transforms:
            parts.append("+".join(transforms))
        if phase_shift_beats > 0:
            parts.append(f"ps{phase_shift_beats}")
        return "|".join(parts)

    def _extract_route_id(self, technique: Dict[str, Any]) -> str:
        text = " ".join(
            str(technique.get(key, "")).strip()
            for key in ("starter_combo", "name", "core_logic")
        )
        match = _ROUTE_RE.search(text)
        if not match:
            return "R001"
        return f"R{int(match.group(1)):03d}"

    def _make_dimensions(
        self,
        phrase: str,
        relationship: str,
        timing: TechniqueTiming,
        mover_pattern: MoverPatternPlan,
    ) -> Dict[str, str]:
        lead_transform = mover_pattern.transforms[0] if mover_pattern.transforms else "base"
        position = f"{mover_pattern.base_route}:{lead_transform}"
        rhythm = f"m{timing.mover_beats}-p{timing.par_beats}-{timing.par_style}"

        if relationship == "unison":
            color_base = "locked"
        elif relationship == "counterpoint":
            color_base = "split"
        else:
            color_base = "handoff"

        if phrase in ("intro", "breakdown", "outro"):
            color = f"{color_base}:narrow"
        elif phrase == "drop":
            color = f"{color_base}:contrast"
        elif phrase == "build":
            color = f"{color_base}:rising"
        else:
            color = f"{color_base}:balanced"

        intensity = _INTENSITY_BY_PHRASE.get(phrase, "medium")
        density_level = self._effect_density_bucket(phrase, timing, relationship)

        return {
            "position": position,
            "rhythm": rhythm,
            "color": color,
            "intensity": intensity,
            "effect_density": density_level,
        }

    def _effect_density_bucket(
        self,
        phrase: str,
        timing: TechniqueTiming,
        relationship: str,
    ) -> str:
        score = 0
        if phrase == "drop":
            score += 3
        elif phrase == "build":
            score += 2
        elif phrase == "verse_groove":
            score += 1

        if relationship == "inclusion":
            score += 1
        if timing.par_style == "chase":
            score += 1
        if timing.par_beats <= 1:
            score += 1
        elif timing.par_beats >= 4:
            score -= 1

        if score <= 1:
            return "low"
        if score <= 3:
            return "medium"
        if score <= 5:
            return "high"
        return "peak"

    def _extract_previous_context(
        self,
        previous: Optional[Union[PlannedTechnique, Dict[str, Any]]],
    ) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
        if previous is None:
            return None, None

        if isinstance(previous, PlannedTechnique):
            return previous.phrase, dict(previous.dimensions)

        if isinstance(previous, dict):
            phrase = str(previous.get("phrase", "")).strip() or None
            dims = previous.get("dimensions")
            if isinstance(dims, dict):
                normalized: Dict[str, str] = {}
                for key in self.contrast_dimensions:
                    if key in dims:
                        normalized[key] = str(dims[key])
                if normalized:
                    return phrase, normalized
            return phrase, None

        return None, None

    def _enforce_phrase_contrast(
        self,
        candidate: PlannedTechnique,
        previous_phrase: Optional[str],
        previous_dimensions: Optional[Dict[str, str]],
    ) -> PlannedTechnique:
        if not previous_phrase or not previous_dimensions:
            return candidate
        if previous_phrase == candidate.phrase:
            return candidate

        changed = self._changed_dimensions(previous_dimensions, candidate.dimensions)
        if len(changed) >= self.min_changed_dimensions:
            return replace(candidate, changed_dimensions=changed)

        # Hard fallback: force both position+rhythm difference when phrase changes.
        transforms = list(candidate.mover_pattern.transforms)
        for token in ("mirror", "reverse", "invert", "phase_shift", "expand", "compress"):
            if token not in transforms:
                transforms.append(token)
                break
        phase_shift = candidate.mover_pattern.phase_shift_beats
        if "phase_shift" in transforms and phase_shift <= 0:
            phase_shift = 1
        mover_pattern = MoverPatternPlan(
            base_route=candidate.mover_pattern.base_route,
            transforms=tuple(transforms),
            phase_shift_beats=phase_shift,
            signature=self._pattern_signature(
                candidate.mover_pattern.base_route,
                tuple(transforms),
                phase_shift,
            ),
        )

        retimed = self._retime_for_contrast(candidate.timing, candidate.phrase)
        dimensions = self._make_dimensions(
            phrase=candidate.phrase,
            relationship=candidate.relationship,
            timing=retimed,
            mover_pattern=mover_pattern,
        )
        changed = self._changed_dimensions(previous_dimensions, dimensions)
        return replace(
            candidate,
            mover_pattern=mover_pattern,
            timing=retimed,
            dimensions=dimensions,
            changed_dimensions=changed,
            contrast_enforced=True,
        )

    def _retime_for_contrast(self, timing: TechniqueTiming, phrase: str) -> TechniqueTiming:
        if timing.par_beats <= 1:
            par_beats = 2
        elif timing.par_beats == 2:
            par_beats = 4
        else:
            par_beats = 1

        par_style = timing.par_style
        if phrase in ("build", "drop"):
            par_style = "chase"
        elif phrase in ("intro", "breakdown", "outro"):
            par_style = "fade"
        elif par_style == "mixed":
            par_style = "chase"

        return TechniqueTiming(
            mover_beats=max(1, timing.mover_beats),
            par_beats=max(1, par_beats),
            par_style=par_style,
        )

    def _changed_dimensions(
        self,
        previous: Dict[str, str],
        current: Dict[str, str],
    ) -> Tuple[str, ...]:
        changed: List[str] = []
        for key in self.contrast_dimensions:
            if str(previous.get(key, "")) != str(current.get(key, "")):
                changed.append(key)
        return tuple(changed)

    def _score_candidate(
        self,
        candidate: PlannedTechnique,
        usage: Optional[Dict[str, int]],
        recent: Optional[List[str]],
        cooldown: int,
        previous_phrase: Optional[str],
        normalized_brand_tokens: Sequence[str],
        normalized_creative: Dict[str, Any],
    ) -> PlannedTechnique:
        novelty = self._score_novelty(candidate, usage=usage, recent=recent, cooldown=cooldown)
        coherence = self._score_coherence(candidate)
        brand_fit = self._score_brand_fit(candidate, normalized_brand_tokens)
        creative_fit = self._score_creative_fit(candidate, normalized_creative)
        phrase_fit = self._score_phrase_fit(candidate)

        phrase_changed = bool(previous_phrase and previous_phrase != candidate.phrase)
        if phrase_changed and len(candidate.changed_dimensions) < self.min_changed_dimensions:
            contrast_gate = 0.0
        else:
            contrast_gate = 1.0

        alignment_weight = float(normalized_creative.get("alignment_weight", 0.65))
        alignment_weight = self._clip01(alignment_weight)
        total = (
            (0.27 * novelty)
            + (0.23 * coherence)
            + (0.14 * brand_fit)
            + (0.10 * creative_fit)
            + (0.20 * phrase_fit)
            + (0.06 * self._score_designer_pack_alignment(candidate))
        )
        if alignment_weight >= 0.70 and creative_fit < 0.40:
            total *= 0.82
        elif alignment_weight >= 0.70 and creative_fit >= 0.72:
            total = min(1.0, total + 0.05)
        if contrast_gate <= 0.0:
            total *= 0.05
        elif phrase_changed and len(candidate.changed_dimensions) >= self.min_changed_dimensions:
            total = min(1.0, total + 0.05)

        score = CandidateScore(
            novelty=round(self._clip01(novelty), 4),
            coherence=round(self._clip01(coherence), 4),
            brand_fit=round(self._clip01(brand_fit), 4),
            creative_fit=round(self._clip01(creative_fit), 4),
            phrase_fit=round(self._clip01(phrase_fit), 4),
            total=round(self._clip01(total), 4),
        )
        return replace(candidate, score=score)

    def _score_designer_pack_alignment(self, candidate: PlannedTechnique) -> float:
        if not candidate.designer_pack_id:
            return 0.5
        score = 0.65 if candidate.designer_role == "dominant" else 0.55
        if candidate.designer_phrase_targeted:
            score += 0.25
        if candidate.designer_role == "contrast":
            if candidate.phrase in ("build", "drop"):
                score += 0.10
            else:
                score -= 0.10
        return self._clip01(score)

    def _score_novelty(
        self,
        candidate: PlannedTechnique,
        usage: Optional[Dict[str, int]],
        recent: Optional[List[str]],
        cooldown: int,
    ) -> float:
        used = usage.get(candidate.technique_id, 0) if usage else 0
        score = 1.0 / (1.0 + float(used))
        score += min(0.24, 0.08 * len(set(candidate.mover_pattern.transforms)))

        if recent and cooldown > 0 and candidate.technique_id in set(recent[-cooldown:]):
            score *= 0.4
        return self._clip01(score)

    def _score_coherence(self, candidate: PlannedTechnique) -> float:
        phrase_rule = self._phrase_rules["phrase_map"][candidate.phrase]
        mover_targets = self._extract_beats(phrase_rule.get("mover_mode", ""))
        par_targets = self._extract_beats(phrase_rule.get("par_mode", ""))

        mover_score = self._score_beats(candidate.timing.mover_beats, mover_targets)
        par_score = self._score_beats(candidate.timing.par_beats, par_targets)

        style_score = 0.75
        if candidate.phrase in ("build", "drop") and candidate.timing.par_style == "chase":
            style_score = 1.0
        elif candidate.phrase in ("intro", "breakdown", "outro") and candidate.timing.par_style == "fade":
            style_score = 1.0
        elif candidate.timing.par_style == "mixed":
            style_score = 0.85

        relation_score = 1.0
        if candidate.phrase in ("intro", "breakdown", "outro") and candidate.relationship == "inclusion":
            relation_score = 0.75

        return self._clip01(
            (0.32 * mover_score)
            + (0.36 * par_score)
            + (0.20 * style_score)
            + (0.12 * relation_score)
        )

    def _score_phrase_fit(self, candidate: PlannedTechnique) -> float:
        base = 1.0 if candidate.technique_id in self.phrase_pools[candidate.phrase] else 0.0

        rhythmic_fit = 0.7
        if candidate.phrase == "drop":
            rhythmic_fit = 1.0 if candidate.timing.par_beats <= 2 else 0.5
        elif candidate.phrase in ("intro", "breakdown", "outro"):
            rhythmic_fit = 1.0 if candidate.timing.par_beats >= 2 else 0.55
        elif candidate.phrase == "build":
            rhythmic_fit = 0.9 if candidate.timing.par_beats <= 2 else 0.7

        density_fit = 0.7
        density = candidate.dimensions.get("effect_density", "medium")
        if candidate.phrase == "drop":
            density_fit = 1.0 if density in {"high", "peak"} else 0.55
        elif candidate.phrase in ("intro", "breakdown", "outro"):
            density_fit = 1.0 if density in {"low", "medium"} else 0.5

        return self._clip01((0.55 * base) + (0.25 * rhythmic_fit) + (0.20 * density_fit))

    def _normalize_brand_tokens(self, brand_tokens: Optional[Sequence[str]]) -> List[str]:
        if not brand_tokens:
            return []
        normalized: List[str] = []
        for token in brand_tokens:
            text = re.sub(r"[^a-z0-9]+", " ", str(token).strip().lower()).strip()
            if not text:
                continue
            normalized.extend(part for part in text.split() if len(part) >= 3)
        return normalized

    def _normalize_creative_directives(
        self,
        creative_directives: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        payload = creative_directives if isinstance(creative_directives, dict) else {}

        def _as_rows(value: Any) -> List[str]:
            if isinstance(value, list):
                return [str(row) for row in value if str(row).strip()]
            if isinstance(value, str) and value.strip():
                return [value]
            return []

        must_include_rows = _as_rows(payload.get("must_include"))
        avoid_rows = _as_rows(payload.get("avoid"))
        hard_avoid_rows = _as_rows(payload.get("do_not_copy"))
        direction_rows = _as_rows(payload.get("direction_notes"))
        branding_rows = _as_rows(payload.get("branding_notes"))
        thesis = str(payload.get("thesis", "")).strip()

        must_include_tokens = [
            tuple(self._normalize_text_tokens(row))
            for row in must_include_rows
            if self._normalize_text_tokens(row)
        ]
        avoid_tokens = [
            tuple(self._normalize_text_tokens(row))
            for row in avoid_rows
            if self._normalize_text_tokens(row)
        ]
        hard_avoid_tokens = [
            tuple(self._normalize_text_tokens(row))
            for row in hard_avoid_rows
            if self._normalize_text_tokens(row)
        ]

        story_token_source = " ".join(direction_rows + branding_rows + ([thesis] if thesis else []))
        story_tokens = self._normalize_text_tokens(story_token_source)

        raw_weight = payload.get("brand_alignment_weight")
        if raw_weight is None:
            raw_score = payload.get("brand_alignment_score")
            try:
                score = float(raw_score)
            except Exception:
                score = 3.0
            raw_weight = score / 5.0
        try:
            alignment_weight = float(raw_weight)
        except Exception:
            alignment_weight = 0.6
        alignment_weight = self._clip01(alignment_weight)

        return {
            "must_include_tokens": must_include_tokens,
            "avoid_tokens": avoid_tokens,
            "hard_avoid_tokens": hard_avoid_tokens,
            "story_tokens": story_tokens,
            "alignment_weight": alignment_weight,
        }

    def _normalize_text_tokens(self, text: str) -> List[str]:
        cleaned = re.sub(r"[^a-z0-9]+", " ", str(text).lower())
        out: List[str] = []
        seen: set[str] = set()
        for token in cleaned.split():
            if len(token) < 3:
                continue
            if token in _TOKEN_STOPWORDS:
                continue
            if token in {"todo", "tbd", "example", "http", "https", "www", "com"}:
                continue
            if token in seen:
                continue
            seen.add(token)
            out.append(token)
        return out

    def _directive_match(self, directive_tokens: Sequence[str], corpus_tokens: set[str]) -> float:
        if not directive_tokens:
            return 0.0
        hits = sum(1 for token in directive_tokens if token in corpus_tokens)
        ratio = hits / float(len(directive_tokens))
        if hits <= 0:
            return 0.0
        if ratio >= 0.80:
            return 1.0
        if ratio >= 0.50:
            return 0.85
        if ratio >= 0.34:
            return 0.65
        return 0.35

    def _candidate_corpus_tokens(self, candidate: PlannedTechnique) -> set[str]:
        technique = self.techniques_by_id.get(candidate.technique_id, {})
        chunks = [
            candidate.technique_name,
            candidate.relationship,
            candidate.mover_pattern.signature,
            " ".join(candidate.mover_pattern.transforms),
            " ".join(candidate.dimensions.values()),
            str(technique.get("core_logic", "")),
            str(technique.get("starter_combo", "")),
            str(technique.get("timing_recipe", "")),
            candidate.designer_pack_name,
        ]
        if candidate.designer_pack_id in self.designer_packs_by_id:
            pack = self.designer_packs_by_id[candidate.designer_pack_id]
            chunks.extend(
                [
                    pack.focus,
                    " ".join(pack.tags),
                    " ".join(pack.mover_ideas),
                    " ".join(pack.par_ideas),
                    " ".join(pack.anti_rules),
                ]
            )
        return set(self._normalize_text_tokens(" ".join(chunks)))

    def _score_creative_fit(
        self,
        candidate: PlannedTechnique,
        creative_directives: Dict[str, Any],
    ) -> float:
        must_include: List[Tuple[str, ...]] = list(creative_directives.get("must_include_tokens") or [])
        avoid: List[Tuple[str, ...]] = list(creative_directives.get("avoid_tokens") or [])
        hard_avoid: List[Tuple[str, ...]] = list(creative_directives.get("hard_avoid_tokens") or [])
        story_tokens: List[str] = list(creative_directives.get("story_tokens") or [])

        if not must_include and not avoid and not hard_avoid and not story_tokens:
            return 0.55

        corpus_tokens = self._candidate_corpus_tokens(candidate)

        include_score = 0.6
        if must_include:
            include_score = sum(self._directive_match(tokens, corpus_tokens) for tokens in must_include) / float(
                len(must_include)
            )

        story_score = 0.6
        if story_tokens:
            story_hits = sum(1 for token in story_tokens if token in corpus_tokens)
            story_score = self._clip01(story_hits / float(max(3, min(len(story_tokens), 8))))

        avoid_penalty = 0.0
        if avoid:
            avoid_penalty = sum(self._directive_match(tokens, corpus_tokens) for tokens in avoid) / float(len(avoid))
        hard_avoid_penalty = 0.0
        if hard_avoid:
            hard_avoid_penalty = sum(self._directive_match(tokens, corpus_tokens) for tokens in hard_avoid) / float(
                len(hard_avoid)
            )

        raw = (
            (0.58 * include_score)
            + (0.42 * story_score)
            - (0.42 * avoid_penalty)
            - (0.62 * hard_avoid_penalty)
        )
        return self._clip01(raw)

    def _score_brand_fit(self, candidate: PlannedTechnique, brand_tokens: Sequence[str]) -> float:
        if not brand_tokens:
            return 0.55

        corpus = " ".join(
            [
                candidate.technique_name.lower(),
                candidate.relationship.lower(),
                candidate.mover_pattern.signature.lower(),
                " ".join(candidate.dimensions.values()).lower(),
                str(self.techniques_by_id[candidate.technique_id].get("core_logic", "")).lower(),
                candidate.designer_pack_name.lower(),
            ]
        )

        token_hits = sum(1 for token in brand_tokens if token in corpus)
        token_score = token_hits / max(1, len(brand_tokens))

        pref_total = 0
        pref_hits = 0
        transform_set = set(candidate.mover_pattern.transforms)
        for token in brand_tokens:
            matched = set()
            for key, preferred in _BRAND_TRANSFORM_HINTS.items():
                if key in token or token in key:
                    matched.update(preferred)
            if matched:
                pref_total += 1
                if transform_set & matched:
                    pref_hits += 1

        pref_score = pref_hits / max(1, pref_total) if pref_total else 0.5
        return self._clip01((0.35 * token_score) + (0.65 * pref_score))

    def _extract_beats(self, text: str) -> List[int]:
        return sorted(
            {
                int(match)
                for match in re.findall(r"(\d+)b", str(text).lower())
                if int(match) > 0
            }
        )

    def _score_beats(self, value: int, targets: List[int]) -> float:
        if not targets:
            return 0.75
        diff = min(abs(value - target) for target in targets)
        # Beat differences above 4 are effectively poor alignment.
        return self._clip01(1.0 - (float(diff) / 4.0))

    def _clip01(self, value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def _classify_instrumental(self, rms: float, sub: float, high: float, progress: float) -> str:
        if progress < 0.14:
            return "intro"
        if progress > 0.86:
            return "outro"
        if rms >= 0.70 or sub >= 0.60:
            return "drop"
        if rms <= 0.32 and sub <= 0.30:
            return "breakdown"
        if high >= 0.50 or rms >= 0.52:
            return "build"
        return "verse_groove"

    def _classify_unknown(self, rms: float, sub: float, high: float, progress: float) -> str:
        if progress < 0.10:
            return "intro"
        if progress > 0.90:
            return "outro"
        if rms >= 0.76 or sub >= 0.66:
            return "drop"
        if rms <= 0.30 and high <= 0.22:
            return "breakdown"
        if high >= 0.50 or rms >= 0.50:
            return "build"
        return "verse_groove"

    # -----------------------------------------------------------------
    # Transition event planning
    # -----------------------------------------------------------------

    def _energy_from_phrase(self, phrase: str) -> str:
        """Map a phrase class to an energy level using transition_events.energy_map."""
        te = self._phrase_rules.get("transition_events", {})
        energy_map = te.get("energy_map", {})
        return energy_map.get(phrase, "mid")

    def plan_transition(
        self,
        prev_phrase: Optional[str],
        next_phrase: Optional[str],
        prev_energy: float,
        next_energy: float,
        segment_index: int,
        total_segments: int,
        recent_transitions: Optional[List[str]] = None,
        show_key: str = "",
        end_of_show: bool = False,
        prev_segment_beats: int = 32,
        next_segment_beats: int = 32,
    ) -> Optional[TransitionEvent]:
        """Select a transition event for a segment boundary.

        Returns a TransitionEvent or None if no transition_events config exists.
        """
        te = self._phrase_rules.get("transition_events")
        if te is None:
            return None

        pools = te.get("pools", {})
        schema = te.get("event_schema", {})
        cooldown = int(te.get("cooldown", 3))
        max_frac = float(te.get("max_duration_fraction", 0.25))
        escalation_restricted = set(te.get("escalation_restricted", []))
        recent = list(recent_transitions or [])

        # Pick the right pool
        if end_of_show:
            pool_key = "end_of_show"
        else:
            pool_key = self._select_pool_key(prev_phrase, next_phrase, pools)

        pool = list(pools.get(pool_key, pools.get("same_to_same", [])))
        if not pool:
            return None

        # Duration cap: 25% of the shorter adjacent segment
        shorter_seg = min(prev_segment_beats, next_segment_beats)
        max_beats = max(1, int(shorter_seg * max_frac))

        # Escalation: first half of show restricts dramatic transitions
        # (build_to_drop and end_of_show are exempt)
        in_first_half = (total_segments > 0 and
                         segment_index < total_segments / 2 and
                         pool_key not in ("build_to_drop", "end_of_show"))

        # Filter pool by duration cap and escalation
        eligible = []
        for t_type in pool:
            t_def = schema.get(t_type)
            if not t_def:
                continue
            if t_def["duration_beats"] > max_beats:
                continue
            if in_first_half and t_type in escalation_restricted:
                continue
            eligible.append(t_type)

        if not eligible:
            # Relax: try all pool items ignoring escalation
            eligible = [t for t in pool if schema.get(t, {}).get("duration_beats", 99) <= max_beats]
        if not eligible:
            # Still empty: pick the shortest transition from the pool
            eligible = sorted(pool, key=lambda t: schema.get(t, {}).get("duration_beats", 99))[:1]
        if not eligible:
            return None

        # Apply cooldown: remove recently used types
        after_cooldown = [t for t in eligible if t not in recent[-cooldown:]]
        if not after_cooldown:
            # Pool exhaustion: relax cooldown with warning
            logger.debug("Transition pool %s exhausted after cooldown; relaxing", pool_key)
            after_cooldown = eligible

        # Deterministic-but-varied selection using show_key + segment_index
        seed = hashlib.md5(f"{show_key}:{segment_index}".encode()).hexdigest()
        idx = int(seed, 16) % len(after_cooldown)
        chosen_type = after_cooldown[idx]

        t_def = schema[chosen_type]
        return TransitionEvent(
            transition_type=chosen_type,
            duration_beats=t_def["duration_beats"],
            fixtures=t_def["fixtures"],
            exit_style=t_def["exit_style"],
            description=t_def.get("description", ""),
            pool_key=pool_key,
            segment_index=segment_index,
            end_of_show=end_of_show,
        )

    def _select_pool_key(
        self,
        prev_phrase: Optional[str],
        next_phrase: Optional[str],
        pools: Dict[str, List[str]],
    ) -> str:
        """Choose the best pool key for a phrase pair.

        Priority: phrase-pair-specific > energy-pair > same_to_same.
        """
        # Check phrase-pair-specific pools (e.g. build_to_drop)
        if prev_phrase and next_phrase:
            pair_key = f"{prev_phrase}_to_{next_phrase}"
            if pair_key in pools:
                return pair_key

        # Energy-pair pools
        prev_e = self._energy_from_phrase(prev_phrase or "intro")
        next_e = self._energy_from_phrase(next_phrase or "outro")
        energy_key = f"{prev_e}_to_{next_e}"
        if energy_key in pools:
            return energy_key

        # Fallback
        return "same_to_same"

    # -----------------------------------------------------------------
    # Beat reactivity helpers
    # -----------------------------------------------------------------

    def get_beat_reactivity(self, phrase: str, show_key: str = "") -> BeatReactivity:
        """Return beat reactivity minimums for a phrase class."""
        br = self._phrase_rules.get("beat_reactivity", {})
        entry = br.get(phrase, {"par_min": "bar", "mover_min": "2bar", "accent_layer": "none"})
        accent_layer = entry.get("accent_layer", "none")

        # Choose accent type deterministically per show for variety
        accent_type = ""
        if accent_layer != "none":
            pools = self._phrase_rules.get("accent_type_pools", [])
            if pools:
                seed = hashlib.md5(f"{show_key}:accent".encode()).hexdigest()
                accent_type = pools[int(seed, 16) % len(pools)]

        return BeatReactivity(
            par_min=entry.get("par_min", "bar"),
            mover_min=entry.get("mover_min", "2bar"),
            accent_layer=accent_layer,
            accent_type=accent_type,
        )


def parse_timing_recipe(recipe: str) -> TechniqueTiming:
    """Parse timing recipes like "movers=4b, pars=1b chase"."""
    text = recipe.lower()

    mover_match = re.search(r"movers\s*=\s*(\d+)b", text)
    par_match = re.search(r"pars\s*=\s*(\d+)b", text)

    mover_beats = int(mover_match.group(1)) if mover_match else 4
    par_beats = int(par_match.group(1)) if par_match else 4

    if "chase" in text or "pulse" in text:
        par_style = "chase"
    elif "fade" in text:
        par_style = "fade"
    else:
        par_style = "mixed"

    return TechniqueTiming(
        mover_beats=max(1, mover_beats),
        par_beats=max(1, par_beats),
        par_style=par_style,
    )


def family_from_phrase_and_relationship(phrase: str, relationship: str, rms: float, sub: float) -> str:
    """Map phrase+coordination relationship to local mover family buckets."""
    if phrase in ("intro", "breakdown", "outro"):
        return "atmospheric"

    if phrase == "drop":
        if relationship == "inclusion":
            return "snap"
        return "snap" if (rms >= 0.62 or sub >= 0.54) else "geometric"

    if phrase == "build":
        if relationship == "counterpoint":
            return "geometric"
        return "snap" if rms >= 0.58 else "geometric"

    # verse_groove
    if relationship == "counterpoint" and rms >= 0.48:
        return "snap"
    return "geometric"


def par_mode_from_timing(timing: TechniqueTiming, phrase: str, seg_bar_idx: int) -> str:
    """Map abstract technique timing to local PAR modes used by generators."""
    beats = timing.par_beats

    if timing.par_style == "chase":
        if beats <= 1:
            return "blink1"
        if beats <= 2:
            return "blink2"
        return "blink4"

    if timing.par_style == "fade":
        if beats >= 8:
            return "fade8"
        if phrase in ("intro", "breakdown", "outro") and beats >= 4 and seg_bar_idx % 2 == 0:
            return "fade8"
        return "fade4"

    # mixed fallback
    if phrase in ("drop", "build"):
        return "blink2"
    if phrase in ("intro", "breakdown", "outro"):
        return "fade8"
    return "fade4"
