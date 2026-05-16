"""CLI for dev-agents."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dev-agents",
        description="Research and coding agents for Python, YAML, and Rust",
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # research
    research = sub.add_parser("research", help="Research a topic")
    research.add_argument("language", choices=["python", "yaml", "rust"])
    research.add_argument("prompt", help="What to research")

    # code
    code = sub.add_parser("code", help="Write code")
    code.add_argument("language", choices=["python", "yaml", "rust"])
    code.add_argument("prompt", help="What to implement")

    # pipeline
    pipeline = sub.add_parser("pipeline", help="Code, test, and ship")
    pipeline.add_argument("language", choices=["python", "yaml", "rust"])
    pipeline.add_argument("prompt", help="What to implement and ship")

    # audit
    audit = sub.add_parser("audit", help="Audit dependencies")
    audit.add_argument("language", choices=["python", "yaml", "rust"])

    # detect
    sub.add_parser("detect", help="Detect project languages")

    # Common flags for all subcommands that take language
    for p in [research, code, pipeline, audit]:
        p.add_argument("--model", choices=["haiku", "sonnet", "opus"], default=None)
        p.add_argument("--dry-run", action="store_true", default=False)

    for p in [code, pipeline]:
        p.add_argument("--no-push", action="store_true", default=False)
        p.add_argument("--base-branch", default="main")

    return parser
