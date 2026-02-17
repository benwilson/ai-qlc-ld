#!/usr/bin/env python3
"""
Fixture Test Generator — Home Studio
Balanced test: verifies each fixture works, tests key features, organized by fixture.
Run from project root: python3 "venue/home-studio/generators/Fixture-Test.py"
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from showlib import *

BPM = 120  # Slow enough to visually verify each scene

scenes = []
vc_buttons = []
vc_id = 0
next_y = 10  # VC layout Y position tracker

# Column layout for VC
COL1_X = 10    # Left column (fixture buttons)
COL2_X = 250   # Right column (combo/utility buttons)
BTN_W = 230
BTN_H = 50

# VC color palette (ARGB hex strings for QLC+)
VC_RED     = "#FF4444"
VC_GREEN   = "#22AA22"
VC_BLUE    = "#4444FF"
VC_PURPLE  = "#8844CC"
VC_ORANGE  = "#FF8800"
VC_CYAN    = "#00AAAA"
VC_YELLOW  = "#CCAA00"
VC_PINK    = "#CC4488"
VC_BLACK   = "#FF0000"  # Blackout button = red

def add_scene(name, *fixtures, path="Tests"):
    """Add a scene and return its ID."""
    scenes.append(scene(name, *fixtures, path=path))
    return len(scenes) - 1

def add_button(caption, func_id, color, col=1):
    """Add a VC button."""
    global vc_id
    x = COL1_X if col == 1 else COL2_X
    vc_buttons.append({
        "caption": caption, "vc_id": vc_id, "func_id": func_id,
        "x": x, "y": next_y, "w": BTN_W, "h": BTN_H,
        "color": color, "action": "Toggle",
    })
    vc_id += 1

def next_row():
    """Advance to next row in VC layout."""
    global next_y
    next_y += BTN_H + 5

# =============================================================================
# BLACKOUT (always first)
# =============================================================================

sid = add_scene("BLACKOUT", *blackout_all(), path="Utility")
add_button("BLACKOUT", sid, VC_BLACK, col=1)
# Also add in col2
vc_buttons.append({
    "caption": "BLACKOUT", "vc_id": vc_id, "func_id": sid,
    "x": COL2_X, "y": next_y, "w": BTN_W, "h": BTN_H,
    "color": VC_BLACK, "action": "Toggle",
})
vc_id += 1
next_row()

# =============================================================================
# 4BAR (ID 2) — RGB pars, simple
# =============================================================================

next_y += 10  # Section gap
# All white
sid = add_scene("4BAR: All White",
    fourbar_solid(255, 255, 255),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_NI3K, CH_NI3K),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/4BAR")
add_button("4BAR: White", sid, VC_GREEN, col=1)
next_row()

# Individual pars (P1=R, P2=G, P3=B, P4=White)
sid = add_scene("4BAR: RGBW Split",
    fourbar(255,0,0, 0,255,0, 0,0,255, 255,255,255),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_NI3K, CH_NI3K),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/4BAR")
add_button("4BAR: RGBW", sid, VC_GREEN, col=1)
next_row()

# Strobe test
sid = add_scene("4BAR: Strobe",
    fourbar_solid(255, 255, 255, strobe=128),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_NI3K, CH_NI3K),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/4BAR")
add_button("4BAR: Strobe", sid, VC_GREEN, col=1)
next_row()

# =============================================================================
# MISSYEE PARS (ID 5 + 6) — RGB LED wash
# =============================================================================

next_y += 10
sid = add_scene("Miss: Both White",
    miss_both(255, 255, 255),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_NI3K, CH_NI3K),
    blackout(FX_4BAR, CH_4BAR),
    path="Tests/Missyee")
add_button("Miss: White", sid, VC_CYAN, col=1)
next_row()

sid = add_scene("Miss: Split RB",
    miss1(255, 0, 0),
    miss2(0, 0, 255),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_NI3K, CH_NI3K),
    blackout(FX_4BAR, CH_4BAR),
    path="Tests/Missyee")
add_button("Miss: R/B Split", sid, VC_CYAN, col=1)
next_row()

# =============================================================================
# SHARPY (ID 8) — 18ch mover
# =============================================================================

next_y += 10
# Center white open
sid = add_scene("Sharpy: Center White",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_WHITE, strobe=SHARPY_OPEN, dim=255),
    blackout(FX_BSW, CH_BSW), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Sharpy")
add_button("Sharpy: Center", sid, VC_BLUE, col=1)
next_row()

# Color cycle positions
sid = add_scene("Sharpy: Red",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED),
    blackout(FX_BSW, CH_BSW), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Sharpy")
add_button("Sharpy: Red", sid, VC_BLUE, col=1)
next_row()

sid = add_scene("Sharpy: Blue",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_BLUE),
    blackout(FX_BSW, CH_BSW), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Sharpy")
add_button("Sharpy: Blue", sid, VC_BLUE, col=1)
next_row()

# Movement test — sweep left to right
sid = add_scene("Sharpy: Pan Left",
    sharpy(pan=90, tilt=0, colormacro=SHARPY_WHITE),
    blackout(FX_BSW, CH_BSW), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Sharpy")
add_button("Sharpy: Pan L", sid, VC_BLUE, col=1)
next_row()

sid = add_scene("Sharpy: Pan Right",
    sharpy(pan=220, tilt=0, colormacro=SHARPY_WHITE),
    blackout(FX_BSW, CH_BSW), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Sharpy")
add_button("Sharpy: Pan R", sid, VC_BLUE, col=1)
next_row()

# Prism test
sid = add_scene("Sharpy: Prism 1",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_BLUE, prism1=128, p1r=200),
    blackout(FX_BSW, CH_BSW), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Sharpy")
add_button("Sharpy: Prism", sid, VC_BLUE, col=1)
next_row()

# Strobe test
sid = add_scene("Sharpy: Strobe",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_WHITE, strobe=SHARPY_STROBE_MED),
    blackout(FX_BSW, CH_BSW), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Sharpy")
add_button("Sharpy: Strobe", sid, VC_BLUE, col=1)
next_row()

# Frost test
sid = add_scene("Sharpy: Frost",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_WHITE, frost=200),
    blackout(FX_BSW, CH_BSW), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Sharpy")
add_button("Sharpy: Frost", sid, VC_BLUE, col=1)
next_row()

# =============================================================================
# BSW (ID 1) — 20ch mover
# =============================================================================

next_y += 10
sid = add_scene("BSW: Center White",
    bsw(pan=177, tilt=19, color=BSW_WHITE, shutter=BSW_SHUT_OPEN, dim=255),
    blackout(FX_SHARPY, CH_SHARPY), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/BSW")
add_button("BSW: Center", sid, VC_PURPLE, col=1)
next_row()

sid = add_scene("BSW: Red",
    bsw(pan=177, tilt=19, color=BSW_RED),
    blackout(FX_SHARPY, CH_SHARPY), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/BSW")
add_button("BSW: Red", sid, VC_PURPLE, col=1)
next_row()

sid = add_scene("BSW: Blue",
    bsw(pan=177, tilt=19, color=BSW_BLUE),
    blackout(FX_SHARPY, CH_SHARPY), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/BSW")
add_button("BSW: Blue", sid, VC_PURPLE, col=1)
next_row()

# Pan test
sid = add_scene("BSW: Pan Left",
    bsw(pan=189, tilt=29, color=BSW_WHITE),
    blackout(FX_SHARPY, CH_SHARPY), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/BSW")
add_button("BSW: Pan L", sid, VC_PURPLE, col=1)
next_row()

sid = add_scene("BSW: Pan Right",
    bsw(pan=170, tilt=23, color=BSW_WHITE),
    blackout(FX_SHARPY, CH_SHARPY), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/BSW")
add_button("BSW: Pan R", sid, VC_PURPLE, col=1)
next_row()

# Gobo 1 test
sid = add_scene("BSW: Gobo 1-3",
    bsw(pan=177, tilt=19, color=BSW_WHITE, gobo1=BSW_G1_3),
    blackout(FX_SHARPY, CH_SHARPY), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/BSW")
add_button("BSW: Gobo", sid, VC_PURPLE, col=1)
next_row()

# Prism test
sid = add_scene("BSW: Prism",
    bsw(pan=177, tilt=19, color=BSW_BLUE, prism=128, prot=160),
    blackout(FX_SHARPY, CH_SHARPY), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/BSW")
add_button("BSW: Prism", sid, VC_PURPLE, col=1)
next_row()

# Strobe test
sid = add_scene("BSW: Strobe",
    bsw(pan=177, tilt=19, color=BSW_WHITE, shutter=BSW_SHUT_STROBE_SLOW),
    blackout(FX_SHARPY, CH_SHARPY), blackout(FX_PROFILE, CH_PROFILE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/BSW")
add_button("BSW: Strobe", sid, VC_PURPLE, col=1)
next_row()

# =============================================================================
# PROFILE (ID 4) — 14ch mover
# =============================================================================

next_y += 10
sid = add_scene("Profile: Center White",
    profile(pan=0, tilt=123, color=PROF_WHITE, strobe=PROFILE_STROBE_OFF, dim=255),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Profile")
add_button("Prof: Center", sid, VC_ORANGE, col=1)
next_row()

sid = add_scene("Profile: Red",
    profile(pan=0, tilt=123, color=PROF_RED),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Profile")
add_button("Prof: Red", sid, VC_ORANGE, col=1)
next_row()

sid = add_scene("Profile: Blue",
    profile(pan=0, tilt=123, color=PROF_BLUE),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Profile")
add_button("Prof: Blue", sid, VC_ORANGE, col=1)
next_row()

# Pan test
sid = add_scene("Profile: Pan Left",
    profile(pan=30, tilt=123, color=PROF_WHITE),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Profile")
add_button("Prof: Pan L", sid, VC_ORANGE, col=1)
next_row()

sid = add_scene("Profile: Pan Right",
    profile(pan=230, tilt=123, color=PROF_WHITE),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Profile")
add_button("Prof: Pan R", sid, VC_ORANGE, col=1)
next_row()

# Prism test
sid = add_scene("Profile: Prism",
    profile(pan=0, tilt=123, color=PROF_BLUE, prism=128),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Profile")
add_button("Prof: Prism", sid, VC_ORANGE, col=1)
next_row()

# =============================================================================
# NI3K (ID 3) — 19ch multi-head + lasers
# =============================================================================

next_y += 10
# RGBW LEDs on
sid = add_scene("NI3K: White LEDs",
    ni3k(pan=128, t1=64, t2=64, t3=64, r=255, g=255, b=255, w=255, dim=255, strobe=0),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/NI3K")
add_button("NI3K: White", sid, VC_PINK, col=1)
next_row()

# RGB test
sid = add_scene("NI3K: Red LEDs",
    ni3k(r=255, g=0, b=0, w=0, dim=255),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/NI3K")
add_button("NI3K: Red", sid, VC_PINK, col=1)
next_row()

# Halo test
sid = add_scene("NI3K: Halo RGB",
    ni3k(r=0, g=0, b=0, w=0, dim=255, halo=H_RGB),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/NI3K")
add_button("NI3K: Halo", sid, VC_PINK, col=1)
next_row()

# Tilt rotation test
sid = add_scene("NI3K: Tilt Rotation",
    ni3k(r=0, g=0, b=255, w=0, dim=255, t1=160, t2=180, t3=200),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/NI3K")
add_button("NI3K: Tilt Rot", sid, VC_PINK, col=1)
next_row()

# Red laser only
sid = add_scene("NI3K: Red Laser",
    ni3k(r=0, g=0, b=0, w=0, dim=0, rl=LASER_ON, gl=LASER_OFF, bl=LASER_OFF),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/NI3K")
add_button("NI3K: Red Laser", sid, VC_PINK, col=1)
next_row()

# Green laser only
sid = add_scene("NI3K: Green Laser",
    ni3k(r=0, g=0, b=0, w=0, dim=0, gl=LASER_ON),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/NI3K")
add_button("NI3K: Grn Laser", sid, VC_PINK, col=1)
next_row()

# Blue laser only
sid = add_scene("NI3K: Blue Laser",
    ni3k(r=0, g=0, b=0, w=0, dim=0, bl=LASER_ON),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/NI3K")
add_button("NI3K: Blu Laser", sid, VC_PINK, col=1)
next_row()

# All lasers
sid = add_scene("NI3K: All Lasers",
    ni3k(r=0, g=0, b=0, w=0, dim=0, rl=LASER_ON, gl=LASER_ON, bl=LASER_ON),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/NI3K")
add_button("NI3K: All Laser", sid, VC_PINK, col=1)
next_row()

# Motor effect test
sid = add_scene("NI3K: Motor FX",
    ni3k(r=255, g=0, b=255, w=0, dim=255, moteff=128, effspd=128),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/NI3K")
add_button("NI3K: Motor FX", sid, VC_PINK, col=1)
next_row()

# =============================================================================
# COMBO SCENES (right column) — multiple fixtures together
# =============================================================================

# Reset right column Y position
combo_y = 10 + BTN_H + 5 + 10  # After blackout + gap
next_y_saved = next_y
next_y = combo_y

# All movers center white
sid = add_scene("All Movers: Center White",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_WHITE),
    bsw(pan=177, tilt=19, color=BSW_WHITE),
    profile(pan=0, tilt=123, color=PROF_WHITE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Combo")
add_button("Movers: Center", sid, VC_YELLOW, col=2)
next_row()

# All movers spread
sid = add_scene("All Movers: Spread",
    sharpy(pan=220, tilt=15, colormacro=SHARPY_BLUE),
    bsw(pan=189, tilt=29, color=BSW_BLUE),
    profile(pan=30, tilt=100, color=PROF_BLUE),
    blackout(FX_NI3K, CH_NI3K), blackout(FX_4BAR, CH_4BAR),
    blackout(FX_MISS1, CH_MISS), blackout(FX_MISS2, CH_MISS),
    path="Tests/Combo")
add_button("Movers: Spread", sid, VC_YELLOW, col=2)
next_row()

# All pars warm
sid = add_scene("All Pars: Warm",
    fourbar_solid(255, 128, 0),
    miss_both(255, 128, 0),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_NI3K, CH_NI3K),
    path="Tests/Combo")
add_button("Pars: Warm", sid, VC_YELLOW, col=2)
next_row()

# All pars cool
sid = add_scene("All Pars: Cool",
    fourbar_solid(0, 128, 255),
    miss_both(0, 128, 255),
    blackout(FX_BSW, CH_BSW), blackout(FX_SHARPY, CH_SHARPY),
    blackout(FX_PROFILE, CH_PROFILE), blackout(FX_NI3K, CH_NI3K),
    path="Tests/Combo")
add_button("Pars: Cool", sid, VC_YELLOW, col=2)
next_row()

# Everything on — full rig test
sid = add_scene("FULL RIG: White",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_WHITE),
    bsw(pan=177, tilt=19, color=BSW_WHITE),
    profile(pan=0, tilt=123, color=PROF_WHITE),
    fourbar_solid(255, 255, 255),
    miss_both(255, 255, 255),
    ni3k(r=255, g=255, b=255, w=255, dim=255, halo=H_RGB),
    path="Tests/Combo")
add_button("FULL: White", sid, VC_YELLOW, col=2)
next_row()

# Everything on — color
sid = add_scene("FULL RIG: Blue",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_BLUE),
    bsw(pan=177, tilt=19, color=BSW_BLUE),
    profile(pan=0, tilt=123, color=PROF_BLUE),
    fourbar_solid(0, 0, 255),
    miss_both(0, 0, 255),
    ni3k(r=0, g=0, b=255, w=0, dim=255, halo=H_BLU),
    path="Tests/Combo")
add_button("FULL: Blue", sid, VC_YELLOW, col=2)
next_row()

# Full rig with lasers
sid = add_scene("FULL RIG: Party",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_PURPLE, prism1=128, p1r=200),
    bsw(pan=177, tilt=19, color=BSW_MAG, prism=128, prot=160),
    profile(pan=0, tilt=123, color=PROF_PINK, prism=128),
    fourbar(255,0,0, 0,255,0, 0,0,255, 255,255,0),
    miss1(255, 0, 128),
    miss2(0, 128, 255),
    ni3k(r=255, g=0, b=255, w=0, dim=255, halo=H_RGB,
         rl=LASER_ON, gl=LASER_ON, bl=LASER_ON, t1=160, t2=180, t3=200),
    path="Tests/Combo")
add_button("FULL: Party", sid, VC_YELLOW, col=2)
next_row()

# =============================================================================
# WRITE WORKSPACE
# =============================================================================

# Use the larger of the two column heights for the VC
next_y = max(next_y, next_y_saved)

output = "venue/home-studio/shows/Fixture-Test.qxw"
write_workspace(output, scenes, [], bpm=BPM, vc_buttons=vc_buttons)
print(f"\nFixture Test generated: {len(scenes)} scenes")
print(f"VC Layout: {len(vc_buttons)} buttons in 2-column layout")
