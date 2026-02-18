#!/usr/bin/env python3
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.qxw_samples import write_sample_qxw


class RunShowUdpTests(unittest.TestCase):
    def test_cli_sends_artnet_packets(self):
        repo_root = Path(__file__).resolve().parent.parent
        cli = repo_root / "run_show.py"

        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            listener.bind(("127.0.0.1", 0))
        except PermissionError as exc:
            listener.close()
            self.skipTest(f"UDP bind not permitted in this environment: {exc}")
        listener.settimeout(0.5)
        port = listener.getsockname()[1]

        packets = []
        try:
            with tempfile.TemporaryDirectory() as td:
                qxw = Path(td) / "sample.qxw"
                write_sample_qxw(qxw)

                proc = subprocess.run(
                    [
                        sys.executable,
                        str(cli),
                        str(qxw),
                        "--ip",
                        "127.0.0.1",
                        "--port",
                        str(port),
                        "--max-seconds",
                        "0.20",
                    ],
                    cwd=str(repo_root),
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

            # Drain queued packets.
            while True:
                try:
                    data, _addr = listener.recvfrom(2048)
                    packets.append(data)
                except socket.timeout:
                    break
        finally:
            listener.close()

        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertTrue(packets, "expected at least one ArtNet packet")
        self.assertTrue(any(pkt.startswith(b"Art-Net\x00") for pkt in packets))


if __name__ == "__main__":
    unittest.main()
