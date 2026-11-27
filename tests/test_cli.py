"""Smoke tests for the CLI parser and module imports."""

from __future__ import annotations

import pytest

from cyberframework.cli import build_parser


def test_parser_builds():
    assert build_parser() is not None


def test_version(capsys):
    parser = build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--version"])
    assert exc.value.code == 0
    assert "2.0.0" in capsys.readouterr().out


def test_scan_defaults():
    args = build_parser().parse_args(["scan", "192.168.1.0/24"])
    assert args.method == "socket"
    assert args.scope == "fast"


def test_recon_subcommand():
    args = build_parser().parse_args(["recon", "whois", "example.com"])
    assert args.recon_action == "whois"
    assert args.target == "example.com"
