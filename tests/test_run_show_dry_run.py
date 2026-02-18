#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.qxw_samples import write_sample_qxw


class RunShowDryRunTests(unittest.TestCase):
    def test_cli_dry_run_executes_and_times_out(self):
        repo_root = Path(__file__).resolve().parent.parent
        cli = repo_root / "run_show.py"

        with tempfile.TemporaryDirectory() as td:
            qxw = Path(td) / "sample.qxw"
            write_sample_qxw(qxw)

            proc = subprocess.run(
                [
                    sys.executable,
                    str(cli),
                    str(qxw),
                    "--dry-run",
                    "--max-seconds",
                    "0.15",
                ],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                timeout=5,
            )

        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("Function: ID=2", proc.stdout)
        self.assertIn("Stop reason: timeout", proc.stdout)


if __name__ == "__main__":
    unittest.main()

