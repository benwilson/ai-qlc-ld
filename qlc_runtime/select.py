#!/usr/bin/env python3
from typing import Optional, Tuple

from qlc_runtime.model import ButtonDef, WorkspaceModel


HEURISTIC_TOKENS = ("full show", "show")


def select_target_function(
    workspace: WorkspaceModel,
    function_id: Optional[int] = None,
    button_id: Optional[int] = None,
    button_caption: Optional[str] = None,
) -> Tuple[int, str]:
    """Resolve the function to execute and describe where it came from."""
    if function_id is not None:
        _assert_function_exists(workspace, function_id)
        return function_id, f"function-id={function_id}"

    if button_id is not None:
        button = _find_button_by_id(workspace, button_id)
        if button is None:
            raise ValueError(f"No VC button found with ID {button_id}")
        _assert_function_exists(workspace, button.function_id)
        return button.function_id, f"button-id={button.id} caption={button.caption!r}"

    if button_caption is not None:
        button = _find_button_by_caption(workspace, button_caption)
        if button is None:
            raise ValueError(f"No VC button found with caption {button_caption!r}")
        _assert_function_exists(workspace, button.function_id)
        return button.function_id, f"button-caption={button.caption!r}"

    button = _choose_default_button(workspace)
    if button is None:
        raise ValueError(
            "No VC buttons found; pass --function-id (or --button-id/--button-caption)"
        )
    _assert_function_exists(workspace, button.function_id)
    return button.function_id, f"default-button id={button.id} caption={button.caption!r}"


def _assert_function_exists(workspace: WorkspaceModel, function_id: int) -> None:
    if function_id not in workspace.functions:
        raise ValueError(f"Function ID {function_id} does not exist in workspace")


def _find_button_by_id(workspace: WorkspaceModel, button_id: int) -> Optional[ButtonDef]:
    for button in workspace.buttons:
        if button.id == button_id:
            return button
    return None


def _find_button_by_caption(workspace: WorkspaceModel, caption: str) -> Optional[ButtonDef]:
    target = caption.casefold().strip()
    for button in workspace.buttons:
        if button.caption.casefold().strip() == target:
            return button
    return None


def _choose_default_button(workspace: WorkspaceModel) -> Optional[ButtonDef]:
    if not workspace.buttons:
        return None

    for button in workspace.buttons:
        caption_cf = button.caption.casefold()
        if "▶" in button.caption:
            return button
        for token in HEURISTIC_TOKENS:
            if token in caption_cf:
                return button

    return workspace.buttons[0]

