"""Tests for CLI argument parsing."""

from __future__ import annotations

from dev_agents.cli import build_parser


def test_research_command():
    parser = build_parser()
    args = parser.parse_args(["research", "python", "best http client"])
    assert args.mode == "research"
    assert args.language == "python"
    assert args.prompt == "best http client"


def test_code_command():
    parser = build_parser()
    args = parser.parse_args(["code", "rust", "add utils crate"])
    assert args.mode == "code"
    assert args.language == "rust"


def test_pipeline_command():
    parser = build_parser()
    args = parser.parse_args(["pipeline", "python", "add pagination"])
    assert args.mode == "pipeline"


def test_detect_command():
    parser = build_parser()
    args = parser.parse_args(["detect"])
    assert args.mode == "detect"


def test_dry_run_flag():
    parser = build_parser()
    args = parser.parse_args(["code", "python", "test", "--dry-run"])
    assert args.dry_run is True


def test_model_override():
    parser = build_parser()
    args = parser.parse_args(["research", "python", "test", "--model", "haiku"])
    assert args.model == "haiku"
