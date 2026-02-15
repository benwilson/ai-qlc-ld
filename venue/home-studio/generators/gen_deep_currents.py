#!/usr/bin/env python3
"""
Deep Currents — 2-minute looping show at 128 BPM

Design brief:
  - Cool & deep palette: blues, teals, cyans, purples
  - Multiple energy waves (2 peaks with valleys between)
  - Leader/follower mover relationship (BSW leads, Sharpy follows)
  - NI3K: 2 dramatic reveals at surprising moments
  - Snap types: position snaps, white flash bursts, gobo/color punches
  - Static fixtures: unified wash throughout
  - Gobos/prisms: sparingly, only at peak energy

Structure (64 bars = 120s):
  Section 1: Emergence       (bars  1-8)   — Fixtures fade in one by one
  Section 2: First Swell     (bars  9-16)  — Rising energy, first snap
  Section 3: Valley          (bars 17-24)  — Pull back, profile solo
  Section 4: Second Build    (bars 25-34)  — Full chain rebuilds, NI3K REVEAL #1
  Section 5: Second Peak     (bars 35-42)  — Biggest moment, prism, gobo punch
  Section 6: Breakdown       (bars 43-52)  — Near darkness, NI3K REVEAL #2
  Section 7: Return & Loop   (bars 53-64)  — Rebuild to opening state, seamless loop
"""

import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
from showlib import *

BPM = 128

# =========================================================================
# COLOR PALETTE
# =========================================================================
DEEP_BLUE    = (0, 0, 180)
DIM_BLUE     = (0, 0, 80)
VDIM_BLUE    = (0, 0, 40)
WASH_TEAL    = (0, 180, 128)
WASH_CYAN    = (0, 220, 255)
WASH_PURPLE  = (80, 0, 180)
DIM_PURPLE   = (40, 0, 90)
BUILD_CYAN   = (0, 80, 120)

# =========================================================================
# MOVER SWEEP POSITIONS
# BSW leads, Sharpy follows one position behind
# Profile does subtle independent movement (front center fixture)
# =========================================================================

# BSW positions (back right, center pan=7)
BSW_R  = dict(pan=240, tilt=25)
BSW_CR = dict(pan=250, tilt=22)
BSW_C  = dict(pan=7,   tilt=19)
BSW_CL = dict(pan=25,  tilt=15)
BSW_L  = dict(pan=45,  tilt=10)

# Sharpy positions (back left, center pan=153)
SH_R  = dict(pan=100, tilt=5)
SH_CR = dict(pan=125, tilt=3)
SH_C  = dict(pan=153, tilt=0)
SH_CL = dict(pan=180, tilt=253)
SH_L  = dict(pan=210, tilt=250)

# Profile positions (front center, center pan=0, tilt=123)
PR_SL = dict(pan=245, tilt=125)
PR_C  = dict(pan=0,   tilt=123)
PR_SR = dict(pan=10,  tilt=121)

# =========================================================================
# DARK FIXTURE HELPERS (positioned but dark)
# Keep shutter/strobe at "open" so crossfades don't pass through strobe ranges
# =========================================================================
def dark_sharpy(colormacro=SHARPY_WHITE, **pos):
    kw = {**SH_C, **pos}
    return sharpy(dim=0, strobe=SHARPY_OPEN, colormacro=colormacro, **kw)

def dark_bsw(**pos):
    kw = {**BSW_C, **pos}
    return bsw(dim=0, shutter=BSW_SHUT_OPEN, **kw)

def dark_profile(color=PROF_WHITE, **pos):
    kw = {**PR_C, **pos}
    return profile(dim=0, color=color, **kw)

def dark_ni3k():
    return ni3k(dim=0, r=0, g=0, b=0, w=0,
                halo=H_OFF, rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF)

def dark_4bar():
    return fourbar_solid(0, 0, 0)

def dark_miss():
    return miss_both(0, 0, 0)

# =========================================================================
# SCENES
# =========================================================================
PATH = "Deep Currents"
scenes = []

# -------------------------------------------------------------------
# Section 1: EMERGENCE (bars 1-8)
# Fixtures fade in one by one. BSW and Sharpy enter sweeping from right.
# -------------------------------------------------------------------

# S0: Single missyee, dim blue. Movers pre-positioned but dark.
scenes.append(scene("Emergence - Darkness",
    dark_bsw(**BSW_R),
    dark_4bar(),
    dark_ni3k(),
    dark_profile(**PR_SL),
    miss1(0, 0, 80),
    miss2(0, 0, 0),
    dark_sharpy(**SH_R),
    path=PATH))

# S1: Both missyees + 4BAR inner pars
scenes.append(scene("Emergence - First Light",
    dark_bsw(**BSW_R),
    fourbar(0,0,0, 0,0,80, 0,0,80, 0,0,0),
    dark_ni3k(),
    dark_profile(**PR_SL),
    miss1(0, 0, 120),
    miss2(0, 0, 80),
    dark_sharpy(**SH_R),
    path=PATH))

# S2: Full wash blue, BSW enters from right
scenes.append(scene("Emergence - BSW Enters",
    bsw(**BSW_R, color=BSW_BLUE, dim=180),
    fourbar_solid(0, 0, 120),
    dark_ni3k(),
    dark_profile(**PR_SL),
    *miss_both(0, 0, 150),
    dark_sharpy(**SH_R),
    path=PATH))

# S3: BSW sweeping center-right, Sharpy entering (following)
scenes.append(scene("Emergence - Sharpy Follows",
    bsw(**BSW_CR, color=BSW_BLUE, dim=220),
    fourbar_solid(0, 0, 150),
    dark_ni3k(),
    dark_profile(**PR_SL),
    *miss_both(0, 0, 180),
    sharpy(**SH_R, dim=120, colormacro=SHARPY_BLUE),
    path=PATH))

# -------------------------------------------------------------------
# Section 2: FIRST SWELL (bars 9-16)
# Rising energy. Wash shifts blue→teal. Position snap at bar 13.
# -------------------------------------------------------------------

# S4: Wash shifts to teal, BSW→center, Sharpy→center-right
scenes.append(scene("Swell 1 - Rising Teal",
    bsw(**BSW_C, color=BSW_TEAL, dim=255),
    fourbar_solid(*WASH_TEAL),
    dark_ni3k(),
    dark_profile(**PR_C),
    *miss_both(*WASH_TEAL),
    sharpy(**SH_CR, dim=200, colormacro=SHARPY_TEAL),
    path=PATH))

# S5: Building, BSW→center-left, Sharpy→center
scenes.append(scene("Swell 1 - Building",
    bsw(**BSW_CL, color=BSW_TEAL, dim=255),
    fourbar_solid(*WASH_TEAL),
    dark_ni3k(),
    dark_profile(**PR_C),
    *miss_both(*WASH_TEAL),
    sharpy(**SH_C, dim=255, colormacro=SHARPY_TEAL),
    path=PATH))

# S6: POSITION SNAP — movers jump to opposite side, cyan flash on wash
scenes.append(scene("Swell 1 - POSITION SNAP",
    bsw(**BSW_R, color=BSW_TEAL, dim=255),
    fourbar_solid(*WASH_CYAN),
    dark_ni3k(),
    profile(**PR_SR, dim=180, color=PROF_TEAL),
    *miss_both(*WASH_CYAN),
    sharpy(**SH_L, dim=255, colormacro=SHARPY_TEAL),
    path=PATH))

# S7: Post-snap flow, movers resume slow sweep from new positions
scenes.append(scene("Swell 1 - Post-Snap Flow",
    bsw(**BSW_CL, color=BSW_TEAL, dim=240),
    fourbar_solid(*WASH_TEAL),
    dark_ni3k(),
    profile(**PR_C, dim=120, color=PROF_TEAL),
    *miss_both(*WASH_TEAL),
    sharpy(**SH_CL, dim=240, colormacro=SHARPY_TEAL),
    path=PATH))

# -------------------------------------------------------------------
# Section 3: VALLEY (bars 17-24)
# Energy drops. Fixtures peel away. Profile enters for the first time.
# -------------------------------------------------------------------

# S8: Wash dims to purple, Sharpy fading
scenes.append(scene("Valley - Retreat",
    bsw(**BSW_C, color=BSW_MAG, dim=180),
    fourbar_solid(*WASH_PURPLE, master=180),
    dark_ni3k(),
    profile(**PR_C, dim=80, color=PROF_PINK),
    *miss_both(*WASH_PURPLE, master=120),
    sharpy(**SH_C, dim=60, colormacro=SHARPY_PURPLE),
    path=PATH))

# S9: BSW alone + dim pars purple
scenes.append(scene("Valley - Solitude",
    bsw(**BSW_CL, color=BSW_MAG, dim=140),
    fourbar_solid(*DIM_PURPLE, master=100),
    dark_ni3k(),
    dark_profile(**PR_SL),
    *miss_both(*DIM_PURPLE, master=80),
    dark_sharpy(**SH_C),
    path=PATH))

# S10: Profile appears as BSW fades, just one missyee
scenes.append(scene("Valley - Profile Appears",
    dark_bsw(**BSW_CL),
    fourbar_solid(*DIM_BLUE, master=60),
    dark_ni3k(),
    profile(**PR_SL, dim=120, color=PROF_BLUE),
    miss1(0, 0, 60),
    miss2(0, 0, 0),
    dark_sharpy(colormacro=SHARPY_BLUE, **SH_CL),
    path=PATH))

# S11: Near darkness — just Profile thin beam + one dim missyee
scenes.append(scene("Valley - Deep Stillness",
    dark_bsw(**BSW_C),
    dark_4bar(),
    dark_ni3k(),
    profile(**PR_C, dim=80, color=PROF_BLUE),
    miss1(0, 0, 40),
    miss2(0, 0, 0),
    dark_sharpy(colormacro=SHARPY_BLUE, **SH_CL),
    path=PATH))

# -------------------------------------------------------------------
# Section 4: SECOND BUILD (bars 25-34)
# Fixtures rejoin in leader/follower chain.
# NI3K REVEAL #1 at bars 31-32 — atmospheric surprise during the build,
# NOT at the peak. Creates eerie tension.
# -------------------------------------------------------------------

# S12: Pars come back cyan, Profile sweeping
scenes.append(scene("Build 2 - Resurface",
    dark_bsw(**BSW_CR),
    fourbar_solid(*BUILD_CYAN, master=120),
    dark_ni3k(),
    profile(**PR_SR, dim=160, color=PROF_TEAL),
    *miss_both(*BUILD_CYAN, master=100),
    dark_sharpy(colormacro=SHARPY_TEAL, **SH_CR),
    path=PATH))

# S13: BSW follows Profile, wash building
scenes.append(scene("Build 2 - Chains Form",
    bsw(**BSW_CR, color=BSW_TEAL, dim=160),
    fourbar_solid(0, 120, 180, master=160),
    dark_ni3k(),
    profile(**PR_C, dim=200, color=PROF_TEAL),
    *miss_both(0, 120, 180, master=140),
    dark_sharpy(colormacro=SHARPY_TEAL, **SH_R),
    path=PATH))

# S14: All 3 movers in leader/follower chain
scenes.append(scene("Build 2 - Full Chain",
    bsw(**BSW_C, color=BSW_TEAL, dim=200),
    fourbar_solid(*WASH_TEAL, master=200),
    dark_ni3k(),
    profile(**PR_SL, dim=220, color=PROF_TEAL),
    *miss_both(*WASH_TEAL, master=180),
    sharpy(**SH_CR, dim=160, colormacro=SHARPY_TEAL),
    path=PATH))

# S15: *** NI3K REVEAL #1 ***
# NI3K fades in with blue/purple glow and cyan halo. No lasers.
# Other fixtures continue their sweep — this is atmospheric, not explosive.
scenes.append(scene("Build 2 - NI3K Emerges",
    bsw(**BSW_CL, color=BSW_BLUE, dim=220),
    fourbar_solid(*DEEP_BLUE, master=200),
    ni3k(r=0, g=0, b=180, w=0, dim=160, halo=H_CYN),
    profile(**PR_C, dim=220, color=PROF_BLUE),
    *miss_both(*DEEP_BLUE, master=180),
    sharpy(**SH_C, dim=200, colormacro=SHARPY_BLUE),
    path=PATH))

# S16: NI3K presence intensifies, all movers building
scenes.append(scene("Build 2 - Tension Peaks",
    bsw(**BSW_L, color=BSW_TEAL, dim=255),
    fourbar_solid(*WASH_TEAL, master=240),
    ni3k(r=0, g=40, b=255, w=0, dim=200, halo=H_BLU),
    profile(**PR_SR, dim=255, color=PROF_TEAL),
    *miss_both(*WASH_TEAL, master=220),
    sharpy(**SH_CL, dim=255, colormacro=SHARPY_TEAL),
    path=PATH))

# -------------------------------------------------------------------
# Section 5: SECOND PEAK (bars 35-42)
# Biggest moment. White flash, prism fracture, gobo punch.
# NI3K still present but diminishing — this section is about the movers.
# -------------------------------------------------------------------

# S17: Full bloom — everything bright cyan
scenes.append(scene("Peak - Full Bloom",
    bsw(**BSW_C, color=BSW_TEAL, dim=255),
    fourbar_solid(*WASH_CYAN),
    ni3k(r=0, g=100, b=255, w=80, dim=255, halo=H_CYN),
    profile(**PR_C, dim=255, color=PROF_TEAL),
    *miss_both(*WASH_CYAN),
    sharpy(**SH_C, dim=255, colormacro=SHARPY_TEAL),
    path=PATH))

# S18: WHITE FLASH — all fixtures blast white via color, not strobe channels
# Avoids strobe crossfade artifacts. The snap timing creates the burst feel.
scenes.append(scene("Peak - WHITE FLASH",
    bsw(**BSW_C, color=BSW_WHITE, dim=255),
    fourbar_solid(255, 255, 255),
    ni3k(r=255, g=255, b=255, w=255, dim=255, halo=H_RGB),
    profile(**PR_C, dim=255),
    *miss_both(255, 255, 255),
    sharpy(**SH_C, dim=255),
    path=PATH))

# S19: Prism fracture — BSW prism on, movers crossing
scenes.append(scene("Peak - Prism Fracture",
    bsw(**BSW_L, color=BSW_TEAL, dim=255, prism=128, prot=180),
    fourbar_solid(*WASH_CYAN),
    ni3k(r=0, g=80, b=255, w=0, dim=200, halo=H_CYN),
    profile(**PR_SL, dim=255, color=PROF_TEAL),
    *miss_both(*WASH_CYAN),
    sharpy(**SH_L, dim=255, colormacro=SHARPY_TEAL),
    path=PATH))

# S20: GOBO PUNCH — gobo + purple shift, movers jump positions
scenes.append(scene("Peak - GOBO PUNCH",
    bsw(**BSW_R, color=BSW_MAG, dim=255, gobo1=BSW_G1_3, prism=128, prot=200),
    fourbar_solid(*WASH_PURPLE),
    ni3k(r=80, g=0, b=180, w=0, dim=200, halo=H_PNK),
    profile(**PR_SR, dim=255, gobo=20, color=PROF_PINK),
    *miss_both(*WASH_PURPLE),
    sharpy(**SH_R, dim=255, gobo=40, colormacro=SHARPY_PURPLE),
    path=PATH))

# S21: Riding out — back to flowing teal, prism/gobo off
scenes.append(scene("Peak - Riding Out",
    bsw(**BSW_CL, color=BSW_TEAL, dim=240),
    fourbar_solid(*WASH_TEAL, master=240),
    ni3k(r=0, g=40, b=200, w=0, dim=140, halo=H_BLU),
    profile(**PR_C, dim=240, color=PROF_TEAL),
    *miss_both(*WASH_TEAL, master=220),
    sharpy(**SH_CL, dim=240, colormacro=SHARPY_TEAL),
    path=PATH))

# -------------------------------------------------------------------
# Section 6: BREAKDOWN (bars 43-52)
# Energy drains. Near darkness.
# NI3K REVEAL #2 at bars 51-52 — total silence shattered by lasers.
# -------------------------------------------------------------------

# S22: Pulling back — NI3K fading, movers slowing
scenes.append(scene("Breakdown - Pulling Back",
    bsw(**BSW_C, color=BSW_BLUE, dim=180),
    fourbar_solid(*DEEP_BLUE, master=180),
    ni3k(r=0, g=0, b=80, w=0, dim=60, halo=H_OFF),
    profile(**PR_C, dim=160, color=PROF_BLUE),
    *miss_both(*DEEP_BLUE, master=150),
    sharpy(**SH_C, dim=140, colormacro=SHARPY_BLUE),
    path=PATH))

# S23: Sparse — just BSW + pars deep blue
scenes.append(scene("Breakdown - Sparse",
    bsw(**BSW_CL, color=BSW_BLUE, dim=120),
    fourbar_solid(*DIM_BLUE, master=100),
    dark_ni3k(),
    dark_profile(**PR_C),
    *miss_both(*DIM_BLUE, master=80),
    dark_sharpy(**SH_C),
    path=PATH))

# S24: Near dark — one dim missyee
scenes.append(scene("Breakdown - Near Dark",
    dark_bsw(**BSW_C),
    dark_4bar(),
    dark_ni3k(),
    dark_profile(**PR_C),
    miss1(0, 0, 40),
    miss2(0, 0, 0),
    dark_sharpy(**SH_C),
    path=PATH))

# S25: Silence — single 4BAR par, dim purple
scenes.append(scene("Breakdown - Silence",
    dark_bsw(**BSW_C),
    fourbar(0,0,0, 0,0,0, 40,0,60, 0,0,0),
    dark_ni3k(),
    dark_profile(**PR_C),
    miss1(0, 0, 0),
    miss2(0, 0, 0),
    dark_sharpy(**SH_C),
    path=PATH))

# S26: *** NI3K REVEAL #2 ***
# Everything dark. NI3K takes over completely.
# All lasers ON, halo RGB cycling, bright blue-white RGBW.
# Tilts spread for maximum room coverage.
scenes.append(scene("NI3K TAKEOVER",
    dark_bsw(**BSW_C),
    dark_4bar(),
    ni3k(r=100, g=100, b=255, w=200, dim=255, halo=H_RGB,
         rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
         t1=80, t2=40, t3=100),
    dark_profile(**PR_C),
    miss1(0, 0, 0),
    miss2(0, 0, 0),
    dark_sharpy(**SH_C),
    path=PATH))

# -------------------------------------------------------------------
# Section 7: RETURN & LOOP (bars 53-64)
# Rebuild from blackout back to opening state for seamless loop.
# -------------------------------------------------------------------

# S27: Blackout breath — total darkness after NI3K cuts
scenes.append(scene("Return - Blackout Breath",
    *blackout_all(),
    path=PATH))

# S28: Pars fade back in blue
scenes.append(scene("Return - First Light Again",
    dark_bsw(**BSW_R),
    fourbar_solid(*DIM_BLUE, master=80),
    dark_ni3k(),
    dark_profile(**PR_SL),
    *miss_both(*DIM_BLUE, master=60),
    dark_sharpy(**SH_R),
    path=PATH))

# S29: BSW returns, slow sweep from right
scenes.append(scene("Return - BSW Returns",
    bsw(**BSW_R, color=BSW_BLUE, dim=140),
    fourbar_solid(*DEEP_BLUE, master=140),
    dark_ni3k(),
    dark_profile(**PR_SL),
    *miss_both(*DEEP_BLUE, master=120),
    dark_sharpy(**SH_R),
    path=PATH))

# S30: All movers rejoin, leader/follower rebuilding
scenes.append(scene("Return - Movers Rejoin",
    bsw(**BSW_CR, color=BSW_BLUE, dim=200),
    fourbar_solid(*DEEP_BLUE, master=180),
    dark_ni3k(),
    profile(**PR_C, dim=120, color=PROF_BLUE),
    *miss_both(*DEEP_BLUE, master=160),
    sharpy(**SH_R, dim=120, colormacro=SHARPY_BLUE),
    path=PATH))

# S31: Settling — dimming, movers centering
scenes.append(scene("Return - Settling",
    bsw(**BSW_C, color=BSW_BLUE, dim=120),
    fourbar_solid(*DIM_BLUE, master=100),
    dark_ni3k(),
    profile(**PR_C, dim=60, color=PROF_BLUE),
    *miss_both(*DIM_BLUE, master=80),
    sharpy(**SH_CR, dim=60, colormacro=SHARPY_BLUE),
    path=PATH))

# S32: Loop point — matches S0 for seamless loop back
scenes.append(scene("Loop Point",
    dark_bsw(**BSW_R),
    dark_4bar(),
    dark_ni3k(),
    dark_profile(**PR_SL),
    miss1(0, 0, 80),
    miss2(0, 0, 0),
    dark_sharpy(**SH_R),
    path=PATH))

# S33: Blackout (for VC button only, not in chaser)
scenes.append(scene("Blackout",
    *blackout_all(),
    path=PATH))

# =========================================================================
# CHASER TIMING
# Each step: scene index + (FadeIn_ms, Hold_ms)
# FadeIn = crossfade time INTO this step
# Hold = dwell time at this step before next crossfade begins
# Total must equal 64 bars = 120,000ms
# =========================================================================
steps = []
timings = []

def add(scene_idx, fade_ms, hold_ms):
    steps.append(scene_idx)
    timings.append((fade_ms, hold_ms))

# Section 1: EMERGENCE (8 bars)
add(0,  *smooth(BPM, 2))      # bars 1-2:   darkness → dim missyee
add(1,  *smooth(BPM, 2))      # bars 3-4:   both missyees, 4BAR inner
add(2,  *smooth(BPM, 2))      # bars 5-6:   full wash blue, BSW enters
add(3,  *smooth(BPM, 2))      # bars 7-8:   Sharpy follows BSW

# Section 2: FIRST SWELL (8 bars)
add(4,  *smooth(BPM, 2))      # bars 9-10:  wash→teal, movers sweeping
add(5,  *smooth(BPM, 1.5))    # bars 11-12.5: building
add(6,  *snap(BPM, 0.5))      # bar 12.5-13: *** POSITION SNAP ***
add(7,  *smooth(BPM, 4))      # bars 13-16: post-snap flow

# Section 3: VALLEY (8 bars)
add(8,  *smooth(BPM, 2))      # bars 17-18: retreat to purple
add(9,  *smooth(BPM, 2))      # bars 19-20: BSW alone
add(10, *smooth(BPM, 2))      # bars 21-22: Profile appears
add(11, *smooth(BPM, 2))      # bars 23-24: deep stillness

# Section 4: SECOND BUILD (10 bars)
add(12, *smooth(BPM, 2))      # bars 25-26: resurface
add(13, *smooth(BPM, 2))      # bars 27-28: chains form
add(14, *smooth(BPM, 2))      # bars 29-30: full chain
add(15, *smooth(BPM, 2))      # bars 31-32: *** NI3K REVEAL #1 ***
add(16, *smooth(BPM, 2))      # bars 33-34: tension peaks

# Section 5: SECOND PEAK (8 bars)
add(17, *smooth(BPM, 1.5))    # bars 35-36.5: full bloom
add(18, *snap(BPM, 0.5))      # bar 36.5-37:  *** WHITE FLASH ***
add(19, *smooth(BPM, 2))      # bars 37-39:   prism fracture
add(20, *snap(BPM, 1))        # bar 39-40:    *** GOBO PUNCH ***
add(21, *smooth(BPM, 3))      # bars 40-42:   riding out

# Section 6: BREAKDOWN (10 bars)
add(22, *smooth(BPM, 2))      # bars 43-44: pulling back
add(23, *smooth(BPM, 2))      # bars 45-46: sparse
add(24, *smooth(BPM, 2))      # bars 47-48: near dark
add(25, *smooth(BPM, 2))      # bars 49-50: silence
add(26, *snap(BPM, 2))        # bars 51-52: *** NI3K TAKEOVER ***

# Section 7: RETURN & LOOP (12 bars)
add(27, *hold(BPM, 1))        # bar 53:     blackout breath
add(28, *smooth(BPM, 2))      # bars 54-55: pars fade back in
add(29, *smooth(BPM, 2))      # bars 56-57: BSW returns
add(30, *smooth(BPM, 3))      # bars 58-60: movers rejoin
add(31, *smooth(BPM, 2))      # bars 61-62: settling
add(32, *smooth(BPM, 2))      # bars 63-64: loop point → S0

# =========================================================================
# VERIFY TIMING
# =========================================================================
total_ms = sum(f + h for f, h in timings)
total_bars = total_ms / bpm_to_ms(BPM, 4)
print(f"Timing: {total_ms}ms = {total_bars:.1f} bars = {total_ms/1000:.1f}s")
assert abs(total_bars - 64) < 0.5, f"Expected 64 bars, got {total_bars:.1f}"
print(f"Scenes: {len(scenes)}, Chaser steps: {len(steps)}")

# =========================================================================
# BUILD & WRITE
# =========================================================================
chaser = make_chaser("Deep Currents", steps, timings,
                     run_order="Loop", path=PATH)

write_workspace(os.path.join(VENUE_DIR, "shows", "Deep-Currents.qxw"),
                scenes, [chaser], bpm=BPM)
