#!/usr/bin/env python3
"""
Show Generator: Nora En Pure - Bartok (Extended Mix)
BPM: 125 | Duration: ~7:08 (428s) | Venue: home-studio

Creative arc: open landscape at dawn — deep earth warming through amber light
to warm gold chorus runs. Two breaks strip back to bare earth. Final run blooms
into full golden warmth with NI3K lasers, then fades back to dark ground.

Structure:
  INTRO      0:00–1:02  32 bars  Slow build, earthy amber, single organism
  CHORUS_1   1:02–1:33  16 bars  First reveal, warm amber
  BRIDGE     1:33–1:48   8 bars  Inst break, soft settle
  CHORUS_2   1:48–2:50  32 bars  Main chorus run, amber → gold
  BREAK_1    2:50–3:37  24 bars  Breakdown, stripping back
  RISING     3:37–4:08  16 bars  Building to climax at 4:04, prism on peak
  BREAK_2    4:08–5:06  28 bars  Re-break → re-intro strip, near-bare
  FINAL      5:06–6:54  56 bars  Final chorus run, NI3K lasers, full gold
  OUTRO      6:54–7:08  12 bars  Fade to earth
  Total: 224 bars ≈ 430s
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from showlib import (
    sharpy, bsw, profile, ni3k, fourbar_solid, miss1, miss2,
    dark_sharpy, dark_bsw, dark_profile, dark_ni3k,
    scene, make_chaser, write_workspace, smooth, bpm_to_ms,
    BSW_ORANGE, BSW_YELLOW,
    LASER_ON, LASER_OFF, LASER_STROBE_SLOW,
    H_OFF, H_YEL, H_RGB,
    require_research_brief, build_creative_context,
    load_focus_position_tuples,
)

# ── Paths ──────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR    = os.path.dirname(SCRIPT_DIR)              # generators/ → venue/<name>/
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
SONG_STEM    = "Nora En Pure - Bartok (Extended Mix)"
SONG_TITLE   = "Bartok"
BPM          = 125

# ── Research gate ──────────────────────────────────────────────
BRIEF    = require_research_brief(SONG_STEM, PROJECT_ROOT, venue_dir=VENUE_DIR)
CREATIVE = build_creative_context(BRIEF, song_stem=SONG_STEM)
print(f"Creative thesis: {BRIEF['thesis']}")
print(f"Generating show: {SONG_STEM}")

# ── Venue positions ────────────────────────────────────────────
# 7-tuple per key: (sh_pan, sh_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt, ni3k_pan)
POS = load_focus_position_tuples(PROJECT_ROOT, VENUE_DIR)

# ── Colour palette ─────────────────────────────────────────────
# All warm earth tones. No cold, no neon.

# PAR (4BAR fourbar_solid + missyees) RGB levels
PAR_EARTH  = (120,  60,  8)   # deep amber-brown — intro dark base
PAR_AMBER  = (200, 100, 15)   # warm amber — verses / chorus base
PAR_GOLD   = (240, 140, 20)   # warm gold — main chorus, rising
PAR_STRAW  = (255, 220, 80)   # pale straw — final run accent
PAR_BURNT  = ( 80,  40,  5)   # burnt sienna — breaks
PAR_DARK   = ( 30,  15,  2)   # near-dark — re-intro strip

MISS_EARTH = (100,  50,  5)
MISS_AMBER = (180,  90, 10)
MISS_GOLD  = (220, 120, 15)
MISS_STRAW = (240, 200, 60)
MISS_BURNT = ( 60,  30,  3)
MISS_DARK  = ( 20,  10,  1)

# Sharpy colour wheel (ch8): 80=amber, 90=orange, 20=yellow/gold
SH_AMBER = 80
SH_GOLD  = 20   # yellow slot — closest warm wheel colour

# BSW colour wheel (ch8): 26=orange, 32=yellow (gold)
BSW_ORG = 26
BSW_YEL = 32

# ── Scene helpers ──────────────────────────────────────────────

def organism(name, pos_key,
             sh_dim, sh_color,
             bsw_dim, bsw_color,
             par_rgb, miss_rgb,
             sh_frost=210, bsw_frost=180,
             prof_dim=0,
             ni3k_rl=LASER_OFF, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
             ni3k_halo=H_OFF,
             path=""):
    """Unified organism: all movers at same named position, same warm palette.
    NI3K is dark (lasers off) unless explicitly requested.
    Profile provides ambient front fill at DSC throughout.
    """
    sp  = POS[pos_key]
    dsc = POS["DSC"]
    ni3k_pan = sp[6]

    return scene(name, [
        sharpy(pan=sp[0], tilt=sp[1], dim=sh_dim, colormacro=sh_color, frost=sh_frost),
        bsw(pan=sp[2], tilt=sp[3], dim=bsw_dim, color=bsw_color, frost=bsw_frost),
        profile(pan=dsc[4], tilt=dsc[5], dim=prof_dim),
        ni3k(pan=ni3k_pan, t1=64, t2=64, t3=64, dim=0,
             r=0, g=0, b=0, w=0,
             halo=ni3k_halo,
             rl=ni3k_rl, gl=ni3k_gl, bl=ni3k_bl),
        fourbar_solid(*par_rgb),
        miss1(*miss_rgb),
        miss2(*miss_rgb),
    ], path=path)


# ── Section builders ───────────────────────────────────────────

def build_intro(bpm):
    """0:00–1:02 — 32 bars. Slow earthy build. 8 steps × 4 bars.
    Single organism breathing in deep amber. Dim arc 50→140."""
    folder = SONG_TITLE
    positions = ["DSC", "C", "USC", "C", "DSC", "C", "USC", "DSC"]
    dims      = [  50,  65,   80,  95,  110, 120,  130,  140]
    scenes, timing = [], []
    for n, (pos_key, dim) in enumerate(zip(positions, dims)):
        # Scale par/miss with dim (0-200 reference)
        par  = tuple(int(c * dim / 200) for c in PAR_AMBER)
        miss = tuple(int(c * dim / 200) for c in MISS_AMBER)
        scenes.append(organism(
            f"Intro {n+1}", pos_key,
            sh_dim=dim, sh_color=SH_AMBER,
            bsw_dim=dim, bsw_color=BSW_ORG,
            par_rgb=par, miss_rgb=miss,
            sh_frost=220, bsw_frost=190,
            prof_dim=max(20, dim // 3),
            path=folder,
        ))
        timing.append(smooth(bpm, 4))
    return scenes, timing


def build_chorus_1(bpm):
    """1:02–1:33 — 16 bars. First reveal. 8 steps × 2 bars.
    Warm amber opens wide — first full-rig look."""
    folder = SONG_TITLE
    positions = ["SL", "C", "SR", "DSC", "USL", "C", "USR", "DSC"]
    scenes, timing = [], []
    for n, pos_key in enumerate(positions):
        scenes.append(organism(
            f"Chorus1 {n+1}", pos_key,
            sh_dim=160, sh_color=SH_AMBER,
            bsw_dim=160, bsw_color=BSW_ORG,
            par_rgb=PAR_AMBER, miss_rgb=MISS_AMBER,
            sh_frost=180, bsw_frost=150,
            prof_dim=60,
            path=folder,
        ))
        timing.append(smooth(bpm, 2))
    return scenes, timing


def build_bridge(bpm):
    """1:33–1:48 — 8 bars. Inst break. 4 steps × 2 bars.
    Soften, park toward DSC — brief exhale between chorus runs."""
    folder = SONG_TITLE
    positions = ["C", "DSC", "C", "DSC"]
    dims      = [130, 120, 120, 130]
    scenes, timing = [], []
    for n, (pos_key, dim) in enumerate(zip(positions, dims)):
        scenes.append(organism(
            f"Bridge {n+1}", pos_key,
            sh_dim=dim, sh_color=SH_AMBER,
            bsw_dim=dim, bsw_color=BSW_ORG,
            par_rgb=PAR_AMBER, miss_rgb=MISS_AMBER,
            sh_frost=210, bsw_frost=185,
            prof_dim=50,
            path=folder,
        ))
        timing.append(smooth(bpm, 2))
    return scenes, timing


def build_chorus_2(bpm):
    """1:48–2:50 — 32 bars. Main chorus run. 16 steps × 2 bars.
    Amber → gold transition at bar 16. Dim arc 170→220."""
    folder = SONG_TITLE
    positions = (["SL", "C", "SR", "DSC", "USL", "C", "USR", "DSC"] * 2)
    scenes, timing = [], []
    for n, pos_key in enumerate(positions):
        progress = n / 15.0
        dim = int(170 + progress * 50)   # 170→220
        # Shift to gold palette in second half
        gold = (n >= 8)
        sh_color  = SH_GOLD  if gold else SH_AMBER
        bsw_color = BSW_YEL  if gold else BSW_ORG
        par       = PAR_GOLD  if gold else PAR_AMBER
        miss      = MISS_GOLD if gold else MISS_AMBER
        sh_frost  = 150       if gold else 175
        bsw_frost = 120       if gold else 155
        scenes.append(organism(
            f"Chorus2 {n+1}", pos_key,
            sh_dim=dim, sh_color=sh_color,
            bsw_dim=dim, bsw_color=bsw_color,
            par_rgb=par, miss_rgb=miss,
            sh_frost=sh_frost, bsw_frost=bsw_frost,
            prof_dim=70,
            path=folder,
        ))
        timing.append(smooth(bpm, 2))
    return scenes, timing


def build_break_1(bpm):
    """2:50–3:37 — 24 bars. Breakdown. 6 steps × 4 bars.
    Dim 140→60, park at DSC then C. Frost up, slow exhale."""
    folder = SONG_TITLE
    positions = ["DSC", "C", "DSC", "C", "DSC", "DSC"]
    dims      = [  140, 120,  100,  80,   70,   60]
    scenes, timing = [], []
    for n, (pos_key, dim) in enumerate(zip(positions, dims)):
        par  = tuple(int(c * dim / 200) for c in PAR_AMBER)
        miss = tuple(int(c * dim / 200) for c in MISS_AMBER)
        scenes.append(organism(
            f"Break1 {n+1}", pos_key,
            sh_dim=dim, sh_color=SH_AMBER,
            bsw_dim=dim, bsw_color=BSW_ORG,
            par_rgb=par, miss_rgb=miss,
            sh_frost=225, bsw_frost=200,
            prof_dim=max(15, dim // 4),
            path=folder,
        ))
        timing.append(smooth(bpm, 4))
    return scenes, timing


def build_rising(bpm):
    """3:37–4:08 — 16 bars. Building to climax. 8 steps × 2 bars.
    Converging positions, dim 140→240. Prism fires at steps 6–7 (peak 4:04)."""
    folder = SONG_TITLE
    positions = ["USL", "SL", "C", "SR", "USR", "C", "DSC", "DSC"]
    scenes, timing = [], []
    for n, pos_key in enumerate(positions):
        progress  = n / 7.0
        dim       = int(140 + progress * 100)  # 140→240
        gold      = (n >= 4)
        sh_color  = SH_GOLD  if gold else SH_AMBER
        bsw_color = BSW_YEL  if gold else BSW_ORG
        par       = PAR_GOLD  if gold else PAR_AMBER
        miss      = MISS_GOLD if gold else MISS_AMBER
        prism1    = 128 if n >= 6 else 0   # Prism for peak moments
        sh_frost  = int(150 - progress * 50)  # Tighten beam as we rise: 150→100
        bsw_frost = int(130 - progress * 50)

        sp  = POS[pos_key]
        dsc = POS["DSC"]
        scenes.append(scene(f"Rising {n+1}", [
            sharpy(pan=sp[0], tilt=sp[1], dim=dim, colormacro=sh_color,
                   frost=sh_frost, prism1=prism1),
            bsw(pan=sp[2], tilt=sp[3], dim=dim, color=bsw_color, frost=bsw_frost),
            profile(pan=dsc[4], tilt=dsc[5], dim=80),
            ni3k(pan=sp[6], t1=64, t2=64, t3=64, dim=0,
                 r=0, g=0, b=0, w=0, halo=H_OFF,
                 rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF),
            fourbar_solid(*par),
            miss1(*miss),
            miss2(*miss),
        ], path=folder))
        timing.append(smooth(bpm, 2))
    return scenes, timing


def build_break_2(bpm):
    """4:08–5:06 — 28 bars. Re-break + re-intro strip. 7 steps × 4 bars.
    Phase 1 (0–2): dim 150→80, amber. Phase 2 (3–6): near-bare 60→25, burnt.
    The 're-intro' moment — world stripped back to almost nothing."""
    folder = SONG_TITLE
    positions = ["C", "DSC", "DSC", "DSC", "DSC", "DSC", "DSC"]
    dims      = [150,  100,   80,   60,   50,   35,   25]
    scenes, timing = [], []
    for n, (pos_key, dim) in enumerate(zip(positions, dims)):
        stripped = (n >= 3)
        par_base = PAR_BURNT if stripped else PAR_AMBER
        mis_base = MISS_BURNT if stripped else MISS_AMBER
        par  = tuple(int(c * dim / 200) for c in par_base)
        miss = tuple(int(c * dim / 200) for c in mis_base)
        scenes.append(organism(
            f"Break2 {n+1}", pos_key,
            sh_dim=dim, sh_color=SH_AMBER,
            bsw_dim=dim, bsw_color=BSW_ORG,
            par_rgb=par, miss_rgb=miss,
            sh_frost=235, bsw_frost=210,
            prof_dim=max(8, dim // 5),
            path=folder,
        ))
        timing.append(smooth(bpm, 4))
    return scenes, timing


def build_final_run(bpm):
    """5:06–6:54 — 56 bars. Triumphant final chorus. 28 steps × 2 bars.
    NI3K lasers ON throughout. Gold → straw accent in later half.
    Tighter frost, full brightness, wide sweeps."""
    folder = SONG_TITLE
    # 28-position wide sweep cycle
    positions = [
        "USL", "SR",  "DSC", "SL",  "USR", "C",
        "DSL", "C",   "DSR", "DSC", "USL", "SR",
        "DSC", "SL",  "C",   "USR", "DSC", "C",
        "DSL", "SR",  "DSC", "USL", "C",   "DSR",
        "DSC", "SL",  "C",   "DSC",
    ]
    scenes, timing = [], []
    for n, pos_key in enumerate(positions):
        progress  = n / 27.0
        dim       = int(200 + progress * 55)   # 200→255
        straw     = (n >= 16)
        sh_color  = SH_GOLD
        bsw_color = BSW_YEL
        par       = PAR_STRAW  if straw else PAR_GOLD
        miss      = MISS_STRAW if straw else MISS_GOLD
        sh_frost  = 110        # Open, tighter beam
        bsw_frost = 90
        ni3k_halo = H_RGB if straw else H_YEL

        sp  = POS[pos_key]
        dsc = POS["DSC"]
        scenes.append(scene(f"Final {n+1}", [
            sharpy(pan=sp[0], tilt=sp[1], dim=dim, colormacro=sh_color, frost=sh_frost),
            bsw(pan=sp[2], tilt=sp[3], dim=dim, color=bsw_color, frost=bsw_frost),
            profile(pan=dsc[4], tilt=dsc[5], dim=80),
            # NI3K: lasers only (dim=0 kills RGBW LED heads)
            ni3k(pan=sp[6], t1=64, t2=64, t3=64, dim=0,
                 r=0, g=0, b=0, w=0,
                 halo=ni3k_halo,
                 rl=LASER_ON, gl=LASER_ON, bl=LASER_ON),
            fourbar_solid(*par),
            miss1(*miss),
            miss2(*miss),
        ], path=folder))
        timing.append(smooth(bpm, 2))
    return scenes, timing


def build_outro(bpm):
    """6:54–7:08+ — 12 bars. Fade to earth. 3 steps × 4 bars.
    Lasers strobe slow then off. Return to dim amber and dark ground."""
    folder = SONG_TITLE
    positions = ["DSC", "C", "DSC"]
    dims      = [100, 60, 30]
    lasers    = [LASER_STROBE_SLOW, LASER_OFF, LASER_OFF]
    scenes, timing = [], []
    for n, (pos_key, dim, laser) in enumerate(zip(positions, dims, lasers)):
        par  = tuple(int(c * dim / 200) for c in PAR_EARTH)
        miss = tuple(int(c * dim / 200) for c in MISS_EARTH)
        sp  = POS[pos_key]
        dsc = POS["DSC"]
        scenes.append(scene(f"Outro {n+1}", [
            sharpy(pan=sp[0], tilt=sp[1], dim=dim, colormacro=SH_AMBER, frost=230),
            bsw(pan=sp[2], tilt=sp[3], dim=dim, color=BSW_ORG, frost=200),
            profile(pan=dsc[4], tilt=dsc[5], dim=max(8, dim // 4)),
            ni3k(pan=sp[6], t1=64, t2=64, t3=64, dim=0,
                 r=0, g=0, b=0, w=0, halo=H_OFF,
                 rl=laser, gl=laser, bl=laser),
            fourbar_solid(*par),
            miss1(*miss),
            miss2(*miss),
        ], path=folder))
        timing.append(smooth(bpm, 4))
    return scenes, timing


# ── Build show ─────────────────────────────────────────────────
print(f"  BPM: {BPM}")

SECTIONS = [
    ("INTRO",    build_intro),
    ("CHORUS_1", build_chorus_1),
    ("BRIDGE",   build_bridge),
    ("CHORUS_2", build_chorus_2),
    ("BREAK_1",  build_break_1),
    ("RISING",   build_rising),
    ("BREAK_2",  build_break_2),
    ("FINAL",    build_final_run),
    ("OUTRO",    build_outro),
]

all_scenes, all_timing = [], []
ms_per_bar = bpm_to_ms(BPM, 1) * 4

for sec_name, builder in SECTIONS:
    sc, tm = builder(BPM)
    bars = sum((fi + ho) / ms_per_bar for fi, ho in tm)
    print(f"  Building {sec_name:12s} ({len(sc):2d} scenes, {bars:.0f} bars)")
    all_scenes.extend(sc)
    all_timing.extend(tm)

total_s = sum(fi + ho for fi, ho in all_timing) / 1000
print(f"\nTotal scenes: {len(all_scenes)}")
print(f"Total duration: {total_s:.1f}s (target: ~428s)")

chaser  = make_chaser(SONG_TITLE, list(range(len(all_scenes))), all_timing, path="Shows")
outpath = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")
write_workspace(outpath, all_scenes, [chaser], bpm=BPM)
print(f"\nWrote {outpath}")
print(f"  Scenes: {len(all_scenes)}, Chasers: 1 ({len(all_timing)} total steps)")
