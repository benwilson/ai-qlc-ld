#!/usr/bin/env python3
"""
Show Generator: Coste - Sunrise (Extended Mix)
===============================================
BPM: 122 | Duration: ~4:44 (144 bars) | Genre: Melodic House / Progressive House

Aesthetic: The show IS a sunrise. Deep pre-dawn indigo → amber horizon bleeding in →
warm orange arrival → gold/white peak → cloud-shadow breakdown → second bigger sunrise.

Mover innovations (distinct from all other shows in this rig):
  1. Profile Arc: Starts at CEIL (tilt=30), descends to DSC (tilt=145) — literal rising sun.
     Returns to ceiling during outro. No other show does this.
  2. Counter-Sweep: Sharpy and BSW always sweep OPPOSITE directions (Sharpy SR ↔ BSW SL).
     Creates "horizon widening" / spreading effect. Other shows use converge/follow.
  3. Spinning color wheels during build (Sharpy CW + BSW CCW) — atmospheric scatter.
  4. No lasers until Drop 2 — lasers = full daylight breaking through.
  5. BSW heavy frost (ch12 ≥ 130) in intro/breaks — soft morning haze quality.

Song Structure:
  0:00 - 0:31  INTRO    (16 bars, rms=0.72, sub=0.07)  Pre-dawn — violet darkness
  0:31 - 0:47  VERSE    (8 bars,  rms=0.74, sub=0.18)  Amber bleeds in one side
  0:47 - 1:18  BUILD_1  (16 bars, rms=0.73, sub=0.42)  Color wheels spin
  1:18 - 1:34  DROP_1   (8 bars,  rms=0.86, sub=0.70)  Sun breaks horizon
  1:34 - 1:50  PEAK_1   (8 bars,  rms=1.00, sub=0.53)  Full sunrise, gold/white
  1:50 - 2:21  SUST     (16 bars, rms=0.80, sub=0.58)  Sustained warmth
  2:21 - 2:53  BREAK    (16 bars, rms=0.19, sub=0.08)  Cloud shadow — near dark
  2:53 - 3:09  RETURN   (8 bars,  rms=0.38, sub=0.12)  Sun re-emerging
  3:09 - 3:58  DROP_2   (25 bars, rms=0.87, sub=0.55)  Bigger sunrise + prisms + lasers
  3:58 - 4:44  OUTRO    (23 bars, rms=0.77, sub=0.31)  Amber glow fading to dark
"""

import json
import os
import sys

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR    = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
from showlib import *

# =============================================================================
# LOAD ANALYSIS DATA
# =============================================================================

SONG_STEM = "Coste - Sunrise (Extended Mix)"
BRIEF = require_research_brief(SONG_STEM, project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)
print(f"Research brief OK: {BRIEF['_meta']['brief_json']}")
print(f"Creative thesis: {BRIEF['thesis']}")
DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", f"{SONG_STEM}.json")

with open(DATA_PATH) as f:
    data = json.load(f)

BPM     = data["bpm"]   # 122
beats   = data["beats"]
BAR_MS  = bpm_to_ms(BPM, 4)   # ~1967ms
BEAT_MS = bpm_to_ms(BPM, 1)   # ~492ms

# =============================================================================
# SUNRISE COLOR PALETTE
# =============================================================================

# Pre-dawn (indigo/violet)
PRE_DAWN     = (20, 10, 80)    # Deep indigo pars
NEAR_BLACK   = (8,  4,  30)    # Near-black indigo
VIOLET_MIST  = (60, 20, 120)   # Violet with depth
CLOUD_VIOLET = (40, 15, 90)    # Shadow violet for break

# Horizon glow
HORIZON_AMBER  = (180, 80,  20)   # First warm glow
HORIZON_PURPLE = (80,  20, 100)   # Purple-pink horizon

# Full sunrise
SUNRISE_ORANGE = (255, 120,  0)   # Saturated orange
WARM_ORANGE    = (220, 100, 20)   # Warm orange
WARM_GOLD      = (255, 180, 40)   # Golden hour
SOFT_GOLD      = (255, 200, 60)   # Brighter gold
GOLDEN_WHITE   = (255, 220, 140)  # Warm white peak

# Outro amber
AMBER_GLOW   = (200, 120, 30)    # Lingering amber
AMBER_FADE   = (140,  70, 20)    # Fading amber

# Mover color wheel constants for the arc
SH_VIOLET   = SHARPY_PURPLE    # 50
SH_AMBER    = SHARPY_AMBER     # 80
SH_ORANGE   = SHARPY_ORANGE    # 90
SH_GOLD     = SHARPY_AMBER     # closest
SH_WHITE    = SHARPY_WHITE     # 0
SH_SPIN_CW  = SHARPY_SPIN_CW   # 180 — moderate CW rotation

BSW_VIOLET  = BSW_MAG          # 50 — closest to violet
BSW_AMBER_C = BSW_ORANGE       # 26
BSW_GOLD_C  = BSW_YELLOW       # 32
BSW_CCW_MED = 160              # 128-189 = CCW fast→slow; 160 = medium CCW

PF_VIOLET   = PROF_PINK        # 30
PF_ORANGE   = PROF_ORANGE      # 25
PF_AMBER    = PROF_ORANGE      # 25
PF_GOLD     = PROF_YELLOW      # 10
PF_WHITE    = PROF_WHITE       # 0

# =============================================================================
# MOVER POSITIONS — loaded from venue focus-positions.md
# =============================================================================

POS = load_focus_position_tuples(project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)

# =============================================================================
# SCENE FACTORY
# =============================================================================

scenes = []
folder = "Sunrise"
scene_cache = {}

# Blackout
scenes.append(scene("Blackout", *blackout_all(), path=folder))
BO = 0


def get_or_create(key, fn):
    if key not in scene_cache:
        scene_cache[key] = len(scenes)
        scenes.append(fn())
    return scene_cache[key]


# ---------------------------------------------------------------------------
# INTRO_DARK (0:00-0:15) — Pre-dawn: near-black indigo, Profile at ceiling
# Sharpy/BSW killed (dark_*), Profile barely glowing aimed up
# ---------------------------------------------------------------------------

def _intro_dark():
    sp, st, bp, bt, pp, pt, np = POS["CEIL"]
    return scene("Intro-Dark",
        dark_sharpy(pan=sp, tilt=st),
        dark_bsw(pan=bp, tilt=bt),
        profile(pan=pp, tilt=pt, color=PF_VIOLET, dim=35, focus=128),
        fourbar_solid(*NEAR_BLACK, master=50),
        miss1(*NEAR_BLACK, master=40),
        miss2(*NEAR_BLACK, master=30),
        ni3k(pan=np, dim=25, r=15, g=5, b=50, w=0, halo=H_PNK, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# INTRO_STIR (0:15-0:31) — Slight re-awakening: movers begin to breathe
# Sharpy/BSW engage dim violet with heavy frost, start their counter-diverge
# ---------------------------------------------------------------------------

def _intro_stir():
    sh_pan, sh_tilt = POS["SL"][:2]   # Sharpy drifts left
    bp, bt = POS["SR"][2:4]           # BSW drifts right (OPPOSITE)
    pp, pt = POS["CEIL"][4:6]         # Profile still at ceiling
    np = POS["CEIL"][6]
    return scene("Intro-Stir",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_VIOLET, dim=40,
               strobe=SHARPY_OPEN, frost=70),
        bsw(pan=bp, tilt=bt, color=BSW_VIOLET, dim=30,
            shutter=BSW_SHUT_OPEN, frost=180),   # frost≥129 = actual frost
        profile(pan=pp, tilt=pt, color=PF_VIOLET, dim=60, focus=128),
        fourbar_gradient(*NEAR_BLACK, *PRE_DAWN, master=70),
        miss1(*VIOLET_MIST, master=50),
        miss2(*NEAR_BLACK, master=40),
        ni3k(pan=np, dim=45, r=25, g=8, b=70, w=0, halo=H_PNK, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# VERSE (0:31-0:47) — Horizon blush: amber bleeds from Sharpy side only
# Sharpy: amber SL. BSW: still violet SR. Asymmetric warmth.
# Profile: descending arc, tilt ~77 (midway CEIL→C)
# ---------------------------------------------------------------------------

def _verse():
    sh_pan, sh_tilt = POS["SL"][:2]
    bp, bt = POS["SR"][2:4]
    pp = POS["C"][4]
    pt = 77    # between CEIL(30) and C(123) — profile mid-arc
    np = 128
    return scene("Verse",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_AMBER, dim=120,
               strobe=SHARPY_OPEN, frost=40),
        bsw(pan=bp, tilt=bt, color=BSW_VIOLET, dim=80,
            shutter=BSW_SHUT_OPEN, frost=170),
        profile(pan=pp, tilt=pt, color=PF_AMBER, dim=100, focus=128),
        fourbar_gradient(*HORIZON_PURPLE, *HORIZON_AMBER, master=100),
        miss1(*HORIZON_AMBER, master=80),
        miss2(*PRE_DAWN, master=60),
        ni3k(pan=np, dim=80, r=80, g=30, b=20, w=0, halo=H_PNK, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# BUILD_SPIN (0:47-1:03) — Spinning color wheels: CW vs CCW
# Both movers centered/near-center, wheels rotating opposite directions.
# Atmospheric scatter — light through morning haze before the sun breaks.
# Profile descending: tilt ~110
# ---------------------------------------------------------------------------

def _build_spin():
    pp = POS["C"][4]
    pt = 110    # nearly at C, still descending
    np = 128
    return scene("Build-Spin",
        sharpy(pan=153, tilt=8, colormacro=SH_SPIN_CW, dim=160,
               strobe=SHARPY_OPEN, frost=20),
        bsw(pan=177, tilt=14, color=BSW_CCW_MED, dim=140,
            shutter=BSW_SHUT_OPEN, frost=0),   # tight beam while spinning
        profile(pan=pp, tilt=pt, color=PF_AMBER, dim=150, focus=128),
        fourbar_gradient(*HORIZON_PURPLE, *WARM_ORANGE, master=140),
        miss1(*WARM_ORANGE, master=110),
        miss2(*HORIZON_PURPLE, master=90),
        ni3k(pan=128, dim=120, r=150, g=50, b=10, w=0,
             halo=H_YEL, t1=128, t2=160, t3=192),
        path=folder,
    )


# ---------------------------------------------------------------------------
# BUILD_ARRIVE (1:03-1:18) — Wheels settle into warm colors, converge on DSC
# Profile arrives at C. Setup for the drop.
# ---------------------------------------------------------------------------

def _build_arrive():
    sp, st, bp, bt, pp, pt, np = POS["C"]
    return scene("Build-Arrive",
        sharpy(pan=sp, tilt=st, colormacro=SH_AMBER, dim=200,
               strobe=SHARPY_OPEN, frost=15),
        bsw(pan=bp, tilt=bt, color=BSW_AMBER_C, dim=180,
            shutter=BSW_SHUT_OPEN, frost=130),
        profile(pan=pp, tilt=pt, color=PF_ORANGE, dim=180, focus=128),
        fourbar_gradient(*HORIZON_AMBER, *WARM_ORANGE, master=180),
        miss1(*WARM_ORANGE, master=150),
        miss2(*HORIZON_AMBER, master=130),
        ni3k(pan=np, dim=160, r=200, g=80, b=0, w=20,
             halo=H_YEL, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# DROP_1_A (1:18-1:26) — Sun breaks: first full counter-sweep
# Sharpy→SR, BSW→SL. They CROSS the room toward opposite sides.
# Profile arrives at DSC — warm orange spotlight on the floor.
# ---------------------------------------------------------------------------

def _drop1_a():
    sh_pan, sh_tilt = POS["SR"][:2]   # 149, 5
    bp, bt = POS["SL"][2:4]           # 189, 29  (BSW goes OPPOSITE to Sharpy)
    pp, pt = POS["DSC"][4:6]
    np = POS["DSC"][6]
    return scene("Drop1-A",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_ORANGE, dim=230,
               strobe=SHARPY_OPEN, frost=0),
        bsw(pan=bp, tilt=bt, color=BSW_AMBER_C, dim=220,
            shutter=BSW_SHUT_OPEN, frost=0),
        profile(pan=pp, tilt=pt, color=PF_ORANGE, dim=220, focus=128),
        fourbar_solid(*SUNRISE_ORANGE, master=220),
        miss1(*SUNRISE_ORANGE, master=200),
        miss2(*WARM_ORANGE, master=190),
        ni3k(pan=np, dim=200, r=255, g=100, b=0, w=30,
             halo=H_YEL, t1=60, t2=80, t3=100),
        path=folder,
    )


# ---------------------------------------------------------------------------
# DROP_1_B (1:26-1:34) — Reverse counter-sweep: Sharpy→SL, BSW→SR
# ---------------------------------------------------------------------------

def _drop1_b():
    sh_pan, sh_tilt = POS["SL"][:2]   # 170, 0
    bp, bt = POS["SR"][2:4]           # 170, 23  (BSW goes right now)
    pp, pt = POS["DSC"][4:6]
    np = POS["DSC"][6]
    return scene("Drop1-B",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_ORANGE, dim=230,
               strobe=SHARPY_OPEN, frost=0),
        bsw(pan=bp, tilt=bt, color=BSW_AMBER_C, dim=220,
            shutter=BSW_SHUT_OPEN, frost=0),
        profile(pan=pp, tilt=pt, color=PF_AMBER, dim=220, focus=128),
        fourbar_gradient(*SUNRISE_ORANGE, *WARM_ORANGE, master=220),
        miss1(*WARM_ORANGE, master=200),
        miss2(*SUNRISE_ORANGE, master=200),
        ni3k(pan=np, dim=200, r=220, g=80, b=0, w=40,
             halo=H_YEL, t1=100, t2=80, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# PEAK_1 (1:34-1:42) — Full sunrise: DSR+DSL maximum diverge, gold
# ---------------------------------------------------------------------------

def _peak1():
    sh_pan, sh_tilt = POS["DSR"][:2]   # 149, 5
    bp, bt = POS["DSL"][2:4]           # 189, 29  (max spread)
    pp, pt = POS["DSC"][4:6]
    np = 128
    return scene("Peak1",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_GOLD, dim=255,
               strobe=SHARPY_OPEN, frost=0),
        bsw(pan=bp, tilt=bt, color=BSW_GOLD_C, dim=255,
            shutter=BSW_SHUT_OPEN, frost=0),
        profile(pan=pp, tilt=pt, color=PF_GOLD, dim=255, focus=128),
        fourbar_solid(*SOFT_GOLD, master=255),
        miss1(*SOFT_GOLD, master=245),
        miss2(*SOFT_GOLD, master=245),
        ni3k(pan=128, dim=255, r=255, g=160, b=20, w=60,
             halo=H_YEL, t1=128, t2=160, t3=200),
        path=folder,
    )


# ---------------------------------------------------------------------------
# PEAK_1_WHITE (1:42-1:50) — Converge to C, warm white flash
# ---------------------------------------------------------------------------

def _peak1_white():
    sp, st, bp, bt, pp, pt, np = POS["C"]
    return scene("Peak1-White",
        sharpy(pan=sp, tilt=st, colormacro=SH_WHITE, dim=255,
               strobe=SHARPY_OPEN, frost=0),
        bsw(pan=bp, tilt=bt, color=BSW_WHITE, dim=255,
            shutter=BSW_SHUT_OPEN, frost=0),
        profile(pan=pp, tilt=pt, color=PF_WHITE, dim=255, focus=128),
        fourbar_solid(*GOLDEN_WHITE, master=255),
        miss1(*GOLDEN_WHITE, master=255),
        miss2(*GOLDEN_WHITE, master=255),
        ni3k(pan=np, dim=255, r=255, g=200, b=100, w=100,
             halo=H_RGB, t1=60, t2=90, t3=120),
        path=folder,
    )


# ---------------------------------------------------------------------------
# SUST_A (1:50-2:00) — Sustained gold: SR + SL counter (Sharpy SR, BSW SL)
# ---------------------------------------------------------------------------

def _sust_a():
    sh_pan, sh_tilt = POS["SR"][:2]
    bp, bt = POS["SL"][2:4]
    pp, pt = POS["C"][4:6]
    np = 128
    return scene("Sust-A",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_AMBER, dim=235,
               strobe=SHARPY_OPEN, frost=0),
        bsw(pan=bp, tilt=bt, color=BSW_GOLD_C, dim=225,
            shutter=BSW_SHUT_OPEN, frost=0),
        profile(pan=pp, tilt=pt, color=PF_GOLD, dim=210, focus=128),
        fourbar_gradient(*WARM_GOLD, *SOFT_GOLD, master=225),
        miss1(*WARM_GOLD, master=210),
        miss2(*SOFT_GOLD, master=210),
        ni3k(pan=np, dim=210, r=240, g=140, b=10, w=30,
             halo=H_YEL, t1=60, t2=70, t3=80),
        path=folder,
    )


# ---------------------------------------------------------------------------
# SUST_B (2:00-2:10) — Reverse: Sharpy SL, BSW SR
# ---------------------------------------------------------------------------

def _sust_b():
    sh_pan, sh_tilt = POS["SL"][:2]
    bp, bt = POS["SR"][2:4]
    pp, pt = POS["DSC"][4:6]
    np = 128
    return scene("Sust-B",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_ORANGE, dim=225,
               strobe=SHARPY_OPEN, frost=0),
        bsw(pan=bp, tilt=bt, color=BSW_AMBER_C, dim=215,
            shutter=BSW_SHUT_OPEN, frost=0),
        profile(pan=pp, tilt=pt, color=PF_AMBER, dim=210, focus=128),
        fourbar_gradient(*AMBER_GLOW, *WARM_GOLD, master=215),
        miss1(*SOFT_GOLD, master=200),
        miss2(*WARM_GOLD, master=200),
        ni3k(pan=np, dim=200, r=220, g=120, b=5, w=20,
             halo=H_YEL, t1=80, t2=60, t3=70),
        path=folder,
    )


# ---------------------------------------------------------------------------
# SUST_C (2:10-2:21) — Converge to DSC — gold unity before breakdown
# ---------------------------------------------------------------------------

def _sust_c():
    sp, st, bp, bt, pp, pt, np = POS["DSC"]
    return scene("Sust-C",
        sharpy(pan=sp, tilt=st, colormacro=SH_GOLD, dim=240,
               strobe=SHARPY_OPEN, frost=0),
        bsw(pan=bp, tilt=bt, color=BSW_GOLD_C, dim=230,
            shutter=BSW_SHUT_OPEN, frost=0),
        profile(pan=pp, tilt=pt, color=PF_GOLD, dim=225, focus=128),
        fourbar_solid(*WARM_GOLD, master=235),
        miss1(*WARM_GOLD, master=220),
        miss2(*WARM_GOLD, master=220),
        ni3k(pan=np, dim=215, r=255, g=150, b=15, w=40,
             halo=H_YEL, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# BREAK_DEEP (2:21-2:37) — Cloud shadow: near-dark, almost silence
# Movers killed with dark_*(). Profile back at ceiling, barely lit.
# ---------------------------------------------------------------------------

def _break_deep():
    sp, st, bp, bt, pp, pt, np = POS["CEIL"]
    return scene("Break-Deep",
        dark_sharpy(pan=sp, tilt=st),
        dark_bsw(pan=bp, tilt=bt),
        profile(pan=pp, tilt=pt, color=PF_VIOLET, dim=25, focus=128),
        fourbar_solid(*NEAR_BLACK, master=35),
        miss1(*CLOUD_VIOLET, master=25),
        miss2(*NEAR_BLACK, master=20),
        ni3k(pan=np, dim=15, r=10, g=0, b=30, w=0,
             halo=H_OFF, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# BREAK_STIR (2:37-2:53) — Slight re-awakening: movers re-engage at low dim
# Violet haze, heavy frost. The sun starting to peek out again.
# ---------------------------------------------------------------------------

def _break_stir():
    sh_pan, sh_tilt = POS["C"][:2]
    bp, bt = POS["C"][2:4]
    pp, pt = POS["CEIL"][4:6]
    pt_mid = 70    # between CEIL(30) and C(123), profile still high
    np = 128
    return scene("Break-Stir",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_VIOLET, dim=45,
               strobe=SHARPY_OPEN, frost=80),
        bsw(pan=bp, tilt=bt, color=BSW_VIOLET, dim=35,
            shutter=BSW_SHUT_OPEN, frost=190),
        profile(pan=pp, tilt=pt_mid, color=PF_VIOLET, dim=50, focus=128),
        fourbar_solid(*CLOUD_VIOLET, master=50),
        miss1(*PRE_DAWN, master=40),
        miss2(*CLOUD_VIOLET, master=35),
        ni3k(pan=np, dim=40, r=20, g=5, b=50, w=0,
             halo=H_PNK, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# RETURN (2:53-3:09) — Sun re-emerging: amber starts building again
# Sharpy → SL amber, BSW → SR still cooler. Profile descending (~tilt=100).
# Counter-diverge reinstating.
# ---------------------------------------------------------------------------

def _return():
    sh_pan, sh_tilt = POS["SL"][:2]
    bp, bt = POS["SR"][2:4]
    pp = POS["C"][4]
    pt = 100    # descending from ~70 toward C(123)
    np = 128
    return scene("Return",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_AMBER, dim=140,
               strobe=SHARPY_OPEN, frost=30),
        bsw(pan=bp, tilt=bt, color=BSW_VIOLET, dim=100,
            shutter=BSW_SHUT_OPEN, frost=160),
        profile(pan=pp, tilt=pt, color=PF_AMBER, dim=120, focus=128),
        fourbar_gradient(*CLOUD_VIOLET, *HORIZON_AMBER, master=120),
        miss1(*HORIZON_AMBER, master=100),
        miss2(*PRE_DAWN, master=80),
        ni3k(pan=np, dim=100, r=120, g=40, b=10, w=0,
             halo=H_PNK, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# DROP_2_A (3:09-3:18) — Second bigger sunrise with prisms + red laser
# Sharpy→DSR, BSW→DSL (max diverge, prisms spinning)
# ---------------------------------------------------------------------------

def _drop2_a():
    sh_pan, sh_tilt = POS["DSR"][:2]
    bp, bt = POS["DSL"][2:4]
    pp, pt = POS["DSC"][4:6]
    np = 128
    return scene("Drop2-A",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_GOLD, dim=255,
               strobe=SHARPY_OPEN, frost=0, prism1=128, p1r=200),
        bsw(pan=bp, tilt=bt, color=BSW_GOLD_C, dim=255,
            shutter=BSW_SHUT_OPEN, frost=0, prism=128, prot=200),
        profile(pan=pp, tilt=pt, color=PF_GOLD, dim=255, focus=128, prism=128),
        fourbar_solid(*SOFT_GOLD, master=255),
        miss1(*SOFT_GOLD, master=245),
        miss2(*SOFT_GOLD, master=245),
        ni3k(pan=np, dim=255, r=255, g=160, b=20, w=60,
             halo=H_YEL, t1=128, t2=160, t3=200,
             rl=LASER_ON),   # Red laser only — warm daylight color
        path=folder,
    )


# ---------------------------------------------------------------------------
# DROP_2_B (3:18-3:26) — Reverse: Sharpy→DSL, BSW→DSR, orange, red laser
# ---------------------------------------------------------------------------

def _drop2_b():
    sh_pan, sh_tilt = POS["DSL"][:2]
    bp, bt = POS["DSR"][2:4]
    pp, pt = POS["C"][4:6]
    np = 128
    return scene("Drop2-B",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_ORANGE, dim=255,
               strobe=SHARPY_OPEN, frost=0, prism1=128, p1r=200),
        bsw(pan=bp, tilt=bt, color=BSW_AMBER_C, dim=255,
            shutter=BSW_SHUT_OPEN, frost=0, prism=128, prot=200),
        profile(pan=pp, tilt=pt, color=PF_ORANGE, dim=245, focus=128, prism=128),
        fourbar_gradient(*WARM_GOLD, *SUNRISE_ORANGE, master=250),
        miss1(*SUNRISE_ORANGE, master=235),
        miss2(*WARM_GOLD, master=235),
        ni3k(pan=np, dim=255, r=255, g=140, b=10, w=50,
             halo=H_YEL, t1=200, t2=160, t3=128,
             rl=LASER_ON),
        path=folder,
    )


# ---------------------------------------------------------------------------
# DROP_2_C (3:26-3:35) — Converge to DSC: red + green lasers
# ---------------------------------------------------------------------------

def _drop2_c():
    sp, st, bp, bt, pp, pt, np = POS["DSC"]
    return scene("Drop2-C",
        sharpy(pan=sp, tilt=st, colormacro=SH_GOLD, dim=255,
               strobe=SHARPY_OPEN, frost=0, prism1=128, p1r=200),
        bsw(pan=bp, tilt=bt, color=BSW_GOLD_C, dim=255,
            shutter=BSW_SHUT_OPEN, frost=0, prism=128, prot=150),
        profile(pan=pp, tilt=pt, color=PF_GOLD, dim=255, focus=128, prism=128),
        fourbar_solid(*WARM_GOLD, master=255),
        miss1(*WARM_GOLD, master=248),
        miss2(*WARM_GOLD, master=248),
        ni3k(pan=np, dim=255, r=255, g=150, b=15, w=60,
             halo=H_RGB, t1=60, t2=60, t3=60,
             rl=LASER_ON, gl=LASER_ON),
        path=folder,
    )


# ---------------------------------------------------------------------------
# DROP_2P_WIDE (3:35-3:44) — inst peak: max spread, warm white, ALL lasers
# ---------------------------------------------------------------------------

def _drop2p_wide():
    sh_pan, sh_tilt = POS["SL"][:2]
    bp, bt = POS["SR"][2:4]
    pp, pt = POS["DSC"][4:6]
    np = 176
    return scene("Drop2P-Wide",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_WHITE, dim=255,
               strobe=SHARPY_OPEN, frost=0, prism1=128, p1r=200),
        bsw(pan=bp, tilt=bt, color=BSW_WHITE, dim=255,
            shutter=BSW_SHUT_OPEN, frost=0, prism=128, prot=200),
        profile(pan=pp, tilt=pt, color=PF_WHITE, dim=255, focus=128, prism=200),
        fourbar_solid(*GOLDEN_WHITE, master=255),
        miss1(*GOLDEN_WHITE, master=255),
        miss2(*GOLDEN_WHITE, master=255),
        ni3k(pan=np, dim=255, r=255, g=200, b=80, w=80,
             halo=H_YEL, t1=192, t2=160, t3=220,
             rl=LASER_ON, gl=LASER_ON, bl=LASER_ON),
        path=folder,
    )


# ---------------------------------------------------------------------------
# DROP_2P_CTR (3:44-3:53) — Center convergence, gold, all 3 lasers
# ---------------------------------------------------------------------------

def _drop2p_ctr():
    sp, st, bp, bt, pp, pt, np = POS["C"]
    return scene("Drop2P-Ctr",
        sharpy(pan=sp, tilt=st, colormacro=SH_GOLD, dim=255,
               strobe=SHARPY_OPEN, frost=0, prism1=128, p1r=200),
        bsw(pan=bp, tilt=bt, color=BSW_GOLD_C, dim=255,
            shutter=BSW_SHUT_OPEN, frost=0, prism=128, prot=150),
        profile(pan=pp, tilt=pt, color=PF_GOLD, dim=255, focus=128, prism=200),
        fourbar_solid(*WARM_GOLD, master=255),
        miss1(*WARM_GOLD, master=252),
        miss2(*WARM_GOLD, master=252),
        ni3k(pan=np, dim=255, r=255, g=180, b=40, w=80,
             halo=H_RGB, t1=128, t2=160, t3=200,
             rl=LASER_ON, gl=LASER_ON, bl=LASER_ON),
        path=folder,
    )


# ---------------------------------------------------------------------------
# OUTRO_WARM (3:58-4:14) — Energy still high, warm amber resolving
# Profile ascending: tilt ~100 (back toward ceiling)
# ---------------------------------------------------------------------------

def _outro_warm():
    sh_pan, sh_tilt = POS["C"][:2]
    bp, bt = POS["C"][2:4]
    pp = POS["C"][4]
    pt = 100    # ascending from DSC(145) toward CEIL(30)
    np = 128
    return scene("Outro-Warm",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_AMBER, dim=185,
               strobe=SHARPY_OPEN, frost=30),
        bsw(pan=bp, tilt=bt, color=BSW_AMBER_C, dim=165,
            shutter=BSW_SHUT_OPEN, frost=130),
        profile(pan=pp, tilt=pt, color=PF_AMBER, dim=155, focus=128),
        fourbar_gradient(*AMBER_GLOW, *WARM_GOLD, master=185),
        miss1(*AMBER_GLOW, master=165),
        miss2(*AMBER_GLOW, master=150),
        ni3k(pan=np, dim=155, r=180, g=80, b=0, w=10,
             halo=H_YEL, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# OUTRO_DIM (4:14-4:27) — Dimming amber, frost builds, profile rising
# ---------------------------------------------------------------------------

def _outro_dim():
    sh_pan, sh_tilt = POS["C"][:2]
    bp, bt = POS["C"][2:4]
    pp = POS["C"][4]
    pt = 65    # higher arc, nearly back toward ceiling
    np = 128
    return scene("Outro-Dim",
        sharpy(pan=sh_pan, tilt=sh_tilt, colormacro=SH_AMBER, dim=90,
               strobe=SHARPY_OPEN, frost=80),
        bsw(pan=bp, tilt=bt, color=BSW_AMBER_C, dim=70,
            shutter=BSW_SHUT_OPEN, frost=180),
        profile(pan=pp, tilt=pt, color=PF_AMBER, dim=70, focus=128),
        fourbar_gradient(*AMBER_FADE, *AMBER_GLOW, master=100),
        miss1(*AMBER_FADE, master=90),
        miss2(*AMBER_FADE, master=80),
        ni3k(pan=np, dim=70, r=80, g=30, b=0, w=0,
             halo=H_OFF, t1=60, t2=60, t3=60),
        path=folder,
    )


# ---------------------------------------------------------------------------
# OUTRO_FADE (4:27-4:44) — Dissolve back to pre-dawn: violet, profile at ceil
# We've come full circle. Day ends; darkness returns.
# ---------------------------------------------------------------------------

def _outro_fade():
    sp, st, bp, bt, pp, pt, np = POS["CEIL"]
    return scene("Outro-Fade",
        dark_sharpy(pan=sp, tilt=st),
        dark_bsw(pan=bp, tilt=bt),
        profile(pan=pp, tilt=pt, color=PF_VIOLET, dim=22, focus=128),
        fourbar_solid(*NEAR_BLACK, master=30),
        miss1(*NEAR_BLACK, master=25),
        miss2(*NEAR_BLACK, master=20),
        ni3k(pan=np, dim=12, r=8, g=3, b=20, w=0,
             halo=H_OFF, t1=60, t2=60, t3=60),
        path=folder,
    )


# =============================================================================
# REGISTER ALL SCENES
# =============================================================================

INTRO_DARK   = get_or_create("intro_dark",   _intro_dark)
INTRO_STIR   = get_or_create("intro_stir",   _intro_stir)
VERSE        = get_or_create("verse",         _verse)
BUILD_SPIN   = get_or_create("build_spin",    _build_spin)
BUILD_ARRIVE = get_or_create("build_arrive",  _build_arrive)
DROP1_A      = get_or_create("drop1_a",       _drop1_a)
DROP1_B      = get_or_create("drop1_b",       _drop1_b)
PEAK1        = get_or_create("peak1",          _peak1)
PEAK1_WHITE  = get_or_create("peak1_white",    _peak1_white)
SUST_A       = get_or_create("sust_a",         _sust_a)
SUST_B       = get_or_create("sust_b",         _sust_b)
SUST_C       = get_or_create("sust_c",         _sust_c)
BREAK_DEEP   = get_or_create("break_deep",     _break_deep)
BREAK_STIR   = get_or_create("break_stir",     _break_stir)
RETURN_SEC   = get_or_create("return_sec",     _return)
DROP2_A      = get_or_create("drop2_a",        _drop2_a)
DROP2_B      = get_or_create("drop2_b",        _drop2_b)
DROP2_C      = get_or_create("drop2_c",        _drop2_c)
DROP2P_WIDE  = get_or_create("drop2p_wide",    _drop2p_wide)
DROP2P_CTR   = get_or_create("drop2p_ctr",     _drop2p_ctr)
OUTRO_WARM   = get_or_create("outro_warm",     _outro_warm)
OUTRO_DIM    = get_or_create("outro_dim",      _outro_dim)
OUTRO_FADE   = get_or_create("outro_fade",     _outro_fade)

# =============================================================================
# CHASER SEQUENCE
# Timings validated to match song timestamps (total ≈ 282s vs 283s actual)
# =============================================================================

steps = [
    # INTRO (16 bars = 31.5s)
    (INTRO_DARK,   smooth(BPM, 8)),    # 0:00-0:15 profile at ceil, pre-dawn dark
    (INTRO_STIR,   smooth(BPM, 8)),    # 0:15-0:31 slight Sharpy/BSW diverge begins

    # VERSE (8 bars = 15.7s)
    (VERSE,        smooth(BPM, 8)),    # 0:31-0:47 amber from Sharpy side

    # BUILD_1 (16 bars = 31.5s)
    (BUILD_SPIN,   smooth(BPM, 8)),    # 0:47-1:03 color wheels spin opposite dirs
    (BUILD_ARRIVE, smooth(BPM, 8)),    # 1:03-1:18 settle warm, profile at C

    # DROP_1 (8 bars = 15.7s)
    (DROP1_A,      snap(BPM, 4)),      # 1:18-1:26 Sharpy→SR / BSW→SL counter
    (DROP1_B,      snap(BPM, 4)),      # 1:26-1:34 Sharpy→SL / BSW→SR reverse

    # PEAK_1 (8 bars = 15.7s)
    (PEAK1,        snap(BPM, 4)),      # 1:34-1:42 DSR+DSL max diverge, gold
    (PEAK1_WHITE,  snap(BPM, 4)),      # 1:42-1:50 converge C, warm white

    # SUST (16 bars = 31.5s)
    (SUST_A,       smooth(BPM, 5)),    # 1:50-2:00 SR/SL counter, amber
    (SUST_B,       smooth(BPM, 5)),    # 2:00-2:10 reverse SL/SR, orange
    (SUST_C,       smooth(BPM, 6)),    # 2:10-2:21 converge DSC, gold unity

    # BREAK (16 bars = 31.5s)
    (BREAK_DEEP,   smooth(BPM, 8)),    # 2:21-2:37 near-dark, movers killed
    (BREAK_STIR,   smooth(BPM, 8)),    # 2:37-2:53 violet haze re-engages

    # RETURN (8 bars = 15.7s)
    (RETURN_SEC,   smooth(BPM, 8)),    # 2:53-3:09 amber re-emerging

    # DROP_2 + DROP_2P (25 bars = 49.2s)
    (DROP2_A,      snap(BPM, 5)),      # 3:09-3:19 prisms + DSR/DSL + red laser
    (DROP2_B,      snap(BPM, 5)),      # 3:19-3:28 reverse DSL/DSR, red laser
    (DROP2_C,      snap(BPM, 5)),      # 3:28-3:37 converge DSC, red+green
    (DROP2P_WIDE,  snap(BPM, 5)),      # 3:37-3:47 SL/SR wide, all 3 lasers
    (DROP2P_CTR,   snap(BPM, 5)),      # 3:47-3:56 center, all 3 lasers

    # OUTRO (23 bars = 45.2s)
    (OUTRO_WARM,   smooth(BPM, 8)),    # 3:58-4:14 amber glow, profile ascending
    (OUTRO_DIM,    smooth(BPM, 7)),    # 4:14-4:27 dimming, frost
    (OUTRO_FADE,   smooth(BPM, 8)),    # 4:27-4:44 dissolve back to pre-dawn
]

# =============================================================================
# BUILD CHASER + WRITE OUTPUT
# =============================================================================

scene_ids = [s[0] for s in steps]
timing    = [s[1] for s in steps]

main_chaser = make_chaser(
    "Sunrise - Full Show",
    scene_ids,
    timing,
    run_order="SingleShot",
    path=folder,
)

OUT_PATH = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")
write_workspace(OUT_PATH, scenes, [main_chaser], bpm=BPM)
print(f"Written: {OUT_PATH}")
print(f"Scenes:  {len(scenes)}  (including blackout)")
print(f"Steps:   {len(steps)}")
total_ms = sum(f + h for f, h in timing)
print(f"Total duration: {total_ms/1000:.1f}s  (track: 283s)")
