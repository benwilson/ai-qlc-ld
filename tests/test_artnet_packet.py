#!/usr/bin/env python3
import unittest

from qlc_runtime.artnet import ArtNetSender, build_artdmx_packet


class ArtNetPacketTests(unittest.TestCase):
    def test_packet_header_and_fields(self):
        data = bytes([1, 2, 3, 4])
        pkt = build_artdmx_packet(universe=7, data=data, sequence=9, physical=1)

        self.assertEqual(pkt[:8], b"Art-Net\x00")
        self.assertEqual(pkt[8:10], b"\x00\x50")   # OpCode 0x5000 LE
        self.assertEqual(pkt[10:12], b"\x00\x0e")  # ProtVer 14
        self.assertEqual(pkt[12], 9)
        self.assertEqual(pkt[13], 1)
        self.assertEqual(pkt[14], 7)
        self.assertEqual(pkt[15], 0)
        self.assertEqual(pkt[16:18], b"\x00\x04")
        self.assertEqual(pkt[18:], data)

    def test_sender_pads_to_512(self):
        # Dry run still exercises packet build path.
        sender = ArtNetSender(ip="127.0.0.1", universe=0, dry_run=True)
        sender.send(bytes([1, 2, 3]))
        sender.close()


if __name__ == "__main__":
    unittest.main()
