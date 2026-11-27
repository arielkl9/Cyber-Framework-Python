"""Unit tests for the pure helpers in cyberframework.utils (no network/root)."""

from __future__ import annotations

import ipaddress

import pytest

from cyberframework.utils import find_cves, normalize_domain, normalize_url, parse_network


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("https://example.com", "example.com"),
        ("http://example.com/path/page", "example.com"),
        ("example.com:8080", "example.com"),
        ("HTTPS://Example.COM/", "example.com"),
        ("ftp://host.example.org/x", "host.example.org"),
    ],
)
def test_normalize_domain(raw, expected):
    assert normalize_domain(raw) == expected


def test_normalize_domain_does_not_strip_leading_letters():
    # Regression: the old code used str.strip("https://") and mangled hosts
    # beginning with those characters (e.g. "sparta.io" -> "arta.io").
    assert normalize_domain("sparta.io") == "sparta.io"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("example.com", "http://example.com"),
        ("http://example.com/", "http://example.com"),
        ("https://example.com/path/", "https://example.com/path"),
    ],
)
def test_normalize_url(raw, expected):
    assert normalize_url(raw) == expected


def test_parse_network_valid():
    assert parse_network("192.168.1.0/24") == ipaddress.ip_network("192.168.1.0/24")


def test_parse_network_invalid():
    with pytest.raises(ValueError):
        parse_network("not-a-network")


def test_find_cves_dedupes_and_sorts():
    text = "CVE-2021-1234 and again CVE-2021-1234, plus CVE-2024-99999"
    assert find_cves(text) == ["CVE-2024-99999", "CVE-2021-1234"]


def test_find_cves_empty():
    assert find_cves("") == []
