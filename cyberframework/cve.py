"""Look up known CVEs for detected services via the NVD REST API (v2.0)."""

from __future__ import annotations

import logging
import time
from pathlib import Path

import requests

from cyberframework.scan import Host, arp_discover, nmap_version_scan
from cyberframework.utils import results_dir

log = logging.getLogger(__name__)

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
# NVD allows ~5 requests / 30s without an API key; ~50 with one. Be conservative.
RATE_LIMIT_SECONDS = 6.0


def cves_for_cpe(cpe: str, session: requests.Session, api_key: str | None = None) -> list[str]:
    """Return CVE IDs associated with a CPE string from NVD."""
    headers = {"apiKey": api_key} if api_key else {}
    try:
        resp = session.get(NVD_API, params={"cpeName": cpe}, headers=headers, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        log.warning("NVD lookup failed for %s: %s", cpe, exc)
        return []
    data = resp.json()
    ids = [
        entry["cve"]["id"]
        for entry in data.get("vulnerabilities", [])
        if entry.get("cve", {}).get("id")
    ]
    return sorted(set(ids), reverse=True)


def scan_network_for_cves(
    network: str, out_dir: Path | None = None, api_key: str | None = None
) -> list[Host]:
    """Discover hosts, fingerprint services with Nmap, then map CPEs to CVEs."""
    out_dir = out_dir or results_dir("CVE_Scan")
    session = requests.Session()
    hosts = arp_discover(network)
    for host in hosts:
        host.services = nmap_version_scan(host.ip)
        for service in host.services:
            cpe = service.get("cpe")
            if not cpe:
                continue
            service["cves"] = cves_for_cpe(cpe, session, api_key)
            time.sleep(RATE_LIMIT_SECONDS if not api_key else 0.6)
    _write_report(hosts, out_dir)
    return hosts


def _write_report(hosts: list[Host], out_dir: Path) -> None:
    with (out_dir / "cves_found.txt").open("w", encoding="utf-8") as fh:
        for host in hosts:
            fh.write(f"\nHost {host.ip}:\n")
            for svc in host.services:
                cves = svc.get("cves", [])
                fh.write(f"  port {svc.get('port')} {svc.get('product', '')}\n")
                if cves:
                    fh.writelines(f"    {cve}\n" for cve in cves)
                else:
                    fh.write("    no CVEs found\n")
