#!/usr/bin/env python3
"""
QLC+ Show Generator Library
Reusable fixture helpers, color constants, and workspace generation
for Ben Wilson's lighting rig.

Usage:
    from showlib import *

    scenes = [
        scene("My Look",
            sharpy(pan=153, tilt=0, color7=BSW_B),
            bsw(pan=7, tilt=19, color=BSW_B),
            profile(pan=0, tilt=123, color=44),
            fourbar_solid(0, 0, 255),
            miss_both(0, 0, 255),
            ni3k(r=0, g=0, b=255, halo=H_BLU),
        ),
    ]

    chaser = make_chaser("My Chaser", scenes, timing=[...])
    write_workspace("shows/My-Show.qxw", scenes, [chaser], bpm=174)
"""

import os
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from typing import List, Tuple, Dict, Optional, Any, Sequence

_PHRASE_PLANNER_CACHE: Dict[str, Any] = {}
_VENUE_PROFILE_CACHE: Dict[Tuple[str, str], Any] = {}
_FOCUS_POSITION_CACHE: Dict[Tuple[str, str], Any] = {}
_DESIGNER_PACK_MEMORY_CACHE: Dict[str, Dict[str, Any]] = {}
_DESIGNER_PACK_MEMORY_SEEN_SHOWS: set[Tuple[str, str]] = set()

# =============================================================================
# FIXTURE CONSTANTS
# =============================================================================

# Fixture IDs (as assigned in QLC+)
FX_BSW = 1
FX_4BAR = 2
FX_NI3K = 3
FX_PROFILE = 4
FX_MISS1 = 5
FX_MISS2 = 6
FX_SHARPY = 8

# DMX Addresses (0-indexed for XML)
ADDR_4BAR = 0
ADDR_MISS1 = 48
ADDR_MISS2 = 56
ADDR_SHARPY = 96
ADDR_BSW = 144
ADDR_PROFILE = 192
ADDR_NI3K = 240

# Channel counts
CH_4BAR = 15
CH_MISS = 7
CH_SHARPY = 18
CH_BSW = 20
CH_PROFILE = 14
CH_NI3K = 19

# =============================================================================
# BSW COLOR WHEEL (Ch8) - Verified from fixture definition
# =============================================================================

BSW_WHITE  = 0
BSW_RED    = 20
BSW_ORANGE = 26
BSW_YELLOW = 32
BSW_GREEN  = 38
BSW_BLUE   = 44
BSW_MAG    = 50
BSW_TEAL   = 56
BSW_PINK   = 62
# 64-127: Color wheel indexing (continuous)
# 128-189: CCW rotation fast→slow
# 190-193: Stop
# 194-255: CW rotation slow→fast
BSW_SPIN_CW  = 220   # Medium CW spin
BSW_SPIN_CCW = 160   # Medium CCW spin

# BSW Gobo 1 positions (Ch9)
BSW_G1_OPEN = 0
BSW_G1_1 = 12; BSW_G1_2 = 21; BSW_G1_3 = 30; BSW_G1_4 = 39; BSW_G1_5 = 48; BSW_G1_6 = 57; BSW_G1_7 = 64

# BSW Gobo 2 positions (Ch10)
BSW_G2_OPEN = 0
BSW_G2_1 = 12; BSW_G2_2 = 21; BSW_G2_3 = 30; BSW_G2_4 = 39; BSW_G2_5 = 48; BSW_G2_6 = 57

# =============================================================================
# NI3K HALO LED (Ch17) - Verified from fixture definition
# =============================================================================

H_OFF = 0
H_RED = 24
H_GRN = 40
H_BLU = 56
H_YEL = 72
H_PNK = 88
H_CYN = 104
H_RGB = 120
# 128-255: Color jump fast→slow
H_JUMP_FAST = 130
H_JUMP_MED  = 190
H_JUMP_SLOW = 250

# NI3K Laser values
LASER_OFF = 0
LASER_ON  = 255    # 250-255 = steady on
LASER_STROBE_SLOW = 20
LASER_STROBE_MED  = 128
LASER_STROBE_FAST = 245

# =============================================================================
# SHARPY CONSTANTS
# =============================================================================

# Strobe (Ch6): 0=closed, 2-127=strobe slow→fast, 128-192=strobe fade out, 252-255=open
SHARPY_CLOSED = 0
SHARPY_OPEN   = 252
SHARPY_STROBE_SLOW = 10
SHARPY_STROBE_MED  = 64
SHARPY_STROBE_FAST = 120

# Color Macro wheel (Ch8) - VERIFIED via physical testing
SHARPY_WHITE      = 0
SHARPY_RED        = 10
SHARPY_YELLOW     = 20
SHARPY_BLUE       = 30
SHARPY_GREEN      = 40
SHARPY_PURPLE     = 50
SHARPY_PINK       = 60
SHARPY_TEAL       = 70
SHARPY_AMBER      = 80
SHARPY_ORANGE     = 90
SHARPY_DARK_YEL   = 100
SHARPY_LIME       = 110
SHARPY_GREY       = 120
# 5,15,25... = split colors (half positions between adjacent colors)
# 150-211 = CW rotation fast→slow
# 211-255 = CCW rotation slow→fast
SHARPY_SPIN_CW    = 180   # Medium CW spin
SHARPY_SPIN_CCW   = 235   # Medium CCW spin

# Color filter (Ch16) - NOT a color wheel
# 0=open/white, gradually overlays a color filter. Leave at 0.
SHARPY_FILTER_OPEN = 0

# =============================================================================
# BSW SHUTTER CONSTANTS (Ch16)
# =============================================================================

BSW_SHUT_CLOSED = 0    # 0-7: Off
BSW_SHUT_OPEN   = 8    # 8-15: On
BSW_SHUT_STROBE_SLOW = 20
BSW_SHUT_STROBE_FAST = 128

# =============================================================================
# PROFILE STROBE (Ch1) - 0=open (verified), exact strobe ranges TBD
# =============================================================================

PROFILE_STROBE_OFF = 0

# =============================================================================
# PROFILE COLOR WHEEL (Ch5) - VERIFIED via physical testing
# =============================================================================

PROF_WHITE  = 0
PROF_RED    = 5
PROF_YELLOW = 10
PROF_BLUE   = 15
PROF_GREEN  = 20
PROF_ORANGE = 25
PROF_PINK   = 30
PROF_TEAL   = 35
# 40-78: split colors (white/red, red/yellow, yellow/blue, etc.)
# 79-255: wheel rotation slow→fast
PROF_SPIN   = 160   # Medium rotation speed

# =============================================================================
# FIXTURE HELPER FUNCTIONS
# Each returns a tuple of (fixture_id, [(ch, val), ...])
# =============================================================================

def sharpy(pan=0, tilt=0, color7=0, gobo=0,
           prism1=0, p1r=0, prism2=0, p2r=0,
           frost=0, focus=128, strobe=SHARPY_OPEN, dim=255,
           colormacro=0):
    """Sharpy Knockoff - 18ch mode (ID 8, addr 96)

    Channel map:
        0:Pan  1:Tilt  2:PanFine  3:TiltFine  4:PTSpeed
        5:Frost  6:Strobe  7:Dimmer  8:ColorMacro  9:ColorFine
        10:Gobo  11:Prism1  12:Prism1.r  13:Prism2  14:Prism2.r
        15:Focus  16:7color  17:Reset
    """
    return (FX_SHARPY, [
        (0,pan),(1,tilt),(2,0),(3,0),(4,0),
        (5,frost),(6,strobe),(7,dim),
        (8,colormacro),(9,0),(10,gobo),
        (11,prism1),(12,p1r),(13,prism2),(14,p2r),
        (15,focus),(16,color7),(17,0)
    ])

def bsw(pan=177, tilt=19, color=0, gobo1=0, gobo2=0, g2rot=0,
         frost=0, prism=0, prot=0, focus=128,
         shutter=BSW_SHUT_OPEN, dim=255):
    """BSW 3-in-1 - 20ch mode (ID 1, addr 144)

    Channel map:
        0:Pan  1:PanFine  2:Tilt  3:TiltFine  4:PTSpeed
        5:ShowMode(0)  6:PTMacro(0)  7:PTMacroSpeed
        8:Color  9:Gobo1  10:Gobo2  11:Gobo2Rot
        12:Angle/Frost  13:Prism  14:PrismRot
        15:Focus  16:Shutter  17:Dimmer  18:DimFine  19:Special(0)
    """
    return (FX_BSW, [
        (0,pan),(1,0),(2,tilt),(3,0),(4,0),
        (5,0),(6,0),(7,0),
        (8,color),(9,gobo1),(10,gobo2),(11,g2rot),
        (12,frost),(13,prism),(14,prot),
        (15,focus),(16,shutter),(17,dim),(18,0),(19,0)
    ])

def profile(pan=0, tilt=0, color=0, gobo=0, gobo1=0, g1rot=0,
            prism=0, focus=128, strobe=PROFILE_STROBE_OFF, dim=255):
    """Profile Knockoff - 14ch mode (ID 4, addr 192)

    Channel map:
        0:Dimmer  1:Strobe  2:Pan  3:Tilt  4:PTSpeed
        5:Color  6:Gobo  7:Gobo1  8:Gobo1Rot
        9:Prism  10:Focus  11:PanFine  12:TiltFine  13:Reset
    """
    return (FX_PROFILE, [
        (0,dim),(1,strobe),(2,pan),(3,tilt),(4,0),
        (5,color),(6,gobo),(7,gobo1),(8,g1rot),
        (9,prism),(10,focus),(11,0),(12,0),(13,0)
    ])

def fourbar(r1,g1,b1, r2,g2,b2, r3,g3,b3, r4,g4,b4, master=255, strobe=0):
    """Chauvet 4BAR - 15ch mode (ID 2, addr 0)

    Channel map:
        0:Program(0)  1:Master  2:Strobe
        3:P1R  4:P1G  5:P1B  6:P2R  7:P2G  8:P2B
        9:P3R  10:P3G  11:P3B  12:P4R  13:P4G  14:P4B
    """
    return (FX_4BAR, [
        (0,0),(1,master),(2,strobe),
        (3,r1),(4,g1),(5,b1),(6,r2),(7,g2),(8,b2),
        (9,r3),(10,g3),(11,b3),(12,r4),(13,g4),(14,b4)
    ])

def fourbar_solid(r, g, b, master=255, strobe=0):
    """4BAR with all 4 pars the same color."""
    return fourbar(r,g,b, r,g,b, r,g,b, r,g,b, master, strobe)

def fourbar_pairs(r1,g1,b1, r2,g2,b2, master=255, strobe=0):
    """4BAR alternating: P1+P3 = color1, P2+P4 = color2."""
    return fourbar(r1,g1,b1, r2,g2,b2, r1,g1,b1, r2,g2,b2, master, strobe)

def fourbar_gradient(r1,g1,b1, r2,g2,b2, master=255, strobe=0):
    """4BAR gradient from color1 (P1) to color2 (P4)."""
    rm = (r1+r2)//2; gm = (g1+g2)//2; bm = (b1+b2)//2
    r3 = (rm+r2)//2; g3 = (gm+g2)//2; b3 = (bm+b2)//2
    return fourbar(r1,g1,b1, rm,gm,bm, r3,g3,b3, r2,g2,b2, master, strobe)

def missyee(r, g, b, master=255, strobe=0, fixture_id=FX_MISS1):
    """Missyee 36 RGB LED - 7ch mode

    Channel map:
        0:Master  1:Red  2:Green  3:Blue  4:Strobe(0)  5:Effect(0)  6:Color(0)
    """
    return (fixture_id, [
        (0,master),(1,r),(2,g),(3,b),(4,strobe),(5,0),(6,0)
    ])

def miss1(r, g, b, master=255, strobe=0):
    """Missyee #1 (ID 5, addr 48) - right wall."""
    return missyee(r, g, b, master, strobe, FX_MISS1)

def miss2(r, g, b, master=255, strobe=0):
    """Missyee #2 (ID 6, addr 56) - right wall."""
    return missyee(r, g, b, master, strobe, FX_MISS2)

def miss_both(r, g, b, master=255, strobe=0):
    """Both Missyee pars with the same color. Returns TWO fixture tuples."""
    return [miss1(r, g, b, master, strobe), miss2(r, g, b, master, strobe)]

def ni3k(pan=128, t1=64, t2=64, t3=64,
         r=255, g=255, b=255, w=0,
         halo=H_OFF, rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF,
         ledeff=0, moteff=0, effspd=0, dim=255, strobe=0):
    """Nausea Inducer 3000 - 19ch mode (ID 3, addr 240)

    Channel map:
        0:Pan  1:Tilt1  2:Tilt2  3:Tilt3  4:PTSpeed
        5:Dimmer  6:Strobe(0=on)  7:Red  8:Green  9:Blue  10:White
        11:LEDeffect  12:MotorEffect  13:EffectSpeed
        14:RedLaser  15:GreenLaser  16:BlueLaser
        17:HaloLED  18:Reset
    """
    return (FX_NI3K, [
        (0,pan),(1,t1),(2,t2),(3,t3),(4,0),
        (5,dim),(6,strobe),
        (7,r),(8,g),(9,b),(10,w),
        (11,ledeff),(12,moteff),(13,effspd),
        (14,rl),(15,gl),(16,bl),(17,halo),(18,0)
    ])

# =============================================================================
# BLACKOUT HELPERS
# =============================================================================

# DSC (Downstage Center) pan/tilt — the default mover park position.
# Movers hold here when blacked out to prevent unwanted pan spins.
_DSC_SHARPY = (158, 6)    # (pan, tilt)
_DSC_BSW    = (179, 27)
_DSC_PROF   = (64, 145)
_DSC_NI3K   = 128          # pan only

def blackout(fixture_id: int, num_channels: int):
    """Generic blackout for any fixture (all channels to 0).

    WARNING: For movers (Sharpy, BSW, Profile, NI3K), this sends pan/tilt
    to 0, causing physical head movement. Use the dark_*() functions instead
    to black out movers while keeping them parked at DSC.
    """
    return (fixture_id, [(i, 0) for i in range(num_channels)])


def dark_sharpy(pan=None, tilt=None):
    """Sharpy with output killed but head parked at a position.
    Defaults to DSC. Prevents pan spins during blackout scenes."""
    p = _DSC_SHARPY[0] if pan is None else pan
    t = _DSC_SHARPY[1] if tilt is None else tilt
    return sharpy(pan=p, tilt=t, dim=0, strobe=SHARPY_CLOSED)


def dark_bsw(pan=None, tilt=None):
    """BSW with output killed but head parked at a position.
    Defaults to DSC. Prevents pan spins during blackout scenes."""
    p = _DSC_BSW[0] if pan is None else pan
    t = _DSC_BSW[1] if tilt is None else tilt
    return bsw(pan=p, tilt=t, dim=0, shutter=BSW_SHUT_CLOSED)


def dark_profile(pan=None, tilt=None):
    """Profile with output killed but head parked at a position.
    Defaults to DSC. Prevents tilt flips during blackout scenes."""
    p = _DSC_PROF[0] if pan is None else pan
    t = _DSC_PROF[1] if tilt is None else tilt
    return profile(pan=p, tilt=t, dim=0)


def dark_ni3k(pan=None):
    """NI3K with all output killed but pan parked at a position.
    Defaults to DSC. LEDs, lasers, halo all off."""
    p = _DSC_NI3K if pan is None else pan
    return ni3k(pan=p, dim=0, r=0, g=0, b=0, w=0,
                halo=H_OFF, rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF)


def blackout_all():
    """All fixtures blacked out with movers parked at DSC.
    Pars/missyees zero all channels. Movers zero output but hold
    pan/tilt at DSC to prevent unwanted physical head movement."""
    return [
        dark_bsw(),
        blackout(FX_4BAR, CH_4BAR),
        dark_ni3k(),
        dark_profile(),
        blackout(FX_MISS1, CH_MISS),
        blackout(FX_MISS2, CH_MISS),
        dark_sharpy(),
    ]

# =============================================================================
# SCENE BUILDER
# =============================================================================

def scene(name: str, *fixtures, path: str = "Show") -> dict:
    """Build a scene dict from fixture tuples.

    Args:
        name: Scene name
        *fixtures: Fixture tuples from helper functions.
                   Can be single tuples or lists (from miss_both).
        path: Folder path in QLC+ function tree

    Returns:
        dict with "name", "path", and "fixtures" (ordered by ID)
    """
    flat = []
    for f in fixtures:
        if isinstance(f, list):
            flat.extend(f)
        else:
            flat.append(f)

    # Sort by fixture ID for consistent XML output
    flat.sort(key=lambda x: x[0])

    return {"name": name, "path": path, "fixtures": flat}

# =============================================================================
# CHASER TIMING HELPERS
# =============================================================================

def bpm_to_ms(bpm: float, beats: float = 4) -> int:
    """Convert BPM and beat count to milliseconds.

    Args:
        bpm: Beats per minute
        beats: Number of beats (default 4 = 1 bar)
    """
    return round((60000 / bpm) * beats)

def smooth(bpm: float, bars: float = 1) -> Tuple[int, int]:
    """Smooth crossfade over N bars. Returns (FadeIn, Hold)."""
    ms = bpm_to_ms(bpm, bars * 4)
    return (ms, 0)

def snap(bpm: float, bars: float = 1, fade_ms: int = 100) -> Tuple[int, int]:
    """Quick snap change, hold for remaining time. Returns (FadeIn, Hold)."""
    ms = bpm_to_ms(bpm, bars * 4)
    return (fade_ms, ms - fade_ms)

def hold(bpm: float, bars: float = 1) -> Tuple[int, int]:
    """Instant change, hold for N bars. Returns (FadeIn, Hold)."""
    ms = bpm_to_ms(bpm, bars * 4)
    return (0, ms)

# =============================================================================
# WORKSPACE XML GENERATION
# =============================================================================

# Fixture definitions for the workspace XML (ID order)
FIXTURE_DEFS = [
    {"id": 1, "mfr": "Generic", "model": "Beam Spot Wash 3 in 1", "mode": "20 channel",
     "name": "Beam Spot Wash 3 in 1", "addr": 144, "ch": 20},
    {"id": 2, "mfr": "Chauvet", "model": "4BAR", "mode": "15 Channel",
     "name": "4BAR", "addr": 0, "ch": 15},
    {"id": 3, "mfr": "Generic", "model": "Nausea Inducer 3000", "mode": "19 channel",
     "name": "Nausea Inducer 3000", "addr": 240, "ch": 19},
    {"id": 4, "mfr": "Generic", "model": "Profile Knockoff", "mode": "14 channel",
     "name": "Profile Knockoff", "addr": 192, "ch": 14},
    {"id": 5, "mfr": "Missyee", "model": "36 RGB LED", "mode": "7 channel",
     "name": "36 RGB LED", "addr": 48, "ch": 7},
    {"id": 6, "mfr": "Missyee", "model": "36 RGB LED", "mode": "7 channel",
     "name": "36 RGB LED #2", "addr": 56, "ch": 7},
    {"id": 8, "mfr": "Generic", "model": "Sharpy Knockoff", "mode": "18 channel",
     "name": "Sharpy Knockoff", "addr": 96, "ch": 18},
]

# Monitor stage positions (from user's QLC+ save)
STAGE_POSITIONS = [
    (1, "386.582", "1000", "287.18"),
    (2, "1961.2", "1000", "386.889"),
    (3, "3355.38", "1000", "335.202"),
    (4, "2342.48", "1000", "4250.46"),
    (5, "25.06", "1000", "1519.79"),
    (6, "22.4348", "1000", "1012.91"),
    (8, "4341.8", "1000", "345.539"),
]


def make_chaser(name: str, scene_ids: List[int], timing: List[Tuple[int, int]],
                run_order: str = "SingleShot", path: str = "Show") -> dict:
    """Build a chaser dict.

    Args:
        name: Chaser name
        scene_ids: List of scene function IDs to sequence
        timing: List of (FadeIn_ms, Hold_ms) per step
        run_order: "SingleShot", "Loop", or "PingPong"
        path: Folder path
    """
    assert len(scene_ids) == len(timing), "scene_ids and timing must match length"
    return {
        "name": name,
        "path": path,
        "scene_ids": scene_ids,
        "timing": timing,
        "run_order": run_order,
    }


_XML_ATTR_ESCAPES = {'"': '&quot;', "'": '&apos;'}


def _xml_attr(value: Any) -> str:
    """Escape text for safe XML attribute interpolation."""
    return escape(str(value), _XML_ATTR_ESCAPES)


def _xml_text(value: Any) -> str:
    """Escape text for safe XML node interpolation."""
    return escape(str(value))


def write_workspace(filename: str, scenes: List[dict], chasers: List[dict] = None,
                    bpm: int = 174, artnet_ip: str = "10.0.0.7",
                    vc_buttons: List[dict] = None,
                    fixture_defs: Optional[List[dict]] = None,
                    stage_positions: Optional[List[Tuple[int, str, str, str]]] = None):
    """Write a complete QLC+ 5.0.1 workspace file.

    Args:
        filename: Output path
        scenes: List of scene dicts from scene()
        chasers: List of chaser dicts from make_chaser()
        bpm: BPM for the beat generator
        artnet_ip: ArtNet output IP
        vc_buttons: Optional custom VC buttons. If None, auto-generates
                    a button for each chaser + blackout.
        fixture_defs: Optional fixture definitions override (defaults to FIXTURE_DEFS)
        stage_positions: Optional monitor stage positions override
                         (defaults to STAGE_POSITIONS)
    """
    chasers = chasers or []
    fixture_defs = fixture_defs if fixture_defs is not None else FIXTURE_DEFS
    stage_positions = stage_positions if stage_positions is not None else STAGE_POSITIONS

    # Assign function IDs: scenes get 0..N-1, chasers get N..N+M-1
    next_id = len(scenes)
    chaser_ids = {}
    for i, ch in enumerate(chasers):
        chaser_ids[i] = next_id + i

    lines = []
    def L(s): lines.append(s)

    L('<?xml version="1.0" encoding="UTF-8"?>')
    L('<!DOCTYPE Workspace>')
    L('<Workspace xmlns="http://www.qlcplus.org/Workspace" CurrentWindow="VC">')
    L(' <Creator>')
    L('  <Name>Q Light Controller Plus</Name>')
    L('  <Version>5.0.1</Version>')
    L('  <Author>Ben Wilson</Author>')
    L(' </Creator>')
    L(' <Engine>')

    # InputOutputMap
    L('  <InputOutputMap>')
    L(f'   <BeatGenerator BeatType="Internal" BPM="{_xml_attr(bpm)}"/>')
    L('   <Universe Name="Universe 1" ID="0">')
    L(f'    <Output Plugin="ArtNet" UID="{_xml_attr(artnet_ip)}" Line="0"/>')
    L('   </Universe>')
    L('  </InputOutputMap>')

    # Fixtures
    for fx in fixture_defs:
        L('  <Fixture>')
        L(f'   <Manufacturer>{_xml_text(fx["mfr"])}</Manufacturer>')
        L(f'   <Model>{_xml_text(fx["model"])}</Model>')
        L(f'   <Mode>{_xml_text(fx["mode"])}</Mode>')
        L(f'   <ID>{fx["id"]}</ID>')
        L(f'   <Name>{_xml_text(fx["name"])}</Name>')
        L('   <Universe>0</Universe>')
        L(f'   <Address>{fx["addr"]}</Address>')
        L(f'   <Channels>{fx["ch"]}</Channels>')
        L('  </Fixture>')

    # Scenes
    for sid, sc in enumerate(scenes):
        L(f'  <Function ID="{sid}" Type="Scene" Name="{_xml_attr(sc["name"])}" Path="{_xml_attr(sc["path"])}">')
        L('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
        for fid, channels in sc["fixtures"]:
            val_str = ','.join(f'{ch},{val}' for ch, val in channels)
            L(f'   <FixtureVal ID="{fid}">{_xml_text(val_str)}</FixtureVal>')
        L('  </Function>')

    # Chasers
    for i, ch in enumerate(chasers):
        cid = chaser_ids[i]
        L(f'  <Function ID="{cid}" Type="Chaser" Name="{_xml_attr(ch["name"])}" Path="{_xml_attr(ch["path"])}">')
        L('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
        L('   <Direction>Forward</Direction>')
        L(f'   <RunOrder>{_xml_text(ch["run_order"])}</RunOrder>')
        L('   <SpeedModes FadeIn="PerStep" FadeOut="Default" Duration="PerStep"/>')
        for step_num, (scene_id, (fi, ho)) in enumerate(zip(ch["scene_ids"], ch["timing"])):
            L(f'   <Step Number="{step_num}" FadeIn="{fi}" Hold="{ho}" FadeOut="0">{scene_id}</Step>')
        L('  </Function>')

    L(' </Engine>')

    # Virtual Console
    L(' <VirtualConsole>')
    L('  <Frame Caption="">')
    L('   <Appearance>')
    L('    <FrameStyle>None</FrameStyle>')
    L('    <ForegroundColor>Default</ForegroundColor>')
    L('    <BackgroundColor>Default</BackgroundColor>')
    L('    <BackgroundImage>None</BackgroundImage>')
    L('    <Font>Default</Font>')
    L('   </Appearance>')

    if vc_buttons:
        for btn in vc_buttons:
            L(f'   <Button Caption="{_xml_attr(btn["caption"])}" ID="{btn["vc_id"]}" Icon="">')
            L(f'    <WindowState Visible="True" X="{btn["x"]}" Y="{btn["y"]}" Width="{btn["w"]}" Height="{btn["h"]}"/>')
            L('    <Appearance>')
            L(f'     <BackgroundColor>{_xml_text(btn["color"])}</BackgroundColor>')
            L('    </Appearance>')
            L(f'    <Function ID="{btn["func_id"]}"/>')
            L(f'    <Action>{_xml_text(btn.get("action", "Toggle"))}</Action>')
            L('   </Button>')
    else:
        # Auto-generate: one button per chaser + blackout
        vc_id = 0
        y = 10
        for i, ch in enumerate(chasers):
            cid = chaser_ids[i]
            L(f'   <Button Caption="{_xml_attr(ch["name"])}" ID="{vc_id}" Icon="">')
            L(f'    <WindowState Visible="True" X="10" Y="{y}" Width="470" Height="80"/>')
            L('    <Appearance>')
            L('     <BackgroundColor>#22AA22</BackgroundColor>')
            L('    </Appearance>')
            L(f'    <Function ID="{cid}"/>')
            L('    <Action>Toggle</Action>')
            L('   </Button>')
            vc_id += 1
            y += 90

        # Find blackout scene (last scene with "blackout" in name, or create reference)
        blackout_id = None
        for sid, sc in enumerate(scenes):
            if "blackout" in sc["name"].lower():
                blackout_id = sid
        if blackout_id is not None:
            L(f'   <Button Caption="BLACKOUT" ID="{vc_id}" Icon="">')
            L(f'    <WindowState Visible="True" X="10" Y="{y}" Width="470" Height="80"/>')
            L('    <Appearance>')
            L('     <BackgroundColor>#FF0000</BackgroundColor>')
            L('    </Appearance>')
            L(f'    <Function ID="{blackout_id}"/>')
            L('    <Action>Toggle</Action>')
            L('   </Button>')

    L('  </Frame>')
    L('  <Properties>')
    L('   <Size Width="1920" Height="1080"/>')
    L('   <GrandMaster ChannelMode="Intensity" ValueMode="Reduce" SliderMode="Normal"/>')
    L('  </Properties>')
    L(' </VirtualConsole>')

    # Monitor
    L(' <Monitor DisplayMode="0" ShowLabels="0">')
    L('  <Font>Arial,12,-1,5,400,0,0,0,0,0,0,0,0,0,0,1</Font>')
    L('  <ChannelStyle>0</ChannelStyle>')
    L('  <ValueStyle>0</ValueStyle>')
    L('  <Grid Width="5" Height="3" Depth="5" Units="0"/>')
    L('  <StageItem>0</StageItem>')
    for fid, x, y_pos, z in stage_positions:
        L(f'  <FxItem ID="{fid}" XPos="{x}" YPos="{y_pos}" ZPos="{z}"/>')
    L(' </Monitor>')
    L('</Workspace>')

    with open(filename, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    total_steps = sum(len(ch["scene_ids"]) for ch in chasers)
    print(f"Wrote {filename}")
    print(f"  Scenes: {len(scenes)}, Chasers: {len(chasers)} ({total_steps} total steps)")


# =============================================================================
# COLOR PRESETS (RGB tuples for 4BAR / Missyee)
# =============================================================================

# Standard colors
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
WHITE   = (255, 255, 255)
CYAN    = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW  = (255, 255, 0)
AMBER   = (255, 128, 0)
PURPLE  = (128, 0, 255)
TEAL    = (0, 255, 128)
PINK    = (255, 64, 128)
ORANGE  = (255, 64, 0)
WARM    = (255, 180, 100)
COOL    = (100, 180, 255)
OFF     = (0, 0, 0)

# =============================================================================
# MOVEMENT PRESETS
# =============================================================================



# =============================================================================
# GENRE-BASED SHOW STRUCTURE TEMPLATES
# =============================================================================
# Each returns a list of section dicts describing the show structure.
# Use these as blueprints when designing shows — fill in the "look" for each section.
#
# Section dict format:
#   {"name": str, "bars": int, "energy": str, "movement": str,
#    "timing_style": str, "notes": str}
#
# energy: "low", "medium", "high", "peak"
# movement: "static", "slow", "medium", "fast", "sweep"
# timing_style: "smooth", "snap", "hold", "mixed"

def structure_dnb(bars: int = 64) -> list:
    """Drum & Bass show structure (174 BPM typical).

    DnB conventions: fast breakbeats, rolling bass, big builds into drops.
    Lighting should be aggressive on drops, restrained on breakdowns.
    64 bars ≈ 88 seconds at 174 BPM.
    """
    return [
        {"name": "Intro",        "bars": 8,  "energy": "medium", "movement": "slow",
         "timing_style": "smooth", "notes": "Establish mood. Movers at center, minimal color. Pars set atmosphere."},
        {"name": "Build 1",      "bars": 8,  "energy": "medium", "movement": "medium",
         "timing_style": "smooth", "notes": "Movers start spreading. Colors shift. Intensity rising."},
        {"name": "Drop 1",       "bars": 16, "energy": "peak",   "movement": "fast",
         "timing_style": "mixed",  "notes": "FULL SEND. Big sweeps, gobos, prisms, color snaps. Lasers on. 4BAR alternating."},
        {"name": "Breakdown",    "bars": 8,  "energy": "low",    "movement": "slow",
         "timing_style": "smooth", "notes": "Pull back hard. Single color wash. Movers slow sweep or center. Kill lasers."},
        {"name": "Build 2",      "bars": 8,  "energy": "medium", "movement": "medium",
         "timing_style": "smooth", "notes": "Rebuild tension. Layer in effects one at a time."},
        {"name": "Drop 2",       "bars": 16, "energy": "peak",   "movement": "fast",
         "timing_style": "mixed",  "notes": "Even bigger than Drop 1. Different color palette. Prism sweeps. All lasers."},
    ]

def structure_melodic_house(bars: int = 64) -> list:
    """Melodic House show structure (120-128 BPM typical).

    Melodic house conventions: smooth builds, emotional progressions, layered textures.
    Lighting should be warm, evolving, atmospheric. Less aggressive than DnB.
    64 bars ≈ 120 seconds at 128 BPM.
    """
    return [
        {"name": "Intro",        "bars": 8,  "energy": "low",    "movement": "static",
         "timing_style": "smooth", "notes": "Warm wash. Movers at center, soft white or amber. Pars warm tones."},
        {"name": "Groove Build", "bars": 8,  "energy": "low",    "movement": "slow",
         "timing_style": "smooth", "notes": "Gentle color evolution. Movers start slow drift. Build mood not energy."},
        {"name": "Melodic Rise",  "bars": 8,  "energy": "medium", "movement": "medium",
         "timing_style": "smooth", "notes": "Colors deepen. Movers wider movements. Add gobos gently."},
        {"name": "Peak",         "bars": 16, "energy": "high",   "movement": "medium",
         "timing_style": "smooth", "notes": "Full color palette. Sweeping movers. Prisms optional. Keep it smooth, not jarring."},
        {"name": "Emotional Break","bars": 8, "energy": "medium", "movement": "slow",
         "timing_style": "smooth", "notes": "Strip back to single color family. Movers converge. Intimate feel."},
        {"name": "Final Build",  "bars": 8,  "energy": "high",   "movement": "medium",
         "timing_style": "smooth", "notes": "Layer everything back. All warm whites for climax."},
        {"name": "Outro",        "bars": 8,  "energy": "low",    "movement": "slow",
         "timing_style": "smooth", "notes": "Fade down. Return to opening colors. Gentle end."},
    ]

def structure_dubstep(bars: int = 64) -> list:
    """Dubstep show structure (140-150 BPM typical).

    Dubstep conventions: massive drops, heavy wobble bass, half-time feel.
    Lighting should be dramatic contrasts — dark vs blinding. Snap changes on drops.
    64 bars ≈ 110 seconds at 140 BPM.
    """
    return [
        {"name": "Dark Intro",   "bars": 8,  "energy": "low",    "movement": "static",
         "timing_style": "hold",   "notes": "Near blackout. Single mover with tight beam. Deep blue or purple. Tension."},
        {"name": "Ominous Build","bars": 8,  "energy": "medium", "movement": "slow",
         "timing_style": "smooth", "notes": "Add fixtures one by one. Movers rising. Colors getting more intense."},
        {"name": "DROP",         "bars": 16, "energy": "peak",   "movement": "fast",
         "timing_style": "snap",   "notes": "SNAP to full intensity. Strobe hits. Movers fast sweeps. Gobos+prisms. All lasers. Color snaps on wobbles."},
        {"name": "Half-time",    "bars": 8,  "energy": "high",   "movement": "medium",
         "timing_style": "mixed",  "notes": "Still intense but slower movement. Heavy single-color moments. Snap on accents."},
        {"name": "Breakdown",    "bars": 8,  "energy": "low",    "movement": "slow",
         "timing_style": "smooth", "notes": "Dark again. Maybe just NI3K lasers. Movers off or dim."},
        {"name": "DROP 2",       "bars": 16, "energy": "peak",   "movement": "fast",
         "timing_style": "snap",   "notes": "Different color palette from Drop 1. Even more aggressive. Strobe everything."},
    ]

def structure_party(bars: int = 64) -> list:
    """General party music show structure (120-130 BPM typical).

    Party conventions: fun, colorful, crowd-pleasing. Not as structured as genre-specific.
    Rainbow colors, big movements, keep it visually exciting.
    64 bars ≈ 120 seconds at 128 BPM.
    """
    return [
        {"name": "Opener",       "bars": 8,  "energy": "high",   "movement": "medium",
         "timing_style": "smooth", "notes": "Bright and colorful from the start. Rainbow 4BAR. Movers sweeping."},
        {"name": "Color Party",  "bars": 8,  "energy": "high",   "movement": "medium",
         "timing_style": "mixed",  "notes": "Rapid color changes across all fixtures. Fun, not aggressive."},
        {"name": "Spotlight",    "bars": 8,  "energy": "medium", "movement": "slow",
         "timing_style": "smooth", "notes": "Feature one or two fixtures. Pull back others. Create a focal point."},
        {"name": "Build Up",     "bars": 8,  "energy": "medium", "movement": "medium",
         "timing_style": "smooth", "notes": "Layer fixtures back in. Rising intensity."},
        {"name": "Full Send",    "bars": 16, "energy": "peak",   "movement": "fast",
         "timing_style": "mixed",  "notes": "Everything on. Big sweeps. Color chases. Gobos + prisms. Lasers. Go wild."},
        {"name": "Cool Down",    "bars": 8,  "energy": "medium", "movement": "slow",
         "timing_style": "smooth", "notes": "Bring it back. Warm colors. Smooth movements."},
        {"name": "Finale",       "bars": 8,  "energy": "peak",   "movement": "fast",
         "timing_style": "snap",   "notes": "One more burst. White convergence. Snap to blackout."},
    ]

def print_structure(structure: list, bpm: int):
    """Print a show structure with timing info."""
    bar_ms = bpm_to_ms(bpm, 4)
    total_bars = sum(s["bars"] for s in structure)
    total_ms = total_bars * bar_ms
    print(f"\nShow Structure ({total_bars} bars, {total_ms/1000:.1f}s at {bpm} BPM)")
    print("-" * 80)
    time_offset = 0
    for s in structure:
        duration_ms = s["bars"] * bar_ms
        print(f"  [{time_offset/1000:6.1f}s] {s['name']:20s} | {s['bars']:2d} bars ({duration_ms/1000:.1f}s) "
              f"| {s['energy']:6s} | {s['movement']:6s} | {s['timing_style']}")
        print(f"           {s['notes']}")
        time_offset += duration_ms
    print("-" * 80)
    print(f"  Total: {total_ms/1000:.1f}s")


# =============================================================================
# PHRASE-AWARE PLANNING WRAPPERS
# =============================================================================

def get_phrase_planner(project_root: Optional[str] = None):
    """Return cached phrase planner loaded from references/data catalogs.

    This keeps showlib as a thin integration point while phrase logic lives in
    qlc_runtime.phrase_planner.
    """
    root = os.path.abspath(project_root or os.path.dirname(os.path.abspath(__file__)))
    planner = _PHRASE_PLANNER_CACHE.get(root)
    if planner is None:
        from qlc_runtime.phrase_planner import PhraseAwarePlanner

        planner = PhraseAwarePlanner.from_project_defaults(root)
        _PHRASE_PLANNER_CACHE[root] = planner
    return planner


def classify_phrase(
    segment_label: str,
    rms: float,
    sub: float,
    high: float,
    progress: float,
    project_root: Optional[str] = None,
) -> str:
    """Classify a segment/bar into canonical phrase buckets."""
    planner = get_phrase_planner(project_root)
    return planner.classify_phrase(
        segment_label=segment_label,
        rms=rms,
        sub=sub,
        high=high,
        progress=progress,
    )


def _dedupe_preserve(items: Sequence[str]) -> List[str]:
    out: List[str] = []
    seen: set[str] = set()
    for raw in items:
        text = str(raw).strip()
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(text)
    return out


def _clean_creative_text(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    lowered = text.lower()
    if lowered in {"todo", "tbd", "na", "n/a", "none", "null"}:
        return ""
    if "todo" in lowered or "example.com" in lowered:
        return ""
    return text


def _clean_creative_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    return _dedupe_preserve(
        [
            text
            for text in (_clean_creative_text(item) for item in value)
            if text
        ]
    )


def build_creative_context(
    brief: Optional[Dict[str, Any]],
    song_stem: Optional[str] = None,
) -> Dict[str, Any]:
    """Build normalized brand tokens + creative directives from a research brief.

    Use this once per generator and pass:
    - context["brand_tokens"] -> pick_phrase_technique(..., brand_tokens=...)
    - context["creative_directives"] -> pick_phrase_technique(..., creative_directives=...)
    """
    payload = brief if isinstance(brief, dict) else {}

    song_title = (
        _clean_creative_text(payload.get("song_title", ""))
        or _clean_creative_text(song_stem or "")
    )
    artist = _clean_creative_text(payload.get("artist", ""))
    thesis = _clean_creative_text(payload.get("thesis", ""))

    branding = payload.get("artist_branding")
    if not isinstance(branding, dict):
        branding = {}
    branding_summary = _clean_creative_text(branding.get("summary", ""))
    visual_cues = _clean_creative_list(branding.get("visual_cues"))
    do_not_copy = _clean_creative_list(branding.get("do_not_copy"))

    title_inspo = payload.get("song_title_inspiration")
    if not isinstance(title_inspo, dict):
        title_inspo = {}
    title_keywords = _clean_creative_list(title_inspo.get("keywords"))
    title_motifs = _clean_creative_list(title_inspo.get("motifs"))

    visual_direction = payload.get("visual_direction")
    if not isinstance(visual_direction, dict):
        visual_direction = {}
    color_story = _clean_creative_text(visual_direction.get("color_story", ""))
    motion_story = _clean_creative_text(visual_direction.get("motion_story", ""))
    staging_story = _clean_creative_text(visual_direction.get("staging_story", ""))
    direction_notes = [row for row in (color_story, motion_story, staging_story) if row]

    style_constraints = payload.get("style_constraints")
    if not isinstance(style_constraints, dict):
        style_constraints = {}
    must_include = _clean_creative_list(style_constraints.get("must_include"))
    avoid = _clean_creative_list(style_constraints.get("avoid"))

    raw_score = payload.get("brand_alignment_score")
    try:
        alignment_score = float(raw_score)
    except Exception:
        alignment_score = 0.0
    alignment_score = max(0.0, min(5.0, alignment_score))
    alignment_weight = round(0.45 + (0.55 * (alignment_score / 5.0)), 4)

    brand_tokens = _dedupe_preserve(
        [
            token
            for token in (
                artist,
                song_title,
                thesis,
                branding_summary,
                *visual_cues,
                *title_keywords,
                *title_motifs,
                *direction_notes,
                *must_include,
            )
            if token
        ]
    )

    creative_directives = {
        "must_include": must_include,
        "avoid": avoid,
        "do_not_copy": do_not_copy,
        "direction_notes": direction_notes,
        "branding_notes": [token for token in (branding_summary, *visual_cues) if token],
        "thesis": thesis,
        "brand_alignment_score": alignment_score,
        "brand_alignment_weight": alignment_weight,
    }

    return {
        "brand_tokens": brand_tokens,
        "creative_directives": creative_directives,
    }


def _designer_pack_memory_path(project_root: Optional[str] = None) -> str:
    root = os.path.abspath(project_root or os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "references", "data", "designer-pack-memory.json")


def _load_designer_pack_memory(project_root: Optional[str] = None) -> Dict[str, Any]:
    root = os.path.abspath(project_root or os.path.dirname(os.path.abspath(__file__)))
    cached = _DESIGNER_PACK_MEMORY_CACHE.get(root)
    if cached is not None:
        return cached

    path = _designer_pack_memory_path(root)
    payload: Dict[str, Any]
    if os.path.exists(path):
        try:
            import json

            with open(path, "r", encoding="utf-8") as handle:
                payload = json.loads(handle.read())
        except Exception:
            payload = {}
    else:
        payload = {}

    usage = payload.get("usage")
    if not isinstance(usage, dict):
        usage = {}
    recent = payload.get("recent")
    if not isinstance(recent, list):
        recent = []

    out = {"usage": usage, "recent": [str(token) for token in recent if str(token).strip()]}
    _DESIGNER_PACK_MEMORY_CACHE[root] = out
    return out


def _save_designer_pack_memory(project_root: Optional[str], payload: Dict[str, Any]) -> None:
    root = os.path.abspath(project_root or os.path.dirname(os.path.abspath(__file__)))
    path = _designer_pack_memory_path(root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    import json

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=2, ensure_ascii=True) + "\n")
    _DESIGNER_PACK_MEMORY_CACHE[root] = payload


def _record_designer_pack_usage_once(
    show_key: Optional[str],
    pack_ids: List[str],
    project_root: Optional[str] = None,
) -> None:
    key = str(show_key or "").strip()
    if not key:
        return

    root = os.path.abspath(project_root or os.path.dirname(os.path.abspath(__file__)))
    seen_key = (root, key)
    if seen_key in _DESIGNER_PACK_MEMORY_SEEN_SHOWS:
        return
    _DESIGNER_PACK_MEMORY_SEEN_SHOWS.add(seen_key)

    memory = _load_designer_pack_memory(root)
    usage = memory.setdefault("usage", {})
    if not isinstance(usage, dict):
        usage = {}
        memory["usage"] = usage
    recent = memory.setdefault("recent", [])
    if not isinstance(recent, list):
        recent = []
        memory["recent"] = recent

    for pack_id in pack_ids:
        token = str(pack_id).strip()
        if not token:
            continue
        usage[token] = int(usage.get(token, 0)) + 1
        recent.append(token)

    if len(recent) > 512:
        del recent[:-512]
    _save_designer_pack_memory(root, memory)


def pick_phrase_technique(
    phrase: str,
    segment_index: int,
    global_bar: int,
    usage: Optional[Dict[str, int]] = None,
    recent: Optional[List[str]] = None,
    cooldown: int = 2,
    previous_plan: Optional[Dict[str, Any]] = None,
    brand_tokens: Optional[List[str]] = None,
    candidate_count: int = 3,
    creative_directives: Optional[Dict[str, Any]] = None,
    show_key: Optional[str] = None,
    pack_usage: Optional[Dict[str, int]] = None,
    pack_recent: Optional[List[str]] = None,
    pack_cooldown: int = 3,
    project_root: Optional[str] = None,
) -> Dict[str, Any]:
    """Choose the top scored coordination technique for a phrase bucket.

    Planner evaluates multiple candidates (default=3) and returns rank-1 plan.
    """
    effective_pack_usage = pack_usage
    effective_pack_recent = pack_recent
    if effective_pack_usage is None or effective_pack_recent is None:
        memory = _load_designer_pack_memory(project_root)
        if effective_pack_usage is None:
            effective_pack_usage = memory.get("usage", {})
        if effective_pack_recent is None:
            effective_pack_recent = memory.get("recent", [])

    planner = get_phrase_planner(project_root)
    planned = planner.pick_technique(
        phrase=phrase,
        segment_index=segment_index,
        global_bar=global_bar,
        usage=usage,
        recent=recent,
        cooldown=cooldown,
        previous=previous_plan,
        brand_tokens=brand_tokens,
        candidate_count=candidate_count,
        creative_directives=creative_directives,
        show_key=show_key,
        pack_usage=effective_pack_usage,
        pack_recent=effective_pack_recent,
        pack_cooldown=pack_cooldown,
    )

    if show_key:
        selected = planner.select_show_designer_packs(
            show_key=show_key,
            brand_tokens=brand_tokens,
            creative_directives=creative_directives,
            pack_usage=effective_pack_usage,
            pack_recent=effective_pack_recent,
            pack_cooldown=pack_cooldown,
        )
        pack_ids = [row["id"] for row in selected.get("dominant", [])]
        contrast = selected.get("contrast")
        if isinstance(contrast, dict):
            pack_ids.append(str(contrast.get("id", "")).strip())
        _record_designer_pack_usage_once(
            show_key=show_key,
            pack_ids=[token for token in pack_ids if token],
            project_root=project_root,
        )

    return _serialize_planned_phrase_technique(planned)


def pick_phrase_technique_candidates(
    phrase: str,
    segment_index: int,
    global_bar: int,
    usage: Optional[Dict[str, int]] = None,
    recent: Optional[List[str]] = None,
    cooldown: int = 2,
    previous_plan: Optional[Dict[str, Any]] = None,
    brand_tokens: Optional[List[str]] = None,
    candidate_count: int = 3,
    creative_directives: Optional[Dict[str, Any]] = None,
    show_key: Optional[str] = None,
    pack_usage: Optional[Dict[str, int]] = None,
    pack_recent: Optional[List[str]] = None,
    pack_cooldown: int = 3,
    project_root: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Return scored phrase-technique candidates, best-first."""
    effective_pack_usage = pack_usage
    effective_pack_recent = pack_recent
    if effective_pack_usage is None or effective_pack_recent is None:
        memory = _load_designer_pack_memory(project_root)
        if effective_pack_usage is None:
            effective_pack_usage = memory.get("usage", {})
        if effective_pack_recent is None:
            effective_pack_recent = memory.get("recent", [])

    planner = get_phrase_planner(project_root)
    planned_rows = planner.plan_candidates(
        phrase=phrase,
        segment_index=segment_index,
        global_bar=global_bar,
        usage=usage,
        recent=recent,
        cooldown=cooldown,
        previous=previous_plan,
        brand_tokens=brand_tokens,
        candidate_count=candidate_count,
        creative_directives=creative_directives,
        show_key=show_key,
        pack_usage=effective_pack_usage,
        pack_recent=effective_pack_recent,
        pack_cooldown=pack_cooldown,
    )
    return [_serialize_planned_phrase_technique(row) for row in planned_rows]


def pick_show_designer_packs(
    show_key: Optional[str] = None,
    brand_tokens: Optional[List[str]] = None,
    creative_directives: Optional[Dict[str, Any]] = None,
    pack_usage: Optional[Dict[str, int]] = None,
    pack_recent: Optional[List[str]] = None,
    pack_cooldown: int = 3,
    project_root: Optional[str] = None,
) -> Dict[str, Any]:
    """Return dominant + contrast designer technical packs for a show."""
    effective_pack_usage = pack_usage
    effective_pack_recent = pack_recent
    if effective_pack_usage is None or effective_pack_recent is None:
        memory = _load_designer_pack_memory(project_root)
        if effective_pack_usage is None:
            effective_pack_usage = memory.get("usage", {})
        if effective_pack_recent is None:
            effective_pack_recent = memory.get("recent", [])

    planner = get_phrase_planner(project_root)
    return planner.select_show_designer_packs(
        show_key=show_key,
        brand_tokens=brand_tokens,
        creative_directives=creative_directives,
        pack_usage=effective_pack_usage,
        pack_recent=effective_pack_recent,
        pack_cooldown=pack_cooldown,
    )


def _serialize_planned_phrase_technique(planned: Any) -> Dict[str, Any]:
    return {
        "phrase": planned.phrase,
        "id": planned.technique_id,
        "name": planned.technique_name,
        "relationship": planned.relationship,
        "timing": {
            "mover_beats": planned.timing.mover_beats,
            "par_beats": planned.timing.par_beats,
            "par_style": planned.timing.par_style,
        },
        "mover_pattern": {
            "base_route": planned.mover_pattern.base_route,
            "transforms": list(planned.mover_pattern.transforms),
            "phase_shift_beats": planned.mover_pattern.phase_shift_beats,
            "signature": planned.mover_pattern.signature,
        },
        "dimensions": dict(planned.dimensions),
        "score": {
            "novelty": planned.score.novelty,
            "coherence": planned.score.coherence,
            "brand_fit": planned.score.brand_fit,
            "creative_fit": planned.score.creative_fit,
            "phrase_fit": planned.score.phrase_fit,
            "total": planned.score.total,
        },
        "designer_pack": {
            "id": planned.designer_pack_id,
            "name": planned.designer_pack_name,
            "ld_id": planned.designer_ld_id,
            "role": planned.designer_role,
            "phrase_targeted": bool(planned.designer_phrase_targeted),
        },
        "candidate_rank": planned.candidate_rank,
        "candidate_count": planned.candidate_count,
        "changed_dimensions": list(planned.changed_dimensions),
        "contrast_enforced": bool(planned.contrast_enforced),
        "beat_reactivity": {
            "par_min": planned.beat_reactivity.par_min,
            "mover_min": planned.beat_reactivity.mover_min,
            "accent_layer": planned.beat_reactivity.accent_layer,
            "accent_type": planned.beat_reactivity.accent_type,
        } if planned.beat_reactivity else None,
    }


def mover_family_from_phrase(
    phrase: str,
    relationship: str,
    rms: float,
    sub: float,
) -> str:
    """Map phrase + technique relationship into local mover family buckets."""
    from qlc_runtime.phrase_planner import family_from_phrase_and_relationship

    return family_from_phrase_and_relationship(
        phrase=phrase,
        relationship=relationship,
        rms=rms,
        sub=sub,
    )


def par_mode_from_phrase_timing(
    par_beats: int,
    par_style: str,
    phrase: str,
    seg_bar_idx: int,
) -> str:
    """Map abstract technique timing into local PAR mode keys."""
    from qlc_runtime.phrase_planner import TechniqueTiming, par_mode_from_timing

    timing = TechniqueTiming(
        mover_beats=4,
        par_beats=par_beats,
        par_style=par_style,
    )
    return par_mode_from_timing(
        timing=timing,
        phrase=phrase,
        seg_bar_idx=seg_bar_idx,
    )


def load_venue_profile(
    project_root: Optional[str] = None,
    venue_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """Load and validate venue-specific creativity profile.

    Profiles live under venue/<name>/references/creative-profile.json.
    """
    root = os.path.abspath(project_root or os.path.dirname(os.path.abspath(__file__)))
    vkey = venue_dir or "__auto__"
    cache_key = (root, vkey)

    profile = _VENUE_PROFILE_CACHE.get(cache_key)
    if profile is not None:
        return profile

    from qlc_runtime.venue_profile import load_and_validate_venue_profile

    profile = load_and_validate_venue_profile(project_root=root, venue_dir=venue_dir)
    _VENUE_PROFILE_CACHE[cache_key] = profile
    return profile


def load_focus_position_tuples(
    project_root: Optional[str] = None,
    venue_dir: Optional[str] = None,
    include_composites: bool = True,
) -> Dict[str, Tuple[int, int, int, int, int, int, int]]:
    """Load canonical mover position tuples from venue focus-positions.md."""
    root = os.path.abspath(project_root or os.path.dirname(os.path.abspath(__file__)))
    vkey = venue_dir or "__auto__"
    cache_key = (root, vkey)

    cached = _FOCUS_POSITION_CACHE.get(cache_key)
    if cached is not None and include_composites:
        return cached

    from qlc_runtime.focus_positions import load_focus_position_tuples as _load

    positions = _load(
        project_root=root,
        venue_dir=venue_dir,
        include_composites=include_composites,
    )

    if include_composites:
        _FOCUS_POSITION_CACHE[cache_key] = positions
    return positions


def require_research_brief(
    song_stem: str,
    project_root: Optional[str] = None,
    venue_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """Enforce artist/song branding research before generating a show.

    If a brief does not exist, a draft stub is auto-created and validation
    raises with instructions to complete/approve it.
    """
    root = os.path.abspath(project_root or os.path.dirname(os.path.abspath(__file__)))
    from qlc_runtime.research_gate import load_and_validate_brief

    venue_profile = load_venue_profile(project_root=root, venue_dir=venue_dir)

    try:
        brief = load_and_validate_brief(
            song_title=song_stem,
            project_root=root,
            venue_dir=venue_dir,
        )
        brief["_meta"]["venue_profile_json"] = venue_profile["_meta"]["profile_json"]
        return brief
    except Exception as exc:
        raise RuntimeError(
            f"Research brief validation failed for {song_stem!r}: {exc}. "
            "Fill <venue>/shows/notes/<song-slug>.json and set status='approved'."
        ) from exc


# =============================================================================
# VENUE TEMPLATE GENERATOR
# =============================================================================

def generate_venue_template(venue_dir: str, bpm: int = 128):
    """Generate a Template-Base.qxw for a venue from its plot.md.

    Reads venue/<name>/plot.md to identify which fixtures are placed,
    maps them to FIXTURE_DEFS, and writes a blank workspace with all
    placed fixtures, ArtNet output, and a BLACKOUT button.

    Args:
        venue_dir: Path to the venue directory (e.g. "venue/home-studio")
        bpm: Default BPM for the beat generator
    """
    plot_path = os.path.join(venue_dir, "plot.md")
    shows_dir = os.path.join(venue_dir, "shows")
    os.makedirs(shows_dir, exist_ok=True)

    with open(plot_path) as f:
        plot_content = f.read()

    # Parse fixture table rows: | Name | Type | X | Y | Z | Orientation |
    fixture_rows = re.findall(
        r'^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*[\d.]+\s*\|\s*[\d.]+\s*\|\s*[\d.]+\s*\|\s*([^|]+?)\s*\|',
        plot_content, re.MULTILINE
    )

    # Build lookup from model/name to list of FIXTURE_DEFS entries
    # (multiple fixtures can share a model, e.g. two Missyee pars)
    model_lookup: Dict[str, List[dict]] = {}
    for fx in FIXTURE_DEFS:
        for key in [fx["model"].lower(), fx["name"].lower()]:
            entries = model_lookup.setdefault(key, [])
            if fx["id"] not in [e["id"] for e in entries]:
                entries.append(fx)

    # Match plot fixture types to FIXTURE_DEFS
    # Count how many of each type appear in the plot to pull the right
    # number of fixtures from FIXTURE_DEFS
    from collections import Counter
    type_counts: Counter = Counter()
    placed_fixture_ids = set()
    for name, ftype, orientation in fixture_rows:
        ftype_lower = ftype.strip().lower()
        if ftype_lower in model_lookup:
            entries = model_lookup[ftype_lower]
            idx = min(type_counts[ftype_lower], len(entries) - 1)
            placed_fixture_ids.add(entries[idx]["id"])
            type_counts[ftype_lower] += 1

    if not placed_fixture_ids:
        print(f"Warning: No known fixtures found in {plot_path}")
        # Fall back to all fixtures
        placed_fixture_ids = {fx["id"] for fx in FIXTURE_DEFS}

    # Filter FIXTURE_DEFS to only placed fixtures
    placed_defs = [fx for fx in FIXTURE_DEFS if fx["id"] in placed_fixture_ids]

    # Build blackout scene for placed fixtures
    blackout_fixtures = []
    for fx in placed_defs:
        blackout_fixtures.append(blackout(fx["id"], fx["ch"]))

    scenes = [scene("BLACKOUT", *blackout_fixtures)]
    output_path = os.path.join(shows_dir, "Template-Base.qxw")

    filtered_positions = [p for p in STAGE_POSITIONS if p[0] in placed_fixture_ids]
    write_workspace(
        output_path,
        scenes,
        [],
        bpm=bpm,
        fixture_defs=placed_defs,
        stage_positions=filtered_positions,
    )

    print(f"  Fixtures: {', '.join(fx['name'] for fx in placed_defs)}")


# =============================================================================
# SEGMENT TRANSITION HELPERS
# =============================================================================

def plan_segment_transition(
    prev_phrase: Optional[str],
    next_phrase: Optional[str],
    prev_energy: float,
    next_energy: float,
    segment_index: int,
    total_segments: int,
    recent_transitions: Optional[List[str]] = None,
    show_key: str = "",
    end_of_show: bool = False,
    prev_segment_beats: int = 32,
    next_segment_beats: int = 32,
    project_root: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Plan a transition event for a segment boundary.

    Thin wrapper around PhraseAwarePlanner.plan_transition().
    Returns a serialized dict or None if no transition config exists.
    """
    planner = get_phrase_planner(project_root)
    event = planner.plan_transition(
        prev_phrase=prev_phrase,
        next_phrase=next_phrase,
        prev_energy=prev_energy,
        next_energy=next_energy,
        segment_index=segment_index,
        total_segments=total_segments,
        recent_transitions=recent_transitions,
        show_key=show_key,
        end_of_show=end_of_show,
        prev_segment_beats=prev_segment_beats,
        next_segment_beats=next_segment_beats,
    )
    if event is None:
        return None
    return {
        "type": event.transition_type,
        "duration_beats": event.duration_beats,
        "fixtures": event.fixtures,
        "exit_style": event.exit_style,
        "description": event.description,
        "pool_key": event.pool_key,
        "segment_index": event.segment_index,
        "end_of_show": event.end_of_show,
    }


def build_transition_scenes(
    transition: Optional[Dict[str, Any]],
    bpm: float,
    pos_tuples: Optional[Dict[str, Any]] = None,
    palette: Optional[Tuple[int, int, int]] = None,
    last_scene: Optional[dict] = None,
) -> Tuple[List[dict], List[Tuple[int, int]]]:
    """Build scene(s) and timing for a transition event.

    Dispatcher that routes to the correct scene factory based on
    transition["type"]. Generators call this one function.

    Args:
        transition: Dict from plan_segment_transition(), or None.
        bpm: Show BPM for timing calculations.
        pos_tuples: Dict of position name -> (pan, tilt) tuples (optional).
        palette: RGB tuple for color-based transitions (optional).
        last_scene: Previous scene dict for freeze/hold transitions (optional).

    Returns:
        (scenes, timing) — scenes to extend into the scene list,
        timing entries for the chaser. Empty lists if transition is None.
    """
    if transition is None:
        return [], []

    t_type = transition.get("type", "")
    duration_beats = int(transition.get("duration_beats", 1))
    exit_style = transition.get("exit_style", "snap")

    factory = _TRANSITION_FACTORIES.get(t_type)
    if factory is not None:
        return factory(bpm=bpm, duration_beats=duration_beats,
                       exit_style=exit_style, pos_tuples=pos_tuples,
                       palette=palette, last_scene=last_scene)

    # Unknown transition type: fall back to a 1-beat blackout
    return _transition_blackout(bpm=bpm, duration_beats=duration_beats,
                                exit_style=exit_style, pos_tuples=pos_tuples,
                                palette=palette, last_scene=last_scene)


def _beat_ms(bpm: float, beats: int) -> int:
    """Milliseconds for N beats at given BPM."""
    return round((60000 / bpm) * beats)


def _transition_blackout(bpm, duration_beats, exit_style, **_kw):
    """Full blackout for N beats. Used by: blackout_slingshot, dead_air."""
    s = scene("T:Blackout", *blackout_all(), path="Transitions")
    if exit_style == "smooth":
        timing = [(_beat_ms(bpm, duration_beats), 0)]
    else:
        timing = [(0, _beat_ms(bpm, duration_beats))]
    return [s], timing


def _transition_white_flash(bpm, duration_beats, exit_style, palette=None, **_kw):
    """All fixtures flash white for N beats."""
    s = scene("T:White Flash",
              sharpy(dim=255, strobe=SHARPY_OPEN, color7=0),
              bsw(dim=255, shutter=BSW_SHUT_OPEN, color=BSW_WHITE),
              profile(dim=255, color=0),
              fourbar_solid(255, 255, 255),
              *miss_both(255, 255, 255),
              ni3k(dim=255, r=255, g=255, b=255, w=255, halo=H_RGB),
              path="Transitions")
    timing = [(0, _beat_ms(bpm, duration_beats))]
    return [s], timing


def _transition_strobe_burst(bpm, duration_beats, exit_style, **_kw):
    """All strobes fire for N beats."""
    s = scene("T:Strobe Burst",
              sharpy(dim=255, strobe=SHARPY_STROBE_FAST, color7=0),
              bsw(dim=255, shutter=BSW_SHUT_STROBE_FAST, color=BSW_WHITE),
              profile(dim=255, strobe=200),
              fourbar_solid(255, 255, 255, strobe=200),
              *miss_both(255, 255, 255, strobe=200),
              ni3k(dim=255, r=255, g=255, b=255, w=255, halo=H_RGB),
              path="Transitions")
    timing = [(0, _beat_ms(bpm, duration_beats))]
    return [s], timing


def _transition_freeze_decay(bpm, duration_beats, exit_style, last_scene=None, **_kw):
    """Hold last frame, then dim/park movers over duration.

    If last_scene is provided, uses it as the hold. Otherwise uses a dim scene.
    """
    # Dim scene: pars at 20%, movers parked at DSC
    s = scene("T:Freeze Decay",
              dark_sharpy(), dark_bsw(), dark_profile(), dark_ni3k(),
              fourbar_solid(30, 30, 30),
              *miss_both(20, 20, 20),
              path="Transitions")
    # Smooth crossfade into the dim state
    timing = [(_beat_ms(bpm, duration_beats), 0)]
    return [s], timing


def _transition_color_swap(bpm, duration_beats, exit_style, palette=None, **_kw):
    """All fixtures snap to a contrasting color on beat 1."""
    r, g, b = palette if palette else (0, 180, 255)
    # Invert the palette for contrast
    ir, ig, ib = 255 - r, 255 - g, 255 - b
    s = scene("T:Color Swap",
              sharpy(dim=200, strobe=SHARPY_OPEN),
              bsw(dim=200, shutter=BSW_SHUT_OPEN),
              profile(dim=200),
              fourbar_solid(ir, ig, ib),
              *miss_both(ir, ig, ib),
              ni3k(dim=200, r=ir, g=ig, b=ib),
              path="Transitions")
    timing = [(0, _beat_ms(bpm, duration_beats))]
    return [s], timing


def _transition_color_inversion(bpm, duration_beats, exit_style, palette=None, **_kw):
    """Swap warm/cool across all fixtures."""
    # Same implementation as color_swap — generators differentiate via palette
    return _transition_color_swap(bpm=bpm, duration_beats=duration_beats,
                                   exit_style=exit_style, palette=palette)


def _transition_position_snap(bpm, duration_beats, exit_style, **_kw):
    """Movers snap to DSC, pars hold."""
    s = scene("T:Position Snap",
              sharpy(dim=200, strobe=SHARPY_OPEN),
              bsw(dim=200, shutter=BSW_SHUT_OPEN),
              profile(dim=200),
              path="Transitions")
    timing = [(0, _beat_ms(bpm, duration_beats))]
    return [s], timing


def _transition_slow_dissolve(bpm, duration_beats, exit_style, **_kw):
    """Smooth crossfade — dim scene acts as a midpoint between old and new looks."""
    s = scene("T:Dissolve Mid",
              sharpy(dim=120, strobe=SHARPY_OPEN),
              bsw(dim=120, shutter=BSW_SHUT_OPEN),
              profile(dim=120),
              fourbar_solid(80, 80, 80),
              *miss_both(60, 60, 60),
              ni3k(dim=100, r=60, g=60, b=60),
              path="Transitions")
    timing = [(_beat_ms(bpm, duration_beats), 0)]
    return [s], timing


def _transition_par_ladder(bpm, duration_beats, exit_style, palette=None, **_kw):
    """Pars light up sequentially L-to-R over duration.

    Creates 2 half-steps: left pars then right pars.
    """
    r, g, b = palette if palette else (0, 100, 255)
    half_beats = max(1, duration_beats // 2)
    s1 = scene("T:Par Ladder 1",
               fourbar_solid(0, 0, 0),
               miss1(r, g, b),
               miss2(0, 0, 0),
               dark_sharpy(), dark_bsw(), dark_profile(), dark_ni3k(),
               path="Transitions")
    s2 = scene("T:Par Ladder 2",
               fourbar_solid(r, g, b),
               *miss_both(r, g, b),
               dark_sharpy(), dark_bsw(), dark_profile(), dark_ni3k(),
               path="Transitions")
    t1 = (0, _beat_ms(bpm, half_beats))
    t2 = (0, _beat_ms(bpm, duration_beats - half_beats))
    return [s1, s2], [t1, t2]


def _transition_stutter_gate(bpm, duration_beats, exit_style, **_kw):
    """Rapid par strobe for N beats."""
    s = scene("T:Stutter Gate",
              fourbar_solid(255, 255, 255, strobe=220),
              *miss_both(255, 255, 255, strobe=220),
              dark_sharpy(), dark_bsw(), dark_profile(), dark_ni3k(),
              path="Transitions")
    timing = [(0, _beat_ms(bpm, duration_beats))]
    return [s], timing


def _transition_pulse_to_glow(bpm, duration_beats, exit_style, palette=None, **_kw):
    """Rhythmic par pulse decays to static glow."""
    r, g, b = palette if palette else (60, 40, 120)
    s = scene("T:Pulse to Glow",
              fourbar_solid(r, g, b),
              *miss_both(r // 2, g // 2, b // 2),
              dark_sharpy(), dark_bsw(), dark_profile(), dark_ni3k(),
              path="Transitions")
    timing = [(_beat_ms(bpm, duration_beats), 0)]
    return [s], timing


def _transition_compression_snap(bpm, duration_beats, exit_style, **_kw):
    """Dim to 30% for half a beat, then snap full bright."""
    half = max(1, duration_beats // 2)
    s_dim = scene("T:Compress Dim",
                  sharpy(dim=80, strobe=SHARPY_OPEN),
                  bsw(dim=80, shutter=BSW_SHUT_OPEN),
                  profile(dim=80),
                  fourbar_solid(80, 80, 80),
                  *miss_both(60, 60, 60),
                  ni3k(dim=80, r=80, g=80, b=80),
                  path="Transitions")
    s_bright = scene("T:Compress Snap",
                     sharpy(dim=255, strobe=SHARPY_OPEN),
                     bsw(dim=255, shutter=BSW_SHUT_OPEN),
                     profile(dim=255),
                     fourbar_solid(255, 255, 255),
                     *miss_both(255, 255, 255),
                     ni3k(dim=255, r=255, g=255, b=255),
                     path="Transitions")
    t1 = (0, _beat_ms(bpm, half))
    t2 = (0, _beat_ms(bpm, duration_beats - half))
    return [s_dim, s_bright], [t1, t2]


def _transition_ladder_build(bpm, duration_beats, exit_style, palette=None, **_kw):
    """Fixtures light up one by one from pars to movers."""
    r, g, b = palette if palette else (0, 80, 200)
    half = max(1, duration_beats // 2)
    s1 = scene("T:Ladder Pars",
               fourbar_solid(r, g, b),
               *miss_both(r, g, b),
               dark_sharpy(), dark_bsw(), dark_profile(), dark_ni3k(),
               path="Transitions")
    s2 = scene("T:Ladder Full",
               sharpy(dim=200, strobe=SHARPY_OPEN),
               bsw(dim=200, shutter=BSW_SHUT_OPEN),
               profile(dim=200),
               fourbar_solid(r, g, b),
               *miss_both(r, g, b),
               ni3k(dim=180, r=r, g=g, b=b),
               path="Transitions")
    t1 = (0, _beat_ms(bpm, half))
    t2 = (0, _beat_ms(bpm, duration_beats - half))
    return [s1, s2], [t1, t2]


def _transition_par_convergence(bpm, duration_beats, exit_style, palette=None, **_kw):
    """Outer pars fade in, converging to center wash."""
    r, g, b = palette if palette else (0, 100, 200)
    s = scene("T:Par Convergence",
              fourbar_solid(r, g, b),
              *miss_both(r, g, b),
              dark_sharpy(), dark_bsw(), dark_profile(), dark_ni3k(),
              path="Transitions")
    timing = [(_beat_ms(bpm, duration_beats), 0)]
    return [s], timing


def _transition_dim_dissolve(bpm, duration_beats, exit_style, **_kw):
    """Smooth dim to 20%, movers park DSC."""
    s = scene("T:Dim Dissolve",
              sharpy(dim=50, strobe=SHARPY_OPEN),
              bsw(dim=50, shutter=BSW_SHUT_OPEN),
              profile(dim=50),
              fourbar_solid(40, 40, 40),
              *miss_both(30, 30, 30),
              ni3k(dim=40, r=30, g=30, b=30),
              path="Transitions")
    timing = [(_beat_ms(bpm, duration_beats), 0)]
    return [s], timing


def _transition_freeze_burst(bpm, duration_beats, exit_style, **_kw):
    """Strobe burst into new look. The 'freeze' is the previous scene holding."""
    s_burst = scene("T:Freeze Burst",
                    sharpy(dim=255, strobe=SHARPY_STROBE_FAST),
                    bsw(dim=255, shutter=BSW_SHUT_STROBE_FAST),
                    profile(dim=255, strobe=200),
                    fourbar_solid(255, 255, 255, strobe=200),
                    *miss_both(255, 255, 255, strobe=200),
                    ni3k(dim=255, r=255, g=255, b=255, halo=H_RGB),
                    path="Transitions")
    timing = [(0, _beat_ms(bpm, duration_beats))]
    return [s_burst], timing


def _transition_stutter_resolve(bpm, duration_beats, exit_style, **_kw):
    """Rapid strobe then hard snap to new look."""
    strobe_beats = max(1, duration_beats - 1)
    s_strobe = scene("T:Stutter Strobe",
                     sharpy(dim=255, strobe=SHARPY_STROBE_FAST),
                     bsw(dim=255, shutter=BSW_SHUT_STROBE_FAST),
                     profile(dim=255, strobe=200),
                     fourbar_solid(255, 255, 255, strobe=200),
                     *miss_both(255, 255, 255, strobe=200),
                     ni3k(dim=255, r=255, g=255, b=255),
                     path="Transitions")
    timing = [(0, _beat_ms(bpm, strobe_beats))]
    return [s_strobe], timing


def _transition_chase_cancel(bpm, duration_beats, exit_style, **_kw):
    """Abrupt stop — all movers freeze, dim pars slightly."""
    s = scene("T:Chase Cancel",
              sharpy(dim=180, strobe=SHARPY_OPEN),
              bsw(dim=180, shutter=BSW_SHUT_OPEN),
              profile(dim=180),
              fourbar_solid(140, 140, 140),
              *miss_both(100, 100, 100),
              ni3k(dim=150, r=100, g=100, b=100),
              path="Transitions")
    timing = [(0, _beat_ms(bpm, duration_beats))]
    return [s], timing


def _transition_fade_to_black(bpm, duration_beats, exit_style, **_kw):
    """Smooth fade to black over N beats."""
    s = scene("T:Fade to Black", *blackout_all(), path="Transitions")
    timing = [(_beat_ms(bpm, duration_beats), 0)]
    return [s], timing


def _transition_freeze_hold(bpm, duration_beats, exit_style, **_kw):
    """Fade to black. The 'freeze hold' is the previous scene holding."""
    s_black = scene("T:Freeze Hold End", *blackout_all(), path="Transitions")
    timing = [(_beat_ms(bpm, duration_beats), 0)]
    return [s_black], timing


# Map transition types to factory functions
_TRANSITION_FACTORIES = {
    "blackout_slingshot": _transition_blackout,
    "dead_air": _transition_blackout,
    "white_flash": _transition_white_flash,
    "strobe_burst": _transition_strobe_burst,
    "freeze_decay": _transition_freeze_decay,
    "color_swap": _transition_color_swap,
    "color_inversion": _transition_color_inversion,
    "position_snap": _transition_position_snap,
    "slow_dissolve": _transition_slow_dissolve,
    "par_ladder": _transition_par_ladder,
    "stutter_gate": _transition_stutter_gate,
    "pulse_to_glow": _transition_pulse_to_glow,
    "compression_snap": _transition_compression_snap,
    "ladder_build": _transition_ladder_build,
    "par_convergence": _transition_par_convergence,
    "dim_dissolve": _transition_dim_dissolve,
    "freeze_burst": _transition_freeze_burst,
    "stutter_resolve": _transition_stutter_resolve,
    "chase_cancel": _transition_chase_cancel,
    "fade_to_black": _transition_fade_to_black,
    "freeze_hold": _transition_freeze_hold,
}


if __name__ == "__main__":
    # Quick test: generate a minimal workspace
    test_scenes = [
        scene("Test White",
              sharpy(dim=255), bsw(dim=255), profile(dim=255),
              fourbar_solid(*WHITE), *miss_both(*BLUE), ni3k(halo=H_RGB)),
        scene("Test Blackout", *blackout_all()),
    ]
    test_chaser = make_chaser("Test", [0, 1],
                              [hold(128), snap(128)],
                              run_order="SingleShot")
    write_workspace("/tmp/test-showlib.qxw", test_scenes, [test_chaser], bpm=128)
    print("Self-test passed!")
