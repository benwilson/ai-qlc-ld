#!/usr/bin/env python3
import unittest

from qlc_runtime.model import (
    ButtonDef,
    FixtureDef,
    SceneFunction,
    WorkspaceModel,
)
from qlc_runtime.select import select_target_function


def _workspace_with_buttons() -> WorkspaceModel:
    fixtures = {1: FixtureDef(id=1, universe=0, address=0, channels=3, name="fx")}
    functions = {
        1: SceneFunction(id=1, name="A", path="Show", fixture_values={1: {0: 0}}),
        2: SceneFunction(id=2, name="B", path="Show", fixture_values={1: {0: 255}}),
        3: SceneFunction(id=3, name="C", path="Show", fixture_values={1: {0: 128}}),
    }
    buttons = [
        ButtonDef(id=10, caption="Color A", function_id=1),
        ButtonDef(id=11, caption="FULL SHOW", function_id=2),
        ButtonDef(id=12, caption="▶ START", function_id=3),
    ]
    return WorkspaceModel(fixtures=fixtures, functions=functions, buttons=buttons)


class SelectorTests(unittest.TestCase):
    def test_default_uses_show_heuristic(self):
        ws = _workspace_with_buttons()
        function_id, selected = select_target_function(ws)
        self.assertEqual(function_id, 2)
        self.assertIn("default-button", selected)

    def test_explicit_precedence(self):
        ws = _workspace_with_buttons()

        function_id, _ = select_target_function(
            ws,
            function_id=3,
            button_id=10,
            button_caption="FULL SHOW",
        )
        self.assertEqual(function_id, 3)

        function_id, _ = select_target_function(
            ws,
            button_id=10,
            button_caption="FULL SHOW",
        )
        self.assertEqual(function_id, 1)

        function_id, _ = select_target_function(ws, button_caption="full show")
        self.assertEqual(function_id, 2)


if __name__ == "__main__":
    unittest.main()

