#!/usr/bin/env python3
import unittest

from qlc_runtime.network import (
    LIMITED_BROADCAST,
    derive_broadcast_ip,
    parse_ifconfig_output,
    parse_linux_ip_addr_output,
)


class NetworkBroadcastTests(unittest.TestCase):
    def test_parse_linux_ip_output_with_brd(self):
        output = (
            "2: en0    inet 10.0.0.7/16 brd 10.0.255.255 scope global dynamic en0\n"
        )
        self.assertEqual(parse_linux_ip_addr_output(output, "10.0.0.7"), "10.0.255.255")

    def test_parse_linux_ip_output_from_prefix(self):
        output = "2: en0    inet 10.0.0.7/16 scope global dynamic en0\n"
        self.assertEqual(parse_linux_ip_addr_output(output, "10.0.0.7"), "10.0.255.255")

    def test_parse_ifconfig_output_macos(self):
        output = (
            "en7: flags=8863<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> mtu 1500\n"
            "    inet 10.0.0.7 netmask 0xffff0000 broadcast 10.0.255.255\n"
        )
        self.assertEqual(parse_ifconfig_output(output, "10.0.0.7"), "10.0.255.255")

    def test_parse_ifconfig_output_legacy_mask(self):
        output = (
            "eth0      Link encap:Ethernet\n"
            "          inet 10.0.0.7  Bcast:10.0.255.255  Mask:255.255.0.0\n"
        )
        self.assertEqual(parse_ifconfig_output(output, "10.0.0.7"), "10.0.255.255")

    def test_derive_broadcast_falls_back(self):
        def fake_runner(_cmd):
            return ""

        ip, source = derive_broadcast_ip("10.0.0.7", command_runner=fake_runner)
        self.assertEqual(ip, LIMITED_BROADCAST)
        self.assertEqual(source, "fallback-limited-broadcast")


if __name__ == "__main__":
    unittest.main()

