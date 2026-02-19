#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class FixtureDef:
    id: int
    universe: int
    address: int
    channels: int
    name: str = ""


@dataclass
class SceneFunction:
    id: int
    name: str
    path: str
    fixture_values: Dict[int, Dict[int, int]]


@dataclass
class ChaserStep:
    number: int
    function_id: int
    fade_in: int = 0
    hold: int = 0
    fade_out: int = 0


@dataclass
class SpeedModes:
    fade_in: str = "Common"
    fade_out: str = "Common"
    duration: str = "Common"


@dataclass
class ChaserFunction:
    id: int
    name: str
    path: str
    run_order: str
    speed_fade_in: int
    speed_fade_out: int
    speed_duration: int
    speed_modes: SpeedModes = field(default_factory=SpeedModes)
    steps: List[ChaserStep] = field(default_factory=list)


@dataclass
class ButtonDef:
    id: int
    caption: str
    function_id: int


FunctionDef = Union[SceneFunction, ChaserFunction]


@dataclass
class WorkspaceModel:
    fixtures: Dict[int, FixtureDef]
    functions: Dict[int, FunctionDef]
    buttons: List[ButtonDef]
    artnet_ip: Optional[str] = None
    artnet_universe: Optional[int] = None

