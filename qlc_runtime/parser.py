#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

from qlc_runtime.model import (
    ButtonDef,
    ChaserFunction,
    ChaserStep,
    FixtureDef,
    SceneFunction,
    SpeedModes,
    WorkspaceModel,
)


def _text(elem: Optional[ET.Element], default: str = "") -> str:
    if elem is None or elem.text is None:
        return default
    return elem.text.strip()


def _to_int(value: Optional[str], default: int = 0) -> int:
    if value is None or str(value).strip() == "":
        return default
    return int(str(value).strip())


def _parse_fixture_vals(raw: str) -> Dict[int, int]:
    values: Dict[int, int] = {}
    text = raw.strip()
    if not text:
        return values
    parts = [p.strip() for p in text.split(",") if p.strip() != ""]
    if len(parts) % 2 != 0:
        raise ValueError(f"Invalid FixtureVal channel,value pairs: {raw!r}")
    for i in range(0, len(parts), 2):
        ch = int(parts[i])
        val = int(parts[i + 1])
        values[ch] = val
    return values


def parse_workspace(path: str) -> WorkspaceModel:
    tree = ET.parse(path)
    root = tree.getroot()
    engine = root.find("./{*}Engine")
    if engine is None:
        raise ValueError(f"No <Engine> found in workspace: {path}")

    # Parse default ArtNet output (if present).
    artnet_ip = None
    artnet_universe = None
    io_map = engine.find("./{*}InputOutputMap")
    if io_map is not None:
        for universe in io_map.findall("./{*}Universe"):
            output = universe.find("./{*}Output")
            if output is not None and output.attrib.get("Plugin") == "ArtNet":
                artnet_ip = output.attrib.get("UID")
                artnet_universe = _to_int(universe.attrib.get("ID"), 0)
                break

    fixtures: Dict[int, FixtureDef] = {}
    for fx in engine.findall("./{*}Fixture"):
        fixture_id = _to_int(_text(fx.find("./{*}ID")))
        fixtures[fixture_id] = FixtureDef(
            id=fixture_id,
            universe=_to_int(_text(fx.find("./{*}Universe")), 0),
            address=_to_int(_text(fx.find("./{*}Address")), 0),
            channels=_to_int(_text(fx.find("./{*}Channels")), 0),
            name=_text(fx.find("./{*}Name")),
        )

    functions: Dict[int, object] = {}

    for fn in engine.findall("./{*}Function"):
        fn_id = _to_int(fn.attrib.get("ID"), -1)
        fn_type = fn.attrib.get("Type", "").strip()
        fn_name = fn.attrib.get("Name", "").strip()
        fn_path = fn.attrib.get("Path", "").strip()

        if fn_id < 0:
            raise ValueError("Function missing valid ID")

        if fn_type == "Scene":
            fixture_values: Dict[int, Dict[int, int]] = {}
            for fx_val in fn.findall("./{*}FixtureVal"):
                fid = _to_int(fx_val.attrib.get("ID"), -1)
                if fid < 0:
                    raise ValueError(f"Scene {fn_id} has FixtureVal with invalid fixture ID")
                fixture_values[fid] = _parse_fixture_vals(_text(fx_val, ""))
            functions[fn_id] = SceneFunction(
                id=fn_id,
                name=fn_name,
                path=fn_path,
                fixture_values=fixture_values,
            )
            continue

        if fn_type == "Chaser":
            speed = fn.find("./{*}Speed")
            speed_fade_in = _to_int(speed.attrib.get("FadeIn") if speed is not None else None, 0)
            speed_fade_out = _to_int(speed.attrib.get("FadeOut") if speed is not None else None, 0)
            speed_duration = _to_int(speed.attrib.get("Duration") if speed is not None else None, 0)

            speed_modes_elem = fn.find("./{*}SpeedModes")
            speed_modes = SpeedModes(
                fade_in=(speed_modes_elem.attrib.get("FadeIn", "Common") if speed_modes_elem is not None else "Common"),
                fade_out=(speed_modes_elem.attrib.get("FadeOut", "Common") if speed_modes_elem is not None else "Common"),
                duration=(speed_modes_elem.attrib.get("Duration", "Common") if speed_modes_elem is not None else "Common"),
            )

            steps: List[ChaserStep] = []
            for step in fn.findall("./{*}Step"):
                step_number = _to_int(step.attrib.get("Number"), len(steps))
                step_function_id = _to_int(_text(step, "-1"), -1)
                if step_function_id < 0:
                    raise ValueError(f"Chaser {fn_id} has step with invalid function target")
                steps.append(
                    ChaserStep(
                        number=step_number,
                        function_id=step_function_id,
                        fade_in=_to_int(step.attrib.get("FadeIn"), 0),
                        hold=_to_int(step.attrib.get("Hold"), 0),
                        fade_out=_to_int(step.attrib.get("FadeOut"), 0),
                    )
                )

            steps.sort(key=lambda s: s.number)
            functions[fn_id] = ChaserFunction(
                id=fn_id,
                name=fn_name,
                path=fn_path,
                run_order=_text(fn.find("./{*}RunOrder"), "SingleShot"),
                speed_fade_in=speed_fade_in,
                speed_fade_out=speed_fade_out,
                speed_duration=speed_duration,
                speed_modes=speed_modes,
                steps=steps,
            )
            continue

        # Keep unsupported types out of the runtime model; they can still exist in file.

    # Parse VC buttons in file order.
    buttons: List[ButtonDef] = []
    for button in root.findall(".//{*}Button"):
        func_ref = button.find("./{*}Function")
        if func_ref is None:
            continue
        buttons.append(
            ButtonDef(
                id=_to_int(button.attrib.get("ID"), -1),
                caption=button.attrib.get("Caption", ""),
                function_id=_to_int(func_ref.attrib.get("ID"), -1),
            )
        )

    workspace = WorkspaceModel(
        fixtures=fixtures,
        functions=functions,
        buttons=buttons,
        artnet_ip=artnet_ip,
        artnet_universe=artnet_universe,
    )

    _validate_workspace(workspace, path=path)
    return workspace


def _validate_workspace(workspace: WorkspaceModel, path: str) -> None:
    for fn in workspace.functions.values():
        if isinstance(fn, SceneFunction):
            for fixture_id in fn.fixture_values.keys():
                if fixture_id not in workspace.fixtures:
                    raise ValueError(
                        f"Scene {fn.id} references missing fixture ID {fixture_id} in {path}"
                    )
        elif isinstance(fn, ChaserFunction):
            if not fn.steps:
                raise ValueError(f"Chaser {fn.id} has no steps in {path}")
            for step in fn.steps:
                target = workspace.functions.get(step.function_id)
                if target is None:
                    raise ValueError(
                        f"Chaser {fn.id} step {step.number} references missing function ID "
                        f"{step.function_id} in {path}"
                    )
                if not isinstance(target, SceneFunction):
                    raise ValueError(
                        f"Chaser {fn.id} step {step.number} targets unsupported function type "
                        f"{type(target).__name__} (ID {step.function_id}) in {path}"
                    )
