#!/usr/bin/env python3
"""
Show Generator: Lorn - Acid Rain (Skeler Remix)
================================================
BPM: 115 | Duration: ~4:23 | Genre: Dark electronic / wave

Creative Direction:
  - False calm intro: cool blue wash that corrupts over 3 intro sections
  - Distinct solo chapters: each with unique movement pattern
  - Predatory hunting: slow stalk punctuated by violent snaps
  - Mixed snap accents: strobes, color flashes, and silence
  - Break: eerie isolation (single fixture, unsettling movement)
  - Lasers: punctuation marks at transitions + sustained during break
  - Static fixtures: counter-rhythm against movers
  - Outro: echo of the false calm, darker and emptier

Song Structure (from allin1 analysis):
  0:00 - 0:19  intro     (9 bars)   "Serene blue"
  0:19 - 0:37  intro     (9 bars)   "Corruption begins"
  0:37 - 0:56  intro     (9 bars)   "Fully corrupt"
  0:56 - 1:14  solo      (9 bars)   "Chapter 1: The Stalk"
  1:14 - 1:48  solo      (16 bars)  "Chapter 2: Cross-room Sweeps"
  1:48 - 2:11  solo      (11 bars)  "Chapter 3: Erratic Whip"
  2:11 - 2:29  break     (8 bars)   "Eerie Isolation"
  2:29 - 3:01  solo      (15 bars)  "Chapter 4: Lockstep Assault"
  3:01 - 3:25  solo      (12 bars)  "Chapter 5: Renewed Hunt"
  3:25 - 3:41  solo      (8 bars)   "Chapter 6: Final Push"
  3:41 - 4:02  solo      (10 bars)  "Chapter 7: Unhinged"
  4:02 - 4:23  outro     (10 bars)  "Echo of the Calm"
  4:23 - 4:33  outro     (5 bars)   "Fade to Black"
"""

import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from showlib import *

# =============================================================================
# TIMING — from analysis JSON
# =============================================================================

BPM = 115
BAR_MS = bpm_to_ms(BPM, 4)  # ~2087ms per bar
BEAT_MS = bpm_to_ms(BPM, 1)  # ~522ms per beat

# Segment boundaries (rounded to nearest bar for chaser steps)
# We'll use bar counts derived from segment durations
# Each segment ~2.087s per bar at 115 BPM

# =============================================================================
# COLOR PALETTES
# =============================================================================

# False calm palette (intro 1)
CALM_BLUE = (40, 80, 180)
CALM_TEAL = (20, 100, 140)

# Corruption palette (intro 2-3)
SICK_GREEN = (60, 140, 20)
SICK_AMBER = (180, 100, 10)
BRUISE_PURPLE = (90, 10, 120)

# Dark aggressive palettes (solo chapters)
BLOOD_RED = (180, 0, 0)
DEEP_RED = (120, 0, 10)
VOID_BLUE = (0, 10, 80)
POISON_GREEN = (0, 100, 20)
COLD_WHITE = (200, 200, 220)
ASH_GREY = (40, 40, 50)
VIOLET = (100, 0, 180)
DARK_CYAN = (0, 80, 100)
NOTHING = (0, 0, 0)

# Eerie isolation
EERIE_DIM = (10, 5, 30)

# Outro (corrupted calm)
DEAD_BLUE = (15, 30, 60)
DEAD_TEAL = (8, 40, 50)

# =============================================================================
# MOVER POSITIONS — predatory hunting vocabulary
# =============================================================================

# Center positions
S_C = {"pan": 153, "tilt": 0}
B_C = {"pan": 7, "tilt": 19}
P_C = {"pan": 0, "tilt": 123}

# Far positions (hunting extremes)
S_FAR_L = {"pan": 80, "tilt": 15}
S_FAR_R = {"pan": 220, "tilt": 15}
S_HIGH  = {"pan": 153, "tilt": 40}
S_LOW   = {"pan": 153, "tilt": 245}

B_FAR_L = {"pan": 80, "tilt": 30}
B_FAR_R = {"pan": 200, "tilt": 5}
B_HIGH  = {"pan": 7, "tilt": 50}
B_LOW   = {"pan": 7, "tilt": 5}

P_FAR_L = {"pan": 60, "tilt": 100}
P_FAR_R = {"pan": 200, "tilt": 100}
P_HIGH  = {"pan": 0, "tilt": 80}
P_LOW   = {"pan": 0, "tilt": 160}

# Cross positions (movers swap sides)
S_CROSS = {"pan": 80, "tilt": 10}
B_CROSS = {"pan": 200, "tilt": 10}
P_CROSS = {"pan": 180, "tilt": 100}

# Wide spread
S_WIDE = {"pan": 220, "tilt": 20}
B_WIDE = {"pan": 80, "tilt": 30}
P_WIDE = {"pan": 50, "tilt": 90}

# Audience positions (beams into crowd)
S_AUD = {"pan": 153, "tilt": 230}
B_AUD = {"pan": 7, "tilt": 0}
P_AUD = {"pan": 0, "tilt": 150}

# =============================================================================
# SCENE CONSTRUCTION HELPERS
# =============================================================================

# BSW → Sharpy color mapping
SHARPY_MAP = {
    BSW_WHITE: SHARPY_WHITE, BSW_RED: SHARPY_RED, BSW_BLUE: SHARPY_BLUE,
    BSW_GREEN: SHARPY_GREEN, BSW_MAG: SHARPY_PURPLE, BSW_TEAL: SHARPY_TEAL,
    BSW_ORANGE: SHARPY_ORANGE, BSW_YELLOW: SHARPY_YELLOW, BSW_PINK: SHARPY_PINK,
}

# BSW → Profile color mapping
PROF_MAP = {
    BSW_WHITE: PROF_WHITE, BSW_RED: PROF_RED, BSW_BLUE: PROF_BLUE,
    BSW_GREEN: PROF_GREEN, BSW_MAG: PROF_PINK, BSW_TEAL: PROF_TEAL,
    BSW_ORANGE: PROF_ORANGE, BSW_YELLOW: PROF_YELLOW, BSW_PINK: PROF_PINK,
}

def dark_sharpy(pos, gobo=0, prism1=0, p1r=0, prism2=0, p2r=0,
                frost=0, focus=128, dim=255, colormacro=SHARPY_WHITE):
    """Sharpy with strobe fixed at OPEN to avoid crossfade artifacts."""
    return sharpy(pan=pos["pan"], tilt=pos["tilt"], color7=0, gobo=gobo,
                  prism1=prism1, p1r=p1r, prism2=prism2, p2r=p2r,
                  frost=frost, focus=focus, strobe=SHARPY_OPEN, dim=dim,
                  colormacro=colormacro)

def dark_bsw(pos, color=BSW_WHITE, gobo1=0, gobo2=0, g2rot=0,
             frost=0, prism=0, prot=0, focus=128, dim=255):
    """BSW with shutter fixed at OPEN to avoid crossfade artifacts."""
    return bsw(pan=pos["pan"], tilt=pos["tilt"], color=color, gobo1=gobo1,
               gobo2=gobo2, g2rot=g2rot, frost=frost, prism=prism, prot=prot,
               focus=focus, shutter=BSW_SHUT_OPEN, dim=dim)

def dark_profile(pos, color=PROF_WHITE, gobo=0, gobo1=0, g1rot=0,
                 prism=0, focus=128, dim=255):
    """Profile with strobe fixed at OFF (0) to avoid crossfade artifacts."""
    return profile(pan=pos["pan"], tilt=pos["tilt"], color=color, gobo=gobo,
                   gobo1=gobo1, g1rot=g1rot, prism=prism, focus=focus,
                   strobe=PROFILE_STROBE_OFF, dim=dim)

def ni3k_dark(r=0, g=0, b=0, w=0, halo=H_OFF, rl=LASER_OFF, gl=LASER_OFF,
              bl=LASER_OFF, t1=64, t2=64, t3=64, dim=255):
    """NI3K with strobe at 0 (on/open)."""
    return ni3k(pan=128, t1=t1, t2=t2, t3=t3, r=r, g=g, b=b, w=w,
                halo=halo, rl=rl, gl=gl, bl=bl, dim=dim, strobe=0)

def flash_sharpy(pos, **kw):
    """Sharpy with white color burst for snap accents."""
    return dark_sharpy(pos, dim=255, colormacro=0, **kw)

# 4BAR counter-rhythm patterns
def bar_chase_a(c1, c2):
    """4BAR: pars 1,3 = c1, pars 2,4 = c2"""
    return fourbar_pairs(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2])

def bar_chase_b(c1, c2):
    """4BAR: pars 2,4 = c1, pars 1,3 = c2 (inverse of chase_a)"""
    return fourbar_pairs(c2[0], c2[1], c2[2], c1[0], c1[1], c1[2])

def bar_sweep_lr(c, pos):
    """4BAR: single par lit, sweeping left to right. pos = 0-3"""
    vals = [NOTHING, NOTHING, NOTHING, NOTHING]
    vals[pos % 4] = c
    return fourbar(vals[0][0], vals[0][1], vals[0][2],
                   vals[1][0], vals[1][1], vals[1][2],
                   vals[2][0], vals[2][1], vals[2][2],
                   vals[3][0], vals[3][1], vals[3][2])

# =============================================================================
# BUILD ALL SCENES
# =============================================================================

scenes = []
folder = "Acid Rain"

# --- BLACKOUT (always scene 0) ---
scenes.append(scene("Blackout", *blackout_all(), path=folder))

# =============================================================================
# INTRO 1: FALSE CALM — Serene blue wash (bars 1-9, ~0:00 - 0:19)
# =============================================================================

# Calm-1A: Gentle blue wash, movers at center, everything peaceful
scenes.append(scene("Calm 1A - Blue Serenity",
    dark_sharpy(S_C, dim=60, frost=200, colormacro=SHARPY_BLUE),
    dark_bsw(B_C, color=BSW_BLUE, dim=60, frost=200),
    dark_profile(P_C, dim=40, color=PROF_BLUE),
    fourbar_solid(*CALM_BLUE, master=80),
    *miss_both(*CALM_TEAL, master=60),
    ni3k_dark(r=20, g=40, b=120, halo=H_BLU, dim=80),
    path=folder))

# Calm-1B: Slightly brighter, movers drift slightly
scenes.append(scene("Calm 1B - Drift",
    dark_sharpy({"pan": 160, "tilt": 5}, dim=70, frost=180, colormacro=SHARPY_BLUE),
    dark_bsw({"pan": 15, "tilt": 22}, color=BSW_BLUE, dim=70, frost=180),
    dark_profile({"pan": 10, "tilt": 120}, dim=50, color=PROF_BLUE),
    fourbar_gradient(CALM_BLUE[0], CALM_BLUE[1], CALM_BLUE[2],
                     CALM_TEAL[0], CALM_TEAL[1], CALM_TEAL[2], master=90),
    *miss_both(*CALM_BLUE, master=70),
    ni3k_dark(r=15, g=50, b=140, halo=H_BLU, dim=90),
    path=folder))

# =============================================================================
# INTRO 2: CORRUPTION BEGINS (bars 10-18, ~0:19 - 0:37)
# =============================================================================

# Colors start shifting sickly. Teal drains toward green/amber.
scenes.append(scene("Corrupt 2A - Teal Drains",
    dark_sharpy({"pan": 145, "tilt": 8}, dim=80, frost=120, colormacro=SHARPY_TEAL),
    dark_bsw({"pan": 20, "tilt": 25}, color=BSW_TEAL, dim=80, frost=120),
    dark_profile({"pan": 15, "tilt": 118}, dim=60, color=PROF_TEAL),
    fourbar_pairs(CALM_TEAL[0], CALM_TEAL[1], CALM_TEAL[2],
                  SICK_GREEN[0], SICK_GREEN[1], SICK_GREEN[2], master=100),
    miss1(*SICK_GREEN, master=80),
    miss2(*CALM_TEAL, master=80),
    ni3k_dark(r=30, g=80, b=60, halo=H_CYN, dim=100),
    path=folder))

scenes.append(scene("Corrupt 2B - Amber Seeps",
    dark_sharpy({"pan": 170, "tilt": 12}, dim=90, frost=80, colormacro=SHARPY_GREEN),
    dark_bsw({"pan": 30, "tilt": 15}, color=BSW_GREEN, dim=90, frost=80),
    dark_profile({"pan": 25, "tilt": 115}, dim=70, color=PROF_GREEN),
    fourbar_pairs(SICK_GREEN[0], SICK_GREEN[1], SICK_GREEN[2],
                  SICK_AMBER[0], SICK_AMBER[1], SICK_AMBER[2], master=110),
    miss1(*SICK_AMBER, master=90),
    miss2(*SICK_GREEN, master=80),
    ni3k_dark(r=80, g=60, b=15, halo=H_YEL, dim=100),
    path=folder))

# =============================================================================
# INTRO 3: FULLY CORRUPT (bars 19-27, ~0:37 - 0:56)
# =============================================================================

# Movement gets twitchy. Colors are wrong. First hint of aggression.
scenes.append(scene("Corrupt 3A - Bruise",
    dark_sharpy({"pan": 130, "tilt": 20}, dim=120, frost=40, colormacro=SHARPY_PURPLE),
    dark_bsw({"pan": 40, "tilt": 10}, color=BSW_MAG, dim=100),
    dark_profile({"pan": 35, "tilt": 110}, dim=80, prism=60, color=PROF_PINK),
    fourbar_solid(*BRUISE_PURPLE, master=120),
    *miss_both(*SICK_AMBER, master=100),
    ni3k_dark(r=90, g=10, b=80, halo=H_PNK, dim=120),
    path=folder))

scenes.append(scene("Corrupt 3B - Twitch",
    dark_sharpy({"pan": 180, "tilt": 3}, dim=130, colormacro=SHARPY_RED),
    dark_bsw({"pan": 50, "tilt": 28}, color=BSW_RED, dim=110),
    dark_profile({"pan": 230, "tilt": 130}, dim=90, color=PROF_RED),
    fourbar_pairs(BRUISE_PURPLE[0], BRUISE_PURPLE[1], BRUISE_PURPLE[2],
                  DEEP_RED[0], DEEP_RED[1], DEEP_RED[2], master=130),
    miss1(*BRUISE_PURPLE, master=110),
    miss2(*DEEP_RED, master=100),
    ni3k_dark(r=120, g=0, b=60, halo=H_RED, dim=130),
    path=folder))

# Laser stab at transition into solo
scenes.append(scene("Corrupt 3C - Laser Stab",
    dark_sharpy(S_C, dim=200, colormacro=SHARPY_RED),
    dark_bsw(B_C, color=BSW_RED, dim=180),
    dark_profile(P_C, dim=150, color=PROF_RED),
    fourbar_solid(*BLOOD_RED, master=180),
    *miss_both(*DEEP_RED, master=150),
    ni3k_dark(r=180, g=0, b=30, halo=H_RED,
              rl=LASER_ON, gl=LASER_OFF, bl=LASER_OFF, dim=200),
    path=folder))

# =============================================================================
# CHAPTER 1: THE STALK (bars 28-36, ~0:56 - 1:14)
# Slow, deliberate movement. Movers creep toward positions then SNAP.
# =============================================================================

# Stalk position A — movers creeping right
scenes.append(scene("Ch1 Stalk A - Creep Right",
    dark_sharpy(S_FAR_R, dim=180, gobo=BSW_G1_3, colormacro=SHARPY_RED),
    dark_bsw(B_FAR_R, color=BSW_RED, dim=160, gobo1=BSW_G1_2),
    dark_profile(P_FAR_R, dim=140, color=PROF_RED),
    bar_chase_a(DEEP_RED, NOTHING),
    miss1(*DEEP_RED, master=60),
    miss2(*NOTHING),
    ni3k_dark(r=80, g=0, b=10, halo=H_RED, dim=100),
    path=folder))

# SNAP to center — strobe burst
scenes.append(scene("Ch1 Snap Center - Strobe",
    sharpy(pan=S_C["pan"], tilt=S_C["tilt"], strobe=SHARPY_STROBE_FAST, dim=255, colormacro=SHARPY_WHITE),
    bsw(pan=B_C["pan"], tilt=B_C["tilt"], color=BSW_WHITE,
        shutter=BSW_SHUT_STROBE_FAST, dim=255),
    profile(pan=P_C["pan"], tilt=P_C["tilt"], dim=255, color=PROF_WHITE),
    fourbar_solid(*COLD_WHITE, master=255),
    *miss_both(*COLD_WHITE, master=255),
    ni3k_dark(r=255, g=255, b=255, w=200, halo=H_RGB, dim=255),
    path=folder))

# Stalk position B — movers creeping left
scenes.append(scene("Ch1 Stalk B - Creep Left",
    dark_sharpy(S_FAR_L, dim=180, gobo=BSW_G1_3, colormacro=SHARPY_RED),
    dark_bsw(B_FAR_L, color=BSW_RED, dim=160, gobo1=BSW_G1_2),
    dark_profile(P_FAR_L, dim=140, color=PROF_RED),
    bar_chase_b(DEEP_RED, NOTHING),
    miss1(*NOTHING),
    miss2(*DEEP_RED, master=60),
    ni3k_dark(r=80, g=0, b=10, halo=H_OFF, dim=100),
    path=folder))

# SNAP to cross — color flash (red burst, no strobe)
scenes.append(scene("Ch1 Snap Cross - Red Flash",
    dark_sharpy(S_CROSS, dim=255, colormacro=SHARPY_RED),
    dark_bsw(B_CROSS, color=BSW_RED, dim=255),
    dark_profile(P_CROSS, dim=255, color=PROF_RED),
    fourbar_solid(*BLOOD_RED, master=255),
    *miss_both(*BLOOD_RED, master=255),
    ni3k_dark(r=255, g=0, b=0, halo=H_RED, dim=255),
    path=folder))

# =============================================================================
# CHAPTER 2: CROSS-ROOM SWEEPS (bars 37-52, ~1:14 - 1:48)
# Wide sweeping movements. Movers trace across the room.
# =============================================================================

scenes.append(scene("Ch2 Sweep A - Wide Left",
    dark_sharpy(S_WIDE, dim=200, prism1=128, p1r=200, colormacro=SHARPY_BLUE),
    dark_bsw(B_WIDE, color=BSW_BLUE, dim=180, prism=80, prot=160),
    dark_profile(P_WIDE, dim=160, color=PROF_BLUE),
    fourbar_gradient(VOID_BLUE[0], VOID_BLUE[1], VOID_BLUE[2],
                     VIOLET[0], VIOLET[1], VIOLET[2], master=140),
    miss1(*VOID_BLUE, master=100),
    miss2(*VIOLET, master=80),
    ni3k_dark(r=30, g=0, b=150, halo=H_BLU, dim=140),
    path=folder))

scenes.append(scene("Ch2 Sweep B - Cross Center",
    dark_sharpy(S_CROSS, dim=220, colormacro=SHARPY_PURPLE),
    dark_bsw(B_CROSS, color=BSW_MAG, dim=200, prism=80, prot=180),
    dark_profile(P_CROSS, dim=180, prism=40, color=PROF_PINK),
    fourbar_pairs(VIOLET[0], VIOLET[1], VIOLET[2],
                  VOID_BLUE[0], VOID_BLUE[1], VOID_BLUE[2], master=160),
    miss1(*VIOLET, master=100),
    miss2(*VOID_BLUE, master=100),
    ni3k_dark(r=60, g=0, b=120, halo=H_PNK, dim=160),
    path=folder))

scenes.append(scene("Ch2 Sweep C - Wide Right",
    dark_sharpy({"pan": 80, "tilt": 20}, dim=200, prism1=128, p1r=200, colormacro=SHARPY_BLUE),
    dark_bsw({"pan": 200, "tilt": 5}, color=BSW_BLUE, dim=180, prism=80, prot=200),
    dark_profile({"pan": 200, "tilt": 100}, dim=160, color=PROF_BLUE),
    fourbar_gradient(VIOLET[0], VIOLET[1], VIOLET[2],
                     VOID_BLUE[0], VOID_BLUE[1], VOID_BLUE[2], master=140),
    miss1(*VIOLET, master=80),
    miss2(*VOID_BLUE, master=100),
    ni3k_dark(r=30, g=0, b=150, halo=H_BLU, dim=140),
    path=folder))

# Snap accent mid-sweep — silent snap (no strobe, no flash, just sudden position)
scenes.append(scene("Ch2 Snap Silent - Converge",
    dark_sharpy(S_C, dim=240, prism1=128, p1r=200, colormacro=SHARPY_PURPLE),
    dark_bsw(B_C, color=BSW_MAG, dim=220, prism=128, prot=200),
    dark_profile(P_C, dim=200, prism=60, color=PROF_PINK),
    fourbar_solid(*VIOLET, master=200),
    *miss_both(*VIOLET, master=160),
    ni3k_dark(r=100, g=0, b=200, halo=H_PNK,
              rl=LASER_STROBE_FAST, gl=LASER_OFF, bl=LASER_STROBE_FAST,
              dim=200),
    path=folder))

# =============================================================================
# CHAPTER 3: ERRATIC WHIP (bars 53-63, ~1:48 - 2:11)
# Fast, unpredictable movements. Movers feel unhinged.
# =============================================================================

scenes.append(scene("Ch3 Whip A - Scatter High",
    dark_sharpy(S_HIGH, dim=220, gobo=BSW_G1_5, colormacro=SHARPY_GREEN),
    dark_bsw(B_LOW, color=BSW_GREEN, dim=200, gobo1=BSW_G1_4),
    dark_profile(P_HIGH, dim=180, color=PROF_GREEN),
    bar_sweep_lr(POISON_GREEN, 0),
    miss1(*POISON_GREEN, master=120),
    miss2(*NOTHING),
    ni3k_dark(r=0, g=120, b=30, halo=H_GRN, dim=160),
    path=folder))

scenes.append(scene("Ch3 Whip B - Scatter Low",
    dark_sharpy(S_LOW, dim=220, gobo=BSW_G1_5, colormacro=SHARPY_GREEN),
    dark_bsw(B_HIGH, color=BSW_GREEN, dim=200, gobo1=BSW_G1_4),
    dark_profile(P_LOW, dim=180, color=PROF_GREEN),
    bar_sweep_lr(POISON_GREEN, 2),
    miss1(*NOTHING),
    miss2(*POISON_GREEN, master=120),
    ni3k_dark(r=0, g=100, b=40, halo=H_OFF, dim=160),
    path=folder))

scenes.append(scene("Ch3 Whip C - Cross Snap",
    dark_sharpy(S_CROSS, dim=240, colormacro=SHARPY_TEAL),
    dark_bsw(B_CROSS, color=BSW_TEAL, dim=220),
    dark_profile(P_CROSS, dim=200, color=PROF_TEAL),
    bar_sweep_lr(DARK_CYAN, 1),
    *miss_both(*DARK_CYAN, master=140),
    ni3k_dark(r=0, g=80, b=100, halo=H_CYN, dim=180),
    path=folder))

# Strobe snap to punctuate the chaos
scenes.append(scene("Ch3 Snap - Strobe Burst",
    sharpy(pan=S_AUD["pan"], tilt=S_AUD["tilt"],
           strobe=SHARPY_STROBE_FAST, dim=255, colormacro=SHARPY_WHITE),
    bsw(pan=B_AUD["pan"], tilt=B_AUD["tilt"], color=BSW_WHITE,
        shutter=BSW_SHUT_STROBE_FAST, dim=255),
    profile(pan=P_AUD["pan"], tilt=P_AUD["tilt"], dim=255, color=PROF_WHITE),
    fourbar_solid(*COLD_WHITE, master=255),
    *miss_both(*COLD_WHITE, master=255),
    ni3k_dark(r=255, g=255, b=255, w=255, halo=H_RGB,
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON, dim=255),
    path=folder))

# =============================================================================
# BREAK: EERIE ISOLATION (bars 64-71, ~2:11 - 2:29)
# Single fixture. Slow, unsettling movement. Minimal color. Creepy.
# =============================================================================

# Only BSW active with slow creep. Everything else dead.
scenes.append(scene("Break - Isolation A",
    dark_sharpy(S_C, dim=0),
    dark_bsw({"pan": 100, "tilt": 40}, color=BSW_BLUE, dim=60,
             gobo2=BSW_G2_3, g2rot=140, frost=100),
    dark_profile(P_C, dim=0),
    fourbar_solid(*NOTHING),
    *miss_both(*NOTHING),
    ni3k_dark(r=5, g=0, b=20, halo=H_OFF,
              rl=LASER_STROBE_SLOW, gl=LASER_OFF, bl=LASER_STROBE_SLOW,
              dim=30),
    path=folder))

scenes.append(scene("Break - Isolation B",
    dark_sharpy(S_C, dim=0),
    dark_bsw({"pan": 170, "tilt": 10}, color=BSW_MAG, dim=50,
             gobo2=BSW_G2_3, g2rot=180, frost=120),
    dark_profile(P_C, dim=0),
    fourbar_solid(*NOTHING),
    miss1(*EERIE_DIM, master=20),
    miss2(*NOTHING),
    ni3k_dark(r=10, g=0, b=15, halo=H_BLU,
              rl=LASER_OFF, gl=LASER_STROBE_SLOW, bl=LASER_OFF,
              dim=20),
    path=folder))

scenes.append(scene("Break - Isolation C",
    dark_sharpy(S_C, dim=0),
    dark_bsw({"pan": 30, "tilt": 35}, color=BSW_TEAL, dim=40,
             gobo2=BSW_G2_5, g2rot=160, frost=150),
    dark_profile(P_C, dim=0),
    fourbar_solid(*NOTHING),
    miss1(*NOTHING),
    miss2(*EERIE_DIM, master=15),
    ni3k_dark(r=0, g=5, b=20, halo=H_OFF,
              rl=LASER_STROBE_SLOW, gl=LASER_STROBE_SLOW, bl=LASER_STROBE_SLOW,
              dim=15),
    path=folder))

# =============================================================================
# CHAPTER 4: LOCKSTEP ASSAULT (bars 72-86, ~2:29 - 3:01)
# All three movers hit positions in UNISON. Coordinated aggression.
# Laser stab at entry transition.
# =============================================================================

# Laser stab on transition from break
scenes.append(scene("Ch4 Entry - Laser Stab",
    dark_sharpy(S_C, dim=255, colormacro=SHARPY_RED),
    dark_bsw(B_C, color=BSW_RED, dim=255),
    dark_profile(P_C, dim=255, color=PROF_RED),
    fourbar_solid(*BLOOD_RED, master=255),
    *miss_both(*BLOOD_RED, master=200),
    ni3k_dark(r=255, g=0, b=0, w=100, halo=H_RED,
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON, dim=255),
    path=folder))

# Lockstep positions — all movers move together
scenes.append(scene("Ch4 Lock A - All Right",
    dark_sharpy(S_FAR_R, dim=220, colormacro=SHARPY_RED),
    dark_bsw(B_FAR_R, color=BSW_RED, dim=200),
    dark_profile(P_FAR_R, dim=180, color=PROF_RED),
    bar_chase_a(BLOOD_RED, DEEP_RED),
    miss1(*DEEP_RED, master=120),
    miss2(*BLOOD_RED, master=80),
    ni3k_dark(r=150, g=0, b=20, halo=H_RED, dim=180),
    path=folder))

scenes.append(scene("Ch4 Lock B - All Left",
    dark_sharpy(S_FAR_L, dim=220, colormacro=SHARPY_RED),
    dark_bsw(B_FAR_L, color=BSW_RED, dim=200),
    dark_profile(P_FAR_L, dim=180, color=PROF_RED),
    bar_chase_b(BLOOD_RED, DEEP_RED),
    miss1(*BLOOD_RED, master=80),
    miss2(*DEEP_RED, master=120),
    ni3k_dark(r=150, g=0, b=20, halo=H_OFF, dim=180),
    path=folder))

# Color flash snap — all converge center with violet
scenes.append(scene("Ch4 Lock Snap - Violet Converge",
    dark_sharpy(S_C, dim=255, colormacro=SHARPY_PURPLE),
    dark_bsw(B_C, color=BSW_MAG, dim=255),
    dark_profile(P_C, dim=255, prism=80, color=PROF_PINK),
    fourbar_solid(*VIOLET, master=255),
    *miss_both(*VIOLET, master=200),
    ni3k_dark(r=120, g=0, b=200, halo=H_PNK, dim=255),
    path=folder))

scenes.append(scene("Ch4 Lock C - All Wide",
    dark_sharpy(S_WIDE, dim=220, prism1=128, colormacro=SHARPY_RED),
    dark_bsw(B_WIDE, color=BSW_RED, dim=200, prism=80),
    dark_profile(P_WIDE, dim=180, color=PROF_RED),
    bar_chase_a(DEEP_RED, NOTHING),
    miss1(*NOTHING),
    miss2(*DEEP_RED, master=100),
    ni3k_dark(r=120, g=0, b=30, halo=H_RED, dim=160),
    path=folder))

# =============================================================================
# CHAPTER 5: RENEWED HUNT (bars 87-98, ~3:01 - 3:25)
# Return to stalking but more aggressive. Longer lunges.
# =============================================================================

scenes.append(scene("Ch5 Hunt A - Low Prowl",
    dark_sharpy(S_LOW, dim=180, gobo=BSW_G1_2, colormacro=SHARPY_TEAL),
    dark_bsw(B_LOW, color=BSW_TEAL, dim=160, gobo1=BSW_G1_3),
    dark_profile(P_LOW, dim=140, color=PROF_TEAL),
    fourbar_gradient(DARK_CYAN[0], DARK_CYAN[1], DARK_CYAN[2],
                     VOID_BLUE[0], VOID_BLUE[1], VOID_BLUE[2], master=120),
    miss1(*DARK_CYAN, master=80),
    miss2(*VOID_BLUE, master=60),
    ni3k_dark(r=0, g=60, b=80, halo=H_CYN, dim=120),
    path=folder))

scenes.append(scene("Ch5 Hunt B - High Lunge",
    dark_sharpy(S_HIGH, dim=240, colormacro=SHARPY_BLUE),
    dark_bsw(B_HIGH, color=BSW_BLUE, dim=220),
    dark_profile(P_HIGH, dim=200, color=PROF_BLUE),
    fourbar_gradient(VOID_BLUE[0], VOID_BLUE[1], VOID_BLUE[2],
                     DARK_CYAN[0], DARK_CYAN[1], DARK_CYAN[2], master=160),
    miss1(*VOID_BLUE, master=60),
    miss2(*DARK_CYAN, master=80),
    ni3k_dark(r=0, g=40, b=100, halo=H_BLU, dim=140),
    path=folder))

# Strobe snap
scenes.append(scene("Ch5 Snap - Cyan Strobe",
    sharpy(pan=S_C["pan"], tilt=S_C["tilt"],
           strobe=SHARPY_STROBE_MED, dim=255, colormacro=SHARPY_TEAL),
    bsw(pan=B_C["pan"], tilt=B_C["tilt"], color=BSW_TEAL,
        shutter=BSW_SHUT_STROBE_FAST, dim=255),
    profile(pan=P_C["pan"], tilt=P_C["tilt"], dim=255, color=PROF_TEAL),
    fourbar_solid(*DARK_CYAN, master=255),
    *miss_both(*DARK_CYAN, master=255),
    ni3k_dark(r=0, g=200, b=255, w=100, halo=H_CYN,
              rl=LASER_OFF, gl=LASER_ON, bl=LASER_ON, dim=255),
    path=folder))

# =============================================================================
# CHAPTER 6: FINAL PUSH (bars 99-106, ~3:25 - 3:41)
# Intensity builds. More prisms. Faster transitions.
# =============================================================================

scenes.append(scene("Ch6 Push A - Prism Assault Left",
    dark_sharpy(S_FAR_L, dim=240, prism1=128, p1r=200, prism2=128, p2r=200, colormacro=SHARPY_PURPLE),
    dark_bsw(B_FAR_L, color=BSW_MAG, dim=220, prism=200, prot=180),
    dark_profile(P_FAR_L, dim=200, prism=120, color=PROF_PINK),
    bar_chase_a(VIOLET, BLOOD_RED),
    miss1(*VIOLET, master=160),
    miss2(*BLOOD_RED, master=120),
    ni3k_dark(r=120, g=0, b=180, halo=H_PNK,
              t1=30, t2=90, t3=50, dim=200),
    path=folder))

scenes.append(scene("Ch6 Push B - Prism Assault Right",
    dark_sharpy(S_FAR_R, dim=240, prism1=128, p1r=200, prism2=128, p2r=200, colormacro=SHARPY_RED),
    dark_bsw(B_FAR_R, color=BSW_RED, dim=220, prism=200, prot=200),
    dark_profile(P_FAR_R, dim=200, prism=120, color=PROF_RED),
    bar_chase_b(VIOLET, BLOOD_RED),
    miss1(*BLOOD_RED, master=120),
    miss2(*VIOLET, master=160),
    ni3k_dark(r=180, g=0, b=120, halo=H_RED,
              t1=90, t2=30, t3=70, dim=200),
    path=folder))

# =============================================================================
# CHAPTER 7: UNHINGED (bars 107-116, ~3:41 - 4:02)
# Everything at once. Maximum aggression before outro pulls back.
# =============================================================================

scenes.append(scene("Ch7 Unhinged A - Full Send Left",
    dark_sharpy(S_FAR_L, dim=255, prism1=128, p1r=200, gobo=BSW_G1_5, colormacro=SHARPY_RED),
    dark_bsw(B_CROSS, color=BSW_RED, dim=255, prism=200, prot=200, gobo1=BSW_G1_4),
    dark_profile(P_WIDE, dim=240, prism=150, color=PROF_RED),
    fourbar_solid(*BLOOD_RED, master=255),
    *miss_both(*DEEP_RED, master=200),
    ni3k_dark(r=200, g=0, b=50, w=50, halo=H_RED,
              rl=LASER_ON, gl=LASER_OFF, bl=LASER_ON,
              t1=130, t2=160, t3=140, dim=255),
    path=folder))

scenes.append(scene("Ch7 Unhinged B - Full Send Right",
    dark_sharpy(S_FAR_R, dim=255, prism1=128, p1r=200, gobo=BSW_G1_5, colormacro=SHARPY_PURPLE),
    dark_bsw(B_WIDE, color=BSW_MAG, dim=255, prism=200, prot=200, gobo1=BSW_G1_4),
    dark_profile(P_CROSS, dim=240, prism=150, color=PROF_PINK),
    fourbar_solid(*VIOLET, master=255),
    *miss_both(*BRUISE_PURPLE, master=200),
    ni3k_dark(r=150, g=0, b=200, w=30, halo=H_PNK,
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
              t1=160, t2=130, t3=170, dim=255),
    path=folder))

scenes.append(scene("Ch7 Unhinged Snap - White Obliteration",
    sharpy(pan=S_C["pan"], tilt=S_C["tilt"],
           strobe=SHARPY_STROBE_FAST, dim=255, prism1=128, p1r=200, colormacro=SHARPY_WHITE),
    bsw(pan=B_C["pan"], tilt=B_C["tilt"], color=BSW_WHITE,
        shutter=BSW_SHUT_STROBE_FAST, dim=255, prism=200, prot=200),
    profile(pan=P_C["pan"], tilt=P_C["tilt"], dim=255, prism=200, color=PROF_WHITE),
    fourbar_solid(*COLD_WHITE, master=255),
    *miss_both(*COLD_WHITE, master=255),
    ni3k_dark(r=255, g=255, b=255, w=255, halo=H_RGB,
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON, dim=255),
    path=folder))

# =============================================================================
# OUTRO: ECHO OF THE CALM (bars 117-131, ~4:02 - 4:33)
# Return to the blue wash, but darker, emptier. A corrupted memory.
# =============================================================================

scenes.append(scene("Outro A - Dead Blue",
    dark_sharpy(S_C, dim=40, frost=200, colormacro=SHARPY_BLUE),
    dark_bsw(B_C, color=BSW_BLUE, dim=30, frost=200),
    dark_profile(P_C, dim=20, color=PROF_BLUE),
    fourbar_solid(*DEAD_BLUE, master=50),
    *miss_both(*DEAD_TEAL, master=30),
    ni3k_dark(r=8, g=15, b=40, halo=H_BLU, dim=40),
    path=folder))

scenes.append(scene("Outro B - Fading Memory",
    dark_sharpy({"pan": 160, "tilt": 5}, dim=25, frost=220, colormacro=SHARPY_BLUE),
    dark_bsw({"pan": 15, "tilt": 22}, color=BSW_BLUE, dim=20, frost=220),
    dark_profile({"pan": 10, "tilt": 120}, dim=15, color=PROF_BLUE),
    fourbar_solid(*DEAD_BLUE, master=30),
    *miss_both(*DEAD_TEAL, master=15),
    ni3k_dark(r=5, g=10, b=25, halo=H_OFF, dim=20),
    path=folder))

scenes.append(scene("Outro C - Almost Gone",
    dark_sharpy(S_C, dim=10, frost=255, colormacro=SHARPY_BLUE),
    dark_bsw(B_C, color=BSW_BLUE, dim=8, frost=255),
    dark_profile(P_C, dim=5, color=PROF_BLUE),
    fourbar_solid(*DEAD_BLUE, master=10),
    *miss_both(*NOTHING),
    ni3k_dark(r=2, g=5, b=12, halo=H_OFF, dim=8),
    path=folder))

# =============================================================================
# BUILD THE MAIN CHASER
# =============================================================================
# Scene IDs: 0=Blackout, 1-7=Intro, 8-13=Ch1, 14-17=Ch2, 18-21=Ch3,
#             22-24=Break, 25-30=Ch4, 31-33=Ch5, 34-35=Ch6, 36-38=Ch7,
#             39-41=Outro

print(f"Total scenes: {len(scenes)}")
for i, s in enumerate(scenes):
    print(f"  {i:2d}: {s['name']}")

# Map scene names to IDs
sid = {s["name"]: i for i, s in enumerate(scenes)}

# Build chaser steps with timing
# Format: (scene_id, (fade_ms, hold_ms))
steps = []

def add(name, bars, fade_style="smooth"):
    """Add a chaser step."""
    if fade_style == "smooth":
        t = smooth(BPM, bars)
    elif fade_style == "snap":
        t = snap(BPM, bars, fade_ms=50)
    elif fade_style == "hold":
        t = hold(BPM, bars)
    elif fade_style == "fast_snap":
        t = snap(BPM, bars, fade_ms=0)
    else:
        t = smooth(BPM, bars)
    steps.append((sid[name], t))

# --- INTRO 1: False calm (9 bars) ---
add("Calm 1A - Blue Serenity", 5, "smooth")
add("Calm 1B - Drift", 4, "smooth")

# --- INTRO 2: Corruption (9 bars) ---
add("Corrupt 2A - Teal Drains", 5, "smooth")
add("Corrupt 2B - Amber Seeps", 4, "smooth")

# --- INTRO 3: Fully corrupt (9 bars) ---
add("Corrupt 3A - Bruise", 4, "smooth")
add("Corrupt 3B - Twitch", 4, "snap")
add("Corrupt 3C - Laser Stab", 1, "fast_snap")

# --- CHAPTER 1: The Stalk (9 bars) ---
add("Ch1 Stalk A - Creep Right", 3, "smooth")
add("Ch1 Snap Center - Strobe", 0.5, "fast_snap")
add("Ch1 Stalk B - Creep Left", 3, "smooth")
add("Ch1 Snap Cross - Red Flash", 0.5, "fast_snap")
add("Ch1 Stalk A - Creep Right", 2, "smooth")

# --- CHAPTER 2: Cross-room Sweeps (16 bars) ---
add("Ch2 Sweep A - Wide Left", 4, "smooth")
add("Ch2 Sweep B - Cross Center", 3, "smooth")
add("Ch2 Snap Silent - Converge", 1, "fast_snap")
add("Ch2 Sweep C - Wide Right", 4, "smooth")
add("Ch2 Sweep B - Cross Center", 3, "smooth")
add("Ch2 Snap Silent - Converge", 1, "fast_snap")

# --- CHAPTER 3: Erratic Whip (11 bars) ---
add("Ch3 Whip A - Scatter High", 2, "snap")
add("Ch3 Whip B - Scatter Low", 2, "snap")
add("Ch3 Whip C - Cross Snap", 1.5, "fast_snap")
add("Ch3 Whip A - Scatter High", 1.5, "snap")
add("Ch3 Whip B - Scatter Low", 1.5, "snap")
add("Ch3 Snap - Strobe Burst", 0.5, "fast_snap")
add("Ch3 Whip C - Cross Snap", 2, "snap")

# --- BREAK: Eerie Isolation (8 bars) ---
add("Blackout", 0.5, "fast_snap")  # Hard cut to darkness
add("Break - Isolation A", 3, "smooth")
add("Break - Isolation B", 2.5, "smooth")
add("Break - Isolation C", 2, "smooth")

# --- CHAPTER 4: Lockstep Assault (15 bars) ---
add("Ch4 Entry - Laser Stab", 1, "fast_snap")
add("Ch4 Lock A - All Right", 2, "snap")
add("Ch4 Lock B - All Left", 2, "snap")
add("Ch4 Lock Snap - Violet Converge", 1, "fast_snap")
add("Ch4 Lock C - All Wide", 2, "snap")
add("Ch4 Lock A - All Right", 2, "snap")
add("Ch4 Lock B - All Left", 2, "snap")
add("Ch4 Lock Snap - Violet Converge", 1, "fast_snap")
add("Ch4 Lock C - All Wide", 2, "snap")

# --- CHAPTER 5: Renewed Hunt (12 bars) ---
add("Ch5 Hunt A - Low Prowl", 4, "smooth")
add("Ch5 Snap - Cyan Strobe", 0.5, "fast_snap")
add("Ch5 Hunt B - High Lunge", 4, "smooth")
add("Ch5 Snap - Cyan Strobe", 0.5, "fast_snap")
add("Ch5 Hunt A - Low Prowl", 3, "smooth")

# --- CHAPTER 6: Final Push (8 bars) ---
add("Ch6 Push A - Prism Assault Left", 2, "snap")
add("Ch6 Push B - Prism Assault Right", 2, "snap")
add("Ch6 Push A - Prism Assault Left", 2, "snap")
add("Ch6 Push B - Prism Assault Right", 2, "snap")

# --- CHAPTER 7: Unhinged (10 bars) ---
add("Ch7 Unhinged A - Full Send Left", 2, "snap")
add("Ch7 Unhinged B - Full Send Right", 2, "snap")
add("Ch7 Unhinged Snap - White Obliteration", 0.5, "fast_snap")
add("Ch7 Unhinged A - Full Send Left", 1.5, "snap")
add("Ch7 Unhinged B - Full Send Right", 1.5, "snap")
add("Ch7 Unhinged Snap - White Obliteration", 0.5, "fast_snap")
add("Ch7 Unhinged A - Full Send Left", 1, "snap")
add("Ch7 Unhinged B - Full Send Right", 1, "snap")

# --- OUTRO: Echo of the Calm (15 bars) ---
add("Outro A - Dead Blue", 6, "smooth")
add("Outro B - Fading Memory", 5, "smooth")
add("Outro C - Almost Gone", 3, "smooth")
add("Blackout", 1, "smooth")

# =============================================================================
# VERIFY TIMING
# =============================================================================

total_ms = sum(fi + ho for _, (fi, ho) in steps)
total_bars = total_ms / BAR_MS
print(f"\nTotal duration: {total_ms/1000:.1f}s ({total_bars:.1f} bars)")
print(f"Target duration: ~263s (track length)")
print(f"Steps: {len(steps)}")

# =============================================================================
# BUILD CHASER AND WRITE
# =============================================================================

scene_ids = [s for s, _ in steps]
timing = [t for _, t in steps]

main_chaser = make_chaser("Acid Rain", scene_ids, timing,
                           run_order="SingleShot", path=folder)

# Custom VC buttons
vc_buttons = [
    {"caption": "▶ ACID RAIN", "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#880000", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

write_workspace("shows/Lorn - Acid Rain (Skeler Remix).qxw", scenes, [main_chaser],
                bpm=BPM, vc_buttons=vc_buttons)
