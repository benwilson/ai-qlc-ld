#!/usr/bin/env python3
"""
Show Generator: Mind Against - OnlyL ft. TSHA & NIMMO
======================================================
BPM: 128 | Duration: ~6:03 | Label: Afterlife-adjacent
Genre: Melodic Techno / Emotional Electronic

Aesthetic: Yearning indigo longing → desaturated rose on vocals →
near-black void (the 'OnlyL' moment) → pale cream-white catharsis.
Movers breathe as one organism throughout. NI3K lasers only from peak.
No strobe. Everything desaturated and cinematic.

Song Structure (hand-crafted from 18 analysis segments):
  0:00 - 0:30  OPENING     (16 bars) Indigo organism, kick from bar 1, sub low
  0:30 - 1:15  VERSE_1     (24 bars) First NIMMO vocal pass, rose warmth on voice
  1:15 - 2:16  BREATHE     (32 bars) Mid-weight breathing verse, sustained vocals
  2:16 - 2:46  SURGE       (16 bars) Pre-break intensity surge
  2:46 - 3:09  DIMMING     (12 bars) Energy starts falling, approach to void
  3:09 - 4:01  VOID        (28 bars) Near-silence — Profile spotlight only, everything else dark
  4:01 - 4:32  REBUILD     (16 bars) Slow accumulation from the void
  4:32 - 5:21  PEAK        (26 bars) Cathartic climax — pale white, lasers, prism
  5:21 - 6:07  FADE        (23 bars) Sustained warmth, return to indigo, slow decay
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

SONG_STEM = "Mind Against - OnlyL ft. TSHA & NIMMO"
BRIEF = require_research_brief(SONG_STEM, project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)
print(f"Research brief OK: {BRIEF['_meta']['brief_json']}")
print(f"Creative thesis: {BRIEF['thesis']}")

CREATIVE = build_creative_context(BRIEF, song_stem=SONG_STEM)
BRAND_TOKENS = CREATIVE["brand_tokens"]
CREATIVE_DIRECTIVES = CREATIVE["creative_directives"]

DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", f"{SONG_STEM}.json")
with open(DATA_PATH) as f:
    data = json.load(f)

BPM = data["bpm"]       # 128
beats = data["beats"]
segments = data["segments"]
e_sub = data["energy"]["sub_bass"]
e_rms = data["energy"]["rms"]
vocal_e = data["stems"]["vocals"]["energy"]

BAR_MS = bpm_to_ms(BPM, 4)   # 1875ms
BEAT_MS = bpm_to_ms(BPM, 1)  # 469ms

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
    return avg_energy(vocal_e, t_start, t_end) > 0.012

def e2d(e, low=30, high=255):
    return int(low + (high - low) * min(1.0, max(0.0, e)))

# =============================================================================
# PHRASE-AWARE TRACKING
# =============================================================================

PHRASE_USAGE_BY_BUCKET = {}
PHRASE_RECENT_BY_BUCKET = {}
PHRASE_BAR_COUNTS = {}
TECHNIQUE_COUNTS = {}
LAST_TECHNIQUE_PLAN = None

def timing_from_phrase_technique(technique, bars_here):
    bars_here = max(0.25, float(bars_here))
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
    progress = min(1.0, max(0.0, mid / max(1.0, beats[-1])))

    phrase = classify_phrase(
        segment_label=label, rms=rms, sub=sub, high=rms,
        progress=progress, project_root=PROJECT_ROOT,
    )

    usage = PHRASE_USAGE_BY_BUCKET.setdefault(phrase, {})
    recent = PHRASE_RECENT_BY_BUCKET.setdefault(phrase, [])
    global_bar = int(round((t_start * 1000.0) / BAR_MS))

    technique = pick_phrase_technique(
        phrase=phrase, segment_index=seg_idx, global_bar=global_bar,
        usage=usage, recent=recent, cooldown=2,
        previous_plan=LAST_TECHNIQUE_PLAN,
        brand_tokens=BRAND_TOKENS, creative_directives=CREATIVE_DIRECTIVES,
        candidate_count=3, show_key=SONG_STEM, project_root=PROJECT_ROOT,
    )
    LAST_TECHNIQUE_PLAN = technique
    technique_id = technique["id"]
    usage[technique_id] = usage.get(technique_id, 0) + 1
    recent.append(technique_id)
    if len(recent) > 8:
        del recent[:-8]

    PHRASE_BAR_COUNTS[phrase] = PHRASE_BAR_COUNTS.get(phrase, 0) + max(1, int(round(bars_here)))
    TECHNIQUE_COUNTS[technique_id] = TECHNIQUE_COUNTS.get(technique_id, 0) + 1
    return (timing_from_phrase_technique(technique, bars_here), technique)

def next_step_bars(technique, default="2bar", cap=4):
    br = technique.get("beat_reactivity") or {}
    return min(cap, reactivity_to_bars(br.get("mover_min", default)))

# =============================================================================
# COLOR PALETTE — Indigo longing + desaturated rose + pale cathartic white
# =============================================================================

# RGB for pars / missyees — all desaturated, cinematic
DEEP_INDIGO   = (8, 5, 40)
DUST_ROSE     = (120, 70, 90)       # muted adult rose — vocal warmth
PALE_ROSE     = (160, 100, 110)     # brighter rose for surges
CREAM_WHITE   = (200, 190, 170)     # warm white for catharsis
PALE_SILVER   = (140, 145, 160)     # cool silver for rebuild
NEAR_BLACK    = (3, 2, 8)
NOTHING       = (0, 0, 0)

# Mover color wheels
SH_INDIGO   = SHARPY_BLUE          # 30
SH_ROSE     = SHARPY_PINK          # 60
SH_SILVER   = SHARPY_WHITE         # 0
SH_AMBER    = SHARPY_AMBER         # 80  — used for peak warmth

BSW_INDIGO  = BSW_BLUE             # 44
BSW_ROSE    = BSW_PINK             # 62
BSW_SILVER  = BSW_WHITE            # 0
BSW_AMBER   = BSW_YELLOW           # 32  — closest warm

PF_INDIGO   = PROF_BLUE            # 15
PF_ROSE     = PROF_PINK            # 30
PF_SILVER   = PROF_WHITE           # 0

# =============================================================================
# POSITIONS
# =============================================================================

POS = load_focus_position_tuples(project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)

# Slow breathing sweeps — all 4-bar minimum
SLOW_PENDULUM = ["SL", "C", "SR", "C"]
CONVERGING    = ["SL", "C", "SR", "DSC", "C"]
WIDE_BREATHE  = ["DSL", "C", "DSR", "C"]

# =============================================================================
# SECTIONS — hand-crafted from 18 analysis segments
# =============================================================================

SECTIONS = [
    {"name": "OPENING",  "start": 0.0,    "end": 30.0,   "bars": 16},
    {"name": "VERSE_1",  "start": 30.0,   "end": 75.0,   "bars": 24},
    {"name": "BREATHE",  "start": 75.0,   "end": 136.0,  "bars": 32},
    {"name": "SURGE",    "start": 136.0,  "end": 166.0,  "bars": 16},
    {"name": "DIMMING",  "start": 166.0,  "end": 189.0,  "bars": 12},
    {"name": "VOID",     "start": 189.0,  "end": 241.0,  "bars": 28},
    {"name": "REBUILD",  "start": 241.0,  "end": 272.0,  "bars": 16},
    {"name": "PEAK",     "start": 272.0,  "end": 321.0,  "bars": 26},
    {"name": "FADE",     "start": 321.0,  "end": 363.0,  "bars": 23},
]

# =============================================================================
# SCENE FACTORY
# =============================================================================

scenes = []
folder = "OnlyL"
scenes.append(scene("Blackout", *blackout_all(), path=folder))

steps = []
cache = {}

def cached(key, fn):
    if key not in cache:
        cache[key] = len(scenes)
        scenes.append(fn())
    return cache[key]


def organism(name, pos_key, energy, frost=210,
             s_color=SH_INDIGO, b_color=BSW_INDIGO, p_color=PF_INDIGO,
             par=DEEP_INDIGO, miss=NEAR_BLACK,
             ni_rgb=DEEP_INDIGO, halo=H_OFF,
             s_dim=None, b_dim=None, p_dim=None, par_m=None,
             prism=False, lasers=False, ni_tilt=(64, 64, 64)):
    """Unified organism scene — all movers breathe together, deep indigo default."""
    sd = s_dim if s_dim is not None else e2d(energy, 25, 160)
    bd = b_dim if b_dim is not None else e2d(energy, 18, 140)
    pd = p_dim if p_dim is not None else e2d(energy * 0.5, 15, 120)
    pm = par_m if par_m is not None else e2d(energy, 12, 180)
    nd = e2d(energy * 0.4, 12, 140)

    return scene(name,
        *mover_look(pos_key, POS,
                    colors=(s_color, b_color, p_color),
                    dims=(sd, bd, pd),
                    frost=(frost, min(255, frost)),
                    prism=prism, focus=128),
        *par_look("solid", par, master=pm,
                  miss_color=miss, miss_master=pm // 3),
        ni3k_look(pos_key, POS, rgb=ni_rgb, dim=nd,
                  halo=halo, lasers=lasers, tilt_values=ni_tilt),
        path=folder)


def vocal_spotlight(name, dim=40, par_c=NEAR_BLACK, par_m=0,
                    ni_rgb=NEAR_BLACK, ni_dim=12):
    """Profile-only spotlight for exposed vocal moments — everything else dark."""
    dsc = POS["DSC"]
    return scene(name,
        dark_sharpy(pan=dsc[0], tilt=dsc[1]),
        dark_bsw(pan=dsc[2], tilt=dsc[3]),
        profile(pan=dsc[4], tilt=dsc[5], color=PF_SILVER,
                dim=dim, focus=128),
        *par_look("solid", par_c, master=par_m,
                  miss_color=NOTHING, miss_master=0),
        ni3k_look("DSC", POS, rgb=ni_rgb, dim=ni_dim, halo=H_OFF),
        path=folder)


# =============================================================================
# SECTION BUILDERS
# =============================================================================

def build_opening(sec):
    """OPENING (0:00–0:30, 16 bars): Organism enters from darkness.

    Full kick from beat 1 but sub stays low. Deep indigo world. Sharpy
    enters first, BSW follows. Profile at DSC dim. No par energy yet —
    just the movers breathing into existence.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 4

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos = SLOW_PENDULUM[n % len(SLOW_PENDULUM)]

        s_dim = int(20 + 60 * prog)
        b_dim = int(15 + 50 * max(0, prog - 0.25)) if prog > 0.25 else 0
        p_dim = max(10, int(15 + 20 * prog))
        par_m = int(10 + 30 * prog)

        sid = cached(f"open_{n}", lambda: organism(
            f"Opening {n}", pos, energy, frost=230,
            s_color=SH_INDIGO, b_color=BSW_INDIGO, p_color=PF_INDIGO,
            par=DEEP_INDIGO, miss=NEAR_BLACK,
            ni_rgb=DEEP_INDIGO, halo=H_OFF,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique, default="4bar", cap=4)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_verse_1(sec):
    """VERSE_1 (0:30–1:15, 24 bars): First NIMMO vocal pass.

    All three movers unified in slow pendulum. Dusty rose appears on
    vocal moments — muted, not saturated. PAR wash warm on vocals,
    indigo on beats. Profile brightens to mid level.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        pos = SLOW_PENDULUM[n % len(SLOW_PENDULUM)]

        if has_vocal:
            s_col, b_col, p_col = SH_ROSE, BSW_ROSE, PF_ROSE
            par_c = DUST_ROSE
            miss_c = tuple(c // 2 for c in DUST_ROSE)
            halo = H_PNK
        else:
            s_col, b_col, p_col = SH_INDIGO, BSW_INDIGO, PF_INDIGO
            par_c = DEEP_INDIGO
            miss_c = NEAR_BLACK
            halo = H_BLU

        s_dim = e2d(energy, 40, 120)
        b_dim = e2d(energy, 30, 100)
        p_dim = e2d(energy * 0.6, 20, 80)
        par_m = e2d(energy, 20, 120)

        sid = cached(f"verse1_{n}", lambda: organism(
            f"Verse1 {n}", pos, energy, frost=210,
            s_color=s_col, b_color=b_col, p_color=p_col,
            par=par_c, miss=miss_c,
            ni_rgb=DUST_ROSE if has_vocal else DEEP_INDIGO, halo=halo,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique, default="2bar", cap=4)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_breathe(sec):
    """BREATHE (1:15–2:16, 32 bars): Main vocal section — sustained organism.

    Mid-weight RMS (0.55). Rose palette holds across the section, slowly
    brightening toward SURGE. 4-bar breathing sweeps, unhurried.
    PAR in pairs for texture without chaos.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 4

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        pos = SLOW_PENDULUM[n % len(SLOW_PENDULUM)]

        # Slowly brighten through the section
        dim_boost = prog * 0.3
        if has_vocal:
            s_col, b_col, p_col = SH_ROSE, BSW_ROSE, PF_ROSE
            par_c = DUST_ROSE
            miss_c = tuple(c // 2 for c in DUST_ROSE)
            halo = H_PNK
        else:
            s_col, b_col, p_col = SH_INDIGO, BSW_INDIGO, PF_INDIGO
            par_c = DEEP_INDIGO
            miss_c = NEAR_BLACK
            halo = H_BLU

        s_dim = e2d(energy + dim_boost, 30, 130)
        b_dim = e2d(energy + dim_boost, 25, 110)
        p_dim = e2d((energy + dim_boost) * 0.6, 15, 90)
        par_m = e2d(energy + dim_boost, 20, 140)

        # PAR in pairs for breathing texture
        p = POS[pos]
        sp, st, bp, bt, pp, pt, ni_pan = p

        sid = cached(f"breathe_{n}", lambda: scene(
            f"Breathe {n}",
            sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=s_dim,
                   frost=200, colormacro=s_col, focus=128),
            bsw(pan=bp, tilt=bt, color=b_col, shutter=BSW_SHUT_OPEN,
                dim=b_dim, frost=200, focus=128),
            profile(pan=pp, tilt=pt, color=p_col, dim=p_dim, focus=128),
            *par_look("pairs", par_c, par_c, master=par_m,
                      miss_color=miss_c, miss_master=par_m // 3),
            ni3k_look(pos, POS, rgb=DUST_ROSE if has_vocal else DEEP_INDIGO,
                      dim=e2d(energy * 0.4, 10, 100),
                      halo=halo),
            path=folder))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique, default="4bar", cap=4)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_surge(sec):
    """SURGE (2:16–2:46, 16 bars): Pre-break intensity rise.

    Organism tightens toward DSC. Rose becomes Pale Rose — brighter,
    more urgent. Sub-bass pulses. 2-bar steps. Profile brightens.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    positions = CONVERGING
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos = positions[n % len(positions)]

        # Surge from rose toward silver-rose (pre-catharsis)
        s_col = SH_ROSE
        b_col = BSW_ROSE
        p_col = PF_ROSE
        par_c = PALE_ROSE
        miss_c = DUST_ROSE

        s_dim = e2d(energy, 60, 160)
        b_dim = e2d(energy, 50, 140)
        p_dim = e2d(energy * 0.65, 25, 110)
        par_m = e2d(energy, 50, 170)
        frost = int(200 - 30 * prog)   # beams sharpening slightly

        sid = cached(f"surge_{n}", lambda: organism(
            f"Surge {n}", pos, energy, frost=frost,
            s_color=s_col, b_color=b_col, p_color=p_col,
            par=par_c, miss=miss_c,
            ni_rgb=PALE_ROSE, halo=H_PNK,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique, default="2bar", cap=2)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_dimming(sec):
    """DIMMING (2:46–3:09, 12 bars): The fall begins.

    Energy dropping from 0.48 → 0.18. Movers dim out, rose fades to
    indigo. Profile stays as the last mover standing.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)

        # Linear dimout — rose drains away
        dim_f = max(0.1, 1.0 - prog * 0.75)
        s_dim = int(100 * dim_f)
        b_dim = int(80 * dim_f)
        p_dim = max(20, int(60 * dim_f))
        par_m = int(80 * dim_f)

        # Colour drains from rose to indigo
        if prog < 0.5:
            s_col, b_col, p_col = SH_ROSE, BSW_ROSE, PF_ROSE
            par_c = tuple(int(DUST_ROSE[i] * (1 - prog * 2)) +
                          int(DEEP_INDIGO[i] * prog * 2) for i in range(3))
        else:
            s_col, b_col, p_col = SH_INDIGO, BSW_INDIGO, PF_INDIGO
            par_c = DEEP_INDIGO

        pos = SLOW_PENDULUM[n % len(SLOW_PENDULUM)]

        sid = cached(f"dimming_{n}", lambda: organism(
            f"Dimming {n}", pos, energy, frost=220,
            s_color=s_col, b_color=b_col, p_color=p_col,
            par=par_c, miss=NEAR_BLACK,
            ni_rgb=DEEP_INDIGO, halo=H_OFF,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique, default="2bar", cap=4)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_void(sec):
    """VOID (3:09–4:01, 28 bars): The 'OnlyL' moment — love stripped to its last syllable.

    Near-silence (rms=0.13, sub=0.02). Profile spotlight at DSC only.
    Everything else dark. The most exposed vocal section. Step size 4 bars —
    almost no movement. Light barely breathes.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 4

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)

        # Very slow breathing — profile dim pulses slightly with energy
        p_dim = max(15, int(20 + 30 * energy))
        par_m = max(0, int(8 * energy))
        ni_dim = max(0, int(10 * energy))

        sid = cached(f"void_{n}", lambda: vocal_spotlight(
            f"Void {n}", dim=p_dim,
            par_c=NEAR_BLACK if energy < 0.1 else DEEP_INDIGO,
            par_m=par_m, ni_dim=ni_dim))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        # Ignore technique step size in void — always 4 bars, stillness is the point
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_rebuild(sec):
    """REBUILD (4:01–4:32, 16 bars): Slow accumulation from the void.

    Movers reappear one by one. Silver-grey first (cold, crystalline),
    then warming toward pale rose as the build intensifies. PAR gradually
    re-enters. Feels like a held breath finally releasing.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 4

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos = CONVERGING[n % len(CONVERGING)]

        # Sharpy enters first, BSW follows
        s_dim = int(25 + 120 * prog)
        b_dim = int(20 + 90 * max(0, prog - 0.25)) if prog > 0.25 else 0
        p_dim = max(15, int(20 + 80 * prog))
        par_m = int(15 + 80 * prog)
        ni_dim = int(10 + 60 * prog)

        # Silver → pale rose as rebuild intensifies
        if prog < 0.5:
            s_col, b_col, p_col = SH_SILVER, BSW_SILVER, PF_SILVER
            par_c = PALE_SILVER
        else:
            s_col, b_col, p_col = SH_ROSE, BSW_ROSE, PF_ROSE
            par_c = DUST_ROSE

        frost = int(230 - 30 * prog)  # sharpening toward peak

        p = POS[pos]
        sp, st, bp, bt, pp, pt, ni_pan = p

        sid = cached(f"rebuild_{n}", lambda: scene(
            f"Rebuild {n}",
            sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=s_dim,
                   frost=frost, colormacro=s_col, focus=128),
            bsw(pan=bp, tilt=bt, color=b_col, shutter=BSW_SHUT_OPEN,
                dim=b_dim, frost=frost, focus=128)
                if b_dim > 0 else dark_bsw(pan=bp, tilt=bt),
            profile(pan=pp, tilt=pt, color=p_col, dim=p_dim, focus=128),
            *par_look("solid", par_c, master=par_m,
                      miss_color=NEAR_BLACK, miss_master=par_m // 5),
            ni3k_look(pos, POS,
                      rgb=PALE_SILVER if prog < 0.5 else DUST_ROSE,
                      dim=ni_dim,
                      halo=H_BLU if prog < 0.5 else H_PNK),
            path=folder))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique, default="4bar", cap=4)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_peak(sec):
    """PEAK (4:32–5:21, 26 bars): Cathartic climax — pale cream white, lasers, prism.

    THE release. RMS peak 1.00 at 5:02. Cream-white washes over everything.
    Prism fractures the beam. NI3K lasers on throughout. Wide sweeps.
    Profile at full. The only moment of near-full brightness.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 2

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos = WIDE_BREATHE[n % len(WIDE_BREATHE)]

        # Full cream-white catharsis
        s_dim = int(160 + 80 * energy)
        b_dim = int(140 + 70 * energy)
        p_dim = int(100 + 80 * energy)
        par_m = int(160 + 80 * energy)
        frost = int(160 - 60 * energy)  # sharpening

        # Prism on — the 'eyes open' fracture
        has_prism = True

        # Late in section: add warm amber accents as the emotion peaks
        if prog > 0.6:
            s_col, b_col, p_col = SH_AMBER, BSW_AMBER, PF_SILVER
            par_c = CREAM_WHITE
        else:
            s_col, b_col, p_col = SH_SILVER, BSW_SILVER, PF_SILVER
            par_c = CREAM_WHITE

        sid = cached(f"peak_{n}", lambda: organism(
            f"Peak {n}", pos, energy, frost=frost,
            s_color=s_col, b_color=b_col, p_color=p_col,
            par=par_c, miss=tuple(c // 2 for c in CREAM_WHITE),
            ni_rgb=CREAM_WHITE, halo=H_YEL,
            s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m,
            prism=has_prism, lasers=True,
            ni_tilt=(160, 180, 170)))  # NI3K heads rotating for laser scan

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique, default="2bar", cap=2)
        steps.append((sid, timing))
        t = next_t
        n += 1


def build_fade(sec):
    """FADE (5:21–6:07, 23 bars): Sustained warmth returning to indigo.

    Phase 1 (~12 bars): cream-white holds then slowly desaturates.
    Phase 2 (~11 bars): back to indigo organism — bookend mirrors OPENING.
    Lasers stay on through phase 1, off in phase 2.
    """
    t, t_end = sec["start"], sec["end"]
    bar = BAR_MS / 1000
    total = max(0.1, t_end - t)
    n = 0
    step_bars = 4
    phase2_start = sec["start"] + bar * 12

    while t < t_end - 0.3:
        next_t = min(t + bar * step_bars, t_end)
        bars_here = max(0.25, (next_t - t) / bar)
        prog = (t - sec["start"]) / total
        energy = avg_energy(e_rms, t, next_t)
        pos = SLOW_PENDULUM[n % len(SLOW_PENDULUM)]

        if t < phase2_start:
            # Phase 1: hold cream warmth, slowly dimming
            fade_f = max(0.4, 1.0 - prog * 0.6)
            s_dim = int(140 * fade_f)
            b_dim = int(120 * fade_f)
            p_dim = int(80 * fade_f)
            par_m = int(140 * fade_f)

            sid = cached(f"fade1_{n}", lambda: organism(
                f"Fade1 {n}", pos, energy, frost=170,
                s_color=SH_SILVER, b_color=BSW_SILVER, p_color=PF_SILVER,
                par=CREAM_WHITE, miss=tuple(c // 3 for c in CREAM_WHITE),
                ni_rgb=CREAM_WHITE, halo=H_BLU,
                s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m,
                prism=False, lasers=(prog < 0.5),
                ni_tilt=(160, 180, 170) if prog < 0.3 else (64, 64, 64)))
        else:
            # Phase 2: return to indigo — the show ends where it began
            star_prog = (t - phase2_start) / max(0.1, t_end - phase2_start)
            dim_f = max(0.0, 1.0 - star_prog)
            s_dim = int(60 * dim_f)
            b_dim = int(50 * dim_f)
            p_dim = max(10, int(40 * dim_f))
            par_m = int(40 * dim_f)

            sid = cached(f"fade2_{n}", lambda: organism(
                f"Fade2 {n}", pos, energy, frost=230,
                s_color=SH_INDIGO, b_color=BSW_INDIGO, p_color=PF_INDIGO,
                par=DEEP_INDIGO, miss=NEAR_BLACK,
                ni_rgb=DEEP_INDIGO, halo=H_OFF,
                s_dim=s_dim, b_dim=b_dim, p_dim=p_dim, par_m=par_m))

        timing, technique = phrase_step_timing(t, next_t, bars_here)
        step_bars = next_step_bars(technique, default="4bar", cap=4)
        steps.append((sid, timing))
        t = next_t
        n += 1

    # Final blackout
    steps.append((0, snap(BPM, 0.5, fade_ms=100)))


# =============================================================================
# MAIN — dispatch sections + insert transitions
# =============================================================================

BUILDERS = {
    "OPENING":  build_opening,
    "VERSE_1":  build_verse_1,
    "BREATHE":  build_breathe,
    "SURGE":    build_surge,
    "DIMMING":  build_dimming,
    "VOID":     build_void,
    "REBUILD":  build_rebuild,
    "PEAK":     build_peak,
    "FADE":     build_fade,
}

print(f"Generating show: {SONG_STEM}")
print(f"  BPM: {BPM}, Beats: {len(beats)}, Duration: {beats[-1]:.1f}s")
print()

prev_phrase = None
prev_energy = 0.0
recent_transitions = []
last_scene_dict = None

for i, sec in enumerate(SECTIONS):
    energy = avg_energy(e_rms, sec["start"], sec["end"])

    # --- Transition at section boundary ---
    trans_offset_s = 0.0
    if i > 0:
        _, seg_here = segment_at(sec["start"])
        cur_phrase = classify_phrase(
            segment_label=seg_here["label"],
            rms=energy, sub=avg_energy(e_sub, sec["start"], sec["end"]),
            high=energy,
            progress=sec["start"] / max(1.0, beats[-1]),
            project_root=PROJECT_ROOT,
        )
        trans = plan_segment_transition(
            prev_phrase=prev_phrase, next_phrase=cur_phrase,
            prev_energy=prev_energy, next_energy=energy,
            segment_index=i, total_segments=len(SECTIONS),
            recent_transitions=recent_transitions,
            show_key=SONG_STEM,
            end_of_show=(i == len(SECTIONS) - 1),
            prev_segment_beats=SECTIONS[i-1]["bars"] * 4,
            next_segment_beats=sec["bars"] * 4,
            project_root=PROJECT_ROOT,
        )
        t_scenes, t_timing = build_transition_scenes(
            trans, BPM, pos_tuples=POS, palette=DEEP_INDIGO,
            last_scene=last_scene_dict,
        )
        for ts, tt in zip(t_scenes, t_timing):
            idx = len(scenes)
            scenes.append(ts)
            steps.append((idx, tt))
            trans_offset_s += (tt[0] + tt[1]) / 1000.0
        if trans:
            recent_transitions.append(trans["type"])
            if len(recent_transitions) > 6:
                del recent_transitions[:-6]

    # Offset section start so transitions borrow time
    build_sec = sec
    if trans_offset_s > 0:
        build_sec = {**sec, "start": sec["start"] + trans_offset_s}

    print(f"  Building {sec['name']:10s} ({sec['bars']:2d} bars, e={energy:.2f})")
    BUILDERS[sec["name"]](build_sec)

    if steps:
        last_scene_dict = scenes[steps[-1][0]]

    _, seg_at_end = segment_at(sec["end"] - 0.1)
    prev_phrase = classify_phrase(
        segment_label=seg_at_end["label"],
        rms=energy, sub=avg_energy(e_sub, sec["start"], sec["end"]),
        high=energy,
        progress=sec["end"] / max(1.0, beats[-1]),
        project_root=PROJECT_ROOT,
    )
    prev_energy = energy

# =============================================================================
# STATS + OUTPUT
# =============================================================================

print(f"\nTotal scenes: {len(scenes)}")
print(f"Total chaser steps: {len(steps)}")
print(f"Phrase bars: {PHRASE_BAR_COUNTS}")
top_techniques = sorted(TECHNIQUE_COUNTS.items(), key=lambda kv: kv[1], reverse=True)[:8]
print(f"Top technique usage: {top_techniques}")

total_ms = sum(fi + ho for _, (fi, ho) in steps)
print(f"Total duration: {total_ms/1000:.1f}s (target: ~{beats[-1]:.0f}s)")

main_chaser = make_chaser("OnlyL", [s for s, _ in steps], [t for _, t in steps],
                           run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "\u25b6 ONLY L",  "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10,  "w": 470, "h": 100, "color": "#08052A", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,  "color": "#FF0000", "action": "Toggle"},
]

output_path = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")
write_workspace(output_path, scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
