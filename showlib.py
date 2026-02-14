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

import xml.etree.ElementTree as ET
from typing import List, Tuple, Dict, Optional, Any

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
# CENTER REFERENCE POSITIONS (floor center from DJ booth perspective)
# =============================================================================

CENTER = {
    "sharpy": {"pan": 153, "tilt": 0},    # Back left
    "bsw":    {"pan": 7,   "tilt": 19},   # Back right
    "profile":{"pan": 0,   "tilt": 123},  # Front center
}

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

# 7-color wheel (Ch16) - UNVERIFIED, needs physical testing
# These are estimates; actual positions TBD
SHARPY_7C_WHITE = 0   # Confirmed

# =============================================================================
# BSW SHUTTER CONSTANTS (Ch16)
# =============================================================================

BSW_SHUT_CLOSED = 0    # 0-7: Off
BSW_SHUT_OPEN   = 8    # 8-15: On
BSW_SHUT_STROBE_SLOW = 20
BSW_SHUT_STROBE_FAST = 128

# =============================================================================
# PROFILE STROBE (Ch1) - UNVERIFIED, needs physical testing
# Uses ShutterStrobeSlowFast preset; actual ranges TBD
# Currently using 0=no strobe (assumed safe)
# =============================================================================

PROFILE_STROBE_OFF = 0

# =============================================================================
# FIXTURE HELPER FUNCTIONS
# Each returns a tuple of (fixture_id, [(ch, val), ...])
# =============================================================================

def sharpy(pan=153, tilt=0, color7=0, gobo=0,
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

def bsw(pan=7, tilt=19, color=0, gobo1=0, gobo2=0, g2rot=0,
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

def profile(pan=0, tilt=123, color=0, gobo=0, gobo1=0, g1rot=0,
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

def blackout(fixture_id: int, num_channels: int):
    """Generic blackout for any fixture."""
    return (fixture_id, [(i, 0) for i in range(num_channels)])

def blackout_all():
    """Returns list of blackout tuples for all 7 fixtures."""
    return [
        blackout(FX_BSW, CH_BSW),
        blackout(FX_4BAR, CH_4BAR),
        blackout(FX_NI3K, CH_NI3K),
        blackout(FX_PROFILE, CH_PROFILE),
        blackout(FX_MISS1, CH_MISS),
        blackout(FX_MISS2, CH_MISS),
        blackout(FX_SHARPY, CH_SHARPY),
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


def write_workspace(filename: str, scenes: List[dict], chasers: List[dict] = None,
                    bpm: int = 174, artnet_ip: str = "10.0.0.7",
                    vc_buttons: List[dict] = None):
    """Write a complete QLC+ 5.0.1 workspace file.

    Args:
        filename: Output path
        scenes: List of scene dicts from scene()
        chasers: List of chaser dicts from make_chaser()
        bpm: BPM for the beat generator
        artnet_ip: ArtNet output IP
        vc_buttons: Optional custom VC buttons. If None, auto-generates
                    a button for each chaser + blackout.
    """
    chasers = chasers or []

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
    L(f'   <BeatGenerator BeatType="Internal" BPM="{bpm}"/>')
    L('   <Universe Name="Universe 1" ID="0">')
    L(f'    <Output Plugin="ArtNet" UID="{artnet_ip}" Line="0"/>')
    L('   </Universe>')
    L('  </InputOutputMap>')

    # Fixtures
    for fx in FIXTURE_DEFS:
        L('  <Fixture>')
        L(f'   <Manufacturer>{fx["mfr"]}</Manufacturer>')
        L(f'   <Model>{fx["model"]}</Model>')
        L(f'   <Mode>{fx["mode"]}</Mode>')
        L(f'   <ID>{fx["id"]}</ID>')
        L(f'   <Name>{fx["name"]}</Name>')
        L('   <Universe>0</Universe>')
        L(f'   <Address>{fx["addr"]}</Address>')
        L(f'   <Channels>{fx["ch"]}</Channels>')
        L('  </Fixture>')

    # Scenes
    for sid, sc in enumerate(scenes):
        L(f'  <Function ID="{sid}" Type="Scene" Name="{sc["name"]}" Path="{sc["path"]}">')
        L('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
        for fid, channels in sc["fixtures"]:
            val_str = ','.join(f'{ch},{val}' for ch, val in channels)
            L(f'   <FixtureVal ID="{fid}">{val_str}</FixtureVal>')
        L('  </Function>')

    # Chasers
    for i, ch in enumerate(chasers):
        cid = chaser_ids[i]
        L(f'  <Function ID="{cid}" Type="Chaser" Name="{ch["name"]}" Path="{ch["path"]}">')
        L('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
        L('   <Direction>Forward</Direction>')
        L(f'   <RunOrder>{ch["run_order"]}</RunOrder>')
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
            L(f'   <Button Caption="{btn["caption"]}" ID="{btn["vc_id"]}" Icon="">')
            L(f'    <WindowState Visible="True" X="{btn["x"]}" Y="{btn["y"]}" Width="{btn["w"]}" Height="{btn["h"]}"/>')
            L('    <Appearance>')
            L(f'     <BackgroundColor>{btn["color"]}</BackgroundColor>')
            L('    </Appearance>')
            L(f'    <Function ID="{btn["func_id"]}"/>')
            L(f'    <Action>{btn.get("action", "Toggle")}</Action>')
            L('   </Button>')
    else:
        # Auto-generate: one button per chaser + blackout
        vc_id = 0
        y = 10
        for i, ch in enumerate(chasers):
            cid = chaser_ids[i]
            L(f'   <Button Caption="{ch["name"]}" ID="{vc_id}" Icon="">')
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
    for fid, x, y_pos, z in STAGE_POSITIONS:
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

def movers_center():
    """All three movers aimed at floor center."""
    return [
        sharpy(pan=153, tilt=0),
        bsw(pan=7, tilt=19),
        profile(pan=0, tilt=123),
    ]

def movers_spread(amount=1.0):
    """Movers spread wide. amount: 0.0=center, 1.0=full spread."""
    a = amount
    return [
        sharpy(pan=int(153 + 67*a), tilt=int(15*a)),
        bsw(pan=int(7 + 73*a), tilt=int(19 - 14*a)),
        profile(pan=int(30*a), tilt=int(123 - 23*a)),
    ]

def movers_cross(amount=1.0):
    """Movers crossed to opposite sides."""
    a = amount
    return [
        sharpy(pan=int(153 - 73*a), tilt=0),
        bsw(pan=int(7 + 193*a), tilt=int(19 + 11*a)),
        profile(pan=int(230*a), tilt=int(123 + 22*a)),
    ]


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


if __name__ == "__main__":
    # Quick test: generate a minimal workspace
    test_scenes = [
        scene("Test White", *movers_center(),
              fourbar_solid(*WHITE), *miss_both(*BLUE), ni3k(halo=H_RGB)),
        scene("Test Blackout", *blackout_all()),
    ]
    test_chaser = make_chaser("Test", [0, 1],
                              [hold(128), snap(128)],
                              run_order="SingleShot")
    write_workspace("/tmp/test-showlib.qxw", test_scenes, [test_chaser], bpm=128)
    print("Self-test passed!")
