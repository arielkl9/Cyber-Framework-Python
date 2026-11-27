"""Reconnaissance: WHOIS, DNS enumeration and subdomain/directory brute force."""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import dns.resolver
import requests

try:  # python-whois exposes ``whois.query``; fall back gracefully if absent.
    import whois as _whois
except ImportError:  # pragma: no cover
    _whois = None

from cyberframework.utils import normalize_domain, normalize_url, results_dir

log = logging.getLogger(__name__)

DNS_RECORD_TYPES = ("A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT")
DEFAULT_TIMEOUT = 3.5


def whois_lookup(target: str, out_dir: Path | None = None) -> dict[str, str]:
    """Run a WHOIS lookup and persist the result. Returns the parsed fields."""
    if _whois is None:
        raise RuntimeError("python-whois is not installed; run 'pip install python-whois'")
    host = normalize_domain(target)
    out_dir = out_dir or results_dir("Recon")
    log.info("WHOIS lookup for %s", host)
    result = _whois.query(host)
    data = {k: str(v) for k, v in (result.__dict__.items() if result else [])}
    report = out_dir / "whois.txt"
    report.write_text(
        "WHOIS results:\n\n" + "\n".join(f"{k}: {v}" for k, v in data.items()),
        encoding="utf-8",
    )
    return data


def dns_enum(target: str, out_dir: Path | None = None) -> dict[str, list[str]]:
    """Enumerate common DNS record types for *target*."""
    host = normalize_domain(target)
    out_dir = out_dir or results_dir("Recon")
    resolver = dns.resolver.Resolver()
    found: dict[str, list[str]] = {}
    log.info("DNS enumeration for %s", host)
    for record_type in DNS_RECORD_TYPES:
        try:
            answers = resolver.resolve(host, record_type)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            continue
        except dns.exception.DNSException as exc:
            log.debug("DNS %s lookup failed: %s", record_type, exc)
            continue
        found[record_type] = [str(r) for r in answers]
    report = out_dir / "dns_enum.txt"
    with report.open("w", encoding="utf-8") as fh:
        fh.write(f"DNS enumeration for {host}:\n\n")
        for record_type, records in found.items():
            fh.write(f"{record_type}:\n")
            fh.writelines(f"    {r}\n" for r in records)
            fh.write("\n")
    return found


def _load_wordlist(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def subdomain_bruteforce(
    target: str,
    wordlist: Path,
    out_dir: Path | None = None,
    workers: int = 50,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[str]:
    """Discover live subdomains by resolving/requesting ``<word>.<domain>``."""
    host = normalize_domain(target)
    out_dir = out_dir or results_dir("Recon")
    words = _load_wordlist(wordlist)
    discovered: list[str] = []
    log.info("Subdomain brute force on %s (%d candidates)", host, len(words))

    def probe(word: str) -> str | None:
        url = f"http://{word}.{host}"
        try:
            requests.get(url, timeout=timeout)
            return url
        except requests.RequestException:
            return None

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(probe, w): w for w in words}
        for future in as_completed(futures):
            url = future.result()
            if url:
                discovered.append(url)
                log.info("[+] %s", url)

    (out_dir / "subdomains.txt").write_text(
        "Discovered subdomains:\n\n" + "\n".join(sorted(discovered)), encoding="utf-8"
    )
    return discovered


def directory_bruteforce(
    target: str,
    wordlist: Path,
    out_dir: Path | None = None,
    workers: int = 50,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[tuple[str, int]]:
    """Brute force web paths, reporting any non-404 response with its status code."""
    base = normalize_url(target)
    out_dir = out_dir or results_dir("Recon")
    words = _load_wordlist(wordlist)
    hits: list[tuple[str, int]] = []
    log.info("Directory brute force on %s (%d candidates)", base, len(words))

    def probe(word: str) -> tuple[str, int] | None:
        url = f"{base}/{word}"
        try:
            resp = requests.get(url, timeout=timeout, allow_redirects=False)
        except requests.RequestException:
            return None
        if resp.status_code != 404:
            return url, resp.status_code
        return None

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(probe, w): w for w in words}
        for future in as_completed(futures):
            hit = future.result()
            if hit:
                hits.append(hit)
                log.info("[+] %s -> %s", hit[0], hit[1])

    (out_dir / "directories.txt").write_text(
        "Discovered paths:\n\n" + "\n".join(f"{code} {url}" for url, code in sorted(hits)),
        encoding="utf-8",
    )
    return hits
