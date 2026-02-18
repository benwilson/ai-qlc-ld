#!/usr/bin/env python3
import socket
import struct
from typing import Optional


ARTNET_PORT = 6454


def build_artdmx_packet(
    universe: int,
    data: bytes,
    sequence: int = 1,
    physical: int = 0,
) -> bytes:
    if len(data) > 512:
        raise ValueError(f"ArtDMX payload cannot exceed 512 bytes (got {len(data)})")

    packet = bytearray()
    packet.extend(b"Art-Net\x00")
    packet.extend(struct.pack("<H", 0x5000))  # OpOutput / ArtDMX
    packet.extend(struct.pack(">H", 14))      # Protocol version
    packet.append(sequence & 0xFF)
    packet.append(physical & 0xFF)
    packet.append(universe & 0xFF)
    packet.append((universe >> 8) & 0xFF)
    packet.extend(struct.pack(">H", len(data)))
    packet.extend(data)
    return bytes(packet)


class ArtNetSender:
    def __init__(
        self,
        ip: str,
        universe: int,
        port: int = ARTNET_PORT,
        dry_run: bool = False,
        bind_ip: Optional[str] = None,
    ):
        self.ip = ip
        self.universe = universe
        self.port = port
        self.dry_run = dry_run
        self.bind_ip = bind_ip
        self.sequence = 0
        self.socket: Optional[socket.socket] = None
        if not dry_run:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if _is_broadcast_ip(ip):
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            if bind_ip:
                self.socket.bind((bind_ip, 0))

    def send(self, frame: bytes) -> None:
        payload = bytes(frame)
        if len(payload) < 512:
            payload = payload + bytes(512 - len(payload))
        elif len(payload) > 512:
            payload = payload[:512]

        self.sequence = 1 if self.sequence >= 255 else self.sequence + 1
        packet = build_artdmx_packet(
            universe=self.universe,
            data=payload,
            sequence=self.sequence,
        )

        if self.dry_run:
            return
        assert self.socket is not None
        self.socket.sendto(packet, (self.ip, self.port))

    def close(self) -> None:
        if self.socket is not None:
            self.socket.close()
            self.socket = None


def _is_broadcast_ip(ip: str) -> bool:
    ip = str(ip).strip()
    if ip == "255.255.255.255":
        return True
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    return parts[-1] == "255"
