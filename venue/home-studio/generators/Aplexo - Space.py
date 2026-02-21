#!/usr/bin/env python3
"""
Show Generator: Aplexo - Space
==============================
BPM: 125 | Duration: ~3:48 | Label: Purified Records (Nora En Pure)
Genre: Melodic House & Techno

Aesthetic: Jan Erik Waider's cold Nordic glacial landscapes — deep navy,
icy cyan, cold white. "Shimmering fractured synths" = prism scatter.
Single beam isolation = star in space. Zero warm colors. Restraint.

Song Structure:
  0:00 - 0:38  INTRO      (20 bars, rms=0.70) Textured groove, sparse sub
  0:38 - 1:08  DROP_1     (16 bars, rms=0.83) First sub hit
  1:08 - 2:01  BREAKDOWN  (28 bars, rms→0.20) Near-silence at 1:31
  2:01 - 2:32  REBUILD    (16 bars, rms=0.38) Sub returns, tension rising
  2:32 - 3:33  DROP_2     (32 bars, rms=0.84) Full peak, NI3K lasers
  3:33 - 3:54  OUTRO      (11 bars, rms=0.35) Wind-down
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

SONG_STEM = "Aplexo - Space"
BRIEF = require_research_brief(SONG_STEM, project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)
print(f"Research brief OK: {BRIEF['_meta']['brief_json']}")
print(f"Creative thesis: {BRIEF['thesis']}")
DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", f"{SONG_STEM}.json")

CREATIVE = build_creative_context(BRIEF, song_stem=SONG_STEM)
BRAND_TOKENS = CREATIVE["brand_tokens"]
CREATIVE_DIRECTIVES = CREATIVE["creative_directives"]

with open(DATA_PATH) as f:
    data = json.load(f)

BPM = data["bpm"]  # 125
beats = data["beats"]
segments = data["segments"]

e_sub = data["energy"]["sub_bass"]
e_rms = data["energy"]["rms"]

vocal_e = data["stems"]["vocals"]["energy"]

BAR_MS = bpm_to_ms(BPM, 4)   # 1920ms
BEAT_MS = bpm_to_ms(BPM, 1)  # 480ms

# =============================================================================
# HELPERS
# =============================================================================

def beat_at(t):
    idx = bisect.bisect_left(beats, t)
    if idx == 0: return 0
    if idx >= len(beats): return len(beats) - 1
    return idx if abs(beats[idx] - t) < abs(beats[idx-1] - t) else idx - 1

def avg_energy(arr, t_start, t_end):
    i0, i1 = beat_at(t_start), beat_at(t_end)
    if i0 >= i1: return 0.0
    return sum(arr[i0:i1]) / (i1 - i0)

def segment_at(t):
    for i, seg in enumerate(segments):
        if seg["start"] <= t < seg["end"]:
            return i, seg
    return len(segments) - 1, segments[-1]

def vocal_present(t_start, t_end):
    return avg_energy(vocal_e, t_start, t_end) > 0.015

def e2d(e, low=30, high=255):
    return int(low + (high - low) * min(1.0, max(0.0, e)))

# =============================================================================
# PHRASE-AWARE HARD LAYER (anti-overuse, not strict uniqueness)
# =============================================================================

PHRASE_BALANCE_ENABLED = True
PHRASE_TECH_COOLDOWN = 2

PHRASE_USAGE_BY_BUCKET = {}
PHRASE_RECENT_BY_BUCKET = {}
PHRASE_BAR_COUNTS = {}
TECHNIQUE_COUNTS = {}
LAST_TECHNIQUE_PLAN = None

def timing_from_phrase_technique(technique, bars_here):
    bars_here = max(1.0, float(bars_here))
    timing = technique["timing"]
    par_style = str(timing["par_style"])
    par_beats = int(timing["par_beats"])
    relationship = str(technique["relationship"])

    if par_style == "fade":
        return smooth(BPM, bars_here)
    if par_style == "chase":
        if par_beats <= 1 and relationship == "inclusion":
            return snap(BPM, bars_here, fade_ms=60)
        if par_beats <= 2:
            return hold(BPM, bars_here)
        return smooth(BPM, bars_here)
    return smooth(BPM, bars_here)

def phrase_step_timing(t_start, t_end, bars_here):
    global LAST_TECHNIQUE_PLAN
    mid = (t_start + t_end) / 2.0
    seg_idx, seg = segment_at(mid)
    label = seg["label"]

    rms = avg_energy(e_rms, t_start, t_end)
    sub = avg_energy(e_sub, t_start, t_end)
    high = rms
    progress = min(1.0, max(0.0, mid / max(1.0, beats[-1])))

    phrase = classify_phrase(
        segment_label=label,
        rms=rms,
        sub=sub,
        high=high,
        progress=progress,
        project_root=PROJECT_ROOT,
    )

    usage = PHRASE_USAGE_BY_BUCKET.setdefault(phrase, {}) if PHRASE_BALANCE_ENABLED else None
    recent = PHRASE_RECENT_BY_BUCKET.setdefault(phrase, [])
    global_bar = int(round((t_start * 1000.0) / BAR_MS))

    technique = pick_phrase_technique(
        phrase=phrase,
        segment_index=seg_idx,
        global_bar=global_bar,
        usage=usage,
        recent=recent,
        cooldown=PHRASE_TECH_COOLDOWN,
        previous_plan=LAST_TECHNIQUE_PLAN,
        brand_tokens=BRAND_TOKENS,
        creative_directives=CREATIVE_DIRECTIVES,
        candidate_count=3,
        show_key=SONG_STEM,
        project_root=PROJECT_ROOT,
    )
    LAST_TECHNIQUE_PLAN = technique
    technique_id = technique["id"]
    if usage is not None:
        usage[technique_id] = usage.get(technique_id, 0) + 1
    recent.append(technique_id)
    if len(recent) > 8:
        del recent[:-8]

    PHRASE_BAR_COUNTS[phrase] = PHRASE_BAR_COUNTS.get(phrase, 0) + max(1, int(round(bars_here)))
    TECHNIQUE_COUNTS[technique_id] = TECHNIQUE_COUNTS.get(technique_id, 0) + 1
    return timing_from_phrase_technique(technique, bars_here)

# =============================================================================
# COLOR PALETTE — cold Nordic glacial, zero warm colors
# =============================================================================

DEEP_NAVY   = (10, 15, 70)
ICY_CYAN    = (130, 210, 230)
PALE_BLUE   = (50, 90, 175)
COLD_WHITE  = (220, 225, 240)
ARCTIC_GREY = (70, 80, 100)
NEAR_BLACK  = (5, 5, 15)
BLUE_TINT   = (30, 50, 120)
NOTHING     = (0, 0, 0)

# =============================================================================
# POSITIONS — loaded from venue focus-positions.md
# =============================================================================

POS = load_focus_position_tuples(project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)

# =============================================================================
# SECTIONS
# =============================================================================

SECTIONS = [
    {"name": "INTRO",     "start": 0.0,   "end": 38.0,  "bars": 20},
    {"name": "DROP_1",    "start": 38.0,  "end": 68.0,  "bars": 16},
    {"name": "BREAKDOWN", "start": 68.0,  "end": 121.0, "bars": 28},
    {"name": "REBUILD",   "start": 121.0, "end": 152.0, "bars": 16},
    {"name": "DROP_2",    "start": 152.0, "end": 213.0, "bars": 32},
    {"name": "OUTRO",     "start": 213.0, "end": 228.8, "bars": 11},
]

# =============================================================================
# SCENE BUILDERS
# =============================================================================

scenes = []
folder = "Space"
scenes.append(scene("Blackout", *blackout_all(), path=folder))

steps = []
cache = {}

def cached(key, fn):
    if key not in cache:
        cache[key] = len(scenes)
        scenes.append(fn())
    return cache[key]


def atmo(name, pos_key, energy, frost,
         s_color=SHARPY_BLUE, b_color=BSW_BLUE, p_color=PROF_BLUE,
         par=DEEP_NAVY, miss=NEAR_BLACK,
         ni_rgb=DEEP_NAVY, halo=H_OFF,
         s_dim=None, b_dim=None, p_dim=None, par_m=None,
         prism=False, gobo=False, lasers=False,
         strobe_s=SHARPY_OPEN, shutter_b=BSW_SHUT_OPEN,
         ni_tilt=(64, 64, 64)):
    """Cold atmosphere scene — all cold colors, no warm."""
    p = POS[pos_key]
    sp, st, bp, bt, pp, pt, ni_pan = p

    sd = s_dim if s_dim is not None else e2d(energy, 40, 230)
    bd = b_dim if b_dim is not None else e2d(energy, 30, 210)
    pd = p_dim if p_dim is not None else e2d(energy * 0.5, 0, 140)
    pm = par_m if par_m is not None else e2d(energy, 15, 200)

    pv = 128 if prism else 0
    pr = 200 if prism else 0
    gv = BSW_G1_2 if gobo else 0   # subtle gobo 2 for texture

    ni_r, ni_g, ni_b = ni_rgb
    nd = e2d(energy * 0.45, 0, 160)
    t1, t2, t3 = ni_tilt

    lr = LASER_ON if lasers else LASER_OFF
    lg = LASER_ON if lasers else LASER_OFF
    lb = LASER_ON if lasers else LASER_OFF

    return scene(name,
        sharpy(pan=sp, tilt=st, strobe=strobe_s, dim=sd,
               frost=frost, colormacro=s_color, focus=128,
               prism1=pv, p1r=pr),
        bsw(pan=bp, tilt=bt, color=b_color, shutter=shutter_b,
            dim=bd, frost=min(255, frost),
            prism=pv, prot=pr, gobo1=gv, focus=128),
        profile(pan=pp, tilt=pt, color=p_color, dim=pd, focus=128),
        fourbar_solid(*par, master=pm),
        miss1(*miss, master=pm // 3),
        miss2(*miss, master=pm // 3),
        ni3k(pan=ni_pan, t1=t1, t2=t2, t3=t3,
             r=ni_r, g=ni_g, b=ni_b, w=0,
             halo=halo, rl=lr, gl=lg, bl=lb,
             dim=nd, strobe=0),
        path=folder)


def solo_sharpy(name, pos_key, dim, color=SHARPY_BLUE, frost=220,
                ni_rgb=NOTHING, halo=H_OFF, par=NOTHING, par_m=0):
    """Single Sharpy beam — star in space aesthetic."""
    p = POS[pos_key]
    sp, st, bp, bt, pp, pt, ni_pan = p
    ni_r, ni_g, ni_b = ni_rgb
    nd = 20 if sum(ni_rgb) > 0 else 0
    return scene(name,
        sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=dim,
               frost=frost, colormacro=color, focus=128),
        dark_bsw(pan=bp, tilt=bt),
        dark_profile(pan=pp, tilt=pt),
        fourbar_solid(*par, master=par_m),
        miss1(*NOTHING), miss2(*NOTHING),
        ni3k(pan=ni_pan, t1=64, t2=64, t3=64,
             r=ni_r, g=ni_g, b=ni_b, w=0,
             halo=halo, dim=nd, strobe=0),
        path=folder)


# =============================================================================
# SECTION BUILDERS
# =============================================================================

def build_intro(sec):
    """INTRO (0:00-0:38, 20 bars): Like eyes adjusting to space.

    Start dark — 4BAR deep navy only. Sharpy comes in at bar 8 aimed
    at CEIL, barely visible. BSW fades in at bar 12. Gradual rise.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = t_end - t
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 4, t_end)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)

        # Fixture reveal: 0-8 bars = 4BAR only, 8-12 = add Sharpy, 12+ = add BSW
        if prog < 0.4:   # bars 0-8
            s_dim = 0
            b_dim = 0
            p_dim = 0
            pos = "C"
        elif prog < 0.6:  # bars 8-12
            s_dim = int(25 + 20 * ((prog - 0.4) / 0.2))
            b_dim = 0
            p_dim = 0
            pos = "CEIL"
        else:             # bars 12-20
            s_dim = int(45 + 40 * ((prog - 0.6) / 0.4))
            b_dim = int(30 + 40 * ((prog - 0.6) / 0.4))
            p_dim = 0
            pos = "C" if n % 2 == 0 else "USC"

        par_m = e2d(energy * prog * 0.6, 10, 100)

        sid = cached(f"intro_{n}", lambda: atmo(
            f"Intro {n}", pos, energy * prog * 0.7, 220,
            s_color=SHARPY_BLUE, b_color=BSW_BLUE, p_color=PROF_BLUE,
            par=DEEP_NAVY, miss=NEAR_BLACK,
            ni_rgb=DEEP_NAVY, halo=H_OFF,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        n += 1


def build_drop1(sec):
    """DROP_1 (0:38-1:08, 16 bars): First sub hit, full engagement.

    Prism on for fractured synth texture. Slow gobo on BSW.
    Water-like sweep: DSC → SR → C → SL → DSC.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    sweep = ["DSC", "SR", "C", "SL", "DSC", "X", "SR", "DSC"]
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        energy = avg_energy(e_rms, t, next_t)
        frost = int(150 - 60 * energy)
        pos = sweep[n % len(sweep)]
        has_vocal = vocal_present(t, next_t)

        # Icy cyan on vocal, blue otherwise
        s_col = SHARPY_TEAL if has_vocal else SHARPY_BLUE
        par_c = ICY_CYAN if has_vocal else PALE_BLUE
        ni_c = ICY_CYAN if has_vocal else DEEP_NAVY

        sid = cached(f"drop1_{n}", lambda: atmo(
            f"Drop1 {n}", pos, energy, frost,
            s_color=s_col, b_color=BSW_TEAL, p_color=PROF_TEAL,
            par=par_c, miss=BLUE_TINT,
            ni_rgb=ni_c, halo=H_BLU,
            prism=True, gobo=(n % 4 == 0),
            ni_tilt=(64, 64, 64)))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        n += 1


def build_breakdown(sec):
    """BREAKDOWN (1:08-2:01, 28 bars): Near-silence at 1:31.

    Phase 1 (12 bars): strip back over darkening sweep.
    Phase 2 (16 bars): Sharpy solo only — star in space.
      Very slow diamond sweep at ceiling/floor alternation, dim=20-40.
      NI3K dim blue glow.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = t_end - t
    n = 0

    # Phase 1: strip down (12 bars, ~23s)
    strip_end = t + bar * 12

    while t < strip_end - 0.3:
        next_t = min(t + bar * 4, strip_end)
        prog = (t - sec["start"]) / (strip_end - sec["start"])
        energy = avg_energy(e_rms, t, next_t)
        dim_f = max(0.05, 1.0 - prog * 0.85)

        sid = cached(f"bd_strip_{n}", lambda: atmo(
            f"BD Strip {n}", "DSC", energy * dim_f, int(200 + 40 * prog),
            s_color=SHARPY_BLUE, b_color=BSW_BLUE, p_color=PROF_BLUE,
            par=tuple(int(c * dim_f) for c in DEEP_NAVY),
            miss=NOTHING,
            ni_rgb=tuple(int(c * dim_f) for c in PALE_BLUE),
            halo=H_BLU if prog < 0.4 else H_OFF,
            s_dim=int(100 * dim_f), b_dim=int(80 * dim_f),
            p_dim=0, par_m=int(80 * dim_f),
            prism=False))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        n += 1

    # Phase 2: Sharpy solo diamond — star in space (16 bars, ~31s)
    # Alternate between CEIL (cosmic) and floor positions (DSC, C)
    diamond = ["CEIL", "DSC", "C", "CEIL", "DJ", "CEIL"]

    while t < t_end - 0.3:
        next_t = min(t + bar * 4, t_end)  # slow 4-bar crossfades
        bd_prog = (t - strip_end) / max(1, t_end - strip_end)
        pos = diamond[n % len(diamond)]

        # Very dim. Barely there.
        dim = int(15 + 25 * bd_prog)

        sid = cached(f"bd_solo_{n}", lambda: solo_sharpy(
            f"BD Solo {n}", pos, dim=dim,
            color=SHARPY_BLUE, frost=230,
            ni_rgb=DEEP_NAVY if bd_prog > 0.3 else NOTHING,
            halo=H_OFF,
            par=NEAR_BLACK if bd_prog > 0.5 else NOTHING,
            par_m=10 if bd_prog > 0.5 else 0))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        n += 1


def build_rebuild(sec):
    """REBUILD (2:01-2:32, 16 bars): Sub returns, tension rising.

    Add BSW back first (frosted), then Profile. 4BAR navy → icy cyan.
    Frost decreasing. Beams sharpening. Prism returns.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = t_end - t
    n = 0
    positions = ["C", "SL", "DSC", "SR"]

    while t < t_end - 0.3:
        next_t = min(t + bar * 4, t_end)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos = positions[n % len(positions)]

        s_dim = int(40 + 120 * prog)
        b_dim = int(70 * prog) if prog > 0.2 else 0
        p_dim = int(50 * prog) if prog > 0.5 else 0
        par_m = int(30 + 100 * prog)
        frost = int(220 - 80 * prog)

        # Par transitions navy → icy cyan as rebuild climaxes
        par_c = PALE_BLUE if prog < 0.5 else ICY_CYAN
        use_prism = prog > 0.6

        p = POS[pos]
        sp, st, bp, bt, pp, pt, ni_pan = p

        sid = cached(f"rebuild_{n}", lambda: scene(
            f"Rebuild {n}",
            sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=s_dim,
                   frost=frost, colormacro=SHARPY_BLUE, focus=128,
                   prism1=128 if use_prism else 0,
                   p1r=200 if use_prism else 0),
            bsw(pan=bp, tilt=bt, color=BSW_TEAL,
                shutter=BSW_SHUT_OPEN, dim=b_dim,
                frost=int(frost * 1.1), focus=128,
                prism=128 if use_prism else 0,
                prot=200 if use_prism else 0)
                if b_dim > 0 else dark_bsw(pan=bp, tilt=bt),
            profile(pan=pp, tilt=pt, color=PROF_TEAL,
                    dim=p_dim, focus=128)
                if p_dim > 0 else dark_profile(pan=pp, tilt=pt),
            fourbar_solid(*par_c, master=par_m),
            miss1(*BLUE_TINT, master=par_m // 4),
            miss2(*BLUE_TINT, master=par_m // 4),
            ni3k(pan=ni_pan, t1=64, t2=64, t3=64,
                 r=PALE_BLUE[0], g=PALE_BLUE[1], b=PALE_BLUE[2],
                 w=0, halo=H_BLU if prog > 0.4 else H_OFF,
                 dim=int(40 * prog), strobe=0),
            path=folder))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        n += 1


def build_drop2(sec):
    """DROP_2 (2:32-3:33, 32 bars): Full peak. The coldest, brightest moment.

    Icy cyan + cold white. Wider positions. Prism sweeping.
    NI3K lasers at absolute climax (roughly 2:47-3:18).
    No strobe — fracturing comes from prism rotation.
    """
    t, t_end = sec["start"], sec["end"]
    total = t_end - t
    bar = BAR_MS / 1000
    n = 0

    # Positions oscillate between cosmic (CEIL) and floor engagement (DSC, X)
    sweep = ["DSC", "X", "SL", "CEIL", "C", "SR", "DSC", "X",
             "DSL", "CEIL", "C", "DSR", "USC", "X", "CEIL", "DSC"]

    # Laser window: ~2:47-3:18 = roughly bars 8-24 of this section
    laser_start = sec["start"] + bar * 8
    laser_end = sec["start"] + bar * 24

    while t < t_end - 0.3:
        next_t = min(t + bar * 2, t_end)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        pos = sweep[n % len(sweep)]

        frost = int(110 - 70 * energy)
        use_lasers = laser_start <= t < laser_end and energy > 0.75

        # At absolute peak (center of section), go cold white
        at_peak = 0.25 <= prog <= 0.75
        if at_peak and energy > 0.82:
            s_col = SHARPY_WHITE
            par_c = COLD_WHITE
            miss_c = ICY_CYAN
        elif has_vocal:
            s_col = SHARPY_TEAL
            par_c = ICY_CYAN
            miss_c = PALE_BLUE
        else:
            s_col = SHARPY_BLUE
            par_c = PALE_BLUE
            miss_c = BLUE_TINT

        ni_c = ICY_CYAN if at_peak else PALE_BLUE
        ni_tilt = (150, 170, 160) if energy > 0.8 else (64, 64, 64)

        sid = cached(f"drop2_{n}", lambda: atmo(
            f"Drop2 {n}", pos, energy, frost,
            s_color=s_col, b_color=BSW_TEAL, p_color=PROF_TEAL,
            par=par_c, miss=miss_c,
            ni_rgb=ni_c, halo=H_CYN,
            prism=True, lasers=use_lasers,
            ni_tilt=ni_tilt))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        n += 1


def build_outro(sec):
    """OUTRO (3:33-3:54, 11 bars): Rapid wind-down to blackout.

    Lasers off. Movers converge to center. Progressive dimming.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = t_end - t
    n = 0

    while t < t_end - 0.3:
        next_t = min(t + bar * 3, t_end)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        dim_f = max(0.0, 1.0 - prog * 0.95)

        sid = cached(f"outro_{n}", lambda: atmo(
            f"Outro {n}", "C", energy * dim_f, 230,
            s_color=SHARPY_BLUE, b_color=BSW_BLUE, p_color=PROF_BLUE,
            par=tuple(int(c * dim_f) for c in DEEP_NAVY),
            miss=NOTHING,
            ni_rgb=tuple(int(c * dim_f) for c in PALE_BLUE),
            halo=H_OFF,
            s_dim=int(80 * dim_f), b_dim=int(50 * dim_f),
            p_dim=0, par_m=int(60 * dim_f)))

        bars_here = max(1, (next_t - t) / bar)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        n += 1

    steps.append((0, phrase_step_timing(max(0.0, t_end - bar * 2), t_end, 2)))  # final blackout


# =============================================================================
# MAIN
# =============================================================================

BUILDERS = {
    "INTRO": build_intro,
    "DROP_1": build_drop1,
    "BREAKDOWN": build_breakdown,
    "REBUILD": build_rebuild,
    "DROP_2": build_drop2,
    "OUTRO": build_outro,
}

print(f"Generating show: {SONG_STEM}")
print(f"  BPM: {BPM}, Beats: {len(beats)}, Duration: {beats[-1]:.1f}s")
print()

for sec in SECTIONS:
    print(f"  Building {sec['name']:10s} ({sec['bars']:2d} bars, "
          f"{sec['start']:.1f}s-{sec['end']:.1f}s)")
    BUILDERS[sec["name"]](sec)

print(f"\nTotal scenes: {len(scenes)}")
print(f"Total chaser steps: {len(steps)}")
print(f"Phrase bars: {PHRASE_BAR_COUNTS}")
top_techniques = sorted(TECHNIQUE_COUNTS.items(), key=lambda kv: kv[1], reverse=True)[:8]
print(f"Top technique usage: {top_techniques}")

total_ms = sum(fi + ho for _, (fi, ho) in steps)
print(f"Total duration: {total_ms/1000:.1f}s (target: ~229s)")

main_chaser = make_chaser("Space", [s for s, _ in steps], [t for _, t in steps],
                           run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "▶ SPACE",  "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10,  "w": 470, "h": 100, "color": "#0A0F46", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,  "color": "#FF0000", "action": "Toggle"},
]

output_path = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")
write_workspace(output_path, scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
