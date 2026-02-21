#!/usr/bin/env python3
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install_fixtures.py"
_SPEC = importlib.util.spec_from_file_location("install_fixtures_script", SCRIPT_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Could not load install_fixtures.py")
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
install_fixtures = _MODULE.install_fixtures


class InstallFixturesScriptTests(unittest.TestCase):
    def test_dry_run_does_not_modify_target(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source"
            target = root / "target"
            source.mkdir()
            target.mkdir()

            src_file = source / "TestFixture.qxf"
            dst_file = target / "TestFixture.qxf"
            src_file.write_text("new-fixture-definition", encoding="utf-8")
            dst_file.write_text("old-fixture-definition", encoding="utf-8")

            summary = install_fixtures(
                target_dir=target,
                source_dir=source,
                dry_run=True,
                backup=True,
            )

            self.assertEqual(summary["updated"], 1)
            self.assertEqual(summary["backed_up"], 1)
            self.assertEqual(dst_file.read_text(encoding="utf-8"), "old-fixture-definition")
            self.assertEqual(list(target.glob("TestFixture.qxf.bak*")), [])

    def test_real_run_updates_and_creates_backup(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source"
            target = root / "target"
            source.mkdir()
            target.mkdir()

            src_file = source / "TestFixture.qxf"
            dst_file = target / "TestFixture.qxf"
            src_file.write_text("new-fixture-definition", encoding="utf-8")
            dst_file.write_text("old-fixture-definition", encoding="utf-8")

            summary = install_fixtures(
                target_dir=target,
                source_dir=source,
                dry_run=False,
                backup=True,
            )

            self.assertEqual(summary["updated"], 1)
            self.assertEqual(summary["backed_up"], 1)
            self.assertEqual(dst_file.read_text(encoding="utf-8"), "new-fixture-definition")

            backups = list(target.glob("TestFixture.qxf.bak*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), "old-fixture-definition")


if __name__ == "__main__":
    unittest.main()
