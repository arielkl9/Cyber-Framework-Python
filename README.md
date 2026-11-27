# Cyber-Framework-Python

A modular reconnaissance and scanning toolkit, wrapped behind a single
command-line entry point. It bundles small, well-scoped security utilities —
reconnaissance, host discovery, port/service scanning, a same-domain web
crawler, and a service-to-CVE lookup against the NVD API.

> **Authorised use only.** Run this only against systems you own or have
> explicit written permission to test. See [SECURITY.md](SECURITY.md).

## Features

| Module | What it does |
| --- | --- |
| **Recon** | WHOIS, DNS enumeration, subdomain brute force, directory brute force |
| **Scan** | ARP host discovery + socket connect-scan or Nmap version detection |
| **Discovery** | Standalone ARP scan and ICMP ping sweep |
| **CVE** | Fingerprints services with Nmap and maps CPEs to known CVEs via NVD |
| **Crawler** | Breadth-first, same-domain web crawler |

## Installation

```bash
git clone https://github.com/arielkl9/Cyber-Framework-Python.git
cd Cyber-Framework-Python
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

Nmap scans require the `nmap` binary on your `PATH`. ARP discovery and ping
sweeps use raw sockets and need root/Administrator privileges.

## Usage

### Command line

```bash
cyberframework recon whois example.com
cyberframework recon dns example.com
cyberframework recon subdomains example.com --wordlist wordlists/subdomains.txt
cyberframework recon dirs https://example.com --wordlist wordlists/dirs.txt

cyberframework scan 192.168.1.0/24 --method socket --scope fast
cyberframework scan 192.168.1.0/24 --method nmap

cyberframework discover arp 192.168.1.0/24
cyberframework discover ping 192.168.1.0/24

cyberframework cve 192.168.1.0/24 --api-key $NVD_API_KEY
cyberframework crawl https://example.com
```

Run with no arguments for the interactive menu:

```bash
cyberframework
```

Results are written to a timestamped folder under `Results/`.

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest -q
```

## What changed in 2.0

This release is a full modernisation of the original 2023 scripts:

- Restructured the flat scripts into an installable `cyberframework` package
  with a proper `argparse` CLI (the interactive menu is still available).
- Fixed real bugs: a menu dispatch that printed "Bad Input" and exited on valid
  choices; `except A or B` clauses that silently caught only `A`; and
  `str.strip("https://")` being used to strip a URL scheme (it strips
  *characters*, so e.g. `sparta.io` became `arta.io`).
- Replaced the corrupted UTF-16 `requirements.txt`, pinned dependencies, and
  added `pyproject.toml` packaging.
- Added type hints, structured `logging`, docstrings, a test suite, and GitHub
  Actions CI (ruff + pytest on Python 3.9–3.12).

## License

MIT — see [LICENSE](LICENSE).
