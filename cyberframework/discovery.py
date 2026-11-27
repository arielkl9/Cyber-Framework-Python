"""Standalone host-discovery helpers: ARP scan and ICMP ping sweep."""

from __future__ import annotations

import logging
from pathlib import Path

from cyberframework.scan import arp_discover
from cyberframework.utils import parse_network, results_dir

log = logging.getLogger(__name__)


def arp_scan(network: str, out_dir: Path | None = None) -> list[dict]:
    """ARP-sweep *network* (CIDR) and write a simple ip/mac report."""
    out_dir = out_dir or results_dir("ArpScan")
    hosts = [{"ip": h.ip, "mac": h.mac} for h in arp_discover(network)]
    (out_dir / "arp_scan.txt").write_text(
        "Alive hosts:\n\n" + "\n".join(f"{h['ip']} - {h['mac']}" for h in hosts),
        encoding="utf-8",
    )
    return hosts


def ping_sweep(
    network: str, out_dir: Path | None = None, timeout: float = 0.5
) -> dict[str, list[str]]:
    """Ping every address in *network* and split them into alive/dead."""
    from icmplib import ping  # lazy: needs privileges for raw sockets

    out_dir = out_dir or results_dir("PingSweep")
    result: dict[str, list[str]] = {"alive": [], "dead": []}
    for host in parse_network(network):
        addr = str(host)
        reply = ping(addr, count=1, timeout=timeout, privileged=True)
        bucket = "alive" if reply.is_alive else "dead"
        result[bucket].append(addr)
        log.info("%s is %s", addr, bucket)
    with (out_dir / "ping_sweep.txt").open("w", encoding="utf-8") as fh:
        fh.write("Alive:\n" + "\n".join(result["alive"]))
        fh.write("\n\nDead:\n" + "\n".join(result["dead"]))
    return result
