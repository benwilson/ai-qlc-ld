#!/usr/bin/env python3
"""
Busking Show Generator — 174 BPM High Energy Party DnB
Home Studio venue

A collection of standalone looks and looping chasers for live busking.
Hit buttons to match whatever track is playing. ~20 VC buttons organized
into categories: Looks, Chasers, Effects, and Control.

Run from project root:
    python3 "venue/home-studio/generators/Busking-174.py"
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from showlib import *

BPM = 174

# =============================================================================
# COLOR PALETTES — high energy party DnB
# =============================================================================

# Neon party colors for pars
NEON_PINK    = (255, 20, 100)
NEON_GREEN   = (0, 255, 80)
NEON_BLUE    = (0, 80, 255)
NEON_PURPLE  = (180, 0, 255)
HOT_ORANGE   = (255, 80, 0)
ICE_WHITE    = (200, 220, 255)

# =============================================================================
# FOCUS POSITION SHORTCUTS (from focus-positions.md)
# =============================================================================

POS = {
    # Verified positions from focus-positions.md
    "C":   {"sharpy": (153, 0),   "bsw": (177, 19),  "profile": (0, 123)},
    "DSC": {"sharpy": (158, 6),   "bsw": (179, 27),  "profile": (64, 145)},
    "USC": {"sharpy": (157, 0),   "bsw": (181, 21),  "profile": (52, 136)},
    "SL":  {"sharpy": (170, 0),   "bsw": (189, 29),  "profile": (50, 165)},
    "SR":  {"sharpy": (149, 5),   "bsw": (170, 23),  "profile": (110, 145)},
    "DSL": {"sharpy": (168, 4),   "bsw": (187, 32),  "profile": (56, 170)},
    "DSR": {"sharpy": (151, 8),   "bsw": (168, 27),  "profile": (115, 150)},
    "USL": {"sharpy": (172, 0),   "bsw": (192, 25),  "profile": (40, 155)},
    "USR": {"sharpy": (147, 2),   "bsw": (173, 18),  "profile": (105, 138)},
    # Effects (from focus-positions.md)
    "CEIL":    {"sharpy": (158, 73), "bsw": (180, 86),  "profile": (91, 30)},
    "BLIND":   {"sharpy": (153, 15), "bsw": (177, 5),   "profile": (0, 155)},
    "BACKWALL":{"sharpy": (153, 0),  "bsw": (180, 35),  "profile": (0, 95)},
    # Sweep extremes — BSW stays within forward-facing range (162-198)
    "FAR_L":   {"sharpy": (90, 5),   "bsw": (198, 25),  "profile": (45, 120)},
    "FAR_R":   {"sharpy": (220, 5),  "bsw": (162, 20),  "profile": (0, 120)},
}

def movers_at(pos_name, sharpy_color=SHARPY_WHITE, bsw_color=BSW_WHITE,
              prof_color=PROF_WHITE, sharpy_gobo=0, bsw_gobo1=0,
              sharpy_prism1=0, bsw_prism=0, sharpy_strobe=SHARPY_OPEN,
              bsw_shutter=BSW_SHUT_OPEN, prof_strobe=PROFILE_STROBE_OFF):
    """Return movers aimed at a named position with optional color/gobo overrides."""
    p = POS[pos_name]
    sp, st = p["sharpy"]
    bp, bt = p["bsw"]
    pp, pt = p["profile"]
    return [
        sharpy(pan=sp, tilt=st, colormacro=sharpy_color, gobo=sharpy_gobo,
               prism1=sharpy_prism1, strobe=sharpy_strobe),
        bsw(pan=bp, tilt=bt, color=bsw_color, gobo1=bsw_gobo1,
            prism=bsw_prism, shutter=bsw_shutter),
        profile(pan=pp, tilt=pt, color=prof_color, strobe=prof_strobe),
    ]


# =============================================================================
# SCENES — Standalone looks (static, triggered by buttons)
# =============================================================================

scenes = []

# -- BLACKOUT (always index 0) --
scenes.append(scene("BLACKOUT", *blackout_all()))

# -- LOOK 1: Full White Center --
# All movers center, all pars white, NI3K white halo
scenes.append(scene("Full White",
    *movers_at("C"),
    fourbar_solid(*ICE_WHITE),
    *miss_both(*ICE_WHITE),
    ni3k(r=200, g=220, b=255, halo=H_CYN),
))

# -- LOOK 2: Neon Pink Blast --
scenes.append(scene("Neon Pink",
    *movers_at("C", sharpy_color=SHARPY_PINK, bsw_color=BSW_PINK, prof_color=PROF_PINK),
    fourbar_solid(*NEON_PINK),
    *miss_both(*MAGENTA),
    ni3k(r=255, g=20, b=100, halo=H_PNK),
))

# -- LOOK 3: Deep Blue + Lasers --
scenes.append(scene("Deep Blue Lasers",
    *movers_at("C", sharpy_color=SHARPY_BLUE, bsw_color=BSW_BLUE, prof_color=PROF_BLUE),
    fourbar_solid(*NEON_BLUE),
    *miss_both(*BLUE),
    ni3k(r=0, g=0, b=255, halo=H_BLU, rl=LASER_ON, gl=LASER_ON, bl=LASER_ON),
))

# -- LOOK 4: Green Machine --
scenes.append(scene("Green Machine",
    *movers_at("C", sharpy_color=SHARPY_GREEN, bsw_color=BSW_GREEN, prof_color=PROF_GREEN),
    fourbar_solid(*NEON_GREEN),
    *miss_both(*GREEN),
    ni3k(r=0, g=255, b=80, halo=H_GRN, gl=LASER_ON),
))

# -- LOOK 5: Fire (Red/Orange, movers spread) --
scenes.append(scene("Fire",
    sharpy(pan=90, tilt=0, colormacro=SHARPY_RED),
    bsw(pan=170, tilt=23, color=BSW_ORANGE),
    profile(pan=110, tilt=145, color=PROF_ORANGE),
    fourbar_gradient(*RED, *HOT_ORANGE),
    *miss_both(*ORANGE),
    ni3k(r=255, g=40, b=0, halo=H_RED, rl=LASER_ON),
))

# -- LOOK 6: Purple Haze (movers crossed, prisms) --
scenes.append(scene("Purple Haze",
    sharpy(pan=220, tilt=0, colormacro=SHARPY_PURPLE, prism1=128, p1r=200),
    bsw(pan=189, tilt=29, color=BSW_MAG, prism=200, prot=160),
    profile(pan=29, tilt=123, color=PROF_PINK),
    fourbar_solid(*NEON_PURPLE),
    *miss_both(*PURPLE),
    ni3k(r=180, g=0, b=255, halo=H_PNK, bl=LASER_ON),
))

# -- LOOK 7: Ceiling Hit (all beams up, tight gobos) --
scenes.append(scene("Ceiling Hit",
    *movers_at("CEIL", sharpy_color=SHARPY_TEAL, bsw_color=BSW_TEAL,
               prof_color=PROF_TEAL, sharpy_gobo=8, bsw_gobo1=BSW_G1_3),
    fourbar_solid(*CYAN),
    *miss_both(*TEAL),
    ni3k(r=0, g=255, b=200, halo=H_CYN, t1=160, t2=170, t3=180),
))

# -- LOOK 8: Audience Blinder (strobes only, brief use!) --
scenes.append(scene("BLINDER",
    *movers_at("BLIND", sharpy_strobe=SHARPY_STROBE_FAST,
               bsw_shutter=BSW_SHUT_STROBE_FAST),
    fourbar_solid(*WHITE, strobe=200),
    *miss_both(*WHITE, strobe=200),
    ni3k(r=255, g=255, b=255, w=255, strobe=200, halo=H_RGB,
         rl=LASER_STROBE_FAST, gl=LASER_STROBE_FAST, bl=LASER_STROBE_FAST),
))

# -- LOOK 9: Minimal — just pars, movers off --
scenes.append(scene("Pars Only",
    sharpy(dim=0, strobe=SHARPY_CLOSED),
    bsw(dim=0, shutter=BSW_SHUT_CLOSED),
    profile(dim=0),
    fourbar_gradient(*NEON_BLUE, *NEON_PURPLE),
    miss1(*NEON_PINK),
    miss2(*NEON_GREEN),
    ni3k(dim=0, r=0, g=0, b=0, halo=H_OFF),
))

# -- LOOK 10: Lasers Only (dark room, just NI3K lasers) --
scenes.append(scene("Lasers Only",
    sharpy(dim=0, strobe=SHARPY_CLOSED),
    bsw(dim=0, shutter=BSW_SHUT_CLOSED),
    profile(dim=0),
    fourbar_solid(*OFF),
    *miss_both(*OFF),
    ni3k(dim=0, r=0, g=0, b=0, halo=H_OFF,
         rl=LASER_ON, gl=LASER_ON, bl=LASER_ON),
))


# =============================================================================
# CHASER SCENES — scenes used as steps within chasers
# =============================================================================

# --- LR Sweep (5 positions, smooth crossfade) ---
sweep_positions = ["FAR_L", "SL", "C", "SR", "FAR_R"]
sweep_colors = [
    (SHARPY_BLUE, BSW_BLUE, PROF_BLUE),
    (SHARPY_TEAL, BSW_TEAL, PROF_TEAL),
    (SHARPY_WHITE, BSW_WHITE, PROF_WHITE),
    (SHARPY_TEAL, BSW_TEAL, PROF_TEAL),
    (SHARPY_BLUE, BSW_BLUE, PROF_BLUE),
]
for i, pos in enumerate(sweep_positions):
    sc, bc, pc = sweep_colors[i]
    scenes.append(scene(f"Sweep {pos}",
        *movers_at(pos, sharpy_color=sc, bsw_color=bc, prof_color=pc),
        fourbar_solid(*CYAN),
        *miss_both(*TEAL),
        ni3k(r=0, g=200, b=255, halo=H_CYN, pan=int(50 + i*40)),
        path="Chasers/Sweep",
    ))
# sweep scene IDs: 11..15

# --- Color Cycle (4 colors, snap changes) ---
cycle_looks = [
    ("Cycle Red", SHARPY_RED, BSW_RED, PROF_RED, RED, RED, H_RED),
    ("Cycle Blue", SHARPY_BLUE, BSW_BLUE, PROF_BLUE, BLUE, NEON_BLUE, H_BLU),
    ("Cycle Green", SHARPY_GREEN, BSW_GREEN, PROF_GREEN, GREEN, NEON_GREEN, H_GRN),
    ("Cycle Pink", SHARPY_PINK, BSW_PINK, PROF_PINK, NEON_PINK, MAGENTA, H_PNK),
]
for name, sc, bc, pc, par_c, miss_c, halo in cycle_looks:
    scenes.append(scene(name,
        *movers_at("C", sharpy_color=sc, bsw_color=bc, prof_color=pc),
        fourbar_solid(*par_c),
        *miss_both(*miss_c),
        ni3k(r=miss_c[0], g=miss_c[1], b=miss_c[2], halo=halo),
        path="Chasers/ColorCycle",
    ))
# cycle scene IDs: 16..19

# --- Drop Strobe (alternating bright/dark) ---
scenes.append(scene("Drop ON",
    *movers_at("C", sharpy_color=SHARPY_WHITE),
    fourbar_solid(*WHITE),
    *miss_both(*WHITE),
    ni3k(r=255, g=255, b=255, w=255, halo=H_RGB,
         rl=LASER_ON, gl=LASER_ON, bl=LASER_ON),
    path="Chasers/DropStrobe",
))
scenes.append(scene("Drop OFF",
    *blackout_all(),
    path="Chasers/DropStrobe",
))
# drop strobe IDs: 20, 21

# --- Cross Beam Swap (movers swap sides) ---
scenes.append(scene("Cross A",
    sharpy(pan=220, tilt=9, colormacro=SHARPY_RED),   # Sharpy to DSR
    bsw(pan=187, tilt=32, color=BSW_BLUE),              # BSW to DSL
    profile(pan=0, tilt=136, color=PROF_RED),
    fourbar_pairs(*RED, *BLUE),
    miss1(*RED), miss2(*BLUE),
    ni3k(r=255, g=0, b=0, halo=H_RED, pan=80),
    path="Chasers/CrossBeam",
))
scenes.append(scene("Cross B",
    sharpy(pan=90, tilt=9, colormacro=SHARPY_BLUE),    # Sharpy to DSL
    bsw(pan=168, tilt=27, color=BSW_RED),               # BSW to DSR
    profile(pan=0, tilt=136, color=PROF_BLUE),
    fourbar_pairs(*BLUE, *RED),
    miss1(*BLUE), miss2(*RED),
    ni3k(r=0, g=0, b=255, halo=H_BLU, pan=176),
    path="Chasers/CrossBeam",
))
# cross IDs: 22, 23

# --- Rolling Bass (slow movers, deep colors, 2-bar smooth) ---
roll_positions = ["SL", "C", "SR", "C"]
for i, pos in enumerate(roll_positions):
    blues = [SHARPY_BLUE, SHARPY_TEAL, SHARPY_PURPLE, SHARPY_BLUE]
    bsw_blues = [BSW_BLUE, BSW_TEAL, BSW_MAG, BSW_BLUE]
    scenes.append(scene(f"Roll {i+1}",
        *movers_at(pos, sharpy_color=blues[i], bsw_color=bsw_blues[i],
                   prof_color=PROF_BLUE),
        fourbar_gradient(*BLUE, *PURPLE),
        *miss_both(*NEON_PURPLE),
        ni3k(r=60, g=0, b=200, halo=H_BLU, pan=int(80 + i*32)),
        path="Chasers/Rolling",
    ))
# rolling IDs: 24..27

# --- Par Chase (4BAR sequential, movers static center) ---
par_chase_colors = [
    (255,0,0, 0,0,0, 0,0,0, 0,0,0),
    (0,0,0, 0,255,0, 0,0,0, 0,0,0),
    (0,0,0, 0,0,0, 0,0,255, 0,0,0),
    (0,0,0, 0,0,0, 0,0,0, 255,0,255),
]
for i, pars in enumerate(par_chase_colors):
    scenes.append(scene(f"ParChase {i+1}",
        *movers_at("C", sharpy_color=SHARPY_WHITE, bsw_color=BSW_WHITE),
        fourbar(*pars),
        miss1(*(NEON_PINK if i % 2 == 0 else OFF)),
        miss2(*(NEON_GREEN if i % 2 == 1 else OFF)),
        ni3k(r=100, g=100, b=255, halo=H_JUMP_FAST),
        path="Chasers/ParChase",
    ))
# par chase IDs: 28..31


# =============================================================================
# CHASERS
# =============================================================================

chasers = []

# Chaser 1: LR Sweep (smooth 1-bar crossfades, loop)
sweep_ids = list(range(11, 16))
chasers.append(make_chaser("LR Sweep",
    sweep_ids + list(reversed(sweep_ids[1:-1])),  # ping-pong manually for smooth
    [smooth(BPM, 1)] * (len(sweep_ids) + len(sweep_ids[1:-1])),
    run_order="Loop", path="Chasers",
))

# Chaser 2: Color Cycle (1-bar snaps, loop)
chasers.append(make_chaser("Color Cycle",
    list(range(16, 20)),
    [hold(BPM, 1)] * 4,
    run_order="Loop", path="Chasers",
))

# Chaser 3: Drop Strobe (1/2-beat alternating, loop)
chasers.append(make_chaser("Drop Strobe",
    [20, 21],
    [hold(BPM, 0.5)] * 2,  # 2 beats on, 2 beats off
    run_order="Loop", path="Chasers",
))

# Chaser 4: Fast Strobe (1/8th note, loop) — for drops
chasers.append(make_chaser("Fast Strobe",
    [20, 21],
    [hold(BPM, 0.125)] * 2,  # 1/8th note = half beat
    run_order="Loop", path="Chasers",
))

# Chaser 5: Cross Beam Swap (2-bar smooth, loop)
chasers.append(make_chaser("Cross Beams",
    [22, 23],
    [smooth(BPM, 2)] * 2,
    run_order="Loop", path="Chasers",
))

# Chaser 6: Rolling Bass (2-bar smooth, loop)
chasers.append(make_chaser("Rolling Bass",
    list(range(24, 28)),
    [smooth(BPM, 2)] * 4,
    run_order="Loop", path="Chasers",
))

# Chaser 7: Par Chase (1-beat snaps, loop)
chasers.append(make_chaser("Par Chase",
    list(range(28, 32)),
    [hold(BPM, 0.25)] * 4,  # 1 beat each
    run_order="Loop", path="Chasers",
))


# =============================================================================
# VIRTUAL CONSOLE LAYOUT
# =============================================================================

# Layout: 4 columns, organized by category
# Col 1 (x=10):  Looks (static scenes)
# Col 2 (x=260): Looks continued
# Col 3 (x=510): Chasers
# Col 4 (x=760): Effects & Control

BTN_W = 240
BTN_H = 65
GAP = 5

def btn(caption, func_id, col, row, color, action="Toggle"):
    x = 10 + col * (BTN_W + GAP)
    y = 10 + row * (BTN_H + GAP)
    return {
        "caption": caption, "func_id": func_id, "vc_id": col * 10 + row,
        "x": x, "y": y, "w": BTN_W, "h": BTN_H,
        "color": color, "action": action,
    }

# Scene IDs: 0=blackout, 1-10=looks
# Chaser IDs: start at len(scenes)
ch_base = len(scenes)  # first chaser function ID

vc_buttons = [
    # Column 0: Looks (warm/bright)
    btn("Full White",    1,  0, 0, "#DDDDDD"),
    btn("Neon Pink",     2,  0, 1, "#FF1464"),
    btn("Deep Blue",     3,  0, 2, "#0050FF"),
    btn("Green Machine", 4,  0, 3, "#00FF50"),
    btn("Fire",          5,  0, 4, "#FF5000"),

    # Column 1: Looks (effects/special)
    btn("Purple Haze",   6,  1, 0, "#B400FF"),
    btn("Ceiling Hit",   7,  1, 1, "#00FFCC"),
    btn("Pars Only",     9,  1, 2, "#4466AA"),
    btn("Lasers Only",   10, 1, 3, "#880000"),
    btn("BLINDER",       8,  1, 4, "#FFFF00"),

    # Column 2: Chasers
    btn("LR Sweep",      ch_base + 0, 2, 0, "#00AAAA"),
    btn("Color Cycle",   ch_base + 1, 2, 1, "#AA00AA"),
    btn("Drop Strobe",   ch_base + 2, 2, 2, "#FF8800"),
    btn("Fast Strobe",   ch_base + 3, 2, 3, "#FF0000"),
    btn("Cross Beams",   ch_base + 4, 2, 4, "#0088FF"),

    # Column 3: Chasers + Control
    btn("Rolling Bass",  ch_base + 5, 3, 0, "#2200AA"),
    btn("Par Chase",     ch_base + 6, 3, 1, "#00AA44"),
    btn("BLACKOUT",      0,           3, 4, "#FF0000"),
]

# =============================================================================
# WRITE OUTPUT
# =============================================================================

output_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "shows", "Busking-174.qxw"
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

write_workspace(output_path, scenes, chasers, bpm=BPM, vc_buttons=vc_buttons)

print(f"\nBusking show ready!")
print(f"  {len(scenes)} scenes, {len(chasers)} chasers")
print(f"  {len(vc_buttons)} VC buttons")
print(f"  BPM: {BPM}")
