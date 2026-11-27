"""Network scanning: ARP host discovery plus socket and Nmap service scans."""

from __future__ import annotations

import logging
import socket
from dataclasses import dataclass, field
from pathlib import Path

from cyberframework.utils import results_dir

log = logging.getLogger(__name__)

TOP_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 5900, 6379, 8080, 8443]


@dataclass
class Host:
    ip: str
    mac: str = ""
    services: list[dict] = field(default_factory=list)


def arp_discover(network: str, timeout: int = 2) -> list[Host]:
    """Return live hosts on *network* (CIDR) via an ARP sweep. Requires scapy + privileges."""
    from scapy.all import ARP, Ether, srp  # imported lazily: needs root/libpcap

    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network)
    answered, _ = srp(request, timeout=timeout, verbose=False)
    hosts = [
        Host(ip=rcv.sprintf("%ARP.psrc%"), mac=rcv.sprintf("%Ether.src%"))
        for _, rcv in answered
    ]
    log.info("ARP discovery found %d host(s) on %s", len(hosts), network)
    return hosts


def socket_scan(ip: str, ports: list[int], timeout: float = 1.0) -> list[dict]:
    """Connect-scan *ports* on *ip*, grabbing a short banner where possible."""
    open_ports: list[dict] = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((ip, port)) != 0:
                continue
            banner = ""
            try:
                banner = sock.recv(1024).decode(errors="replace").strip()
            except (socket.timeout, OSError):
                pass
            open_ports.append({"port": port, "service": banner})
    return open_ports


def nmap_version_scan(ip: str) -> list[dict]:
    """Run an Nmap version-detection scan via python3-nmap and normalise the output."""
    import nmap3

    results = nmap3.Nmap().nmap_version_detection(ip)
    services: list[dict] = []
    for port in results.get(ip, {}).get("ports", []):
        service = port.get("service", {})
        services.append(
            {
                "port": port.get("portid"),
                "name": service.get("name", ""),
                "product": f"{service.get('product', '')} {service.get('version', '')}".strip(),
            }
        )
    return services


def _port_list(scope: str) -> list[int]:
    return TOP_PORTS if scope == "fast" else list(range(1, 65536))


def run_scan(
    network: str, method: str = "socket", scope: str = "fast", out_dir: Path | None = None
) -> list[Host]:
    """Discover hosts on *network* and scan each with *method* ('socket' or 'nmap')."""
    out_dir = out_dir or results_dir("Scan")
    hosts = arp_discover(network)
    for host in hosts:
        log.info("Scanning %s", host.ip)
        if method == "nmap":
            host.services = nmap_version_scan(host.ip)
        else:
            host.services = socket_scan(host.ip, _port_list(scope))
    _write_report(hosts, out_dir)
    return hosts


def _write_report(hosts: list[Host], out_dir: Path) -> None:
    report = out_dir / "scan.txt"
    with report.open("w", encoding="utf-8") as fh:
        for index, host in enumerate(hosts, start=1):
            fh.write(f"Result {index}:\nip: {host.ip}\nmac: {host.mac}\nservices:\n")
            for svc in host.services:
                fh.write("  " + ", ".join(f"{k}={v}" for k, v in svc.items()) + "\n")
            fh.write("\n")
