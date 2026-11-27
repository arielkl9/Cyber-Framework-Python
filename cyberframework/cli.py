"""Command-line interface: argparse subcommands plus an interactive menu."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from cyberframework import __version__, ui
from cyberframework.utils import clear_screen

WORDLIST_DIR = Path(__file__).resolve().parent.parent / "wordlists"
DEFAULT_SUBDOMAINS = WORDLIST_DIR / "subdomains.txt"
DEFAULT_DIRS = WORDLIST_DIR / "dirs.txt"


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )


# --- subcommand handlers ---------------------------------------------------

def _cmd_recon(args: argparse.Namespace) -> int:
    from cyberframework import recon

    if args.recon_action == "whois":
        print(recon.whois_lookup(args.target))
    elif args.recon_action == "dns":
        for rtype, records in recon.dns_enum(args.target).items():
            print(f"{rtype}: {', '.join(records)}")
    elif args.recon_action == "subdomains":
        recon.subdomain_bruteforce(args.target, Path(args.wordlist))
    elif args.recon_action == "dirs":
        recon.directory_bruteforce(args.target, Path(args.wordlist))
    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    from cyberframework import scan

    scan.run_scan(args.network, method=args.method, scope=args.scope)
    return 0


def _cmd_discover(args: argparse.Namespace) -> int:
    from cyberframework import discovery

    if args.discover_action == "arp":
        discovery.arp_scan(args.network)
    else:
        discovery.ping_sweep(args.network)
    return 0


def _cmd_cve(args: argparse.Namespace) -> int:
    from cyberframework import cve

    cve.scan_network_for_cves(args.network, api_key=args.api_key)
    return 0


def _cmd_crawl(args: argparse.Namespace) -> int:
    from cyberframework.crawler import Crawler

    path = Crawler().crawl_to_file(args.url)
    print(f"Results written to {path}")
    return 0


# --- interactive menu ------------------------------------------------------

def _interactive() -> int:
    while True:
        ui.main_menu()
        choice = input("Choose: ").strip().lower()
        if choice == "q":
            return 0
        try:
            if choice == "1":
                _interactive_recon()
            elif choice == "2":
                _interactive_scan()
            elif choice == "3":
                _interactive_discovery()
            elif choice == "4":
                from cyberframework import cve

                cve.scan_network_for_cves(input("Network (CIDR): ").strip())
            else:
                continue
        except KeyboardInterrupt:
            continue
        except Exception as exc:  # keep the menu alive on operational errors
            print(f"Error: {exc}")
        input("\nPress Enter to continue...")


def _interactive_recon() -> None:
    from cyberframework import recon

    ui.recon_menu()
    choice = input("Choose: ").strip().lower()
    if choice == "b":
        return
    target = input("Domain: ").strip()
    if choice in ("1", "5"):
        print(recon.whois_lookup(target))
    if choice in ("2", "5"):
        recon.dns_enum(target)
    if choice in ("3", "5"):
        recon.subdomain_bruteforce(target, DEFAULT_SUBDOMAINS)
    if choice in ("4", "5"):
        recon.directory_bruteforce(target, DEFAULT_DIRS)


def _interactive_scan() -> None:
    from cyberframework import scan

    ui.scan_menu()
    choice = input("Choose: ").strip().lower()
    if choice == "b":
        return
    network = input("Network (CIDR): ").strip()
    if choice == "1":
        scan.run_scan(network, method="nmap")
    elif choice == "2":
        scope = "full" if input("Full scan? [y/N]: ").strip().lower() == "y" else "fast"
        scan.run_scan(network, method="socket", scope=scope)


def _interactive_discovery() -> None:
    from cyberframework import discovery

    ui.discovery_menu()
    choice = input("Choose: ").strip().lower()
    if choice == "b":
        return
    network = input("Network (CIDR): ").strip()
    if choice == "1":
        discovery.arp_scan(network)
    elif choice == "2":
        discovery.ping_sweep(network)


# --- parser ----------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cyberframework",
        description="Modular reconnaissance and scanning toolkit (authorised use only).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable debug logging")
    sub = parser.add_subparsers(dest="command")

    recon = sub.add_parser("recon", help="reconnaissance tools")
    recon_sub = recon.add_subparsers(dest="recon_action", required=True)
    recon_sub.add_parser("whois").add_argument("target")
    recon_sub.add_parser("dns").add_argument("target")
    sd = recon_sub.add_parser("subdomains")
    sd.add_argument("target")
    sd.add_argument("--wordlist", default=str(DEFAULT_SUBDOMAINS))
    db = recon_sub.add_parser("dirs")
    db.add_argument("target")
    db.add_argument("--wordlist", default=str(DEFAULT_DIRS))
    recon.set_defaults(func=_cmd_recon)

    scan = sub.add_parser("scan", help="ARP discovery + port/service scan")
    scan.add_argument("network")
    scan.add_argument("--method", choices=["socket", "nmap"], default="socket")
    scan.add_argument("--scope", choices=["fast", "full"], default="fast")
    scan.set_defaults(func=_cmd_scan)

    discover = sub.add_parser("discover", help="host discovery")
    discover.add_argument("discover_action", choices=["arp", "ping"])
    discover.add_argument("network")
    discover.set_defaults(func=_cmd_discover)

    cve = sub.add_parser("cve", help="map detected services to known CVEs via NVD")
    cve.add_argument("network")
    cve.add_argument("--api-key", default=None, help="NVD API key (raises rate limits)")
    cve.set_defaults(func=_cmd_cve)

    crawl = sub.add_parser("crawl", help="same-domain web crawler")
    crawl.add_argument("url")
    crawl.set_defaults(func=_cmd_crawl)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _configure_logging(getattr(args, "verbose", False))
    if not getattr(args, "command", None):
        try:
            return _interactive()
        except KeyboardInterrupt:
            clear_screen()
            return 0
    return args.func(args)
