#!/usr/bin/env python3
"""
DnB Banger — High-energy drum & bass show at 174 BPM
Home Studio venue

Structure (96 bars total, ~132s):
  Intro       8 bars  — Dark pulse, movers center, par breathe
  Build 1     8 bars  — Rising energy, colors layer in, movers start moving
  Drop 1     16 bars  — FULL SEND. Beat-synced snaps, strobes, lasers, prisms
  Breakdown   8 bars  — Pull back hard, single color wash, slow sweep
  Build 2     8 bars  — Rebuild with different palette, faster layering
  Drop 2     16 bars  — Even bigger. Different colors, all effects maxed
  Outro       8 bars  — Wind down, converge to center, fade

Palette:
  Drop 1: Red/Amber/Orange — aggressive, fiery
  Drop 2: Blue/Cyan/Purple — cold, electric
  Breakdown: Deep blue solo wash
  Builds: Transition colors between sections
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from showlib import *

BPM = 174
BEAT = bpm_to_ms(BPM, 1)   # ~345ms per beat
BAR = bpm_to_ms(BPM, 4)    # ~1379ms per bar

# =============================================================================
# FOCUS POSITIONS (from focus-positions.md, verified)
# =============================================================================
POS = {
    'C':    {'sharpy': (153, 0),  'bsw': (177, 19),  'profile': (0, 123),   'ni3k': 128},
    'DSC':  {'sharpy': (158, 6),  'bsw': (179, 27),  'profile': (64, 145),  'ni3k': 128},
    'USC':  {'sharpy': (157, 0),  'bsw': (181, 21),  'profile': (52, 136),  'ni3k': 128},
    'SL':   {'sharpy': (170, 0),  'bsw': (189, 29),  'profile': (50, 165),  'ni3k': 80},
    'SR':   {'sharpy': (149, 5),  'bsw': (170, 23),  'profile': (110, 145), 'ni3k': 176},
    'DSL':  {'sharpy': (170, 0),  'bsw': (189, 29),  'profile': (50, 165),  'ni3k': 80},
    'DSR':  {'sharpy': (149, 5),  'bsw': (170, 23),  'profile': (110, 145), 'ni3k': 176},
    'USL':  {'sharpy': (170, 0),  'bsw': (189, 29),  'profile': (50, 165),  'ni3k': 80},
    'USR':  {'sharpy': (149, 5),  'bsw': (170, 23),  'profile': (110, 145), 'ni3k': 176},
    'DJ':   {'sharpy': (142, 3),  'bsw': (196, 25),  'profile': (95, 107),  'ni3k': 128},
    'CEIL': {'sharpy': (158, 73), 'bsw': (180, 86),  'profile': (91, 30),   'ni3k': 128},
    'DISCO':{'sharpy': (144, 34), 'bsw': (170, 56),  'profile': (154, 168), 'ni3k': 128},
    'SWEEP_L': {'sharpy': (90, 5), 'bsw': (198, 25), 'profile': (45, 120), 'ni3k': 40},
    'SWEEP_R': {'sharpy': (220, 5), 'bsw': (162, 20), 'profile': (0, 120), 'ni3k': 220},
}

def pos_sharpy(name):
    return POS[name]['sharpy']

def pos_bsw(name):
    return POS[name]['bsw']

def pos_profile(name):
    return POS[name]['profile']

def pos_ni3k_pan(name):
    return POS[name]['ni3k']

# =============================================================================
# SCENE BUILDERS
# =============================================================================

scenes = []
sid = 0  # scene ID counter

def add_scene(name, *fixtures, path="Show"):
    global sid
    s = scene(name, *fixtures, path=path)
    scenes.append(s)
    this_id = sid
    sid += 1
    return this_id

# BLACKOUT
s_black = add_scene("BLACKOUT", *blackout_all())

# =============================================================================
# INTRO (8 bars) — Dark pulse. Movers center. Pars breathe red.
# Beat-level alternation: dim red pulse on pars, movers barely visible
# =============================================================================

# Intro beat A: dim red wash, movers at center with low dim
s_intro_a = add_scene("Intro Beat A",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED, dim=40, strobe=SHARPY_OPEN),
    bsw(pan=177, tilt=19, color=BSW_RED, dim=40, shutter=BSW_SHUT_OPEN),
    profile(pan=0, tilt=123, color=PROF_RED, dim=30),
    fourbar_solid(80, 0, 0),
    *miss_both(60, 0, 0),
    ni3k(pan=128, r=80, g=0, b=0, w=0, dim=40, halo=H_RED),
    path="Intro"
)

# Intro beat B: slightly brighter, hint of amber
s_intro_b = add_scene("Intro Beat B",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED, dim=80, strobe=SHARPY_OPEN),
    bsw(pan=177, tilt=19, color=BSW_RED, dim=80, shutter=BSW_SHUT_OPEN),
    profile(pan=0, tilt=123, color=PROF_RED, dim=60),
    fourbar_solid(120, 30, 0),
    *miss_both(100, 20, 0),
    ni3k(pan=128, r=120, g=20, b=0, w=0, dim=80, halo=H_RED),
    path="Intro"
)

# =============================================================================
# BUILD 1 (8 bars) — Rising energy. Colors layer in. Movers start moving.
# 2-beat pattern cycling through positions, each one brighter
# =============================================================================

build1_positions = ['C', 'SL', 'C', 'SR', 'DSC', 'SL', 'SR', 'C',
                    'DSL', 'C', 'DSR', 'C', 'SL', 'SR', 'DSC', 'C']
build1_scenes = []
for i, pos in enumerate(build1_positions):
    energy = min(255, 80 + i * 11)  # ramp from 80 to 255
    par_r = min(255, 100 + i * 10)
    par_g = min(255, i * 8)
    sp, st = pos_sharpy(pos)
    bp, bt = pos_bsw(pos)
    pp, pt = pos_profile(pos)
    np = pos_ni3k_pan(pos)

    s = add_scene(f"Build1 {pos} {i}",
        sharpy(pan=sp, tilt=st, colormacro=SHARPY_RED if i < 8 else SHARPY_AMBER,
               dim=energy, strobe=SHARPY_OPEN),
        bsw(pan=bp, tilt=bt, color=BSW_RED if i < 8 else BSW_ORANGE,
            dim=energy, shutter=BSW_SHUT_OPEN),
        profile(pan=pp, tilt=pt, color=PROF_RED if i < 8 else PROF_ORANGE,
                dim=energy),
        fourbar_solid(par_r, par_g, 0),
        *miss_both(par_r, par_g, 0),
        ni3k(pan=np, r=par_r, g=par_g, b=0, w=0, dim=energy,
             halo=H_RED if i < 12 else H_YEL),
        path="Build 1"
    )
    build1_scenes.append(s)

# =============================================================================
# DROP 1 (16 bars = 64 beats) — FULL SEND. Red/Amber/Orange.
# Beat-level snaps. Every beat = different look. Strobes. Lasers. Prisms.
# Movers bounce between positions. Pars chase.
# =============================================================================

drop1_positions = ['DSC', 'SL', 'SR', 'C', 'DSL', 'DSR', 'CEIL', 'C',
                   'SWEEP_L', 'C', 'SWEEP_R', 'C', 'SL', 'SR', 'DSC', 'DJ']
drop1_colors_sharpy = [SHARPY_RED, SHARPY_AMBER, SHARPY_ORANGE, SHARPY_RED,
                       SHARPY_YELLOW, SHARPY_RED, SHARPY_AMBER, SHARPY_ORANGE,
                       SHARPY_RED, SHARPY_YELLOW, SHARPY_RED, SHARPY_AMBER,
                       SHARPY_ORANGE, SHARPY_RED, SHARPY_YELLOW, SHARPY_RED]
drop1_colors_bsw = [BSW_RED, BSW_ORANGE, BSW_YELLOW, BSW_RED,
                    BSW_ORANGE, BSW_RED, BSW_YELLOW, BSW_ORANGE,
                    BSW_RED, BSW_ORANGE, BSW_YELLOW, BSW_RED,
                    BSW_ORANGE, BSW_RED, BSW_YELLOW, BSW_RED]

# Par chase colors for drop 1 — alternating red/amber pairs
drop1_par_a = (255, 40, 0)   # hot red-orange
drop1_par_b = (255, 128, 0)  # amber
drop1_par_c = (255, 0, 0)    # pure red
drop1_par_d = (255, 200, 0)  # yellow-amber

drop1_scenes = []
for beat in range(64):
    pos = drop1_positions[beat % 16]
    sp, st = pos_sharpy(pos)
    bp, bt = pos_bsw(pos)
    pp, pt = pos_profile(pos)
    np = pos_ni3k_pan(pos)

    sharpy_col = drop1_colors_sharpy[beat % 16]
    bsw_col = drop1_colors_bsw[beat % 16]

    # Alternate prisms every 4 beats
    use_prism = (beat % 8) < 4
    # Strobe hit on every other beat for first half, every beat for second half
    use_strobe = (beat >= 32) or (beat % 2 == 0)

    # NI3K: lasers on, tilts in rotation mode for chaos
    ni3k_t1 = 160 + (beat * 7) % 60   # varying forward rotation
    ni3k_t2 = 180 + (beat * 11) % 40
    ni3k_t3 = 170 + (beat * 5) % 50

    # Par chase: cycle through 4 colors across the 4BAR pars
    par_colors = [drop1_par_a, drop1_par_b, drop1_par_c, drop1_par_d]
    p1 = par_colors[(beat + 0) % 4]
    p2 = par_colors[(beat + 1) % 4]
    p3 = par_colors[(beat + 2) % 4]
    p4 = par_colors[(beat + 3) % 4]

    # Missyee alternate
    miss_a = par_colors[(beat) % 4]
    miss_b = par_colors[(beat + 2) % 4]

    s = add_scene(f"Drop1 B{beat}",
        sharpy(pan=sp, tilt=st, colormacro=sharpy_col, dim=255,
               strobe=SHARPY_OPEN,
               prism1=128 if use_prism else 0, p1r=200 if use_prism else 0),
        bsw(pan=bp, tilt=bt, color=bsw_col, dim=255,
            shutter=BSW_SHUT_OPEN,
            prism=200 if use_prism else 0, prot=160 if use_prism else 0,
            gobo1=BSW_G1_3 if beat % 4 == 0 else BSW_G1_OPEN),
        profile(pan=pp, tilt=pt,
                color=PROF_RED if beat % 2 == 0 else PROF_ORANGE,
                dim=255,
                strobe=0),
        fourbar(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2],
                p3[0], p3[1], p3[2], p4[0], p4[1], p4[2],
                strobe=0),
        miss1(*miss_a),
        miss2(*miss_b),
        ni3k(pan=np, t1=ni3k_t1, t2=ni3k_t2, t3=ni3k_t3,
             r=255, g=40, b=0, w=0, dim=255,
             halo=H_RED if beat % 2 == 0 else H_YEL,
             rl=LASER_ON, gl=LASER_OFF, bl=LASER_OFF),
        path="Drop 1"
    )
    drop1_scenes.append(s)

# =============================================================================
# BREAKDOWN (8 bars) — Pull back hard. Deep blue wash. Slow sweep center.
# 4-beat scenes, smooth crossfades
# =============================================================================

breakdown_positions = ['C', 'SL', 'C', 'SR', 'DSC', 'C', 'SL', 'C']
breakdown_scenes = []
for i, pos in enumerate(breakdown_positions):
    sp, st = pos_sharpy(pos)
    bp, bt = pos_bsw(pos)
    pp, pt = pos_profile(pos)
    np = pos_ni3k_pan(pos)

    dim = 60 + (i % 3) * 20  # gentle pulse between 60-100

    s = add_scene(f"Break {pos} {i}",
        sharpy(pan=sp, tilt=st, colormacro=SHARPY_BLUE, dim=dim,
               strobe=SHARPY_OPEN, frost=80),
        bsw(pan=bp, tilt=bt, color=BSW_BLUE, dim=dim,
            shutter=BSW_SHUT_OPEN, frost=120),
        profile(pan=pp, tilt=pt, color=PROF_BLUE, dim=dim),
        fourbar_solid(0, 0, dim),
        *miss_both(0, 0, dim),
        ni3k(pan=np, r=0, g=0, b=dim, w=0, dim=dim, halo=H_BLU),
        path="Breakdown"
    )
    breakdown_scenes.append(s)

# =============================================================================
# BUILD 2 (8 bars) — Rebuild with blue/cyan/purple palette. Faster layering.
# 2-beat steps, intensity climbing
# =============================================================================

build2_positions = ['C', 'SR', 'C', 'SL', 'DSR', 'C', 'DSL', 'C',
                    'SR', 'SL', 'DSC', 'C', 'CEIL', 'C', 'DSC', 'C']
build2_scenes = []
for i, pos in enumerate(build2_positions):
    energy = min(255, 60 + i * 13)
    sp, st = pos_sharpy(pos)
    bp, bt = pos_bsw(pos)
    pp, pt = pos_profile(pos)
    np = pos_ni3k_pan(pos)

    # Transition from blue to cyan to purple
    if i < 5:
        s_col, b_col, p_col = SHARPY_BLUE, BSW_BLUE, PROF_BLUE
        par_rgb = (0, 0, energy)
    elif i < 10:
        s_col, b_col, p_col = SHARPY_TEAL, BSW_TEAL, PROF_TEAL
        par_rgb = (0, energy, energy)
    else:
        s_col, b_col, p_col = SHARPY_PURPLE, BSW_MAG, PROF_PINK
        par_rgb = (energy // 2, 0, energy)

    # Add prism at the end
    use_prism = i >= 12

    s = add_scene(f"Build2 {pos} {i}",
        sharpy(pan=sp, tilt=st, colormacro=s_col, dim=energy,
               strobe=SHARPY_OPEN,
               prism1=128 if use_prism else 0, p1r=200 if use_prism else 0),
        bsw(pan=bp, tilt=bt, color=b_col, dim=energy,
            shutter=BSW_SHUT_OPEN),
        profile(pan=pp, tilt=pt, color=p_col, dim=energy),
        fourbar_solid(*par_rgb),
        *miss_both(*par_rgb),
        ni3k(pan=np, r=par_rgb[0], g=par_rgb[1], b=par_rgb[2], w=0,
             dim=energy, halo=H_BLU if i < 10 else H_PNK),
        path="Build 2"
    )
    build2_scenes.append(s)

# =============================================================================
# DROP 2 (16 bars = 64 beats) — Even bigger. Blue/Cyan/Purple palette.
# All effects maxed. All lasers. Color spin. Gobo rotation.
# =============================================================================

drop2_positions = ['C', 'DSR', 'DSL', 'CEIL', 'SR', 'SL', 'DSC', 'C',
                   'SWEEP_R', 'C', 'SWEEP_L', 'DJ', 'DSC', 'CEIL', 'C', 'DSC']
drop2_colors_sharpy = [SHARPY_BLUE, SHARPY_PURPLE, SHARPY_TEAL, SHARPY_BLUE,
                       SHARPY_PINK, SHARPY_BLUE, SHARPY_PURPLE, SHARPY_TEAL,
                       SHARPY_BLUE, SHARPY_PINK, SHARPY_BLUE, SHARPY_PURPLE,
                       SHARPY_TEAL, SHARPY_BLUE, SHARPY_PINK, SHARPY_BLUE]
drop2_colors_bsw = [BSW_BLUE, BSW_MAG, BSW_TEAL, BSW_BLUE,
                    BSW_PINK, BSW_BLUE, BSW_MAG, BSW_TEAL,
                    BSW_BLUE, BSW_PINK, BSW_BLUE, BSW_MAG,
                    BSW_TEAL, BSW_BLUE, BSW_PINK, BSW_BLUE]

drop2_par_a = (0, 0, 255)     # pure blue
drop2_par_b = (0, 255, 255)   # cyan
drop2_par_c = (128, 0, 255)   # purple
drop2_par_d = (255, 0, 200)   # magenta

drop2_scenes = []
for beat in range(64):
    pos = drop2_positions[beat % 16]
    sp, st = pos_sharpy(pos)
    bp, bt = pos_bsw(pos)
    pp, pt = pos_profile(pos)
    np = pos_ni3k_pan(pos)

    sharpy_col = drop2_colors_sharpy[beat % 16]
    bsw_col = drop2_colors_bsw[beat % 16]

    # Prisms on most beats, gobos rotating
    use_prism = (beat % 4) != 3  # prism off every 4th beat for variety
    use_gobo = (beat % 8) < 6

    # NI3K: ALL lasers on, tilts going wild
    ni3k_t1 = 150 + (beat * 9) % 70
    ni3k_t2 = 160 + (beat * 13) % 60
    ni3k_t3 = 140 + (beat * 7) % 80

    # Par chase
    par_colors = [drop2_par_a, drop2_par_b, drop2_par_c, drop2_par_d]
    p1 = par_colors[(beat + 0) % 4]
    p2 = par_colors[(beat + 1) % 4]
    p3 = par_colors[(beat + 2) % 4]
    p4 = par_colors[(beat + 3) % 4]

    miss_a = par_colors[(beat) % 4]
    miss_b = par_colors[(beat + 2) % 4]

    # Every 8th beat: strobe flash on BSW
    bsw_shutter = BSW_SHUT_STROBE_FAST if (beat % 8 == 0 and beat >= 16) else BSW_SHUT_OPEN

    s = add_scene(f"Drop2 B{beat}",
        sharpy(pan=sp, tilt=st, colormacro=sharpy_col, dim=255,
               strobe=SHARPY_OPEN,
               prism1=128 if use_prism else 0, p1r=200 if use_prism else 0,
               prism2=128 if (beat >= 32 and use_prism) else 0,
               p2r=200 if (beat >= 32 and use_prism) else 0,
               gobo=BSW_G1_4 if use_gobo else 0),
        bsw(pan=bp, tilt=bt, color=bsw_col, dim=255,
            shutter=bsw_shutter,
            prism=200 if use_prism else 0, prot=180 if use_prism else 0,
            gobo1=BSW_G1_5 if use_gobo else BSW_G1_OPEN,
            gobo2=BSW_G2_3 if (beat >= 32 and use_gobo) else BSW_G2_OPEN),
        profile(pan=pp, tilt=pt,
                color=PROF_BLUE if beat % 3 != 0 else PROF_TEAL,
                dim=255),
        fourbar(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2],
                p3[0], p3[1], p3[2], p4[0], p4[1], p4[2],
                strobe=0),
        miss1(*miss_a),
        miss2(*miss_b),
        ni3k(pan=np, t1=ni3k_t1, t2=ni3k_t2, t3=ni3k_t3,
             r=0, g=0, b=255, w=0, dim=255,
             halo=H_BLU if beat % 2 == 0 else H_PNK,
             rl=LASER_ON, gl=LASER_ON, bl=LASER_ON),
        path="Drop 2"
    )
    drop2_scenes.append(s)

# =============================================================================
# OUTRO (8 bars) — Wind down. Converge to center. Fade.
# =============================================================================

outro_positions = ['DSC', 'C', 'SL', 'C', 'SR', 'C', 'C', 'C']
outro_scenes = []
for i, pos in enumerate(outro_positions):
    energy = max(0, 200 - i * 28)
    sp, st = pos_sharpy(pos)
    bp, bt = pos_bsw(pos)
    pp, pt = pos_profile(pos)
    np = pos_ni3k_pan(pos)

    s = add_scene(f"Outro {pos} {i}",
        sharpy(pan=sp, tilt=st, colormacro=SHARPY_BLUE, dim=energy,
               strobe=SHARPY_OPEN, frost=60),
        bsw(pan=bp, tilt=bt, color=BSW_BLUE, dim=energy,
            shutter=BSW_SHUT_OPEN, frost=80),
        profile(pan=pp, tilt=pt, color=PROF_BLUE, dim=energy),
        fourbar_solid(0, 0, energy),
        *miss_both(0, 0, energy // 2),
        ni3k(pan=np, r=0, g=0, b=energy, w=0, dim=energy, halo=H_BLU if energy > 50 else H_OFF),
        path="Outro"
    )
    outro_scenes.append(s)

# =============================================================================
# BUILD CHASERS
# =============================================================================

# Intro: alternating A/B on each beat, 8 bars = 32 beats
intro_ids = [s_intro_a if i % 2 == 0 else s_intro_b for i in range(32)]
intro_timing = [hold(BPM, 0.25)] * 32  # 1-beat hold each
ch_intro = make_chaser("01 Intro", intro_ids, intro_timing, run_order="SingleShot", path="Show")

# Build 1: 2-beat steps, smooth transitions, 16 steps = 8 bars
build1_timing = [snap(BPM, 0.5, fade_ms=80)] * 16
ch_build1 = make_chaser("02 Build 1", build1_scenes, build1_timing, run_order="SingleShot", path="Show")

# Drop 1: 1-beat snaps, 64 steps = 16 bars
drop1_timing = [hold(BPM, 0.25)] * 64
ch_drop1 = make_chaser("03 Drop 1", drop1_scenes, drop1_timing, run_order="SingleShot", path="Show")

# Breakdown: 4-beat smooth crossfades, 8 steps = 8 bars
breakdown_timing = [smooth(BPM, 0.25)] * 8  # smooth over 1 beat each... wait, 8 bars / 8 steps = 1 bar each
breakdown_timing = [(BAR, 0)] * 8  # 1-bar smooth crossfade
ch_breakdown = make_chaser("04 Breakdown", breakdown_scenes, breakdown_timing, run_order="SingleShot", path="Show")

# Build 2: 2-beat snaps, 16 steps = 8 bars
build2_timing = [snap(BPM, 0.5, fade_ms=60)] * 16
ch_build2 = make_chaser("05 Build 2", build2_scenes, build2_timing, run_order="SingleShot", path="Show")

# Drop 2: 1-beat snaps, 64 steps = 16 bars
drop2_timing = [hold(BPM, 0.25)] * 64
ch_drop2 = make_chaser("06 Drop 2", drop2_scenes, drop2_timing, run_order="SingleShot", path="Show")

# Outro: 4-beat smooth, 8 steps = 8 bars (same pattern as breakdown)
outro_timing = [(BAR, 0)] * 8
ch_outro = make_chaser("07 Outro", outro_scenes, outro_timing, run_order="SingleShot", path="Show")

# =============================================================================
# FULL SHOW CHASER (all sections sequenced)
# =============================================================================

full_ids = intro_ids + build1_scenes + drop1_scenes + breakdown_scenes + build2_scenes + drop2_scenes + outro_scenes
full_timing = intro_timing + build1_timing + drop1_timing + breakdown_timing + build2_timing + drop2_timing + outro_timing
ch_full = make_chaser("FULL SHOW", full_ids, full_timing, run_order="SingleShot", path="Show")

all_chasers = [ch_intro, ch_build1, ch_drop1, ch_breakdown, ch_build2, ch_drop2, ch_outro, ch_full]

# =============================================================================
# VIRTUAL CONSOLE
# =============================================================================

# Scene count to get chaser function IDs
num_scenes = len(scenes)
chaser_func_ids = {i: num_scenes + i for i in range(len(all_chasers))}

vc_buttons = []
vc_id = 0

# Full show button (big, top)
vc_buttons.append({
    "caption": "FULL SHOW", "vc_id": vc_id,
    "x": 10, "y": 10, "w": 470, "h": 100,
    "color": "#22CC22", "func_id": chaser_func_ids[7], "action": "Toggle"
})
vc_id += 1

# Section buttons
section_names = ["01 Intro", "02 Build 1", "03 Drop 1", "04 Breakdown",
                 "05 Build 2", "06 Drop 2", "07 Outro"]
section_colors = ["#555555", "#886600", "#CC2200", "#003388",
                  "#004488", "#2200CC", "#333333"]

for i, (name, color) in enumerate(zip(section_names, section_colors)):
    vc_buttons.append({
        "caption": name, "vc_id": vc_id,
        "x": 10, "y": 120 + i * 70, "w": 470, "h": 60,
        "color": color, "func_id": chaser_func_ids[i], "action": "Toggle"
    })
    vc_id += 1

# Blackout button
vc_buttons.append({
    "caption": "BLACKOUT", "vc_id": vc_id,
    "x": 10, "y": 120 + 7 * 70, "w": 470, "h": 80,
    "color": "#FF0000", "func_id": s_black, "action": "Toggle"
})

# =============================================================================
# WRITE WORKSPACE
# =============================================================================

output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shows")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "DnB-Banger.qxw")

write_workspace(output_path, scenes, all_chasers, bpm=BPM, vc_buttons=vc_buttons)

# Print summary
total_beats = 32 + 16 + 64 + 8 + 16 + 64 + 8
total_bars = (32 + 64 + 64) + (16 + 16) * BEAT / BAR  # approximate
print(f"\nShow: DnB Banger")
print(f"  BPM: {BPM}")
print(f"  Beat duration: {BEAT}ms")
print(f"  Bar duration: {BAR}ms")
print(f"  Total scenes: {len(scenes)}")
print(f"  Total chaser steps: {sum(len(c['scene_ids']) for c in all_chasers)}")
print(f"  Sections: Intro(8) → Build1(8) → Drop1(16) → Breakdown(8) → Build2(8) → Drop2(16) → Outro(8) = 72 bars")
print(f"  Duration: ~{72 * BAR / 1000:.0f}s")
