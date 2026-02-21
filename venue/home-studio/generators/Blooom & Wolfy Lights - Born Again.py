#!/usr/bin/env python3
"""
Show Generator: Blooom & Wolfy Lights - Born Again
BPM: 174 | Duration: ~2:42 (160s) | Venue: home-studio
Genre: Drum & Bass — high-energy void-to-light arc

DnB design: independent mover chase (Sharpy leads, BSW lags 3 steps),
1-bar hold snaps at drops, strobe on every 8th bar, NI3K heads spinning.

Structure (116 bars ≈ 160s):
  VERSE     0:00–0:24   16 bars   Near-dark void,       4  × smooth(174,4)
  DROP_1    0:24–1:19   40 bars   Chase drop,           40 × hold(174,1)
  BREAK     1:19–1:48   20 bars   Rose/magenta pull-back, 5 × smooth(174,4)
  BRIDGE    1:48–2:03   12 bars   Final void,            3 × smooth(174,4)
  DROP_2    2:03–2:36   24 bars   Born Again catharsis, 24 × hold(174,1)
  END       2:36–2:42    4 bars   Violet return,         2 × smooth(174,2)
  Total: 78 scenes ≈ 160s

Note on BPM: analysis pipeline detected 87 BPM (half-time). Actual is 174 DnB.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from showlib import (
    sharpy, bsw, profile, ni3k, fourbar_solid, miss1, miss2,
    scene, make_chaser, write_workspace,
    smooth, hold, bpm_to_ms,
    LASER_ON, LASER_OFF, LASER_STROBE_SLOW,
    H_OFF, H_PNK, H_RGB,
    SHARPY_OPEN, SHARPY_STROBE_MED,
    BSW_SHUT_OPEN, BSW_SHUT_STROBE_SLOW,
    require_research_brief, build_creative_context,
    load_focus_position_tuples,
)

# ── Paths ──────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR    = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
SONG_STEM    = "Blooom & Wolfy Lights - Born Again"
SONG_TITLE   = "Born Again"
BPM          = 174

# ── Research gate ──────────────────────────────────────────────
BRIEF    = require_research_brief(SONG_STEM, PROJECT_ROOT, venue_dir=VENUE_DIR)
CREATIVE = build_creative_context(BRIEF, song_stem=SONG_STEM)
print(f"Creative thesis: {BRIEF['thesis']}")
print(f"Generating show: {SONG_STEM}")

# ── Venue positions ────────────────────────────────────────────
POS = load_focus_position_tuples(PROJECT_ROOT, VENUE_DIR)

# ── Colour palette ─────────────────────────────────────────────
# Arc: void → violet → rose-magenta → white catharsis → return to violet

# PAR (4BAR + missyees) RGB
PAR_VOID    = (  8,   2,  20)   # near-black violet-tinted void
PAR_VIOLET  = ( 30,   5,  80)   # deep violet — primary colour world
PAR_PURPLE  = ( 60,  10, 120)   # richer purple — drop bloom
PAR_ROSE    = (120,  30,  80)   # warm rose — break transition
PAR_MAGENTA = (160,  20, 100)   # rose-magenta — break peak
PAR_WHITE   = (255, 230, 240)   # warm white — catharsis ONLY

MISS_VOID    = (  5,   1,  15)
MISS_VIOLET  = ( 25,   5,  60)
MISS_PURPLE  = ( 50,   8,  90)
MISS_ROSE    = ( 90,  20,  60)
MISS_MAGENTA = (120,  15,  75)
MISS_WHITE   = (240, 210, 230)

# Sharpy colour wheel (ch8)
SH_PURPLE = 50   # purple/violet
SH_PINK   = 60   # pink — closest to rose
SH_WHITE  = 0    # white — catharsis only

# BSW colour wheel (ch8)
BSW_MAG_VAL   = 50  # magenta
BSW_PINK_VAL  = 62  # pink
BSW_WHITE_VAL = 0   # white


# ── Scene helpers ────────────────────────────────────────────────

def soul(name, pos_key,
         sh_dim, sh_color,
         bsw_dim, bsw_color,
         par_rgb, miss_rgb,
         sh_frost=210, bsw_frost=180,
         prof_dim=0,
         ni3k_halo=H_OFF,
         ni3k_rl=LASER_OFF, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
         path=""):
    """Unified: Sharpy + BSW at same position. For atmospheric sections
    (VERSE, BREAK, BRIDGE) where unified movement and smooth sweeps are right.
    """
    sp  = POS[pos_key]
    dsc = POS["DSC"]
    return scene(name, [
        sharpy(pan=sp[0], tilt=sp[1], dim=sh_dim, colormacro=sh_color, frost=sh_frost),
        bsw(pan=sp[2], tilt=sp[3], dim=bsw_dim, color=bsw_color, frost=bsw_frost),
        profile(pan=dsc[4], tilt=dsc[5], dim=prof_dim),
        ni3k(pan=sp[6], t1=64, t2=64, t3=64, dim=0,
             r=0, g=0, b=0, w=0,
             halo=ni3k_halo,
             rl=ni3k_rl, gl=ni3k_gl, bl=ni3k_bl),
        fourbar_solid(*par_rgb),
        miss1(*miss_rgb),
        miss2(*miss_rgb),
    ], path=path)


def stab(name, sh_pos, bsw_pos,
         sh_dim, sh_color,
         bsw_dim, bsw_color,
         par_rgb, miss_rgb,
         sh_frost=100, bsw_frost=80,
         sh_strobe=SHARPY_OPEN, bsw_shutter=BSW_SHUT_OPEN,
         prof_dim=0,
         ni3k_t=64, ni3k_halo=H_OFF,
         ni3k_rl=LASER_OFF, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
         path=""):
    """Chase: Sharpy and BSW at independent positions.
    BSW lags Sharpy by 3 steps in the position cycle — creates chase illusion.
    NI3K follows Sharpy pan, heads in rotation mode during drops (ni3k_t=160).
    Strobe via sh_strobe/bsw_shutter on accent bars.
    """
    sp_sh  = POS[sh_pos]
    sp_bsw = POS[bsw_pos]
    dsc    = POS["DSC"]
    return scene(name, [
        sharpy(pan=sp_sh[0], tilt=sp_sh[1],
               dim=sh_dim, colormacro=sh_color,
               frost=sh_frost, strobe=sh_strobe),
        bsw(pan=sp_bsw[2], tilt=sp_bsw[3],
            dim=bsw_dim, color=bsw_color,
            frost=bsw_frost, shutter=bsw_shutter),
        profile(pan=dsc[4], tilt=dsc[5], dim=prof_dim),
        ni3k(pan=sp_sh[6], t1=ni3k_t, t2=ni3k_t, t3=ni3k_t, dim=0,
             r=0, g=0, b=0, w=0,
             halo=ni3k_halo,
             rl=ni3k_rl, gl=ni3k_gl, bl=ni3k_bl),
        fourbar_solid(*par_rgb),
        miss1(*miss_rgb),
        miss2(*miss_rgb),
    ], path=path)


# ── Section builders ────────────────────────────────────────────

def build_verse(bpm):
    """0:00–0:24 — 16 bars. Near-dark void. 4 × smooth(174,4) = 22s.
    The void before birth. Nearly still — DSC→DSC→C→DSC.
    Dim arc 20→60. Heavy frost (235/210). Profile 5–15."""
    folder = SONG_TITLE
    positions = ["DSC", "DSC", "C", "DSC"]
    dims      = [20, 35, 50, 60]
    scenes, timing = [], []
    for n, (pos_key, dim) in enumerate(zip(positions, dims)):
        par  = tuple(int(c * dim / 80) for c in PAR_VIOLET)
        miss = tuple(int(c * dim / 80) for c in MISS_VIOLET)
        scenes.append(soul(
            f"Verse {n+1}", pos_key,
            sh_dim=dim, sh_color=SH_PURPLE,
            bsw_dim=dim, bsw_color=BSW_MAG_VAL,
            par_rgb=par, miss_rgb=miss,
            sh_frost=235, bsw_frost=210,
            prof_dim=max(5, dim // 4),
            ni3k_halo=H_OFF,
            path=folder,
        ))
        timing.append(smooth(bpm, 4))
    return scenes, timing


def build_drop_1(bpm):
    """0:24–1:19 — 40 bars. Chase drop. 40 × hold(174,1) = 55s.
    Sharpy leads full-room sweep. BSW lags 3 steps — two beams chasing.
    Strobe bursts every 8 bars. NI3K heads spinning, H_PNK halo.
    Lasers arm at step 20 (halfway through drop). Dim arc 160→209.
    Frost tightens 175→125 (beams sharpen as energy peaks)."""
    folder = SONG_TITLE

    # 40-step Sharpy cycle: full room sweep + specials at intentional moments
    sh_cycle = [
        # Bars 0–19 (first pass — violet world)
        "DSC", "C",   "SL",  "USR", "SR",
        "DJ",  "USL", "C",   "DSR", "DSC",   # DJ at step 5 — performer focus
        "SL",  "SR",  "USC", "DANCE", "DSR",  # DANCE at step 13 — floor hit
        "C",   "USL", "USR", "DSL", "DSC",
        # Bars 20–39 (second pass — purple world, lasers armed)
        "C",   "SL",  "DSC", "SR",  "USL",
        "DJ",  "USR", "C",   "DSL", "DSC",   # DJ at step 25 — mid-drop anchor
        "SL",  "SR",  "C",   "DANCE", "DSC",  # DANCE at step 33 — energy out
        "USL", "USR", "DSL", "DSR", "DSC",
    ]
    bsw_cycle = sh_cycle[3:] + sh_cycle[:3]  # BSW lags 3 steps behind Sharpy

    scenes, timing = [], []
    for n in range(40):
        is_accent = (n % 8 == 7)             # strobe on bars 7,15,23,31,39
        dim       = int(160 + n * 1.25)      # 160→209
        par       = PAR_PURPLE if n >= 20 else PAR_VIOLET
        miss      = MISS_PURPLE if n >= 20 else MISS_VIOLET
        sh_frost  = int(175 - (n / 39.0) * 50)   # 175→125
        bsw_frost = int(150 - (n / 39.0) * 50)   # 150→100
        sh_strobe   = SHARPY_STROBE_MED   if is_accent else SHARPY_OPEN
        bsw_shutter = BSW_SHUT_STROBE_SLOW if is_accent else BSW_SHUT_OPEN
        ni3k_rl = LASER_ON if n >= 20 else LASER_OFF
        ni3k_gl = LASER_ON if n >= 20 else LASER_OFF
        ni3k_bl = LASER_ON if n >= 20 else LASER_OFF

        scenes.append(stab(
            f"Drop1 {n+1}", sh_cycle[n], bsw_cycle[n],
            sh_dim=dim, sh_color=SH_PURPLE,
            bsw_dim=dim, bsw_color=BSW_MAG_VAL,
            par_rgb=par, miss_rgb=miss,
            sh_frost=sh_frost, bsw_frost=bsw_frost,
            sh_strobe=sh_strobe, bsw_shutter=bsw_shutter,
            prof_dim=max(30, dim // 4),
            ni3k_t=160, ni3k_halo=H_PNK,
            ni3k_rl=ni3k_rl, ni3k_gl=ni3k_gl, ni3k_bl=ni3k_bl,
            path=folder,
        ))
        timing.append(hold(bpm, 1))
    return scenes, timing


def build_break(bpm):
    """1:19–1:48 — 20 bars. Rose-magenta pull-back. 5 × smooth(174,4) = 28s.
    Energy strips back after DROP_1. Colour shifts from violet to rose-magenta.
    Dim arc 155→110. Soul() unified movement — the rigs breathes together.
    H_PNK halo activates — first time halo joins the rig."""
    folder = SONG_TITLE
    positions = ["SL", "C", "SR", "DSC", "C"]
    dims      = [155, 145, 135, 120, 110]
    scenes, timing = [], []
    for n, (pos_key, dim) in enumerate(zip(positions, dims)):
        rose      = (n >= 2)
        par       = PAR_MAGENTA if rose else PAR_ROSE
        miss      = MISS_MAGENTA if rose else MISS_ROSE
        bsw_color = BSW_PINK_VAL if rose else BSW_MAG_VAL
        scenes.append(soul(
            f"Break {n+1}", pos_key,
            sh_dim=dim, sh_color=SH_PINK,
            bsw_dim=dim, bsw_color=bsw_color,
            par_rgb=par, miss_rgb=miss,
            sh_frost=180, bsw_frost=155,
            prof_dim=50,
            ni3k_halo=H_PNK,
            path=folder,
        ))
        timing.append(smooth(bpm, 4))
    return scenes, timing


def build_bridge(bpm):
    """1:48–2:03 — 12 bars. Final void. 3 × smooth(174,4) = 17s.
    Strip to near-darkness. Parked at DSC, heavy frost (240/220).
    Dim arc 80→40→20. Step 3 at dim 20 — last dark before the light."""
    folder = SONG_TITLE
    positions = ["DSC", "DSC", "DSC"]
    dims      = [80, 40, 20]
    scenes, timing = [], []
    for n, (pos_key, dim) in enumerate(zip(positions, dims)):
        par  = tuple(int(c * dim / 100) for c in PAR_VIOLET)
        miss = tuple(int(c * dim / 100) for c in MISS_VIOLET)
        scenes.append(soul(
            f"Bridge {n+1}", pos_key,
            sh_dim=dim, sh_color=SH_PURPLE,
            bsw_dim=dim, bsw_color=BSW_MAG_VAL,
            par_rgb=par, miss_rgb=miss,
            sh_frost=240, bsw_frost=220,
            prof_dim=max(5, dim // 5),
            ni3k_halo=H_OFF,
            path=folder,
        ))
        timing.append(smooth(bpm, 4))
    return scenes, timing


def build_drop_2(bpm):
    """2:03–2:36 — 24 bars. Born Again catharsis. 24 × hold(174,1) = 33s.

    Steps 0–11 (RISE): violet→rose→magenta builds from void. H_PNK halo.
    Steps 12–23 (BORN AGAIN): SH_WHITE, PAR_WHITE, H_RGB, all lasers ON.
      Strobe on EVERY bar — the blazing white catharsis moment.
      DISCO_BALL + CEIL woven into position cycle (beams scatter, shafts descend).
    """
    folder = SONG_TITLE

    # 24-step Sharpy cycle — rise, then catharsis with DISCO_BALL + CEIL
    sh_cycle = [
        # Steps 0–11 (rise from void)
        "DSC", "C",   "SL",  "USL",        "SR",  "C",
        "USR", "DSC", "SL",  "SR",          "C",   "DSC",
        # Steps 12–23 (BORN AGAIN — white catharsis, widest sweeps + specials)
        "DISCO_BALL", "C",          "SL",  "USL",  "SR",   "CEIL",
        "DSC",        "SL",  "DISCO_BALL",  "CEIL", "DSR",  "DSC",
    ]
    bsw_cycle = sh_cycle[3:] + sh_cycle[:3]  # BSW lags 3 steps

    dims = [
        # Rise (steps 0–11): void → near-full
         80, 100, 130, 155, 175, 195,
        210, 220, 230, 240, 248, 253,
        # Catharsis (steps 12–23): full blast
        255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255,
    ]

    scenes, timing = [], []
    for n in range(24):
        catharsis = (n >= 12)
        if catharsis:
            sh_color    = SH_WHITE
            bsw_color   = BSW_WHITE_VAL
            par         = PAR_WHITE
            miss        = MISS_WHITE
            ni3k_halo   = H_RGB
            ni3k_rl     = LASER_ON
            ni3k_gl     = LASER_ON
            ni3k_bl     = LASER_ON
            sh_frost    = 120
            bsw_frost   = 90
            prof_dim    = 90
            sh_strobe   = SHARPY_STROBE_MED    # every bar — relentless white blast
            bsw_shutter = BSW_SHUT_STROBE_SLOW
        else:
            sh_color    = SH_PINK
            bsw_color   = BSW_PINK_VAL
            par         = PAR_ROSE if n < 3 else PAR_MAGENTA
            miss        = MISS_ROSE if n < 3 else MISS_MAGENTA
            ni3k_halo   = H_PNK
            ni3k_rl     = LASER_OFF
            ni3k_gl     = LASER_OFF
            ni3k_bl     = LASER_OFF
            sh_frost    = int(200 - n * 10)   # 200→110 (tightens to peak)
            bsw_frost   = int(175 - n * 10)   # 175→65
            prof_dim    = int(20 + n * 8)     # 20→108
            sh_strobe   = SHARPY_OPEN
            bsw_shutter = BSW_SHUT_OPEN

        scenes.append(stab(
            f"Drop2 {n+1}", sh_cycle[n], bsw_cycle[n],
            sh_dim=dims[n], sh_color=sh_color,
            bsw_dim=dims[n], bsw_color=bsw_color,
            par_rgb=par, miss_rgb=miss,
            sh_frost=sh_frost, bsw_frost=bsw_frost,
            sh_strobe=sh_strobe, bsw_shutter=bsw_shutter,
            prof_dim=prof_dim,
            ni3k_t=160, ni3k_halo=ni3k_halo,
            ni3k_rl=ni3k_rl, ni3k_gl=ni3k_gl, ni3k_bl=ni3k_bl,
            path=folder,
        ))
        timing.append(hold(bpm, 1))
    return scenes, timing


def build_end(bpm):
    """2:36–2:42 — 4 bars. Violet return. 2 × smooth(174,2) = 5.5s.
    White drains. Laser STROBE_SLOW step 1, LASER_OFF step 2. Violet reclaims."""
    folder = SONG_TITLE
    sp  = POS["DSC"]
    dsc = POS["DSC"]

    s1 = scene("End 1", [
        sharpy(pan=sp[0], tilt=sp[1], dim=120, colormacro=SH_PURPLE, frost=210),
        bsw(pan=sp[2], tilt=sp[3], dim=120, color=BSW_MAG_VAL, frost=180),
        profile(pan=dsc[4], tilt=dsc[5], dim=30),
        ni3k(pan=sp[6], t1=64, t2=64, t3=64, dim=0,
             r=0, g=0, b=0, w=0,
             halo=H_OFF,
             rl=LASER_STROBE_SLOW, gl=LASER_STROBE_SLOW, bl=LASER_STROBE_SLOW),
        fourbar_solid(*PAR_PURPLE),
        miss1(*MISS_PURPLE),
        miss2(*MISS_PURPLE),
    ], path=folder)

    s2 = scene("End 2", [
        sharpy(pan=sp[0], tilt=sp[1], dim=60, colormacro=SH_PURPLE, frost=230),
        bsw(pan=sp[2], tilt=sp[3], dim=60, color=BSW_MAG_VAL, frost=200),
        profile(pan=dsc[4], tilt=dsc[5], dim=10),
        ni3k(pan=sp[6], t1=64, t2=64, t3=64, dim=0,
             r=0, g=0, b=0, w=0,
             halo=H_OFF,
             rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF),
        fourbar_solid(*PAR_VIOLET),
        miss1(*MISS_VIOLET),
        miss2(*MISS_VIOLET),
    ], path=folder)

    return [s1, s2], [smooth(bpm, 2), smooth(bpm, 2)]


# ── Build show ──────────────────────────────────────────────────
print(f"  BPM: {BPM}")

SECTIONS = [
    ("VERSE",   build_verse),
    ("DROP_1",  build_drop_1),
    ("BREAK",   build_break),
    ("BRIDGE",  build_bridge),
    ("DROP_2",  build_drop_2),
    ("END",     build_end),
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
print(f"Total duration: {total_s:.1f}s (target: ~160s)")

chaser  = make_chaser(SONG_TITLE, list(range(len(all_scenes))), all_timing,
                      run_order="SingleShot", path="Shows")
outpath = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")
write_workspace(outpath, all_scenes, [chaser], bpm=BPM)
print(f"\nWrote {outpath}")
print(f"  Scenes: {len(all_scenes)}, Chasers: 1 ({len(all_timing)} total steps)")
