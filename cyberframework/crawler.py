"""A small, same-domain web crawler (breadth-first, thread-pooled)."""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from cyberframework.utils import results_dir

log = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


class Crawler:
    """Crawl pages within a single registered domain, collecting reachable URLs."""

    def __init__(self, workers: int = 20, timeout: float = 12.0, max_pages: int = 2000) -> None:
        self.workers = workers
        self.timeout = timeout
        self.max_pages = max_pages
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def _fetch(self, url: str) -> str | None:
        try:
            resp = self.session.get(url, timeout=self.timeout)
        except requests.RequestException:
            return None
        if resp.status_code == 200 and "text/html" in resp.headers.get("Content-Type", ""):
            return resp.text
        return None

    @staticmethod
    def _same_domain(url: str, domain: str) -> bool:
        return urlparse(url).netloc.endswith(domain)

    def crawl(self, start_url: str) -> list[str]:
        """Return the sorted list of same-domain URLs reachable from *start_url*."""
        start = time.time()
        domain = urlparse(start_url).netloc
        seen: set[str] = {start_url}
        found: set[str] = set()
        frontier = [start_url]

        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            while frontier and len(found) < self.max_pages:
                batch, frontier = frontier, []
                for url, html in zip(batch, pool.map(self._fetch, batch)):
                    if html is None:
                        continue
                    found.add(url)
                    for anchor in BeautifulSoup(html, "html.parser").find_all("a", href=True):
                        link = urljoin(url, anchor["href"]).split("#")[0]
                        if link not in seen and self._same_domain(link, domain):
                            seen.add(link)
                            frontier.append(link)

        elapsed = time.time() - start
        log.info("Crawled %d page(s) in %.1fs", len(found), elapsed)
        return sorted(found)

    def crawl_to_file(self, start_url: str, out_dir: Path | None = None) -> Path:
        import json

        out_dir = out_dir or results_dir("Crawler")
        urls = self.crawl(start_url)
        path = out_dir / "log.json"
        path.write_text(json.dumps(urls, indent=2), encoding="utf-8")
        return path
