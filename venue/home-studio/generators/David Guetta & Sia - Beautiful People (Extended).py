#!/usr/bin/env python3
"""
Phrase-aware show generator (auto-derived template).
"""

import bisect
import json
import os
import sys
from typing import Dict, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
from showlib import *


# =============================================================================
# INPUT / OUTPUT
# =============================================================================

SONG_STEM = 'David Guetta & Sia - Beautiful People (Extended)'
BRIEF = require_research_brief(SONG_STEM, project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)
print(f"Research brief OK: {BRIEF['_meta']['brief_json']}")
print(f"Creative thesis: {BRIEF['thesis']}")
DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", f"{SONG_STEM}.json")
OUT_PATH = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")

CREATIVE = build_creative_context(BRIEF, song_stem=SONG_STEM)
BRAND_TOKENS = CREATIVE["brand_tokens"]
CREATIVE_DIRECTIVES = CREATIVE["creative_directives"]

with open(DATA_PATH) as f:
    data = json.load(f)

BPM = data["bpm"]  # 125
BAR_SEC = (60.0 / BPM) * 4.0

beats = data["beats"]
downbeats = data["downbeats"]
segments = data["segments"]
e_rms = data["energy"]["rms"]
e_sub = data["energy"]["sub_bass"]
e_high = data["energy"]["high"]
song_end = segments[-1]["end"] if segments else beats[-1]


# =============================================================================
# HELPERS
# =============================================================================

def beat_at(t: float) -> int:
    idx = bisect.bisect_left(beats, t)
    if idx == 0:
        return 0
    if idx >= len(beats):
        return len(beats) - 1
    if abs(beats[idx] - t) < abs(beats[idx - 1] - t):
        return idx
    return idx - 1


def avg_energy(arr: List[float], t0: float, t1: float) -> float:
    i0 = beat_at(t0)
    i1 = beat_at(t1)
    if i1 <= i0:
        i1 = min(i0 + 1, len(arr))
    if i0 >= len(arr):
        return 0.0
    return float(sum(arr[i0:i1])) / max(1, (i1 - i0))


def segment_at(t: float) -> Tuple[int, dict]:
    for i, seg in enumerate(segments):
        if seg["start"] <= t < seg["end"]:
            return i, seg
    return len(segments) - 1, segments[-1]


def clamp(x: int, lo: int = 0, hi: int = 255) -> int:
    return max(lo, min(hi, x))


def e2d(e: float, lo: int, hi: int) -> int:
    e = max(0.0, min(1.0, e))
    return int(lo + (hi - lo) * e)


def build_bar_grid() -> List[Tuple[float, float]]:
    starts = sorted(downbeats)
    if not starts:
        starts = [0.0]

    # Include pre-roll if first downbeat is late.
    if starts[0] > 0.25:
        starts.insert(0, 0.0)

    # Extend downbeat grid to end of song for trailing outro bars.
    while starts[-1] + BAR_SEC < song_end - 0.01:
        starts.append(round(starts[-1] + BAR_SEC, 4))

    bars = []
    for i, t0 in enumerate(starts):
        if t0 >= song_end:
            break
        if i + 1 < len(starts):
            t1 = min(song_end, starts[i + 1])
        else:
            t1 = min(song_end, t0 + BAR_SEC)
        if t1 - t0 >= 0.10:
            bars.append((t0, t1))
    return bars


# =============================================================================
# FOCUS POSITIONS — loaded from venue focus-positions.md
# =============================================================================

POS: Dict[str, Tuple[int, int, int, int, int, int, int]] = load_focus_position_tuples(
    project_root=PROJECT_ROOT,
    venue_dir=VENUE_DIR,
)


# =============================================================================
# PALETTES
# =============================================================================

PALETTES = {
    "oath_steel": {
        "par_a": (10, 20, 62), "par_b": (18, 34, 100),
        "miss1": (20, 32, 88), "miss2": (10, 18, 45),
        "sh": SHARPY_BLUE, "bsw": BSW_BLUE, "prof": PROF_BLUE,
        "halo": H_BLU, "ni": (20, 36, 108)
    },
    "trust_teal": {
        "par_a": (0, 78, 108), "par_b": (0, 54, 76),
        "miss1": (0, 110, 132), "miss2": (0, 65, 92),
        "sh": SHARPY_TEAL, "bsw": BSW_TEAL, "prof": PROF_TEAL,
        "halo": H_CYN, "ni": (0, 118, 148)
    },
    "midnight_violet": {
        "par_a": (86, 24, 140), "par_b": (28, 16, 80),
        "miss1": (120, 38, 162), "miss2": (64, 28, 110),
        "sh": SHARPY_PURPLE, "bsw": BSW_MAG, "prof": PROF_PINK,
        "halo": H_PNK, "ni": (112, 40, 152)
    },
    "ember_signal": {
        "par_a": (185, 92, 18), "par_b": (32, 58, 128),
        "miss1": (218, 122, 26), "miss2": (36, 72, 162),
        "sh": SHARPY_AMBER, "bsw": BSW_ORANGE, "prof": PROF_ORANGE,
        "halo": H_YEL, "ni": (160, 74, 28)
    },
    "resolve_crimson": {
        "par_a": (210, 24, 34), "par_b": (122, 170, 232),
        "miss1": (244, 34, 48), "miss2": (135, 188, 245),
        "sh": SHARPY_RED, "bsw": BSW_RED, "prof": PROF_RED,
        "halo": H_RED, "ni": (208, 35, 50)
    },
    "loyal_cobalt": {
        "par_a": (12, 62, 168), "par_b": (0, 118, 190),
        "miss1": (38, 88, 212), "miss2": (0, 136, 212),
        "sh": SHARPY_BLUE, "bsw": BSW_TEAL, "prof": PROF_TEAL,
        "halo": H_CYN, "ni": (96, 140, 198)
    },
    "covenant_white": {
        "par_a": (255, 232, 188), "par_b": (178, 210, 255),
        "miss1": (255, 240, 205), "miss2": (182, 220, 255),
        "sh": SHARPY_WHITE, "bsw": BSW_WHITE, "prof": PROF_WHITE,
        "halo": H_RGB, "ni": (255, 236, 198)
    },
    "bond_lime": {
        "par_a": (118, 208, 4), "par_b": (36, 102, 12),
        "miss1": (138, 230, 16), "miss2": (60, 132, 8),
        "sh": SHARPY_LIME, "bsw": BSW_GREEN, "prof": PROF_GREEN,
        "halo": H_GRN, "ni": (138, 216, 28)
    },
    "night_minimal": {
        "par_a": (8, 8, 24), "par_b": (18, 8, 40),
        "miss1": (20, 10, 40), "miss2": (8, 8, 18),
        "sh": SHARPY_PURPLE, "bsw": BSW_BLUE, "prof": PROF_BLUE,
        "halo": H_OFF, "ni": (20, 10, 35)
    },
    "break_slate": {
        "par_a": (48, 52, 68), "par_b": (24, 30, 50),
        "miss1": (72, 78, 100), "miss2": (28, 34, 54),
        "sh": SHARPY_BLUE, "bsw": BSW_BLUE, "prof": PROF_BLUE,
        "halo": H_BLU, "ni": (70, 84, 112)
    },
}


# =============================================================================
# PATTERNS
# All patterns advance every 4 beats (1 bar) unless timing variant is applied.
# =============================================================================

GEOMETRIC = [
    {"name": "CenterFan", "layout": "unison", "route": ["C", "SL", "C", "SR"]},
    {"name": "DepthPush", "layout": "unison", "route": ["C", "DSC", "C", "USC"]},
    {"name": "BackRail", "layout": "unison", "route": ["USL", "USC", "USR", "USC"]},
    {"name": "FrontRail", "layout": "unison", "route": ["DSL", "DSC", "DSR", "DSC"]},
    {"name": "OuterRing", "layout": "unison", "route": ["USL", "USR", "DSR", "DSL"]},
    {"name": "TriangleUp", "layout": "unison", "route": ["SL", "USC", "SR", "C"]},
    {"name": "TriangleDown", "layout": "unison", "route": ["SL", "DSC", "SR", "C"]},
    {"name": "Orbit", "layout": "unison", "route": ["C", "SL", "USC", "SR", "DSC", "C"]},
    {"name": "BoothDrive", "layout": "unison", "route": ["DJ", "C", "DSC", "C"]},
    {"name": "CeilingDrop", "layout": "unison", "route": ["CEIL", "USC", "C", "DSC"]},
    {"name": "WallNarrative", "layout": "unison", "route": ["PAR_WALL", "SR", "C", "SR"]},
    {"name": "CrossLane", "layout": "unison", "route": ["USL", "C", "DSR", "C"]},
]

SNAP = [
    {
        "name": "Crossfire",
        "layout": "split",
        "route": [
            ("USL", "DSR", "C", "USL"),
            ("USR", "DSL", "C", "USR"),
            ("DSL", "USR", "DSC", "DSL"),
            ("DSR", "USL", "DSC", "DSR"),
        ],
    },
    {
        "name": "Hammer",
        "layout": "split",
        "route": [
            ("C", "SL", "C", "SL"),
            ("C", "SR", "C", "SR"),
            ("DSC", "USC", "DSC", "C"),
            ("USC", "DSC", "DSC", "C"),
        ],
    },
    {
        "name": "XHits",
        "layout": "split",
        "route": [
            ("USL", "DSR", "DSC", "USL"),
            ("USR", "DSL", "DSC", "USR"),
            ("USL", "DSR", "C", "DSL"),
            ("USR", "DSL", "C", "DSR"),
        ],
    },
    {
        "name": "CrowdRake",
        "layout": "split",
        "route": [
            ("DSR", "SL", "DSC", "DSR"),
            ("DSC", "C", "DSC", "C"),
            ("DSL", "SR", "DSC", "DSL"),
            ("DSC", "C", "C", "C"),
        ],
    },
    {
        "name": "CeilStab",
        "layout": "split",
        "route": [
            ("CEIL", "SL", "C", "USL"),
            ("CEIL", "SR", "C", "USR"),
            ("USC", "DSC", "DSC", "C"),
            ("DSC", "USC", "C", "C"),
        ],
    },
    {
        "name": "Knife",
        "layout": "split",
        "route": [
            ("USL", "SL", "C", "USL"),
            ("DSL", "SL", "C", "DSL"),
            ("USR", "SR", "C", "USR"),
            ("DSR", "SR", "C", "DSR"),
        ],
    },
]

ATMOSPHERIC = [
    {"name": "SlowCenter", "layout": "unison", "route": ["C", "USC", "C", "DSC"]},
    {"name": "Skyline", "layout": "unison", "route": ["CEIL", "USR", "CEIL", "USL"]},
    {"name": "BreatheLR", "layout": "unison", "route": ["SL", "C", "SR", "C"]},
    {"name": "BoothHalo", "layout": "unison", "route": ["DJ", "USC", "DJ", "C"]},
    {"name": "FrontBreathe", "layout": "unison", "route": ["DSR", "DSC", "DSL", "DSC"]},
    {"name": "BackBreathe", "layout": "unison", "route": ["USR", "USC", "USL", "USC"]},
]

FAMILY_PATTERNS = {
    "geometric": GEOMETRIC,
    "snap": SNAP,
    "atmospheric": ATMOSPHERIC,
}


def pick_palette(phrase: str, seg_idx: int, rms: float, seg_bar_idx: int) -> str:
    if phrase == "intro":
        seq = ["night_minimal", "oath_steel", "trust_teal"]
        return seq[(seg_idx + seg_bar_idx // 4) % len(seq)]
    if phrase == "breakdown":
        seq = ["night_minimal", "oath_steel", "midnight_violet"]
        return seq[(seg_idx + seg_bar_idx // 4) % len(seq)]
    if phrase == "outro":
        seq = ["break_slate", "oath_steel", "covenant_white"]
        return seq[(seg_idx + seg_bar_idx // 4) % len(seq)]
    if phrase == "drop":
        if seg_bar_idx % 8 == 0:
            return "covenant_white"
        seq = ["loyal_cobalt", "resolve_crimson", "ember_signal", "bond_lime"]
        return seq[(seg_idx + seg_bar_idx // 2) % len(seq)]
    # verse_groove, build, and fallback
    seq = ["oath_steel", "trust_teal", "ember_signal", "midnight_violet"]
    if rms > 0.70:
        seq = ["ember_signal", "resolve_crimson", "trust_teal", "loyal_cobalt"]
    return seq[(seg_idx + seg_bar_idx // 3) % len(seq)]


def pose_from_pattern(pattern: dict, state_idx: int) -> Tuple[int, int, int, int, int, int, int]:
    state = pattern["route"][state_idx % len(pattern["route"])]
    if pattern["layout"] == "unison":
        return POS[state]

    # split layout: (sh_key, bsw_key, profile_key, ni_key)
    sh_key, b_key, p_key, n_key = state
    sp, st = POS[sh_key][0], POS[sh_key][1]
    bp, bt = POS[b_key][2], POS[b_key][3]
    pp, pt = POS[p_key][4], POS[p_key][5]
    np = POS[n_key][6]
    return (sp, st, bp, bt, pp, pt, np)


PAR_STROBE = {
    "blink1": 230,
    "blink2": 165,
    "blink4": 105,
    "fade4": 0,
    "fade8": 0,
}


# =============================================================================
# SHOW BUILD
# =============================================================================

scenes = [scene("Blackout", *blackout_all(), path="Generated")]
scene_cache: Dict[Tuple, int] = {}
step_scene_ids: List[int] = []
step_timing: List[Tuple[int, int]] = []
phrase_counts: Dict[str, int] = {}
technique_counts: Dict[str, int] = {}
technique_usage_by_phrase: Dict[str, Dict[str, int]] = {}
technique_recent_by_phrase: Dict[str, List[str]] = {}

bars = build_bar_grid()
current_seg = None
seg_bar_idx = 0
previous_plan = None

for global_bar, (t0, t1) in enumerate(bars):
    mid = (t0 + t1) / 2.0
    seg_idx, seg = segment_at(mid)
    label = seg["label"]

    if seg_idx != current_seg:
        current_seg = seg_idx
        seg_bar_idx = 0
    else:
        seg_bar_idx += 1

    rms = avg_energy(e_rms, t0, t1)
    sub = avg_energy(e_sub, t0, t1)
    high = avg_energy(e_high, t0, t1)

    progress = min(1.0, max(0.0, (mid / song_end))) if song_end > 0 else 0.0
    phrase = classify_phrase(
        segment_label=label,
        rms=rms,
        sub=sub,
        high=high,
        progress=progress,
        project_root=PROJECT_ROOT,
    )
    phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

    phrase_usage = technique_usage_by_phrase.setdefault(phrase, {})
    phrase_recent = technique_recent_by_phrase.setdefault(phrase, [])
    technique = pick_phrase_technique(
        phrase=phrase,
        segment_index=seg_idx,
        global_bar=global_bar,
        usage=phrase_usage,
        recent=phrase_recent,
        cooldown=2,
        previous_plan=previous_plan,
        brand_tokens=BRAND_TOKENS,
        creative_directives=CREATIVE_DIRECTIVES,
        candidate_count=3,
        show_key=SONG_STEM,
        project_root=PROJECT_ROOT,
    )
    previous_plan = technique
    technique_id = technique["id"]
    technique_counts[technique_id] = technique_counts.get(technique_id, 0) + 1
    phrase_usage[technique_id] = phrase_usage.get(technique_id, 0) + 1
    phrase_recent.append(technique_id)
    if len(phrase_recent) > 8:
        del phrase_recent[:-8]

    family = mover_family_from_phrase(
        phrase=phrase,
        relationship=technique["relationship"],
        rms=rms,
        sub=sub,
    )
    par_mode = par_mode_from_phrase_timing(
        par_beats=int(technique["timing"]["par_beats"]),
        par_style=str(technique["timing"]["par_style"]),
        phrase=phrase,
        seg_bar_idx=seg_bar_idx,
    )
    palette_id = pick_palette(phrase, seg_idx, rms, seg_bar_idx)
    pal = PALETTES[palette_id]

    # Pattern selection rotates by segment + phrase to increase uniqueness.
    phrase_idx = global_bar // 8
    patterns = FAMILY_PATTERNS[family]
    pat = patterns[(seg_idx * 7 + phrase_idx) % len(patterns)]
    pose = pose_from_pattern(pat, seg_bar_idx)
    if phrase in ("verse_groove", "build", "drop") and (seg_bar_idx % 4 == 3):
        pose = POS["C"]
    sp, st, bp, bt, pp, pt, np = pose

    base_e = (0.62 * rms) + (0.28 * sub) + (0.10 * high)
    family_scale = {"atmospheric": 0.62, "geometric": 0.84, "snap": 1.00}[family]
    if phrase in ("breakdown", "outro"):
        family_scale *= 0.78

    mover_dim = clamp(e2d(base_e * family_scale, 60, 255))
    profile_dim = clamp(e2d(base_e * family_scale * 0.75, 30, 220))
    par_master = clamp(e2d(base_e * max(0.45, family_scale), 30, 255))
    miss_master = clamp(int(par_master * 0.75))
    ni_dim = clamp(e2d(base_e * family_scale, 20, 230))

    # Slow breathing for long fades.
    if par_mode == "fade8":
        if global_bar % 2 == 0:
            par_master = clamp(int(par_master * 0.68))
            miss_master = clamp(int(miss_master * 0.68))
        else:
            par_master = clamp(int(par_master * 0.90))
            miss_master = clamp(int(miss_master * 0.90))

    par_strobe = PAR_STROBE[par_mode]
    mover_frost = {"atmospheric": 180, "geometric": 90, "snap": 25}[family]
    prism_on = (phrase == "drop" and rms > 0.72)
    laser_on = (phrase == "drop" and rms > 0.84 and seg_bar_idx % 8 in (0, 1))

    sh_strobe = SHARPY_OPEN
    bsw_shutter = BSW_SHUT_OPEN
    prof_strobe = PROFILE_STROBE_OFF
    if family == "snap" and par_mode == "blink1":
        sh_strobe = SHARPY_STROBE_MED
        bsw_shutter = BSW_SHUT_STROBE_FAST
        prof_strobe = 64

    # NI3K tilt spread follows sub-bass energy to make lows feel bigger.
    ni_t_center = clamp(e2d(sub, 58, 185))
    ni_t1 = clamp(ni_t_center)
    ni_t2 = clamp(ni_t_center + 18)
    ni_t3 = clamp(ni_t_center - 16)

    dim_bucket = int(mover_dim / 8) * 8
    par_bucket = int(par_master / 8) * 8
    key = (
        phrase, technique_id, family, par_mode, palette_id,
        pat["name"], seg_bar_idx % len(pat["route"]),
        sp, st, bp, bt, pp, pt, np, dim_bucket, par_bucket, int(prism_on), int(laser_on),
    )

    if key not in scene_cache:
        scene_name = (
            f"{phrase[:4].upper()}-{technique_id}-{pat['name']}-"
            f"B{(seg_bar_idx % len(pat['route'])) + 1}"
        )
        if par_mode.startswith("blink"):
            par_fx = fourbar_solid(*pal["par_a"], master=par_master, strobe=par_strobe)
        else:
            par_fx = fourbar_gradient(*pal["par_a"], *pal["par_b"], master=par_master, strobe=0)

        pv = 128 if prism_on else 0
        pr = 180 if prism_on else 0
        lr = LASER_ON if laser_on else LASER_OFF
        scene_cache[key] = len(scenes)
        scenes.append(
            scene(
                scene_name,
                sharpy(
                    pan=sp, tilt=st, colormacro=pal["sh"], dim=mover_dim,
                    strobe=sh_strobe, frost=mover_frost, prism1=pv, p1r=pr
                ),
                bsw(
                    pan=bp, tilt=bt, color=pal["bsw"], dim=mover_dim,
                    shutter=bsw_shutter, frost=min(255, mover_frost + 20),
                    prism=pv, prot=pr
                ),
                profile(
                    pan=pp, tilt=pt, color=pal["prof"], dim=profile_dim, strobe=prof_strobe
                ),
                par_fx,
                miss1(*pal["miss1"], master=miss_master, strobe=par_strobe),
                miss2(*pal["miss2"], master=miss_master, strobe=par_strobe),
                ni3k(
                    pan=np, t1=ni_t1, t2=ni_t2, t3=ni_t3,
                    r=pal["ni"][0], g=pal["ni"][1], b=pal["ni"][2], w=0,
                    halo=pal["halo"], rl=lr, gl=lr, bl=lr,
                    dim=ni_dim, strobe=0
                ),
                path="Generated",
            )
        )

    sid = scene_cache[key]
    step_scene_ids.append(sid)

    bar_len = max(0.10, (t1 - t0))
    if 0.95 <= (bar_len / BAR_SEC) <= 1.05:
        if par_mode.startswith("fade"):
            timing = smooth(BPM, 1)
        elif family == "snap":
            timing = snap(BPM, 1, fade_ms=60)
        else:
            timing = hold(BPM, 1)
    else:
        ms = max(120, int(round(bar_len * 1000)))
        if par_mode.startswith("fade"):
            timing = (ms, 0)
        elif family == "snap":
            fi = min(60, max(20, ms // 4))
            timing = (fi, ms - fi)
        else:
            timing = (0, ms)
    step_timing.append(timing)

# Graceful tail.
step_scene_ids.append(0)
step_timing.append(smooth(BPM, 2))

main = make_chaser(
    SONG_STEM,
    step_scene_ids,
    step_timing,
    run_order="SingleShot",
    path="Generated",
)

write_workspace(OUT_PATH, scenes, [main], bpm=BPM)

total_ms = sum(fi + ho for fi, ho in step_timing)
print(f"Wrote: {OUT_PATH}")
print(f"  BPM: {BPM}")
print(f"  Segments: {len(segments)}")
print(f"  Bars: {len(bars)}")
print(f"  Scenes: {len(scenes)}")
print(f"  Chaser steps: {len(step_scene_ids)}")
print(f"  Runtime: {total_ms / 1000:.1f}s ({total_ms / 60000:.2f} min)")
print(f"  Phrase bars: {phrase_counts}")
print(f"  Techniques used: {len(technique_counts)} unique")
top_techniques = sorted(technique_counts.items(), key=lambda kv: kv[1], reverse=True)[:8]
print(f"  Top technique usage: {top_techniques}")
