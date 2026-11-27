"""Shared helpers: output paths, terminal control and input normalisation."""

from __future__ import annotations

import ipaddress
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
_CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}")


def clear_screen() -> None:
    """Clear the terminal on both POSIX and Windows without a shell injection risk."""
    command = "cls" if os.name == "nt" else "clear"
    try:
        subprocess.run([command], shell=False, check=False)
    except FileNotFoundError:
        # Fall back to ANSI clear if the platform command is missing.
        print("\033c", end="")


def results_dir(category: str, base: Path | None = None) -> Path:
    """Return (and create) a timestamped results directory for *category*."""
    base = base or Path.cwd() / "Results"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = base / f"{category}_Results" / stamp
    path.mkdir(parents=True, exist_ok=True)
    return path


def normalize_domain(value: str) -> str:
    """Strip a URL scheme and any path, returning the bare host.

    The original code used ``str.strip("https://")`` which removes *characters*
    (h, t, p, s, :, /) from both ends rather than a prefix -- a long-standing
    bug. This parses properly instead.
    """
    value = value.strip()
    value = _SCHEME_RE.sub("", value)
    value = value.split("/", 1)[0]
    return value.split(":", 1)[0].strip().lower()


def normalize_url(value: str) -> str:
    """Ensure *value* has a scheme and a single trailing slash removed."""
    value = value.strip()
    if not _SCHEME_RE.match(value):
        value = f"http://{value}"
    return value.rstrip("/")


def parse_network(value: str) -> ipaddress.IPv4Network:
    """Validate and return an IPv4 network in CIDR notation, raising ValueError."""
    return ipaddress.ip_network(value.strip(), strict=False)


def find_cves(text: str) -> list[str]:
    """Return a sorted, de-duplicated list of CVE identifiers found in *text*."""
    return sorted(set(_CVE_RE.findall(text or "")), reverse=True)
