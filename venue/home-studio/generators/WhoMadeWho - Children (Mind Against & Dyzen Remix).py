#!/usr/bin/env python3
"""
Show Generator: WhoMadeWho - Children (Mind Against & Dyzen Remix)
==================================================================
BPM: 122 | Duration: ~5:27 | Label: Embassy One (Afterlife adjacent)
Genre: Melodic Techno

Aesthetic: Afterlife unified beam organisms — all movers breathe as one
living entity through deep indigo darkness. Sunshine-to-moonbeams arc:
warm gold on vocal moments, cool silver-white on instrumental peaks.
Single euphoric revelation at 3:56 — the only moment of pure white.

Song Structure:
  0:00 - 0:45  DARK_DAWN       (23 bars) Profile at ceiling, distant star
  0:45 - 1:54  FIRST_WAVE      (35 bars) Movers enter, unified breathing
  1:54 - 2:22  CHOIR           (14 bars) Full vocal chorus, warm gold
  2:22 - 2:53  SCATTERED       (16 bars) Breakdown, fixtures isolate
  2:53 - 3:23  RECONVERGE      (15 bars) Fixtures pull back together
  3:23 - 3:56  BUILD           (17 bars) Tightening toward revelation
  3:56 - 4:16  REVELATION      (10 bars) THE CLIMAX — pure white + gold
  4:16 - 4:59  LASER_PLATEAU   (22 bars) Sustained euphoria, lasers
  4:59 - 5:36  FADE_TO_STARS   (19 bars) Decay to distant star, blackout
"""

import json
import os
import sys
import bisect

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
from showlib import *

# =============================================================================
# LOAD ANALYSIS DATA
# =============================================================================

SONG_STEM = "WhoMadeWho - Children (Mind Against & Dyzen Remix)"
BRIEF = require_research_brief(SONG_STEM, project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)
print(f"Research brief OK: {BRIEF['_meta']['brief_json']}")
print(f"Creative thesis: {BRIEF['thesis']}")

CREATIVE = build_creative_context(BRIEF, song_stem=SONG_STEM)
BRAND_TOKENS = CREATIVE["brand_tokens"]
CREATIVE_DIRECTIVES = CREATIVE["creative_directives"]

DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", f"{SONG_STEM}.json")
with open(DATA_PATH) as f:
    data = json.load(f)

BPM = data["bpm"]  # 122
beats = data["beats"]
segments = data["segments"]
e_sub = data["energy"]["sub_bass"]
e_rms = data["energy"]["rms"]
vocal_e = data["stems"]["vocals"]["energy"]

BAR_MS = bpm_to_ms(BPM, 4)   # ~1967ms
BEAT_MS = bpm_to_ms(BPM, 1)  # ~492ms

# =============================================================================
# HELPERS
# =============================================================================

def beat_at(t):
    idx = bisect.bisect_left(beats, t)
    if idx == 0: return 0
    if idx >= len(beats): return len(beats) - 1
    return idx if abs(beats[idx] - t) < abs(beats[idx-1] - t) else idx - 1

def avg_energy(arr, t_start, t_end):
    i0, i1 = beat_at(t_start), beat_at(t_end)
    if i0 >= i1: return 0.0
    return sum(arr[i0:i1]) / (i1 - i0)

def segment_at(t):
    for i, seg in enumerate(segments):
        if seg["start"] <= t < seg["end"]:
            return i, seg
    return len(segments) - 1, segments[-1]

def vocal_present(t_start, t_end):
    return avg_energy(vocal_e, t_start, t_end) > 0.015

def e2d(e, low=30, high=255):
    return int(low + (high - low) * min(1.0, max(0.0, e)))

# =============================================================================
# PHRASE-AWARE TRACKING
# =============================================================================

PHRASE_USAGE_BY_BUCKET = {}
PHRASE_RECENT_BY_BUCKET = {}
PHRASE_BAR_COUNTS = {}
TECHNIQUE_COUNTS = {}
LAST_TECHNIQUE_PLAN = None

def timing_from_phrase_technique(technique, bars_here):
    bars_here = max(0.25, float(bars_here))
    timing = technique["timing"]
    par_style = str(timing["par_style"])
    par_beats = int(timing["par_beats"])
    relationship = str(technique["relationship"])

    if par_style == "fade":
        return smooth(BPM, bars_here)
    if par_style == "chase":
        if par_beats <= 1 and relationship == "inclusion":
            return snap(BPM, bars_here, fade_ms=60)
        if par_beats <= 2:
            return hold(BPM, bars_here)
        return smooth(BPM, bars_here)
    return smooth(BPM, bars_here)

def phrase_step_timing(t_start, t_end, bars_here):
    """Returns (timing_tuple, technique_dict) — timing + full technique."""
    global LAST_TECHNIQUE_PLAN
    mid = (t_start + t_end) / 2.0
    seg_idx, seg = segment_at(mid)
    label = seg["label"]

    rms = avg_energy(e_rms, t_start, t_end)
    sub = avg_energy(e_sub, t_start, t_end)
    high = rms
    progress = min(1.0, max(0.0, mid / max(1.0, beats[-1])))

    phrase = classify_phrase(
        segment_label=label, rms=rms, sub=sub, high=high,
        progress=progress, project_root=PROJECT_ROOT,
    )

    usage = PHRASE_USAGE_BY_BUCKET.setdefault(phrase, {})
    recent = PHRASE_RECENT_BY_BUCKET.setdefault(phrase, [])
    global_bar = int(round((t_start * 1000.0) / BAR_MS))

    technique = pick_phrase_technique(
        phrase=phrase, segment_index=seg_idx, global_bar=global_bar,
        usage=usage, recent=recent, cooldown=2,
        previous_plan=LAST_TECHNIQUE_PLAN,
        brand_tokens=BRAND_TOKENS, creative_directives=CREATIVE_DIRECTIVES,
        candidate_count=3, show_key=SONG_STEM, project_root=PROJECT_ROOT,
    )
    LAST_TECHNIQUE_PLAN = technique
    technique_id = technique["id"]
    usage[technique_id] = usage.get(technique_id, 0) + 1
    recent.append(technique_id)
    if len(recent) > 8:
        del recent[:-8]

    PHRASE_BAR_COUNTS[phrase] = PHRASE_BAR_COUNTS.get(phrase, 0) + max(1, int(round(bars_here)))
    TECHNIQUE_COUNTS[technique_id] = TECHNIQUE_COUNTS.get(technique_id, 0) + 1
    return (timing_from_phrase_technique(technique, bars_here), technique)

def next_step_bars(technique):
    """Extract dynamic step size from technique's beat_reactivity, capped at 2."""
    br = technique.get("beat_reactivity") or {}
    return min(2, reactivity_to_bars(br.get("mover_min", "2bar")))

# =============================================================================
# COLOR PALETTE — Afterlife: deep indigo + desaturated gold/silver
# =============================================================================

# RGB for pars/missyees (desaturated per Afterlife principle)
DEEP_INDIGO  = (8, 5, 40)
PALE_GOLD    = (160, 120, 50)
WARM_CREAM   = (140, 110, 70)
COOL_SILVER  = (120, 135, 160)
REVEAL_WHITE = (220, 200, 160)   # warm white-gold for the climax
BLOOD_MIST   = (90, 8, 12)      # single red punctuation (desaturated)
NEAR_BLACK   = (3, 2, 8)
NOTHING      = (0, 0, 0)

# Mover color wheels — Afterlife palette
SH_INDIGO  = SHARPY_BLUE       # 30
SH_GOLD    = SHARPY_AMBER      # 80
SH_SILVER  = SHARPY_WHITE      # 0
SH_RED     = SHARPY_RED        # 10

BSW_INDIGO = BSW_BLUE          # 44
BSW_GOLD   = BSW_YELLOW        # 32
BSW_SILVER = BSW_WHITE         # 0
BSW_RED_C  = BSW_RED           # 20

PF_INDIGO  = PROF_BLUE         # 15
PF_GOLD    = PROF_YELLOW       # 10
PF_SILVER  = PROF_WHITE        # 0

# =============================================================================
# POSITIONS
# =============================================================================

POS = load_focus_position_tuples(project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)

# Organism breathing: slow unified pendulum
PENDULUM   = ["SL", "C", "SR", "C"]
WIDE_SWEEP = ["DSL", "C", "DSR", "C"]
CONVERGE   = ["SL", "C", "SR", "DSC", "C"]

# =============================================================================
# SECTIONS — hand-crafted from 20 analysis segments
# =============================================================================

SECTIONS = [
    {"name": "DARK_DAWN",      "start": 0.0,    "end": 45.35,  "bars": 23},
    {"name": "FIRST_WAVE",     "start": 45.35,  "end": 114.20, "bars": 35},
    {"name": "CHOIR",          "start": 114.20, "end": 141.76, "bars": 14},
    {"name": "SCATTERED",      "start": 141.76, "end": 173.23, "bars": 16},
    {"name": "RECONVERGE",     "start": 173.23, "end": 202.74, "bars": 15},
    {"name": "BUILD",          "start": 202.74, "end": 236.18, "bars": 17},
    {"name": "REVELATION",     "start": 236.18, "end": 255.85, "bars": 10},
    {"name": "LASER_PLATEAU",  "start": 255.85, "end": 299.12, "bars": 22},
    {"name": "FADE_TO_STARS",  "start": 299.12, "end": 336.40, "bars": 19},
]

# =============================================================================
# SCENE FACTORY
# =============================================================================

scenes = []
folder = "Children"
scenes.append(scene("Blackout", *blackout_all(), path=folder))

steps = []
cache = {}

def cached(key, fn):
    if key not in cache:
        cache[key] = len(scenes)
        scenes.append(fn())
    return cache[key]


def atmo(name, pos_key, energy, frost=210,
         s_color=SH_INDIGO, b_color=BSW_INDIGO, p_color=PF_INDIGO,
         par=DEEP_INDIGO, miss=NEAR_BLACK,
         ni_rgb=DEEP_INDIGO, halo=H_OFF,
         s_dim=None, b_dim=None, p_dim=None, par_m=None,
         prism=False, lasers=False,
         ni_tilt=(64, 64, 64)):
    """Afterlife atmosphere using look helpers — deep indigo defaults."""
    sd = s_dim if s_dim is not None else e2d(energy, 30, 180)
    bd = b_dim if b_dim is not None else e2d(energy, 20, 160)
    pd = p_dim if p_dim is not None else e2d(energy * 0.5, 20, 140)
    pm = par_m if par_m is not None else e2d(energy, 15, 200)
    nd = e2d(energy * 0.45, 15, 160)

    return scene(name,
        *mover_look(pos_key, POS,
                    colors=(s_color, b_color, p_color),
                    dims=(sd, bd, pd),
                    frost=(frost, min(255, frost)),
                    prism=prism, focus=128),
        *par_look("solid", par, master=pm,
                  miss_color=miss, miss_master=pm // 3),
        ni3k_look(pos_key, POS, rgb=ni_rgb, dim=nd,
                  halo=halo, lasers=lasers,
                  tilt_values=ni_tilt),
        path=folder)


def distant_star(name, dim, halo=H_OFF, par=NEAR_BLACK, par_m=0,
                 ni_rgb=NEAR_BLACK, ni_dim=15):
    """Profile at ceiling only — all else dark. Distant star in space."""
    dsc = POS["DSC"]
    ceil_p = POS["CEIL"]

    return scene(name,
        dark_sharpy(pan=dsc[0], tilt=dsc[1]),
        dark_bsw(pan=dsc[2], tilt=dsc[3]),
        profile(pan=ceil_p[4], tilt=ceil_p[5], color=PF_INDIGO,
                dim=dim, focus=128),
        *par_look("solid", par, master=par_m,
                  miss_color=NOTHING, miss_master=0),
        ni3k_look("DSC", POS, rgb=ni_rgb, dim=ni_dim, halo=halo),
        path=folder)


# =============================================================================
# SECTION BUILDERS
# =============================================================================

def build_dark_dawn(sec):
    """DARK_DAWN (0:00-0:45, 23 bars): Eyes adjusting to the infinite.

    Profile at CEIL as a distant star, barely visible. 4BAR deep indigo
    atmosphere. NI3K subtle blue. Everything else dark.
    At ~14s when first vocals appear, a breath of warmth in the 4BAR.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        has_vocal = vocal_present(t, next_t)

        p_dim = int(10 + 25 * prog)
        par_m = int(5 + 40 * prog)
        par_c = PALE_GOLD if has_vocal and prog > 0.3 else DEEP_INDIGO
        ni_dim = max(15, int(15 + 10 * prog)) if prog > 0.3 else 15
        h = H_BLU if prog > 0.4 else H_OFF

        sid = cached(f"dawn_{n}", lambda: distant_star(
            f"Dawn {n}", dim=p_dim, halo=h,
            par=par_c, par_m=par_m,
            ni_rgb=DEEP_INDIGO, ni_dim=ni_dim))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_first_wave(sec):
    """FIRST_WAVE (0:45-1:54, 35 bars): The organism awakens.

    Sharpy enters first (dim 30-80), BSW joins at bar 4. Both breathe
    together in slow pendulum sweeps. Profile stays at CEIL (dim 20).
    Vocal moments: 4BAR shifts to pale gold (sunshine).
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    ceil_p = POS["CEIL"]
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        pos = PENDULUM[n % len(PENDULUM)]

        s_dim = int(30 + 50 * prog)
        b_dim = int(30 + 50 * max(0, (prog - 0.11)) / 0.89) if prog > 0.11 else 0
        par_m = int(20 + 80 * prog)
        ni_dim = max(15, int(15 + 15 * prog))

        if has_vocal:
            s_col, b_col = SH_GOLD, BSW_GOLD
            par_c = PALE_GOLD
        else:
            s_col, b_col = SH_INDIGO, BSW_INDIGO
            par_c = DEEP_INDIGO

        p = POS[pos]
        sp, st, bp, bt, _, _, ni_pan = p

        sid = cached(f"wave_{n}", lambda: scene(
            f"Wave {n}",
            sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=s_dim,
                   frost=210, colormacro=s_col, focus=128),
            bsw(pan=bp, tilt=bt, color=b_col, shutter=BSW_SHUT_OPEN,
                dim=b_dim, frost=220, focus=128)
                if b_dim > 0 else dark_bsw(pan=bp, tilt=bt),
            profile(pan=ceil_p[4], tilt=ceil_p[5], color=PF_INDIGO,
                    dim=20, focus=128),
            *par_look("solid", par_c, master=par_m,
                      miss_color=NEAR_BLACK, miss_master=par_m // 5),
            ni3k_look(pos, POS, rgb=DEEP_INDIGO, dim=ni_dim,
                      halo=H_BLU if prog > 0.3 else H_OFF),
            path=folder))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_choir(sec):
    """CHOIR (1:54-2:22, 14 bars): Full vocal chorus — warm gold organism.

    All three movers now breathing together at floor level. Profile
    descends from ceiling to join the organism. Warm cream/gold palette
    on vocals, indigo on instrumental beats. NI3K warm amber halo.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    sweep = ["C", "SL", "C", "SR", "DSC", "C"]
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        pos = sweep[n % len(sweep)]

        s_dim = int(60 + 40 * energy)
        b_dim = int(50 + 35 * energy)
        p_dim = int(30 + 30 * energy)

        if has_vocal:
            s_col, b_col, p_col = SH_GOLD, BSW_GOLD, PF_GOLD
            par_c = WARM_CREAM
            miss_c = PALE_GOLD
        else:
            s_col, b_col, p_col = SH_INDIGO, BSW_INDIGO, PF_INDIGO
            par_c = DEEP_INDIGO
            miss_c = NEAR_BLACK

        par_m = int(40 + 60 * energy)

        sid = cached(f"choir_{n}", lambda: atmo(
            f"Choir {n}", pos, energy, 200,
            s_color=s_col, b_color=b_col, p_color=p_col,
            par=par_c, miss=miss_c,
            ni_rgb=WARM_CREAM if has_vocal else DEEP_INDIGO,
            halo=H_YEL if has_vocal else H_BLU,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim,
            par_m=par_m))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_scattered(sec):
    """SCATTERED (2:22-2:53, 16 bars): Children scatter — fixtures isolate.

    THE BREAKDOWN. Movers separate to different positions — the only time
    they aren't moving as one organism. Cool silver-white "moonbeams"
    palette. Dimming toward center, recover on bridge vocals (2:36).
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 2

    s_targets = ["SL", "USL", "DSL", "SL"]
    b_targets = ["SR", "USR", "DSR", "SR"]
    p_targets = ["CEIL", "CEIL", "USC", "CEIL"]

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)

        # Dim curve: dips in center of section, recovers for bridge vocals
        dim_curve = max(0.25, 1.0 - 0.6 * (1.0 - abs(prog - 0.5) * 2))
        s_dim = max(30, int(55 * dim_curve))
        b_dim = max(30, int(45 * dim_curve))
        p_dim = max(20, int(35 * dim_curve))

        s_pos = POS[s_targets[n % len(s_targets)]]
        b_pos = POS[b_targets[n % len(b_targets)]]
        p_pos = POS[p_targets[n % len(p_targets)]]

        par_c = COOL_SILVER if has_vocal else NEAR_BLACK
        par_m = int(30 * dim_curve) if has_vocal else int(15 * dim_curve)
        ni_dim = max(15, int(25 * dim_curve))

        sid = cached(f"scat_{n}", lambda: scene(
            f"Scattered {n}",
            sharpy(pan=s_pos[0], tilt=s_pos[1], strobe=SHARPY_OPEN,
                   dim=s_dim, frost=230, colormacro=SH_SILVER, focus=128),
            bsw(pan=b_pos[2], tilt=b_pos[3], color=BSW_SILVER,
                shutter=BSW_SHUT_OPEN, dim=b_dim, frost=240, focus=128),
            profile(pan=p_pos[4], tilt=p_pos[5], color=PF_SILVER,
                    dim=p_dim, focus=128),
            *par_look("solid", par_c, master=par_m,
                      miss_color=NOTHING, miss_master=0),
            ni3k_look("C", POS,
                      rgb=(COOL_SILVER[0] // 3, COOL_SILVER[1] // 3,
                           COOL_SILVER[2] // 3),
                      dim=ni_dim,
                      halo=H_BLU if ni_dim > 15 else H_OFF),
            path=folder))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_reconverge(sec):
    """RECONVERGE (2:53-3:23, 15 bars): Children gather — organism reforms.

    Fixtures slowly pull back together. Phase 1 (0-50%): Sharpy + BSW
    converge, Profile still at ceiling. Phase 2 (50-100%): all three
    unified again. Cool silver fading back to deep indigo.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    ceil_p = POS["CEIL"]
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos = CONVERGE[n % len(CONVERGE)]

        s_dim = int(30 + 60 * prog)
        b_dim = int(30 + 55 * prog)
        p_dim = max(20, int(50 * max(0, (prog - 0.3)) / 0.7)) if prog > 0.3 else 20
        par_m = int(20 + 60 * prog)
        frost = int(230 - 20 * prog)
        ni_dim = max(15, int(15 + 15 * prog))

        if prog < 0.5:
            par_c = COOL_SILVER
            s_col, b_col = SH_SILVER, BSW_SILVER
        else:
            par_c = DEEP_INDIGO
            s_col, b_col = SH_INDIGO, BSW_INDIGO

        p = POS[pos]
        sp, st, bp, bt, pp, pt, ni_pan = p

        # Profile: at CEIL in phase 1, joins floor in phase 2
        use_floor = prog > 0.4
        p_pan = pp if use_floor else ceil_p[4]
        p_tilt = pt if use_floor else ceil_p[5]

        sid = cached(f"reconv_{n}", lambda: scene(
            f"Reconverge {n}",
            sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=s_dim,
                   frost=frost, colormacro=s_col, focus=128),
            bsw(pan=bp, tilt=bt, color=b_col, shutter=BSW_SHUT_OPEN,
                dim=b_dim, frost=frost, focus=128),
            profile(pan=p_pan, tilt=p_tilt, color=PF_INDIGO,
                    dim=p_dim, focus=128),
            *par_look("solid", par_c, master=par_m,
                      miss_color=NEAR_BLACK, miss_master=par_m // 5),
            ni3k_look(pos, POS, rgb=DEEP_INDIGO, dim=ni_dim,
                      halo=H_BLU if prog > 0.3 else H_OFF),
            path=folder))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_build(sec):
    """BUILD (3:23-3:56, 17 bars): Converging toward revelation.

    All movers unified, pulling toward DSC. Dynamic step sizes (faster
    as build progresses). Frost decreasing (beams sharpening). One
    blood-red punctuation at ~bar 11. Everything saving for THE moment.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    positions = ["C", "SR", "DSC", "SL", "C", "DSC", "C", "DSC"]
    n = 0
    step_bars = 2

    red_start = sec["start"] + bar * 11
    red_end = red_start + bar * 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos = positions[n % len(positions)]

        s_dim = int(50 + 80 * prog)
        b_dim = int(40 + 70 * prog)
        p_dim = int(20 + 50 * prog)
        par_m = int(40 + 100 * prog)
        frost = int(210 - 60 * prog)

        is_red = red_start <= t < red_end
        if is_red:
            s_col, b_col = SH_RED, BSW_RED_C
            par_c = BLOOD_MIST
        else:
            s_col, b_col = SH_INDIGO, BSW_INDIGO
            par_c = DEEP_INDIGO

        # Last 4 bars: lock on DSC, intensity surging
        if prog > 0.75:
            pos = "DSC"
            s_dim = min(200, int(s_dim * 1.3))
            b_dim = min(180, int(b_dim * 1.3))

        sid = cached(f"build_{n}", lambda: atmo(
            f"Build {n}", pos, energy, frost,
            s_color=s_col, b_color=b_col, p_color=PF_INDIGO,
            par=par_c, miss=NEAR_BLACK,
            ni_rgb=BLOOD_MIST if is_red else DEEP_INDIGO,
            halo=H_RED if is_red else H_BLU,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim,
            par_m=par_m))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_revelation(sec):
    """REVELATION (3:56-4:16, 10 bars): The single euphoric moment.

    Pure white + pale gold. Full rig at maximum brightness. THE reveal.
    All movers converge at DSC then sweep wide. Prism on for the
    "eyes opening" fracture. The ONLY moment of full white in the show.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    sweep = ["DSC", "C", "SL", "DSC", "SR"]
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos = sweep[n % len(sweep)]

        # Full brightness — the only time we go this high
        s_dim = int(200 + 55 * energy)
        b_dim = int(180 + 50 * energy)
        p_dim = int(100 + 55 * energy)
        par_m = int(180 + 75 * energy)

        # First 2 bars: hold at DSC for maximum impact
        if prog < 0.2:
            pos = "DSC"

        frost = int(140 - 60 * energy)

        sid = cached(f"rev_{n}", lambda: atmo(
            f"Revelation {n}", pos, energy, frost,
            s_color=SH_SILVER, b_color=BSW_SILVER, p_color=PF_SILVER,
            par=REVEAL_WHITE, miss=PALE_GOLD,
            ni_rgb=REVEAL_WHITE, halo=H_YEL,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m,
            prism=True))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_laser_plateau(sec):
    """LASER_PLATEAU (4:16-4:59, 22 bars): Sustained euphoria with lasers.

    Post-climax energy sustain. NI3K lasers ON. Deep indigo + gold on
    vocals. Movers breathe in wide slow sweeps. NI3K tilt heads rotate
    for laser scanning effect.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        pos = WIDE_SWEEP[n % len(WIDE_SWEEP)]

        s_dim = int(120 + 40 * energy)
        b_dim = int(100 + 35 * energy)
        p_dim = int(40 + 30 * energy)
        par_m = int(80 + 60 * energy)

        if has_vocal:
            par_c, s_col = WARM_CREAM, SH_GOLD
        else:
            par_c, s_col = DEEP_INDIGO, SH_INDIGO

        sid = cached(f"plateau_{n}", lambda: atmo(
            f"Plateau {n}", pos, energy, 180,
            s_color=s_col, b_color=BSW_INDIGO, p_color=PF_INDIGO,
            par=par_c, miss=NEAR_BLACK,
            ni_rgb=DEEP_INDIGO, halo=H_CYN,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m,
            lasers=True, ni_tilt=(160, 180, 170)))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_fade_to_stars(sec):
    """FADE_TO_STARS (4:59-5:36, 19 bars): Return to the distant star.

    Phase 1 (~8 bars): movers dim out one by one (BSW first, then Sharpy).
    Phase 2 (~11 bars): back to Profile at ceiling — bookending the show.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 2
    phase2_start = sec["start"] + bar * 8

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)

        if t < phase2_start:
            # Phase 1: strip down
            dim_f = max(0.0, 1.0 - prog * 1.5)
            s_dim = int(80 * dim_f)
            b_dim = int(50 * dim_f) if prog < 0.25 else 0
            p_dim = max(20, int(30 * dim_f))
            par_m = int(60 * dim_f)
            ni_dim = max(15, int(30 * dim_f))

            p = POS["C"]
            dsc = POS["DSC"]

            sid = cached(f"fade1_{n}", lambda: scene(
                f"Fade {n}",
                sharpy(pan=p[0], tilt=p[1], strobe=SHARPY_OPEN, dim=s_dim,
                       frost=220, colormacro=SH_INDIGO, focus=128)
                    if s_dim > 0 else dark_sharpy(pan=p[0], tilt=p[1]),
                bsw(pan=p[2], tilt=p[3], color=BSW_INDIGO,
                    shutter=BSW_SHUT_OPEN, dim=b_dim, frost=220, focus=128)
                    if b_dim > 0 else dark_bsw(pan=p[2], tilt=p[3]),
                profile(pan=p[4], tilt=p[5], color=PF_INDIGO,
                        dim=p_dim, focus=128),
                *par_look("solid",
                          tuple(int(c * dim_f) for c in DEEP_INDIGO),
                          master=par_m,
                          miss_color=NOTHING, miss_master=0),
                ni3k_look("C", POS, rgb=DEEP_INDIGO, dim=ni_dim,
                          halo=H_BLU if dim_f > 0.3 else H_OFF),
                path=folder))
        else:
            # Phase 2: distant star bookend
            star_prog = (t - phase2_start) / max(0.1, t_end - phase2_start)
            p_dim = max(0, int(25 * (1.0 - star_prog)))
            par_m = max(0, int(15 * (1.0 - star_prog)))
            ni_dim = max(0, int(15 * (1.0 - star_prog)))

            sid = cached(f"fade2_{n}", lambda: distant_star(
                f"Star {n}", dim=p_dim,
                halo=H_BLU if star_prog < 0.5 else H_OFF,
                par=DEEP_INDIGO if star_prog < 0.6 else NOTHING,
                par_m=par_m, ni_dim=ni_dim))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique)
        steps.append((sid, timing))
        t = next_t
        n += 1

    # Final blackout
    steps.append((0, snap(BPM, 0.5, fade_ms=100)))


# =============================================================================
# MAIN — dispatch sections + insert transitions
# =============================================================================

BUILDERS = {
    "DARK_DAWN":      build_dark_dawn,
    "FIRST_WAVE":     build_first_wave,
    "CHOIR":          build_choir,
    "SCATTERED":      build_scattered,
    "RECONVERGE":     build_reconverge,
    "BUILD":          build_build,
    "REVELATION":     build_revelation,
    "LASER_PLATEAU":  build_laser_plateau,
    "FADE_TO_STARS":  build_fade_to_stars,
}

print(f"Generating show: {SONG_STEM}")
print(f"  BPM: {BPM}, Beats: {len(beats)}, Duration: {beats[-1]:.1f}s")
print()

prev_phrase = None
prev_energy = 0.0
recent_transitions = []
last_scene_dict = None

for i, sec in enumerate(SECTIONS):
    energy = avg_energy(e_rms, sec["start"], sec["end"])

    # --- Transition at section boundary ---
    trans_offset_s = 0.0
    if i > 0:
        _, seg_here = segment_at(sec["start"])
        cur_phrase = classify_phrase(
            segment_label=seg_here["label"],
            rms=energy, sub=avg_energy(e_sub, sec["start"], sec["end"]),
            high=energy,
            progress=sec["start"] / max(1.0, beats[-1]),
            project_root=PROJECT_ROOT,
        )
        trans = plan_segment_transition(
            prev_phrase=prev_phrase, next_phrase=cur_phrase,
            prev_energy=prev_energy, next_energy=energy,
            segment_index=i, total_segments=len(SECTIONS),
            recent_transitions=recent_transitions,
            show_key=SONG_STEM,
            end_of_show=(i == len(SECTIONS) - 1),
            prev_segment_beats=SECTIONS[i-1]["bars"] * 4,
            next_segment_beats=sec["bars"] * 4,
            project_root=PROJECT_ROOT,
        )
        t_scenes, t_timing = build_transition_scenes(
            trans, BPM, pos_tuples=POS, palette=DEEP_INDIGO,
            last_scene=last_scene_dict,
        )
        for ts, tt in zip(t_scenes, t_timing):
            idx = len(scenes)
            scenes.append(ts)
            steps.append((idx, tt))
            trans_offset_s += (tt[0] + tt[1]) / 1000.0
        if trans:
            recent_transitions.append(trans["type"])
            if len(recent_transitions) > 6:
                del recent_transitions[:-6]

    # Offset section start so transitions borrow time
    build_sec = sec
    if trans_offset_s > 0:
        build_sec = {**sec, "start": sec["start"] + trans_offset_s}

    print(f"  Building {sec['name']:16s} ({sec['bars']:2d} bars, e={energy:.2f})")
    BUILDERS[sec["name"]](build_sec)

    # Track last scene for freeze-style transitions
    if steps:
        last_scene_dict = scenes[steps[-1][0]]

    # Use analysis segment label for prev_phrase
    _, seg_at_end = segment_at(sec["end"] - 0.1)
    prev_phrase = classify_phrase(
        segment_label=seg_at_end["label"],
        rms=energy, sub=avg_energy(e_sub, sec["start"], sec["end"]),
        high=energy,
        progress=sec["end"] / max(1.0, beats[-1]),
        project_root=PROJECT_ROOT,
    )
    prev_energy = energy

# =============================================================================
# STATS + OUTPUT
# =============================================================================

print(f"\nTotal scenes: {len(scenes)}")
print(f"Total chaser steps: {len(steps)}")
print(f"Phrase bars: {PHRASE_BAR_COUNTS}")
top_techniques = sorted(TECHNIQUE_COUNTS.items(), key=lambda kv: kv[1], reverse=True)[:8]
print(f"Top technique usage: {top_techniques}")

total_ms = sum(fi + ho for _, (fi, ho) in steps)
print(f"Total duration: {total_ms/1000:.1f}s (target: ~{beats[-1]:.0f}s)")

main_chaser = make_chaser("Children", [s for s, _ in steps], [t for _, t in steps],
                           run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "\u25b6 CHILDREN",  "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10,  "w": 470, "h": 100, "color": "#080528", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,  "color": "#FF0000", "action": "Toggle"},
]

output_path = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")
write_workspace(output_path, scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
