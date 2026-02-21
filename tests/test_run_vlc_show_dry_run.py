#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from tests.qxw_samples import write_sample_qxw


def _start_fake_vlc(statuses):
    state = {"idx": 0}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            if self.path != "/requests/status.json":
                self.send_response(404)
                self.end_headers()
                return

            idx = state["idx"]
            state["idx"] = idx + 1
            payload = statuses[idx] if idx < len(statuses) else statuses[-1]
            body = json.dumps(payload).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):  # noqa: A003
            return

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{server.server_port}"


class RunVlcShowDryRunTests(unittest.TestCase):
    def test_cli_oneshot_dry_run(self):
        repo_root = Path(__file__).resolve().parent.parent
        cli = repo_root / "run_vlc_show.py"

        with tempfile.TemporaryDirectory() as td:
            shows_dir = Path(td)
            show = shows_dir / "Track Name.qxw"
            write_sample_qxw(show)

            try:
                server, thread, vlc_url = _start_fake_vlc(
                    [
                        {
                            "state": "playing",
                            "time": 12,
                            "length": 100,
                            "position": 0.12345,
                            "information": {
                                "category": {
                                    "meta": {
                                        "url": "file:///Users/test/Music/Track%20Name.mp3",
                                        "filename": "Track Name.mp3",
                                    }
                                }
                            },
                        }
                    ]
                )
            except PermissionError as exc:
                self.skipTest(f"TCP bind not permitted in this environment: {exc}")
            try:
                proc = subprocess.run(
                    [
                        sys.executable,
                        str(cli),
                        str(shows_dir),
                        "--dry-run",
                        "--vlc-url",
                        vlc_url,
                        "--max-seconds",
                        "0.15",
                    ],
                    cwd=str(repo_root),
                    capture_output=True,
                    text=True,
                    timeout=8,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2.0)

        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("media='Track Name.mp3' time=12.345s", proc.stdout)
        self.assertIn("Show:", proc.stdout)
        self.assertIn("Stop reason: timeout", proc.stdout)

    def test_cli_follow_restarts_on_track_change(self):
        repo_root = Path(__file__).resolve().parent.parent
        cli = repo_root / "run_vlc_show.py"

        with tempfile.TemporaryDirectory() as td:
            shows_dir = Path(td)
            show_a = shows_dir / "Track A.qxw"
            show_b = shows_dir / "Track B.qxw"
            write_sample_qxw(show_a)
            write_sample_qxw(show_b)

            try:
                server, thread, vlc_url = _start_fake_vlc(
                    [
                        {
                            "state": "playing",
                            "time": 0,
                            "information": {
                                "category": {"meta": {"url": "file:///Music/Track%20A.mp3"}}
                            },
                        },
                        {
                            "state": "playing",
                            "time": 1,
                            "information": {
                                "category": {"meta": {"url": "file:///Music/Track%20A.mp3"}}
                            },
                        },
                        {
                            "state": "playing",
                            "time": 0,
                            "information": {
                                "category": {"meta": {"url": "file:///Music/Track%20B.mp3"}}
                            },
                        },
                        {
                            "state": "playing",
                            "time": 1,
                            "information": {
                                "category": {"meta": {"url": "file:///Music/Track%20B.mp3"}}
                            },
                        },
                    ]
                )
            except PermissionError as exc:
                self.skipTest(f"TCP bind not permitted in this environment: {exc}")
            try:
                proc = subprocess.run(
                    [
                        sys.executable,
                        str(cli),
                        str(shows_dir),
                        "--dry-run",
                        "--follow",
                        "--poll-interval",
                        "0.05",
                        "--resync-threshold",
                        "100",
                        "--max-seconds",
                        "0.35",
                        "--vlc-url",
                        vlc_url,
                    ],
                    cwd=str(repo_root),
                    capture_output=True,
                    text=True,
                    timeout=8,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2.0)

        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("Follow: track/function changed; restarting run", proc.stdout)
        self.assertIn(str(show_a), proc.stdout)
        self.assertIn(str(show_b), proc.stdout)
        self.assertIn("Stop reason: timeout", proc.stdout)


if __name__ == "__main__":
    unittest.main()
