#!/usr/bin/env python3
"""
Show Generator: CamelPhat & Josh Gigante - The One
===================================================
BPM: 125 | Duration: ~3:38 | Label: When Stars Align

Aesthetic: Dark warehouse, CamelPhat "Dark Matter" era. Charcoal/cold blue
base, electric teal transitions, warm amber at emotional peaks. Josh Gigante's
Afterlife/Diynamic influence = controlled cinematic journey, restrained strobing.

Wide coverage: Split positions — Sharpy and BSW aim at DIFFERENT parts of the
room simultaneously. Cycles through all corners — CEIL, DSC, DSL, DSR, SL, SR,
USC, DJ, X — using distinct sweep paths per section.

Song Structure:
  0:00 - 0:23  INTRO      (12 bars, rms=0.68, sub=0.39) Opens with impact
  0:23 - 0:54  STRIP      (16 bars, rms=0.30, sub=0.09) Energy drops
  0:54 - 1:25  PEAK_1     (16 bars, rms=0.90, sub=0.56) First full peak
  1:25 - 2:15  BREAKDOWN  (26 bars, rms=0.24, sub=0.04) Near-silence valley
  2:15 - 2:35  BUILD      (10 bars, rms=0.50, sub=0.10) Tension rising
  2:35 - 3:37  PEAK_2     (32 bars, rms=0.88, sub=0.55) Sustained climax
  3:37 - 3:44  OUTRO      ( 4 bars, rms=0.13)           Quick fade
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

SONG_STEM = "CamelPhat & Josh Gigante - The One"
BRIEF = require_research_brief(SONG_STEM, project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)
print(f"Research brief OK: {BRIEF['_meta']['brief_json']}")
print(f"Creative thesis: {BRIEF['thesis']}")
DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", f"{SONG_STEM}.json")

CREATIVE = build_creative_context(BRIEF, song_stem=SONG_STEM)
BRAND_TOKENS = CREATIVE["brand_tokens"]
CREATIVE_DIRECTIVES = CREATIVE["creative_directives"]

with open(DATA_PATH) as f:
    data = json.load(f)

BPM = data["bpm"]  # 125
beats = data["beats"]
segments = data["segments"]

e_sub  = data["energy"]["sub_bass"]
e_rms  = data["energy"]["rms"]
e_high = data["energy"]["high"]

vocal_e      = data["stems"]["vocals"]["energy"]
bass_onsets  = data["stems"]["bass"]["onsets"]
drum_onsets  = data["stems"]["drums"]["onsets"]

BAR_MS  = bpm_to_ms(BPM, 4)   # 1920 ms
BEAT_MS = bpm_to_ms(BPM, 1)   #  480 ms

# =============================================================================
# HELPERS
# =============================================================================

def beat_at(t):
    idx = bisect.bisect_left(beats, t)
    if idx == 0: return 0
    if idx >= len(beats): return len(beats) - 1
    return idx if abs(beats[idx] - t) < abs(beats[idx-1] - t) else idx - 1

def avg_energy(arr, t0, t1):
    i0, i1 = beat_at(t0), beat_at(t1)
    if i0 >= i1: return 0.0
    return sum(arr[i0:i1]) / (i1 - i0)

def segment_at(t):
    for i, seg in enumerate(segments):
        if seg["start"] <= t < seg["end"]:
            return i, seg
    return len(segments) - 1, segments[-1]

def vocal_present(t0, t1):
    return avg_energy(vocal_e, t0, t1) > 0.015

def e2d(e, lo=30, hi=255):
    return int(lo + (hi - lo) * min(1.0, max(0.0, e)))

# =============================================================================
# PHRASE-AWARE HARD LAYER (anti-overuse, not strict uniqueness)
# =============================================================================

PHRASE_BALANCE_ENABLED = True
PHRASE_TECH_COOLDOWN = 2

PHRASE_USAGE_BY_BUCKET = {}
PHRASE_RECENT_BY_BUCKET = {}
PHRASE_BAR_COUNTS = {}
TECHNIQUE_COUNTS = {}
LAST_TECHNIQUE_PLAN = None

def timing_from_phrase_technique(technique, bars_here):
    bars_here = max(1.0, float(bars_here))
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
    global LAST_TECHNIQUE_PLAN
    mid = (t_start + t_end) / 2.0
    seg_idx, seg = segment_at(mid)
    label = seg["label"]

    rms = avg_energy(e_rms, t_start, t_end)
    sub = avg_energy(e_sub, t_start, t_end)
    high = avg_energy(e_high, t_start, t_end)
    progress = min(1.0, max(0.0, mid / max(1.0, beats[-1])))

    phrase = classify_phrase(
        segment_label=label,
        rms=rms,
        sub=sub,
        high=high,
        progress=progress,
        project_root=PROJECT_ROOT,
    )

    usage = PHRASE_USAGE_BY_BUCKET.setdefault(phrase, {}) if PHRASE_BALANCE_ENABLED else None
    recent = PHRASE_RECENT_BY_BUCKET.setdefault(phrase, [])
    global_bar = int(round((t_start * 1000.0) / BAR_MS))

    technique = pick_phrase_technique(
        phrase=phrase,
        segment_index=seg_idx,
        global_bar=global_bar,
        usage=usage,
        recent=recent,
        cooldown=PHRASE_TECH_COOLDOWN,
        previous_plan=LAST_TECHNIQUE_PLAN,
        brand_tokens=BRAND_TOKENS,
        creative_directives=CREATIVE_DIRECTIVES,
        candidate_count=3,
        show_key=SONG_STEM,
        project_root=PROJECT_ROOT,
    )
    LAST_TECHNIQUE_PLAN = technique
    technique_id = technique["id"]
    if usage is not None:
        usage[technique_id] = usage.get(technique_id, 0) + 1
    recent.append(technique_id)
    if len(recent) > 8:
        del recent[:-8]

    PHRASE_BAR_COUNTS[phrase] = PHRASE_BAR_COUNTS.get(phrase, 0) + max(1, int(round(bars_here)))
    TECHNIQUE_COUNTS[technique_id] = TECHNIQUE_COUNTS.get(technique_id, 0) + 1
    return timing_from_phrase_technique(technique, bars_here)

# =============================================================================
# COLOR PALETTE
# =============================================================================

COLD_BLUE     = (30,  50,  150)
ELECTRIC_TEAL = (20,  180, 200)
DEEP_VIOLET   = (80,  20,  150)
WARM_AMBER    = (220, 150, 40)
COLD_WHITE    = (220, 220, 230)
NEAR_BLACK    = (5,   5,   10)
DARK_CHARCOAL = (25,  25,  35)
NOTHING       = (0,   0,   0)

# =============================================================================
# POSITION TABLES — loaded from venue focus-positions.md
# =============================================================================

POS = load_focus_position_tuples(project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)

# =============================================================================
# SPLIT POSITION TABLE
# Each entry is (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt,
#                prof_pan, prof_tilt, ni3k_pan)
# Sharpy and BSW aim at DIFFERENT parts of the room for wide spatial coverage.
# =============================================================================

SPLIT = {
    # Name          sharpy from    bsw from      prof middle
    "HIGH_LOW":  (POS["CEIL"][0], POS["CEIL"][1], POS["DSC"][2],  POS["DSC"][3],   POS["C"][4],   POS["C"][5],   128),
    "SPREAD":    (POS["SL"][0],   POS["SL"][1],   POS["SR"][2],   POS["SR"][3],    POS["C"][4],   POS["C"][5],   128),
    "DEEP":      (POS["USC"][0],  POS["USC"][1],  POS["DSC"][2],  POS["DSC"][3],   POS["C"][4],   POS["C"][5],   128),
    "DIAG_L":    (POS["DSR"][0],  POS["DSR"][1],  POS["SL"][2],   POS["SL"][3],    POS["DSC"][4], POS["DSC"][5], 80),
    "DIAG_R":    (POS["DSL"][0],  POS["DSL"][1],  POS["SR"][2],   POS["SR"][3],    POS["DSC"][4], POS["DSC"][5], 176),
    "FAR_L":     (POS["DSC"][0],  POS["DSC"][1],  POS["SL"][2],   POS["SL"][3],    POS["DSL"][4], POS["DSL"][5], 80),
    "FAR_R":     (POS["DSC"][0],  POS["DSC"][1],  POS["SR"][2],   POS["SR"][3],    POS["DSR"][4], POS["DSR"][5], 176),
    "CEIL_DJ":   (POS["CEIL"][0], POS["CEIL"][1], POS["DJ"][2],   POS["DJ"][3],    POS["DSC"][4], POS["DSC"][5], 128),
    "CEIL_SL":   (POS["CEIL"][0], POS["CEIL"][1], POS["SL"][2],   POS["SL"][3],    POS["C"][4],   POS["C"][5],   80),
    "CEIL_SR":   (POS["CEIL"][0], POS["CEIL"][1], POS["SR"][2],   POS["SR"][3],    POS["C"][4],   POS["C"][5],   176),
    "USC_DSL":   (POS["USC"][0],  POS["USC"][1],  POS["DSL"][2],  POS["DSL"][3],   POS["C"][4],   POS["C"][5],   80),
    "USC_DSR":   (POS["DSL"][0],  POS["DSL"][1],  POS["USC"][2],  POS["USC"][3],   POS["C"][4],   POS["C"][5],   176),
    "X_CEIL":    (POS["SR"][0],   POS["SR"][1],   POS["DSL"][2],  POS["DSL"][3],   POS["CEIL"][4],POS["CEIL"][5],128),
    "FULL_L":    (POS["DSR"][0],  POS["DSR"][1],  POS["USC"][2],  POS["USC"][3],   POS["DSL"][4], POS["DSL"][5], 80),
    "FULL_R":    (POS["DSL"][0],  POS["DSL"][1],  POS["USR"][2],  POS["USR"][3], POS["DSR"][4], POS["DSR"][5], 176),
}

# =============================================================================
# SECTIONS
# =============================================================================

SECTIONS = [
    {"name": "INTRO",     "start": 0.0,   "end": 23.0,  "bars": 12},
    {"name": "STRIP",     "start": 23.0,  "end": 54.0,  "bars": 16},
    {"name": "PEAK_1",    "start": 54.0,  "end": 85.0,  "bars": 16},
    {"name": "BREAKDOWN", "start": 85.0,  "end": 135.0, "bars": 26},
    {"name": "BUILD",     "start": 135.0, "end": 155.0, "bars": 10},
    {"name": "PEAK_2",    "start": 155.0, "end": 217.0, "bars": 32},
    {"name": "OUTRO",     "start": 217.0, "end": 218.9, "bars":  4},
]

# =============================================================================
# SCENE FACTORY
# =============================================================================

scenes = []
folder = "The One"
scenes.append(scene("Blackout", *blackout_all(), path=folder))

steps = []
cache = {}

def cached(key, fn):
    if key not in cache:
        cache[key] = len(scenes)
        scenes.append(fn())
    return cache[key]


def atmo(name, pos_tuple, energy, frost,
         s_color=SHARPY_BLUE, b_color=BSW_TEAL, p_color=PROF_TEAL,
         par=COLD_BLUE, miss=DEEP_VIOLET,
         ni_rgb=COLD_BLUE, halo=H_OFF,
         s_dim=None, b_dim=None, p_dim=None, par_m=None,
         prism=False, lasers=False,
         strobe_s=SHARPY_OPEN, shutter_b=BSW_SHUT_OPEN,
         ni_tilt=(64, 64, 64)):
    """Build an atmosphere scene from a position tuple.

    pos_tuple can be from POS[] or SPLIT[] — same 7-element format.
    """
    sp, st, bp, bt, pp, pt, ni_pan = pos_tuple

    sd = s_dim if s_dim is not None else e2d(energy, 40, 235)
    bd = b_dim if b_dim is not None else e2d(energy, 30, 215)
    pd = p_dim if p_dim is not None else e2d(energy * 0.55, 0, 150)
    pm = par_m if par_m is not None else e2d(energy, 15, 205)

    pv = 128 if prism else 0
    pr = 200 if prism else 0

    ni_r, ni_g, ni_b = ni_rgb
    nd = e2d(energy * 0.45, 0, 170)
    t1, t2, t3 = ni_tilt

    lr = LASER_ON if lasers else LASER_OFF
    lg = LASER_ON if lasers else LASER_OFF
    lb = LASER_ON if lasers else LASER_OFF

    return scene(name,
        sharpy(pan=sp, tilt=st, strobe=strobe_s, dim=sd,
               frost=frost, colormacro=s_color, focus=128,
               prism1=pv, p1r=pr),
        bsw(pan=bp, tilt=bt, color=b_color, shutter=shutter_b,
            dim=bd, frost=min(255, frost),
            prism=pv, prot=pr, focus=128),
        profile(pan=pp, tilt=pt, color=p_color, dim=pd, focus=128),
        fourbar_solid(*par, master=pm),
        miss1(*miss, master=pm // 2),
        miss2(*miss, master=pm // 2),
        ni3k(pan=ni_pan, t1=t1, t2=t2, t3=t3,
             r=ni_r, g=ni_g, b=ni_b, w=0,
             halo=halo, rl=lr, gl=lg, bl=lb,
             dim=nd, strobe=0),
        path=folder)


def solo(name, pos_key, active, dim, color_s=SHARPY_BLUE,
         color_b=BSW_TEAL, color_p=PROF_TEAL, frost=215,
         ni_rgb=NOTHING, halo=H_OFF, par=NOTHING, par_m=0):
    """Single mover — star/solo moment. Others dark at same position."""
    p = POS[pos_key]
    sp, st, bp, bt, pp, pt, ni_pan = p
    nr, ng, nb = ni_rgb
    nd = 20 if sum(ni_rgb) > 0 else 0
    if active == "sharpy":
        s = sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=dim,
                   frost=frost, colormacro=color_s, focus=128)
        b = dark_bsw(pan=bp, tilt=bt)
        pr_ = dark_profile(pan=pp, tilt=pt)
    elif active == "bsw":
        s = dark_sharpy(pan=sp, tilt=st)
        b = bsw(pan=bp, tilt=bt, color=color_b, shutter=BSW_SHUT_OPEN,
                dim=dim, frost=frost, focus=128)
        pr_ = dark_profile(pan=pp, tilt=pt)
    else:  # both dark (just for parked state)
        s = dark_sharpy(pan=sp, tilt=st)
        b = dark_bsw(pan=bp, tilt=bt)
        pr_ = dark_profile(pan=pp, tilt=pt)
    return scene(name, s, b, pr_,
        fourbar_solid(*par, master=par_m),
        miss1(*NOTHING), miss2(*NOTHING),
        ni3k(pan=ni_pan, t1=64, t2=64, t3=64,
             r=nr, g=ng, b=nb, w=0, halo=halo, dim=nd, strobe=0),
        path=folder)


# =============================================================================
# SECTION BUILDERS
# =============================================================================

def build_intro(sec):
    """INTRO (0:00-0:23, 12 bars): Opens with immediate impact.

    Start moderately bright (sub is already present). Tight positions first,
    then widen. Sweep: C → USC → SL → SR → DSC over 12 bars.
    Sets up the dark warehouse atmosphere from bar 1.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    # Tight→wide path — each position distinct
    seq = [POS["C"], POS["USC"], SPLIT["SPREAD"], POS["DSC"],
           SPLIT["HIGH_LOW"], POS["C"]]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        prog = (t - sec["start"]) / (sec["end"] - sec["start"])
        energy = avg_energy(e_rms, t, next_t)
        has_v = vocal_present(t, next_t)
        pos_t = seq[n % len(seq)]
        frost = int(175 - 40 * prog)

        par_c = WARM_AMBER if has_v else COLD_BLUE
        miss_c = ELECTRIC_TEAL if has_v else DEEP_VIOLET

        sid = cached(f"intro_{n}", lambda: atmo(
            f"Intro {n}", pos_t, energy * 0.75, frost,
            s_color=SHARPY_BLUE, b_color=BSW_TEAL, p_color=PROF_TEAL,
            par=par_c, miss=miss_c,
            ni_rgb=COLD_BLUE, halo=H_BLU))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t; n += 1


def build_strip(sec):
    """STRIP (0:23-0:54, 16 bars): Energy drops — wide atmospheric sweeping.

    Use big sweeps to fill the space while energy is low. Ceiling hits,
    diagonal crosses, L-R spreads. Creates visual tension through movement
    even as audio energy is low.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    # Wide variety — deliberately hit all corners during this strip
    seq = [
        SPLIT["HIGH_LOW"],   # CEIL vs DSC — maximum height contrast
        SPLIT["SPREAD"],     # SL vs SR — full width
        POS["CEIL"],         # Both up — cosmic
        SPLIT["DIAG_L"],     # DSR vs SL — diagonal
        SPLIT["DEEP"],       # USC vs DSC — front-back depth
        SPLIT["CEIL_SR"],    # CEIL vs SR
        POS["DSC"],          # Forward convergence
        SPLIT["DIAG_R"],     # DSL vs SR — mirror diagonal
    ]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        energy = avg_energy(e_rms, t, next_t)
        pos_t = seq[n % len(seq)]
        # Low energy → higher frost, dimmer beams, but visually wide
        frost = 195

        sid = cached(f"strip_{n}", lambda: atmo(
            f"Strip {n}", pos_t, energy * 0.55, frost,
            s_color=SHARPY_BLUE, b_color=BSW_BLUE, p_color=PROF_BLUE,
            par=DARK_CHARCOAL, miss=NEAR_BLACK,
            ni_rgb=COLD_BLUE, halo=H_OFF,
            s_dim=e2d(energy, 30, 120),
            b_dim=e2d(energy, 20, 100),
            p_dim=0, par_m=e2d(energy, 10, 80)))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t; n += 1


def build_peak1(sec):
    """PEAK_1 (0:54-1:25, 16 bars): First full peak — all corners in rotation.

    Every 2 bars a different split position — systematically covers
    DSL, DSR, CEIL, X, USC, SL, SR, C in a deliberate circuit.
    Prism on. Colors: cold blue → electric teal → amber on vocal.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    # Deliberate circuit covering every zone — 8 unique positions for 8 steps
    circuit = [
        SPLIT["HIGH_LOW"],   # step 1: CEIL / DSC — iconic CamelPhat look
        SPLIT["SPREAD"],     # step 2: SL / SR — full width
        SPLIT["DIAG_L"],     # step 3: DSR / SL — diagonal
        POS["X"],            # step 4: cross-beam
        SPLIT["DEEP"],       # step 5: USC / DSC — depth
        SPLIT["CEIL_DJ"],    # step 6: CEIL / DJ — cosmic + intimate
        SPLIT["DIAG_R"],     # step 7: DSL / SR — mirror diagonal
        SPLIT["FAR_L"],      # step 8: DSC / SL
    ]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        energy = avg_energy(e_rms, t, next_t)
        has_v = vocal_present(t, next_t)
        pos_t = circuit[n % len(circuit)]
        frost = int(140 - 60 * energy)

        if has_v:
            s_col, par_c, miss_c = SHARPY_AMBER, WARM_AMBER, ELECTRIC_TEAL
        else:
            s_col, par_c, miss_c = SHARPY_TEAL, ELECTRIC_TEAL, DEEP_VIOLET

        sid = cached(f"peak1_{n}", lambda: atmo(
            f"Peak1 {n}", pos_t, energy, frost,
            s_color=s_col, b_color=BSW_TEAL, p_color=PROF_TEAL,
            par=par_c, miss=miss_c,
            ni_rgb=ELECTRIC_TEAL, halo=H_CYN,
            prism=True, ni_tilt=(64, 64, 64)))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t; n += 1


def build_breakdown(sec):
    """BREAKDOWN (1:25-2:15, 26 bars): Near-silence then slow rebuild.

    Phase 1 (10 bars): strip to single Sharpy sweeping all positions solo —
    uses every position in sequence so it covers the whole room even alone.
    Phase 2 (16 bars): gradual rebuild, add BSW, then pars.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    n = 0

    # Phase 1: Sharpy solo tour — deliberately visits every position
    phase1_end = t + bar * 10
    solo_tour = ["C", "USC", "CEIL", "SL", "DSC", "SR", "DJ", "CEIL", "DSC", "C"]

    while t < phase1_end - 0.3:
        next_t = min(t + bar * (4 if n < 2 else 2), phase1_end)
        prog = (t - sec["start"]) / (phase1_end - sec["start"])
        dim = int(25 + 15 * (1.0 - prog))  # dim from ~40 down to 25
        pos_k = solo_tour[n % len(solo_tour)]

        sid = cached(f"bd_solo_{n}", lambda: solo(
            f"BD Solo {n}", pos_k, "sharpy", dim=dim,
            color_s=SHARPY_BLUE, frost=225,
            ni_rgb=DEEP_VIOLET if n % 3 == 0 else NOTHING,
            halo=H_OFF))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t; n += 1

    # Phase 2: Rebuild — BSW joins, then pars
    rebuild_seq = [
        SPLIT["DEEP"],       # USC / DSC — depth first
        SPLIT["HIGH_LOW"],   # CEIL / DSC
        SPLIT["SPREAD"],     # SL / SR
        SPLIT["DIAG_L"],     # diagonal
        POS["DSC"],          # converge forward
        SPLIT["CEIL_SL"],    # ceiling + left
        SPLIT["FAR_R"],      # forward + right
        POS["C"],            # center
    ]
    rb_n = 0
    total_rb = t_end - t

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        rb_prog = (t - phase1_end) / max(1, total_rb)
        energy = avg_energy(e_rms, t, next_t)
        pos_t = rebuild_seq[rb_n % len(rebuild_seq)]
        dim_f = rb_prog * 0.8  # starts near-zero, rises

        p = pos_t
        sp, st, bp, bt, pp, pt, ni_pan = p

        # Only add BSW after first 4 bars of rebuild
        b_dim = int(80 * max(0, rb_prog - 0.25)) if rb_prog > 0.25 else 0
        p_dim = int(50 * max(0, rb_prog - 0.5)) if rb_prog > 0.5 else 0
        par_m = int(60 * dim_f)

        sid = cached(f"bd_rebuild_{rb_n}", lambda: scene(
            f"BD Rebuild {rb_n}",
            sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN,
                   dim=int(40 + 100 * dim_f), frost=int(220 - 60 * rb_prog),
                   colormacro=SHARPY_BLUE, focus=128),
            bsw(pan=bp, tilt=bt, color=BSW_TEAL,
                shutter=BSW_SHUT_OPEN, dim=b_dim,
                frost=220, focus=128) if b_dim > 0 else dark_bsw(pan=bp, tilt=bt),
            profile(pan=pp, tilt=pt, color=PROF_TEAL,
                    dim=p_dim, focus=128) if p_dim > 0 else dark_profile(pan=pp, tilt=pt),
            fourbar_solid(*COLD_BLUE, master=par_m),
            miss1(*DEEP_VIOLET, master=par_m // 3),
            miss2(*DEEP_VIOLET, master=par_m // 3),
            ni3k(pan=ni_pan, t1=64, t2=64, t3=64,
                 r=COLD_BLUE[0], g=COLD_BLUE[1], b=COLD_BLUE[2],
                 w=0, halo=H_BLU if rb_prog > 0.5 else H_OFF,
                 dim=int(50 * dim_f), strobe=0),
            path=folder))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t; rb_n += 1


def build_build(sec):
    """BUILD (2:15-2:35, 10 bars): Tension rising toward Drop 2.

    Converge from spread positions toward cross-beam / forward.
    Prism returns. Frost sharpening. Teal → violet → amber transition.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    # Converging path: spread → diagonal → cross → forward
    seq = [
        SPLIT["SPREAD"],
        SPLIT["DIAG_L"],
        SPLIT["HIGH_LOW"],
        POS["X"],
        SPLIT["DEEP"],
    ]
    n = 0
    total = t_end - t

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos_t = seq[n % len(seq)]
        frost = int(190 - 80 * prog)
        use_prism = prog > 0.4

        # Transition cold blue → electric teal → starts warming to amber at end
        if prog < 0.5:
            s_col, par_c, miss_c = SHARPY_TEAL, ELECTRIC_TEAL, COLD_BLUE
        else:
            s_col, par_c, miss_c = SHARPY_AMBER, WARM_AMBER, ELECTRIC_TEAL

        sid = cached(f"build_{n}", lambda: atmo(
            f"Build {n}", pos_t, energy * (0.5 + 0.5 * prog), frost,
            s_color=s_col, b_color=BSW_TEAL, p_color=PROF_TEAL,
            par=par_c, miss=miss_c,
            ni_rgb=ELECTRIC_TEAL, halo=H_CYN if prog > 0.3 else H_OFF,
            prism=use_prism))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t; n += 1


def build_peak2(sec):
    """PEAK_2 (2:35-3:37, 32 bars): Maximum coverage. The sustained climax.

    Uses the widest possible position variety — 16 unique split positions
    cycle over 32 bars so every step covers a different part of the room.
    Lasers at bars 8-24. Cold white at absolute peak.
    """
    t, t_end = sec["start"], sec["end"]
    total = t_end - t
    bar = BAR_MS / 1000

    # 16-step circuit — every position in the room, no repeats for 16 bars
    mega_circuit = [
        SPLIT["HIGH_LOW"],   #  1: CEIL / DSC
        SPLIT["SPREAD"],     #  2: SL / SR
        SPLIT["DIAG_L"],     #  3: DSR / SL
        SPLIT["DEEP"],       #  4: USC / DSC
        POS["X"],            #  5: cross-beam
        SPLIT["CEIL_DJ"],    #  6: CEIL / DJ
        SPLIT["FAR_L"],      #  7: DSC / SL
        SPLIT["DIAG_R"],     #  8: DSL / SR
        SPLIT["CEIL_SR"],    #  9: CEIL / SR
        SPLIT["USC_DSL"],    # 10: USC / DSL
        SPLIT["FULL_L"],     # 11: DSR / USC
        SPLIT["FAR_R"],      # 12: DSC / SR
        SPLIT["CEIL_SL"],    # 13: CEIL / SL
        SPLIT["X_CEIL"],     # 14: SR / DSL / CEIL
        SPLIT["FULL_R"],     # 15: DSL / USR
        SPLIT["HIGH_LOW"],   # 16: back to iconic — sets up repeat
    ]

    laser_start = sec["start"] + bar * 8
    laser_end   = sec["start"] + bar * 24
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        has_v = vocal_present(t, next_t)
        pos_t = mega_circuit[n % len(mega_circuit)]
        frost = int(120 - 70 * energy)

        use_lasers = laser_start <= t < laser_end and energy > 0.72
        at_peak = 0.25 <= prog <= 0.75 and energy > 0.85

        if at_peak:
            s_col, par_c, miss_c = SHARPY_WHITE, COLD_WHITE, ELECTRIC_TEAL
        elif has_v:
            s_col, par_c, miss_c = SHARPY_AMBER, WARM_AMBER, ELECTRIC_TEAL
        else:
            s_col, par_c, miss_c = SHARPY_TEAL, ELECTRIC_TEAL, DEEP_VIOLET

        ni_c = WARM_AMBER if has_v else ELECTRIC_TEAL
        ni_t = (150, 170, 160) if energy > 0.8 else (64, 64, 64)

        sid = cached(f"peak2_{n}", lambda: atmo(
            f"Peak2 {n}", pos_t, energy, frost,
            s_color=s_col, b_color=BSW_TEAL, p_color=PROF_TEAL,
            par=par_c, miss=miss_c,
            ni_rgb=ni_c, halo=H_CYN,
            prism=True, lasers=use_lasers,
            ni_tilt=ni_t))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t; n += 1


def build_outro(sec):
    """OUTRO (3:37-3:44, 4 bars): Quick fade to blackout."""
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    energy = avg_energy(e_rms, t, t_end)

    sid = cached("outro", lambda: atmo(
        "Outro", POS["C"], energy * 0.25, 230,
        s_color=SHARPY_BLUE, b_color=BSW_BLUE, p_color=PROF_BLUE,
        par=NEAR_BLACK, miss=NOTHING,
        ni_rgb=NOTHING, halo=H_OFF,
        s_dim=30, b_dim=20, p_dim=0, par_m=15))

    dur = t_end - t
    steps.append((sid, phrase_step_timing(t, t_end, max(1, dur / bar))))
    steps.append((0, phrase_step_timing(max(0.0, t_end - bar * 2), t_end, 2)))  # blackout


# =============================================================================
# MAIN
# =============================================================================

BUILDERS = {
    "INTRO":     build_intro,
    "STRIP":     build_strip,
    "PEAK_1":    build_peak1,
    "BREAKDOWN": build_breakdown,
    "BUILD":     build_build,
    "PEAK_2":    build_peak2,
    "OUTRO":     build_outro,
}

print(f"Generating show: {SONG_STEM}")
print(f"  BPM: {BPM}, Beats: {len(beats)}, Duration: {beats[-1]:.1f}s")
print()

for sec in SECTIONS:
    print(f"  Building {sec['name']:10s} ({sec['bars']:2d} bars, "
          f"{sec['start']:.1f}s-{sec['end']:.1f}s)")
    BUILDERS[sec["name"]](sec)

print(f"\nTotal scenes: {len(scenes)}")
print(f"Total chaser steps: {len(steps)}")
print(f"Phrase bars: {PHRASE_BAR_COUNTS}")
top_techniques = sorted(TECHNIQUE_COUNTS.items(), key=lambda kv: kv[1], reverse=True)[:8]
print(f"Top technique usage: {top_techniques}")

total_ms = sum(fi + ho for _, (fi, ho) in steps)
print(f"Total duration: {total_ms/1000:.1f}s (target: ~219s)")

main_chaser = make_chaser("The One", [s for s, _ in steps], [t for _, t in steps],
                           run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "▶ THE ONE",  "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10,  "w": 470, "h": 100, "color": "#1E0A32", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,  "color": "#FF0000", "action": "Toggle"},
]

output_path = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")
write_workspace(output_path, scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
