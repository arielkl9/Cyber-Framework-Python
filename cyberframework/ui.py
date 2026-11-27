"""ASCII banners and interactive-menu rendering."""

from __future__ import annotations

from cyberframework.utils import clear_screen

BANNER = r"""
     _____                                   
    |  ___|  _ __    __ _   _ __ ___     ___ 
    | |_    | '__|  / _` | | '_ ` _ \   / _ \
    |  _|   | |    | (_| | | | | | | | |  __/
    |_|_    |_| __  \__,_| |_| |_| |_|  \___|
       \ \      / /   ___    _ __  | | __     
        \ \ /\ / /   / _ \  | '__| | |/ /     
         \ V  V /   | (_) | | |    |   <      
          \_/\_/     \___/  |_|    |_|\_\     
"""

RECON_BANNER = r"""
         ____                                
        |  _ \    ___    ___    ___    _ __  
        | |_) |  / _ \  / __|  / _ \  | '_ \ 
        |  _ <  |  __/ | (__  | (_) | | | | |
        |_| \_\  \___|  \___|  \___/  |_| |_|
"""

SCAN_BANNER = r"""
     ____                                   _                 
    / ___|    ___    __ _   _ __    _ __   (_)  _ __     __ _ 
    \___ \   / __|  / _` | | '_ \  | '_ \  | | | '_ \   / _` |
     ___) | | (__  | (_| | | | | | | | | | | | | | | | | (_| |
    |____/   \___|  \__,_| |_| |_| |_| |_| |_| |_| |_|  \__, |
                                                         |___/ 
"""


def _box(title: str, options: list[str]) -> None:
    width = max([len(title)] + [len(o) for o in options]) + 6
    bar = "*" * (width + 4)
    print(bar)
    print(f"*  {title.ljust(width)}*")
    print(f"*  {' '.ljust(width)}*")
    for opt in options:
        print(f"*  {opt.ljust(width)}*")
    print(bar)


def main_menu() -> None:
    clear_screen()
    print(BANNER)
    _box("Modules:", ["[1] Recon", "[2] Scan", "[3] Discovery / Misc", "[4] Kernel CVE lookup", "[q] Quit"])


def recon_menu() -> None:
    clear_screen()
    print(RECON_BANNER)
    _box(
        "Recon options:",
        [
            "[1] WHOIS lookup",
            "[2] DNS enumeration",
            "[3] Subdomain brute force",
            "[4] Directory brute force",
            "[5] Run everything",
            "[b] Back",
        ],
    )


def scan_menu() -> None:
    clear_screen()
    print(SCAN_BANNER)
    _box(
        "Scan options:",
        [
            "[1] ARP + Nmap version scan (needs nmap)",
            "[2] ARP + socket scan (no dependencies)",
            "[b] Back",
        ],
    )


def discovery_menu() -> None:
    clear_screen()
    _box(
        "Discovery / Misc tools:",
        [
            "[1] ARP scanner",
            "[2] Ping sweep",
            "[3] Socket port scanner",
            "[b] Back",
        ],
    )
