#!/usr/bin/env python3
"""
Show Generator: Claptone & Sea Girls - Put Your Love On Me [Korolova Extended Mix]
===================================================================================
BPM: 125 | Duration: 5:19 | Label: When Stars Align

Aesthetic: Claptone's golden masquerade — amber/gold hero color on near-black.
Deep purple/violet as masquerade luxury accent. Warm white bloom at climax.
"Start near-monochrome, let color bloom on peak." (ref: Claptone 'Immortal Live' arc)
Korolova influence: cinematic patience, deliberate emotional build.

User direction: "lots of beams with slightly faster sweeps"
- All movers active simultaneously throughout (no solo scenes)
- 1-bar crossfades during drops/climax; 2-bar during verses/builds
- SPLIT positions: Sharpy and BSW aim at different parts of the room
  simultaneously for wide spatial coverage.

Song Structure:
  0:00 - 0:45  INTRO      (24 bars, rms=0.59-0.75) Dark reveal, amber whisper
  0:45 - 1:16  VERSE_1    (16 bars, rms=0.36, sub=0.20) Stripped, vocal-forward
  1:16 - 1:46  CHORUS_1   (16 bars, rms=0.45, sub=0.35) Building, amber brightens
  1:46 - 2:17  DROP_1     (16 bars, rms=0.85, sub=0.63) Full amber, SPLIT coverage
  2:17 - 2:32  POST_DROP  ( 8 bars, rms=0.87, sub=0.64) Sustained, purple bleeding in
  2:32 - 3:02  VERSE_2    (16 bars, rms=0.65, sub=0.51) Gold + purple balance
  3:02 - 3:33  CHORUS_2   (16 bars, rms=0.43, sub=0.34) Rich gold + purple build
  3:33 - 4:03  DROP_2     (16 bars, rms=0.85, sub=0.66) Gold/purple interleave
  4:03 - 4:34  CLIMAX     (16 bars, rms=1.00, sub=0.63) Warm white bloom, lasers
  4:34 - 5:20  OUTRO      (24 bars, rms=0.74→0.67) Warm white → amber → dark
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

SONG_STEM = "Claptone & Sea Girls - Put Your Love On Me (feat. Henry Camamile) [Korolova Extended Mix]"
BRIEF = require_research_brief(SONG_STEM, project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)
print(f"Research brief OK: {BRIEF['_meta']['brief_json']}")
print(f"Creative thesis: {BRIEF['thesis']}")
DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", f"{SONG_STEM}.json")

with open(DATA_PATH) as f:
    data = json.load(f)

BPM    = data["bpm"]        # 125
beats  = data["beats"]
e_rms  = data["energy"]["rms"]
e_sub  = data["energy"]["sub_bass"]
vocal_e = data["stems"]["vocals"]["energy"]

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

def vocal_present(t0, t1):
    return avg_energy(vocal_e, t0, t1) > 0.015

def e2d(e, lo=30, hi=255):
    return int(lo + (hi - lo) * min(1.0, max(0.0, e)))

# =============================================================================
# COLOR PALETTE — Claptone masquerade
# =============================================================================

# 4BAR / Missyee RGB tuples
DARK_EMBER  = (15,   5,   0)   # Near-black, amber tint
DIM_AMBER   = (50,  20,   0)   # Dim amber ember
MID_AMBER   = (120,  50,   0)  # Medium amber wash
FULL_AMBER  = (220,  90,   0)  # Full amber glow
SOFT_GOLD   = (240, 140,  10)  # Bright gold (chorus/drop peak)
WARM_WHITE  = (255, 220, 160)  # Warm white bloom (climax only)
DEEP_PURPLE = (40,    0,  80)  # Masquerade shadow
MID_PURPLE  = (90,    0, 150)  # Rich purple accent
GOLD_PURPLE = (120,  20,  80)  # Blend: gold + purple
NEAR_BLACK  = (2,     1,   0)  # Absolute darkness

# =============================================================================
# POSITION TABLES — loaded from venue focus-positions.md
# =============================================================================

POS = load_focus_position_tuples(project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)

# Split positions: Sharpy and BSW aim at DIFFERENT spots simultaneously.
# Profile sits at a neutral position (DSC or near-DSC) unless indicated.
SPLIT = {
    "HIGH_LOW": (POS["CEIL"][0], POS["CEIL"][1], POS["DSC"][2],  POS["DSC"][3],  POS["C"][4],   POS["C"][5],   128),
    "SPREAD":   (POS["SL"][0],   POS["SL"][1],   POS["SR"][2],   POS["SR"][3],   POS["C"][4],   POS["C"][5],   128),
    "DEEP":     (POS["USC"][0],  POS["USC"][1],  POS["DSC"][2],  POS["DSC"][3],  POS["C"][4],   POS["C"][5],   128),
    "DIAG_L":   (POS["DSR"][0],  POS["DSR"][1],  POS["SL"][2],   POS["SL"][3],   POS["DSC"][4], POS["DSC"][5],  80),
    "DIAG_R":   (POS["DSL"][0],  POS["DSL"][1],  POS["SR"][2],   POS["SR"][3],   POS["DSC"][4], POS["DSC"][5], 176),
    "FAR_L":    (POS["DSC"][0],  POS["DSC"][1],  POS["SL"][2],   POS["SL"][3],   POS["DSL"][4], POS["DSL"][5],  80),
    "FAR_R":    (POS["DSC"][0],  POS["DSC"][1],  POS["SR"][2],   POS["SR"][3],   POS["DSR"][4], POS["DSR"][5], 176),
    "CEIL_DJ":  (POS["CEIL"][0], POS["CEIL"][1], POS["DJ"][2],   POS["DJ"][3],   POS["DSC"][4], POS["DSC"][5], 128),
    "CEIL_SL":  (POS["CEIL"][0], POS["CEIL"][1], POS["SL"][2],   POS["SL"][3],   POS["C"][4],   POS["C"][5],    80),
    "CEIL_SR":  (POS["CEIL"][0], POS["CEIL"][1], POS["SR"][2],   POS["SR"][3],   POS["C"][4],   POS["C"][5],   176),
    "USC_DSL":  (POS["USC"][0],  POS["USC"][1],  POS["DSL"][2],  POS["DSL"][3],  POS["C"][4],   POS["C"][5],    80),
    "USC_DSR":  (POS["DSL"][0],  POS["DSL"][1],  POS["USC"][2],  POS["USC"][3],  POS["C"][4],   POS["C"][5],   176),
}

# =============================================================================
# SECTIONS
# =============================================================================

SECTIONS = [
    {"name": "INTRO",     "start":   0.0, "end":  45.0, "bars": 24},
    {"name": "VERSE_1",   "start":  45.0, "end":  76.0, "bars": 16},
    {"name": "CHORUS_1",  "start":  76.0, "end": 106.0, "bars": 16},
    {"name": "DROP_1",    "start": 106.0, "end": 137.0, "bars": 16},
    {"name": "POST_DROP", "start": 137.0, "end": 152.0, "bars":  8},
    {"name": "VERSE_2",   "start": 152.0, "end": 182.0, "bars": 16},
    {"name": "CHORUS_2",  "start": 182.0, "end": 213.0, "bars": 16},
    {"name": "DROP_2",    "start": 213.0, "end": 243.0, "bars": 16},
    {"name": "CLIMAX",    "start": 243.0, "end": 274.0, "bars": 16},
    {"name": "OUTRO",     "start": 274.0, "end": 320.0, "bars": 24},
]

# =============================================================================
# SCENE FACTORY
# =============================================================================

scenes = []
folder = "Put Your Love On Me"
scenes.append(scene("Blackout", *blackout_all(), path=folder))

steps = []
cache = {}

def cached(key, fn):
    if key not in cache:
        cache[key] = len(scenes)
        scenes.append(fn())
    return cache[key]


def atmo(name, pos_tuple, energy, frost,
         s_color=SHARPY_AMBER, b_color=BSW_ORANGE, p_color=PROF_ORANGE,
         par=MID_AMBER, miss=DIM_AMBER,
         ni_rgb=MID_AMBER, halo=H_OFF,
         s_dim=None, b_dim=None, p_dim=None, par_m=None,
         prism=False, lasers=False,
         ni_tilt=(64, 64, 64)):
    """Build an atmosphere scene from a position tuple.

    pos_tuple can be from POS[] or SPLIT[] — same 7-element format.
    All movers always active (no solo scenes per user direction).
    """
    sp, st, bp, bt, pp, pt, ni_pan = pos_tuple

    sd = s_dim if s_dim is not None else e2d(energy, 50, 240)
    bd = b_dim if b_dim is not None else e2d(energy, 40, 220)
    pd = p_dim if p_dim is not None else e2d(energy * 0.5, 0, 140)
    pm = par_m if par_m is not None else e2d(energy, 20, 200)

    pv = 128 if prism else 0
    pr = 200 if prism else 0

    ni_r, ni_g, ni_b = ni_rgb
    nd = e2d(energy * 0.5, 0, 180)
    t1, t2, t3 = ni_tilt

    lr = LASER_ON if lasers else LASER_OFF

    return scene(name,
        sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=sd,
               frost=frost, colormacro=s_color, focus=128,
               prism1=pv, p1r=pr),
        bsw(pan=bp, tilt=bt, color=b_color, shutter=BSW_SHUT_OPEN,
            dim=bd, frost=min(255, frost + 20),
            prism=pv, prot=pr, focus=128),
        profile(pan=pp, tilt=pt, color=p_color, dim=pd, focus=128),
        fourbar_solid(*par, master=pm),
        miss1(*miss, master=pm // 2),
        miss2(*miss, master=pm // 2),
        ni3k(pan=ni_pan, t1=t1, t2=t2, t3=t3,
             r=ni_r, g=ni_g, b=ni_b, w=0,
             halo=halo, rl=lr, gl=lr, bl=lr,
             dim=nd, strobe=0),
        path=folder)

# =============================================================================
# SECTION BUILDERS
# =============================================================================

def build_intro(sec):
    """INTRO (0:00-0:45, 24 bars): Dark reveal — amber whisper building.

    Masquerade opening: room is near-black, a golden glow slowly emerges.
    All movers visit wide positions but start very frosted (soft beams).
    Amber builds from 20% to 100% over the 24 bars. 2-bar crossfades.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000

    seq = [
        POS["C"],             # Dark center anchor
        SPLIT["DEEP"],        # USC vs DSC — depth contrast
        SPLIT["SPREAD"],      # SL vs SR — reveal the room width
        POS["CEIL"],          # Both ceiling — masquerade grandeur
        SPLIT["HIGH_LOW"],    # CEIL vs DSC — maximum drama
        SPLIT["DIAG_L"],      # Cross diagonal
        SPLIT["DIAG_R"],      # Mirror cross
        SPLIT["FAR_L"],       # DSC vs SL spread
        SPLIT["FAR_R"],       # DSC vs SR spread
        SPLIT["DEEP"],        # Back to depth
        POS["DSC"],           # Converge forward
        POS["C"],             # Home — ready for drop
    ]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        prog = (t - sec["start"]) / (sec["end"] - sec["start"])
        energy = avg_energy(e_rms, t, next_t)
        pos_t = seq[n % len(seq)]

        # Amber builds from dark ember to full amber
        amb_scale = 0.2 + prog * 0.8
        par_c = tuple(int(v * amb_scale) for v in FULL_AMBER)
        miss_c = tuple(int(v * amb_scale * 0.6) for v in MID_AMBER)
        ni_c   = tuple(int(v * amb_scale * 0.35) for v in MID_AMBER)
        eff_e  = energy * 0.5 + amb_scale * 0.5  # Drive dimmers via scale, not raw energy

        # Frost: very soft at start, sharpens by end
        frost = int(190 - 110 * prog)

        sid = cached(f"intro_{n}", lambda pos_t=pos_t, eff_e=eff_e, frost=frost,
                     par_c=par_c, miss_c=miss_c, ni_c=ni_c: atmo(
            "Intro", pos_t, eff_e, frost,
            s_color=SHARPY_AMBER, b_color=BSW_ORANGE, p_color=PROF_ORANGE,
            par=par_c, miss=miss_c, ni_rgb=ni_c, halo=H_OFF))

        steps.append((sid, smooth(BPM, max(1, round((next_t - t) / bar)))))
        t = next_t; n += 1


def build_verse(sec, ver=1):
    """VERSE (16 bars): Stripped, vocal-forward. 2-bar crossfades.

    Verse 1: pure amber. Vocal moments slightly brighter pars.
    Verse 2: purple starts emerging (pars + missyees), amber stays on movers.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    is_v2 = (ver == 2)
    tag = f"v{ver}"

    seq = [
        POS["DSC"],       SPLIT["FAR_L"],
        POS["SL"],        SPLIT["DEEP"],
        POS["SR"],        SPLIT["FAR_R"],
        POS["USC"],       POS["C"],
    ]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        energy = avg_energy(e_rms, t, next_t)
        has_v = vocal_present(t, next_t)
        pos_t = seq[n % len(seq)]

        if is_v2:
            par_c  = GOLD_PURPLE if has_v else MID_AMBER
            miss_c = DEEP_PURPLE
            ni_c   = DEEP_PURPLE
        else:
            par_c  = FULL_AMBER if has_v else MID_AMBER
            miss_c = DIM_AMBER
            ni_c   = DIM_AMBER

        sid = cached(f"{tag}_{n}", lambda pos_t=pos_t, energy=energy,
                     par_c=par_c, miss_c=miss_c, ni_c=ni_c: atmo(
            f"V{ver}", pos_t, energy, 80,
            s_color=SHARPY_AMBER, b_color=BSW_ORANGE, p_color=PROF_ORANGE,
            par=par_c, miss=miss_c, ni_rgb=ni_c, halo=H_OFF))

        steps.append((sid, smooth(BPM, 2)))
        t = next_t; n += 1


def build_chorus(sec, ch=1):
    """CHORUS (16 bars): Building energy, color gaining richness. 2-bar crossfades.

    Chorus 1: amber brightens to soft gold, more active SPLIT positions.
    Chorus 2: prism on, gold + purple interleave in pars, anticipatory.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    is_c2 = (ch == 2)
    tag = f"ch{ch}"

    seq = [
        SPLIT["HIGH_LOW"],   SPLIT["SPREAD"],
        POS["DSC"],           SPLIT["DIAG_L"],
        SPLIT["DIAG_R"],      POS["CEIL"],
        SPLIT["DEEP"],        SPLIT["FAR_L"],
    ]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        energy = avg_energy(e_rms, t, next_t)
        has_v = vocal_present(t, next_t)
        pos_t = seq[n % len(seq)]

        if is_c2:
            par_c  = GOLD_PURPLE if has_v else MID_PURPLE
            miss_c = MID_PURPLE
            ni_c   = MID_PURPLE
        else:
            par_c  = SOFT_GOLD if has_v else FULL_AMBER
            miss_c = DIM_AMBER
            ni_c   = DIM_AMBER

        sid = cached(f"{tag}_{n}", lambda pos_t=pos_t, energy=energy,
                     par_c=par_c, miss_c=miss_c, ni_c=ni_c, is_c2=is_c2: atmo(
            f"Ch{ch}", pos_t, energy, 60,
            s_color=SHARPY_AMBER, b_color=BSW_ORANGE, p_color=PROF_ORANGE,
            par=par_c, miss=miss_c, ni_rgb=ni_c, halo=H_OFF,
            prism=is_c2))

        steps.append((sid, smooth(BPM, 2)))
        t = next_t; n += 1


def build_drop(sec, drop=1):
    """DROP_1 (16 bars): Full amber/gold SPLIT coverage. 1-bar crossfades.

    The masquerade in full swing. Pure amber/gold — no purple yet (that comes
    later). All SPLIT positions cycle rapidly. Prism on both movers.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    tag = f"d{drop}"

    seq = [
        SPLIT["HIGH_LOW"],   SPLIT["SPREAD"],
        POS["DSC"],           SPLIT["DIAG_L"],
        SPLIT["DIAG_R"],      SPLIT["DEEP"],
        SPLIT["FAR_L"],       SPLIT["FAR_R"],
        SPLIT["CEIL_SL"],     SPLIT["CEIL_SR"],
        POS["CEIL"],          SPLIT["CEIL_DJ"],
        SPLIT["USC_DSL"],     SPLIT["USC_DSR"],
        POS["SL"],            POS["SR"],
    ]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar, t_end)
        energy = avg_energy(e_rms, t, next_t)
        sub    = avg_energy(e_sub, t, next_t)
        pos_t  = seq[n % len(seq)]

        frost = max(0, int(40 - sub * 25))  # Sub present = sharpest beam

        sid = cached(f"{tag}_{n}", lambda pos_t=pos_t, energy=energy, frost=frost: atmo(
            f"Drop{drop}", pos_t, energy, frost,
            s_color=SHARPY_AMBER, b_color=BSW_ORANGE, p_color=PROF_ORANGE,
            par=SOFT_GOLD, miss=FULL_AMBER,
            ni_rgb=FULL_AMBER, halo=H_OFF,
            prism=True))

        steps.append((sid, smooth(BPM, 1)))
        t = next_t; n += 1


def build_post_drop(sec):
    """POST_DROP (2:17-2:32, 8 bars): Sustained energy, purple starts bleeding in.

    Coming out of Drop 1 while staying high-energy. Purple slowly seeps into
    the pars as the masquerade deepens toward verse 2.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000

    seq = [
        SPLIT["SPREAD"],      POS["DSC"],
        SPLIT["HIGH_LOW"],    SPLIT["DIAG_L"],
        POS["CEIL"],          SPLIT["DIAG_R"],
        SPLIT["FAR_L"],       SPLIT["FAR_R"],
    ]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar, t_end)
        energy = avg_energy(e_rms, t, next_t)
        prog   = (t - sec["start"]) / (sec["end"] - sec["start"])
        pos_t  = seq[n % len(seq)]

        # Purple bleeds in over 8 bars
        par_c  = SOFT_GOLD if prog < 0.5 else GOLD_PURPLE
        miss_c = FULL_AMBER if prog < 0.5 else MID_PURPLE

        sid = cached(f"pd_{n}", lambda pos_t=pos_t, energy=energy,
                     par_c=par_c, miss_c=miss_c: atmo(
            "PostDrop", pos_t, energy, 30,
            s_color=SHARPY_AMBER, b_color=BSW_ORANGE, p_color=PROF_ORANGE,
            par=par_c, miss=miss_c,
            ni_rgb=FULL_AMBER, halo=H_OFF, prism=True))

        steps.append((sid, smooth(BPM, 1)))
        t = next_t; n += 1


def build_drop2(sec):
    """DROP_2 (3:33-4:03, 16 bars): Gold/purple interleave. Maximum richness.

    The masquerade at its height — gold and purple beams alternate positions.
    Odd steps: amber/gold palette. Even steps: purple palette.
    Maximum SPLIT coverage. Prism on. Prelude to warm white climax.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000

    seq = [
        SPLIT["HIGH_LOW"],   SPLIT["SPREAD"],
        POS["DSC"],           SPLIT["DIAG_L"],
        SPLIT["DIAG_R"],      SPLIT["DEEP"],
        SPLIT["FAR_L"],       SPLIT["FAR_R"],
        SPLIT["CEIL_SL"],     SPLIT["CEIL_SR"],
        POS["CEIL"],          SPLIT["CEIL_DJ"],
        SPLIT["USC_DSL"],     SPLIT["USC_DSR"],
        POS["SL"],            POS["SR"],
    ]
    n = 0

    while t < t_end - 0.3:
        next_t  = min(t + bar, t_end)
        energy  = avg_energy(e_rms, t, next_t)
        pos_t   = seq[n % len(seq)]
        is_gold = (n % 2 == 0)

        par_c  = SOFT_GOLD  if is_gold else MID_PURPLE
        miss_c = FULL_AMBER if is_gold else DEEP_PURPLE
        ni_c   = FULL_AMBER if is_gold else MID_PURPLE
        s_col  = SHARPY_AMBER  if is_gold else SHARPY_PURPLE
        b_col  = BSW_ORANGE    if is_gold else BSW_MAG

        n += 1

        sid = cached(f"d2_{n}", lambda pos_t=pos_t, energy=energy,
                     par_c=par_c, miss_c=miss_c, ni_c=ni_c,
                     s_col=s_col, b_col=b_col: atmo(
            "Drop2", pos_t, energy, 20,
            s_color=s_col, b_color=b_col, p_color=PROF_ORANGE,
            par=par_c, miss=miss_c, ni_rgb=ni_c,
            halo=H_OFF, prism=True))

        steps.append((sid, smooth(BPM, 1)))
        t = next_t


def build_climax(sec):
    """CLIMAX (4:03-4:34, 16 bars): Warm white bloom — the earned payoff.

    "Let color bloom on peak." Warm white floods everything. NI3K lasers on.
    Prism spinning. All movers at full output. Maximum spatial coverage.
    1-bar crossfades cycling through all SPLIT positions.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000

    seq = [
        SPLIT["HIGH_LOW"],   SPLIT["SPREAD"],
        POS["DSC"],           SPLIT["DIAG_L"],
        POS["CEIL"],          SPLIT["DIAG_R"],
        SPLIT["DEEP"],        SPLIT["FAR_L"],
        SPLIT["FAR_R"],       SPLIT["CEIL_SL"],
        SPLIT["CEIL_SR"],     SPLIT["CEIL_DJ"],
        SPLIT["USC_DSL"],     SPLIT["USC_DSR"],
        POS["SL"],            POS["SR"],
    ]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar, t_end)
        energy = avg_energy(e_rms, t, next_t)
        pos_t  = seq[n % len(seq)]

        sid = cached(f"cl_{n}", lambda pos_t=pos_t, energy=energy: atmo(
            "Climax", pos_t, energy, 0,
            s_color=SHARPY_WHITE, b_color=BSW_WHITE, p_color=PROF_WHITE,
            par=WARM_WHITE, miss=WARM_WHITE,
            ni_rgb=WARM_WHITE, halo=H_YEL,
            s_dim=255, b_dim=255, p_dim=200,
            prism=True, lasers=True))

        steps.append((sid, smooth(BPM, 1)))
        t = next_t; n += 1


def build_outro(sec):
    """OUTRO (4:34-5:20, 24 bars): Warm white → gold → amber → near-black.

    The masquerade ends. Color drains away. Frost rises (beams soften).
    NI3K lasers off. 2-bar crossfades. Movers return to center positions.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000

    seq = [
        SPLIT["HIGH_LOW"],  SPLIT["SPREAD"],
        POS["DSC"],          SPLIT["DEEP"],
        POS["C"],            SPLIT["FAR_L"],
        POS["DSC"],          POS["USC"],
        POS["C"],            POS["DSC"],
        POS["C"],            POS["C"],
    ]
    n = 0

    while t < t_end - 0.3:
        next_t    = min(t + bar * 2, t_end)
        prog      = (t - sec["start"]) / (sec["end"] - sec["start"])
        energy    = avg_energy(e_rms, t, next_t)
        pos_t     = seq[n % len(seq)]
        dim_scale = max(0.05, 1.0 - prog * 0.95)

        # Palette fade: warm white → soft gold → full amber → dark ember
        if prog < 0.25:
            par_c   = WARM_WHITE
            s_col   = SHARPY_WHITE
            b_col   = BSW_WHITE
            p_col   = PROF_WHITE
        elif prog < 0.5:
            par_c   = SOFT_GOLD
            s_col   = SHARPY_AMBER
            b_col   = BSW_ORANGE
            p_col   = PROF_ORANGE
        elif prog < 0.75:
            par_c   = FULL_AMBER
            s_col   = SHARPY_AMBER
            b_col   = BSW_ORANGE
            p_col   = PROF_ORANGE
        else:
            par_c   = DARK_EMBER
            s_col   = SHARPY_AMBER
            b_col   = BSW_ORANGE
            p_col   = PROF_ORANGE

        ni_c  = tuple(int(v * dim_scale) for v in par_c)
        frost = int(prog * 160)  # Frostier toward end

        sid = cached(f"out_{n}", lambda pos_t=pos_t, energy=energy, dim_scale=dim_scale,
                     par_c=par_c, ni_c=ni_c, s_col=s_col, b_col=b_col, p_col=p_col,
                     frost=frost: atmo(
            "Outro", pos_t, energy * dim_scale, frost,
            s_color=s_col, b_color=b_col, p_color=p_col,
            par=par_c, miss=tuple(v // 2 for v in par_c),
            ni_rgb=ni_c, halo=H_OFF, lasers=False))

        steps.append((sid, smooth(BPM, max(1, round((next_t - t) / bar)))))
        t = next_t; n += 1


# =============================================================================
# BUILD SHOW
# =============================================================================

for sec in SECTIONS:
    name = sec["name"]
    if   name == "INTRO":     build_intro(sec)
    elif name == "VERSE_1":   build_verse(sec, ver=1)
    elif name == "CHORUS_1":  build_chorus(sec, ch=1)
    elif name == "DROP_1":    build_drop(sec, drop=1)
    elif name == "POST_DROP": build_post_drop(sec)
    elif name == "VERSE_2":   build_verse(sec, ver=2)
    elif name == "CHORUS_2":  build_chorus(sec, ch=2)
    elif name == "DROP_2":    build_drop2(sec)
    elif name == "CLIMAX":    build_climax(sec)
    elif name == "OUTRO":     build_outro(sec)

# =============================================================================
# ASSEMBLE + WRITE
# =============================================================================

scene_ids = [s for s, _ in steps]
timing    = [t for _, t in steps]

total_ms = sum(fi + ho for fi, ho in timing)
print(f"Show: {len(scenes)} scenes, {len(steps)} steps")
print(f"Duration: {total_ms/1000:.1f}s  ({total_ms/1000/60:.2f} min)")

chaser = make_chaser(
    "Put Your Love On Me - Full Show",
    scene_ids,
    timing,
    run_order="SingleShot",
    path=folder,
)

OUT = os.path.join(
    VENUE_DIR, "shows",
    "Claptone & Sea Girls - Put Your Love On Me (feat. Henry Camamile) [Korolova Extended Mix].qxw",
)
write_workspace(OUT, scenes, [chaser], bpm=BPM)
print(f"Written: {OUT}")
