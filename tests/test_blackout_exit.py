#!/usr/bin/env python3
import unittest

from run_show import send_blackout


class _FakeSender:
    def __init__(self):
        self.frames = []

    def send(self, frame: bytes):
        self.frames.append(bytes(frame))


class BlackoutExitTests(unittest.TestCase):
    def test_blackout_is_sent_multiple_times(self):
        sender = _FakeSender()
        send_blackout(sender, repeats=3, interval_s=0.0)

        self.assertEqual(len(sender.frames), 3)
        for frame in sender.frames:
            self.assertEqual(len(frame), 512)
            self.assertEqual(frame, bytes(512))


if __name__ == "__main__":
    unittest.main()

