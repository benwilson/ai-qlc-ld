#!/usr/bin/env python3
"""
Show Generator: PhatAdam - Never Cared Enough (v2 - Beat-Synced)
================================================================
BPM: 133 | Duration: ~2:28 | Genre: Happy / upbeat electronic

v2 Creative Direction:
  - EVERYTHING to the beat: pars snap on every beat (or 2/4 in slower sections)
  - 4BAR + Missyees = unified wash unit (Missyees extend the 4BAR chase/pattern)
  - Par patterns rotate per section: chase → pairs → solid → alternating
  - Movers reposition every 4 beats, color/effect changes every beat
  - Neon pop palette: hot pink, electric blue, vivid green, magenta, yellow, orange
  - Strobe accents on chorus downbeats and big moments (more than v1)
  - NI3K halo: beat-synced in verses/tease, hardware jump mode in choruses
  - All timing: FadeIn=0 instant snaps for maximum punch

Song Structure (from allin1 analysis):
  0:00 - 0:14  intro     (8 bars)   "Tease" — chase pattern, pars building, movers dark
  0:14 - 0:29  intro     (8 bars)   "Opens up" — pairs pattern, movers come alive
  0:29 - 0:43  inst      (8 bars)   "Full party" — chase every beat, movers dancing
  0:43 - 0:59  chorus    (9 bars)   "Chorus 1" — chase+solid, strobe accents, jump halo
  0:59 - 1:12  verse     (7 bars)   "Pull back" — pairs every 2 beats, frosted movers
  1:12 - 1:26  break     (8 bars)   "Strobe build" — accelerating 4→2→1 beat, strobe ramp
  1:26 - 1:44  chorus    (10 bars)  "Chorus 2" — prisms, 6-color cycle, strobe accents
  1:44 - 2:11  chorus    (15 bars)  "Chorus 3" — maximum variety, widest moves, fastest
  2:11 - 2:28  chorus    (9 bars)   "Climax" — all strobes, all lasers, rotating NI3K
  2:28 - end   end                  "Snap to black"
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from showlib import *

BPM = 133
BEAT_MS = bpm_to_ms(BPM, 1)  # ~451ms

# =============================================================================
# NEON PALETTE
# =============================================================================

HOT_PINK    = (255, 20, 100)
ELEC_BLUE   = (0, 100, 255)
VIVID_GREEN = (0, 255, 80)
NEON_MAG    = (255, 0, 200)
NEON_YELLOW = (255, 220, 0)
NEON_ORANGE = (255, 100, 0)
BRIGHT_WHITE = (255, 255, 255)

NEON_4 = [HOT_PINK, ELEC_BLUE, VIVID_GREEN, NEON_MAG]
NEON_6 = [HOT_PINK, ELEC_BLUE, VIVID_GREEN, NEON_MAG, NEON_YELLOW, NEON_ORANGE]

# Neon RGB → BSW color wheel mapping
BSW_FOR = {
    HOT_PINK: BSW_PINK, ELEC_BLUE: BSW_BLUE, VIVID_GREEN: BSW_GREEN,
    NEON_MAG: BSW_MAG, NEON_YELLOW: BSW_YELLOW, NEON_ORANGE: BSW_ORANGE,
    BRIGHT_WHITE: BSW_WHITE,
}

# Neon RGB → Sharpy color macro mapping
SHARPY_FOR = {
    HOT_PINK: SHARPY_PINK, ELEC_BLUE: SHARPY_BLUE, VIVID_GREEN: SHARPY_GREEN,
    NEON_MAG: SHARPY_PURPLE, NEON_YELLOW: SHARPY_YELLOW, NEON_ORANGE: SHARPY_ORANGE,
    BRIGHT_WHITE: SHARPY_WHITE,
}

# Neon RGB → Profile color wheel mapping
PROF_FOR = {
    HOT_PINK: PROF_PINK, ELEC_BLUE: PROF_BLUE, VIVID_GREEN: PROF_GREEN,
    NEON_MAG: PROF_PINK, NEON_YELLOW: PROF_YELLOW, NEON_ORANGE: PROF_ORANGE,
    BRIGHT_WHITE: PROF_WHITE,
}

# Neon RGB → NI3K halo mapping
HALO_FOR = {
    HOT_PINK: H_PNK, ELEC_BLUE: H_BLU, VIVID_GREEN: H_GRN,
    NEON_MAG: H_PNK, NEON_YELLOW: H_YEL, NEON_ORANGE: H_RED,
    BRIGHT_WHITE: H_RGB,
}

# =============================================================================
# MOVER POSITIONS — (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt)
# =============================================================================

POS = {
    "C": (153, 0,   7, 19,  0, 123),   # center
    "L": (100, 10,  80, 25,  50, 110),  # left
    "R": (210, 10,  190, 10, 200, 110), # right
    "W": (220, 20,  80, 30,  50, 90),   # wide
    "H": (153, 40,  7, 50,   0, 80),    # high
    "A": (153, 230, 7, 0,    0, 150),   # audience
    "X": (80, 5,    200, 15, 200, 130), # cross
}

# Position sequences for different section energies
POS_DANCE = ["C", "L", "R", "W", "X", "H", "A", "C"]
POS_WIDE  = ["W", "X", "A", "H", "W", "L", "R", "X"]
POS_BIG   = ["C", "W", "X", "A", "H", "L", "R", "C",
             "X", "W", "H", "A", "L", "R", "C", "W"]

# =============================================================================
# SCENE BUILDING WITH DEDUP
# =============================================================================

folder = "Never Cared Enough"
scenes = []
scene_cache = {}
dedup_hits = 0
steps = []


def add_scene(name, *fixtures):
    """Add scene with dedup — identical channel values reuse existing scene."""
    global dedup_hits
    flat = []
    for f in fixtures:
        if isinstance(f, list):
            flat.extend(f)
        else:
            flat.append(f)
    flat.sort(key=lambda x: x[0])
    key = tuple((fid, tuple(tuple(cv) for cv in chs)) for fid, chs in flat)
    if key in scene_cache:
        dedup_hits += 1
        return scene_cache[key]
    idx = len(scenes)
    scenes.append(scene(name, *fixtures, path=folder))
    scene_cache[key] = idx
    return idx


def beat_step(scene_idx, beats=1):
    """Add chaser step: instant snap (FadeIn=0), hold for N beats."""
    ms = bpm_to_ms(BPM, beats)
    steps.append((scene_idx, (0, ms)))


# =============================================================================
# FIXTURE BUILDERS
# =============================================================================

def mkvrs(pos_key, color, dim=255, frost=0, focus=128,
          prism_s=0, p1r_s=0, prism_b=0, prot_b=0, prism_p=0,
          s_strobe=SHARPY_OPEN, b_shutter=BSW_SHUT_OPEN):
    """Build all 3 movers from position key + color."""
    sp, st, bp, bt, pp, pt = POS[pos_key]
    bsw_c = BSW_FOR.get(color, BSW_WHITE)
    sharpy_c = SHARPY_FOR.get(color, SHARPY_WHITE)
    prof_c = PROF_FOR.get(color, PROF_WHITE)
    s = sharpy(pan=sp, tilt=st, strobe=s_strobe, dim=dim,
               frost=frost, focus=focus, prism1=prism_s, p1r=p1r_s,
               colormacro=sharpy_c)
    b = bsw(pan=bp, tilt=bt, color=bsw_c, shutter=b_shutter,
            dim=dim, prism=prism_b, prot=prot_b, focus=focus)
    p = profile(pan=pp, tilt=pt, dim=dim, prism=prism_p, focus=focus,
                color=prof_c)
    return s, b, p


def par_chase(color, beat_idx, master=255):
    """4BAR: one par lit per beat, cycling. Missyees alternate each beat."""
    r, g, b = color
    v = [(0, 0, 0)] * 4
    v[beat_idx % 4] = (r, g, b)
    fb = fourbar(v[0][0], v[0][1], v[0][2], v[1][0], v[1][1], v[1][2],
                 v[2][0], v[2][1], v[2][2], v[3][0], v[3][1], v[3][2],
                 master=master)
    if beat_idx % 2 == 0:
        return fb, miss1(r, g, b, master=master), miss2(0, 0, 0, master=0)
    else:
        return fb, miss1(0, 0, 0, master=0), miss2(r, g, b, master=master)


def par_pairs(c1, c2, flip=False, master=255):
    """4BAR: P1+P3=c1, P2+P4=c2 (or flipped). Missyees split."""
    if flip:
        c1, c2 = c2, c1
    fb = fourbar_pairs(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], master=master)
    return fb, miss1(*c1, master=master), miss2(*c2, master=master)


def par_solid(color, master=255):
    """All 4BAR pars + both Missyees: same color, maximum impact."""
    r, g, b = color
    return (fourbar_solid(r, g, b, master=master),
            miss1(r, g, b, master=master),
            miss2(r, g, b, master=master))


def mkni(color, dim=255, halo_mode="sync",
         rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF,
         t1=64, t2=64, t3=64, strobe=0):
    """Build NI3K fixture with color-matched halo."""
    r, g, b = color
    halo_map = {"sync": HALO_FOR.get(color, H_RGB),
                "jump_fast": H_JUMP_FAST, "jump_med": H_JUMP_MED,
                "jump_slow": H_JUMP_SLOW, "off": H_OFF}
    halo = halo_map.get(halo_mode, H_RGB)
    return ni3k(pan=128, t1=t1, t2=t2, t3=t3, r=r, g=g, b=b,
                halo=halo, dim=dim, strobe=strobe, rl=rl, gl=gl, bl=bl)


# =============================================================================
# BLACKOUT (always scene 0)
# =============================================================================

add_scene("Blackout", *blackout_all())


# =============================================================================
# TEASE — 8 bars, pars every bar (4 beats)
# Chase pattern building from dim to moderate. Movers dark. Soft NI3K.
# =============================================================================

for bar in range(8):
    c = NEON_4[bar % 4]
    fb, m1, m2 = par_chase(c, bar, master=60 + bar * 20)
    s, b, p = mkvrs("C", c, dim=0)
    n = mkni(c, dim=40 + bar * 12, halo_mode="sync")
    idx = add_scene(f"Tease-{bar+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=4)


# =============================================================================
# OPENS UP — 8 bars, pars every 2 beats, movers every bar (brightening)
# Pairs pattern with complementary colors. Movers fade in.
# =============================================================================

open_positions = POS_DANCE  # 8 positions for 8 bars

for i in range(16):
    bar = i // 2
    half = i % 2
    c1 = NEON_6[i % 6]
    c2 = NEON_6[(i + 3) % 6]
    fb, m1, m2 = par_pairs(c1, c2, flip=(half == 1), master=140 + bar * 14)
    pos = open_positions[bar % len(open_positions)]
    mc = NEON_4[bar % 4]
    s, b, p = mkvrs(pos, mc, dim=60 + bar * 24)
    n = mkni(c1, dim=80 + bar * 20, halo_mode="sync")
    idx = add_scene(f"Open-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=2)


# =============================================================================
# FULL PARTY — 8 bars, pars EVERY BEAT, movers reposition every bar
# Chase pattern cycling 4 neon colors. Mover color shifts every beat.
# =============================================================================

party_positions = POS_DANCE

for beat in range(32):
    bar = beat // 4
    bib = beat % 4
    c = NEON_4[beat % 4]
    mc = NEON_4[beat % 4]
    pos = party_positions[bar % len(party_positions)]
    fb, m1, m2 = par_chase(c, beat)
    s, b, p = mkvrs(pos, mc, dim=255)
    n = mkni(c, dim=220, halo_mode="sync")
    idx = add_scene(f"Party-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# CHORUS 1 — 9 bars, pars EVERY BEAT
# Chase + solid hits. Strobe accent on beat 1 of every other bar.
# NI3K: jump mode. NI3K tilts start moving.
# =============================================================================

ch1_positions = POS_DANCE + ["X"]  # 9 for 9 bars

for beat in range(36):
    bar = beat // 4
    bib = beat % 4
    c = NEON_4[beat % 4]
    pos = ch1_positions[bar % len(ch1_positions)]
    t1 = 50 + bar * 5
    t2 = 70 + bar * 3
    t3 = 60 + bar * 4

    # Beat 1 of every other bar: solid color hit + strobe accent
    if bib == 0 and bar % 2 == 0:
        fb, m1, m2 = par_solid(c)
        s, b, p = mkvrs(pos, c,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)
        n = mkni(c, dim=255, halo_mode="jump_med", t1=t1, t2=t2, t3=t3)
    else:
        fb, m1, m2 = par_chase(c, beat)
        s, b, p = mkvrs(pos, c)
        n = mkni(c, dim=255, halo_mode="jump_med", t1=t1, t2=t2, t3=t3)

    idx = add_scene(f"Ch1-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# VERSE — 7 bars, pars every 2 beats, movers every 8 beats (slow)
# Pairs pattern, softer. Movers frosted. NI3K beat-synced.
# =============================================================================

verse_positions = ["C", "L", "R", "C"]

for i in range(14):
    bar = i // 2
    half = i % 2
    c1 = NEON_4[i % 4]
    c2 = NEON_4[(i + 2) % 4]
    fb, m1, m2 = par_pairs(c1, c2, flip=(half == 1), master=160)

    beat_num = i * 2
    pos_idx = beat_num // 8
    pos = verse_positions[pos_idx % len(verse_positions)]
    mc = NEON_4[i % 4]
    s, b, p = mkvrs(pos, mc, dim=140, frost=150, focus=200)
    n = mkni(c1, dim=100, halo_mode="sync")
    idx = add_scene(f"Verse-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=2)


# =============================================================================
# BREAK — 8 bars, strobe buildup with accelerating par rate
# Bars 1-3: pars every 4 beats, slow strobe on movers
# Bars 4-5: pars every 2 beats, medium strobe
# Bars 6-8: pars every beat, fast strobe, building to white
# =============================================================================

# Bars 1-3: slow buildup (3 steps × 4 beats each)
build_slow_colors = [HOT_PINK, ELEC_BLUE, NEON_MAG]
for bar in range(3):
    c = build_slow_colors[bar]
    fb, m1, m2 = par_solid(c, master=100 + bar * 30)
    s, b, p = mkvrs("C", BRIGHT_WHITE, dim=120 + bar * 30,
                     s_strobe=SHARPY_STROBE_SLOW, b_shutter=20)
    n = mkni(c, dim=80 + bar * 30, halo_mode="sync")
    idx = add_scene(f"Build-S{bar+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=4)

# Bars 4-5: medium buildup (4 steps × 2 beats each)
for i in range(4):
    c = NEON_4[i % 4]
    fb, m1, m2 = par_chase(c, i, master=180)
    s, b, p = mkvrs("C", BRIGHT_WHITE, dim=200,
                     s_strobe=SHARPY_STROBE_MED, b_shutter=70)
    n = mkni(c, dim=160, halo_mode="sync")
    idx = add_scene(f"Build-M{i+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=2)

# Bars 6-8: fast buildup (12 steps × 1 beat each)
for beat in range(12):
    c = NEON_6[beat % 6]
    fb, m1, m2 = par_chase(c, beat)
    s, b, p = mkvrs("C", BRIGHT_WHITE, dim=240,
                     s_strobe=SHARPY_STROBE_FAST,
                     b_shutter=BSW_SHUT_STROBE_FAST)
    n = mkni(BRIGHT_WHITE, dim=220, halo_mode="jump_fast")
    idx = add_scene(f"Build-F{beat+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# CHORUS 2 — 10 bars, pars EVERY BEAT, 6-color cycle
# Prisms spinning on all movers. Strobe accents on beat 1 every other bar.
# NI3K: jump fast, tilts dancing.
# =============================================================================

for beat in range(40):
    bar = beat // 4
    bib = beat % 4
    c = NEON_6[beat % 6]
    pos = POS_WIDE[bar % len(POS_WIDE)]
    t1 = 40 + (beat % 5) * 12
    t2 = 70 + (beat % 3) * 15
    t3 = 55 + (beat % 7) * 8

    if bib == 0 and bar % 2 == 0:
        # Strobe accent + solid hit
        fb, m1, m2 = par_solid(c)
        s, b, p = mkvrs(pos, c, prism_s=128, p1r_s=200,
                         prism_b=80, prot_b=180, prism_p=60,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)
    else:
        fb, m1, m2 = par_chase(c, beat)
        s, b, p = mkvrs(pos, c, prism_s=128, p1r_s=200,
                         prism_b=80, prot_b=180, prism_p=60)

    n = mkni(c, dim=255, halo_mode="jump_fast", t1=t1, t2=t2, t3=t3)
    idx = add_scene(f"Ch2-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# CHORUS 3 — 15 bars, pars EVERY BEAT, maximum variety
# Alternates chase + pairs patterns every 2 bars. All 6 neon colors.
# Widest mover moves. Prisms spinning harder. Strobe every 4 bars.
# =============================================================================

for beat in range(60):
    bar = beat // 4
    bib = beat % 4
    c = NEON_6[beat % 6]
    pos = POS_BIG[bar % len(POS_BIG)]
    t1 = 40 + (beat * 7 % 50)
    t2 = 60 + (beat * 11 % 40)
    t3 = 50 + (beat * 13 % 45)

    # Alternate par pattern every 2 bars: chase vs pairs
    if (bar // 2) % 2 == 0:
        fb, m1, m2 = par_chase(c, beat)
    else:
        c2 = NEON_6[(beat + 3) % 6]
        fb, m1, m2 = par_pairs(c, c2, flip=(bib % 2 == 1))

    # Strobe accent on beat 1 every 4 bars
    if bib == 0 and bar % 4 == 0:
        s, b, p = mkvrs(pos, c, prism_s=128, p1r_s=200,
                         prism_b=128, prot_b=200, prism_p=80,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)
    else:
        s, b, p = mkvrs(pos, c, prism_s=128, p1r_s=200,
                         prism_b=128, prot_b=200, prism_p=80)

    n = mkni(c, dim=255, halo_mode="jump_fast", t1=t1, t2=t2, t3=t3)
    idx = add_scene(f"Ch3-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# CLIMAX — 9 bars, ALL strobes + ALL lasers, maximum sensory overload
# Solid color hits every beat. Prisms spinning. NI3K tilts rotating.
# All 3 NI3K lasers on permanently.
# =============================================================================

climax_positions = POS_DANCE + ["X"]  # 9 for 9 bars

for beat in range(36):
    bar = beat // 4
    bib = beat % 4
    c = NEON_6[beat % 6]
    pos = climax_positions[bar % len(climax_positions)]

    fb, m1, m2 = par_solid(c)
    s, b, p = mkvrs(pos, c, prism_s=128, p1r_s=200,
                     prism_b=128, prot_b=200, prism_p=120,
                     s_strobe=SHARPY_STROBE_FAST,
                     b_shutter=BSW_SHUT_STROBE_FAST)
    n = mkni(c, dim=255, halo_mode="jump_fast",
             rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
             t1=160, t2=140, t3=180)  # auto-rotating tilts
    idx = add_scene(f"Climax-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# END — snap to black
# =============================================================================

beat_step(0, beats=1)


# =============================================================================
# STATS & VERIFICATION
# =============================================================================

total_ms = sum(ho for _, (fi, ho) in steps)
total_bars = total_ms / bpm_to_ms(BPM, 4)

print(f"\nScene dedup: {len(scenes)} unique scenes ({dedup_hits} reuses)")
print(f"Total steps: {len(steps)}")
print(f"Total duration: {total_ms/1000:.1f}s ({total_bars:.1f} bars)")
print(f"Target: ~148s")

# Section timing breakdown
sections = [
    ("Tease",    8),
    ("Opens",    16),
    ("Party",    32),
    ("Chorus 1", 36),
    ("Verse",    14),
    ("Break",    19),
    ("Chorus 2", 40),
    ("Chorus 3", 60),
    ("Climax",   36),
    ("Blackout", 1),
]
offset = 0
for name, count in sections:
    section_ms = sum(ho for _, (fi, ho) in steps[offset:offset + count])
    print(f"  {name:12s}: {count:3d} steps, {section_ms/1000:.1f}s")
    offset += count


# =============================================================================
# BUILD AND WRITE
# =============================================================================

scene_ids = [s for s, _ in steps]
timing = [t for _, t in steps]

main_chaser = make_chaser("Never Cared Enough", scene_ids, timing,
                          run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "▶ NEVER CARED ENOUGH", "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#FF1488", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

write_workspace("shows/PhatAdam - Never Cared Enough.qxw", scenes, [main_chaser],
                bpm=BPM, vc_buttons=vc_buttons)
