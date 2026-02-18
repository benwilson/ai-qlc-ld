#!/usr/bin/env python3
import ipaddress
import re
import subprocess
from typing import Callable, Optional, Sequence, Tuple


LIMITED_BROADCAST = "255.255.255.255"


def derive_broadcast_ip(
    bind_ip: str,
    command_runner: Optional[Callable[[Sequence[str]], str]] = None,
) -> Tuple[str, str]:
    """Derive directed broadcast for a local interface IP.

    Returns (broadcast_ip, source), where source describes how it was derived.
    Falls back to limited broadcast if interface metadata can't be found.
    """
    runner = command_runner or _run_command

    linux_output = runner(["ip", "-o", "-f", "inet", "addr", "show"])
    broadcast = parse_linux_ip_addr_output(linux_output, bind_ip)
    if broadcast:
        return broadcast, "linux-ip"

    ifconfig_output = runner(["ifconfig"])
    broadcast = parse_ifconfig_output(ifconfig_output, bind_ip)
    if broadcast:
        return broadcast, "ifconfig"

    return LIMITED_BROADCAST, "fallback-limited-broadcast"


def parse_linux_ip_addr_output(output: str, bind_ip: str) -> Optional[str]:
    for line in output.splitlines():
        line = line.strip()
        if f"inet {bind_ip}/" not in line:
            continue

        brd_match = re.search(r"\bbrd\s+(\d+\.\d+\.\d+\.\d+)\b", line)
        if brd_match:
            return brd_match.group(1)

        cidr_match = re.search(rf"\binet\s+{re.escape(bind_ip)}/(\d{{1,2}})\b", line)
        if cidr_match:
            prefix_len = int(cidr_match.group(1))
            iface = ipaddress.IPv4Interface(f"{bind_ip}/{prefix_len}")
            return str(iface.network.broadcast_address)

    return None


def parse_ifconfig_output(output: str, bind_ip: str) -> Optional[str]:
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if line.startswith("inet "):
            ip_match = re.search(r"\binet\s+(\d+\.\d+\.\d+\.\d+)\b", line)
            if not ip_match or ip_match.group(1) != bind_ip:
                continue

            # macOS/BSD style: "... broadcast 10.0.255.255"
            bcast_match = re.search(r"\bbroadcast\s+(\d+\.\d+\.\d+\.\d+)\b", line)
            if bcast_match:
                return bcast_match.group(1)

            # Legacy style: "... Bcast:10.0.255.255 ..."
            bcast_legacy = re.search(r"\bBcast:(\d+\.\d+\.\d+\.\d+)\b", line)
            if bcast_legacy:
                return bcast_legacy.group(1)

            # Compute from netmask if broadcast field is absent.
            mask_match = (
                re.search(r"\bnetmask\s+([0-9a-fxA-F\.]+)\b", line)
                or re.search(r"\bMask:(\d+\.\d+\.\d+\.\d+)\b", line)
            )
            if mask_match:
                normalized = _normalize_netmask(mask_match.group(1))
                iface = ipaddress.IPv4Interface(f"{bind_ip}/{normalized}")
                return str(iface.network.broadcast_address)

    return None


def _normalize_netmask(raw_mask: str) -> str:
    raw_mask = raw_mask.strip()
    if raw_mask.startswith("0x") or raw_mask.startswith("0X"):
        value = int(raw_mask, 16)
        return str(ipaddress.IPv4Address(value))
    return raw_mask


def _run_command(cmd: Sequence[str]) -> str:
    try:
        proc = subprocess.run(
            list(cmd),
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            return ""
        return proc.stdout
    except Exception:
        return ""

