"""Entry point for dev-agents CLI."""

from __future__ import annotations

import asyncio
import sys

from dev_agents.cli import build_parser
from dev_agents.config import detect_languages


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.mode == "detect":
        langs = detect_languages()
        print(f"Detected languages: {', '.join(langs)}")
        return

    if getattr(args, "dry_run", False):
        print(f"[dry-run] Would run: mode={args.mode} language={args.language}")
        print(f"[dry-run] Prompt: {args.prompt}")
        print(f"[dry-run] Model override: {args.model or 'default'}")
        return

    asyncio.run(run_agent(args))


async def run_agent(args) -> None:
    """Dispatch to the appropriate agent pipeline."""
    try:
        from claude_agent_sdk import query
    except ImportError:
        print(
            "Error: claude-agent-sdk not installed. Run: pip install claude-agent-sdk",
            file=sys.stderr,
        )
        sys.exit(1)

    from dev_agents.agents import build_agent_options

    options = build_agent_options(model_override=args.model)

    mode = args.mode
    language = args.language
    prompt = args.prompt

    if mode == "research":
        agent_prompt = f"Use the research_{language} agent to research: {prompt}"
    elif mode == "code":
        agent_prompt = (
            f"Use the code_{language} agent to implement the following. "
            f"After writing code, run the linter and tests. Fix any failures. "
            f"Instruction: {prompt}"
        )
    elif mode == "pipeline":
        no_push = getattr(args, "no_push", False)
        base = getattr(args, "base_branch", "main")
        agent_prompt = (
            f"Use the code_{language} agent to implement the following. "
            f"After writing code, run the linter and tests, fix any failures. "
            f"Then commit, push to a feature branch, and create a PR against {base}. "
            f"Watch CI until it passes, fixing any failures. "
            f"{'Do NOT push or create a PR.' if no_push else ''}"
            f"Instruction: {prompt}"
        )
    elif mode == "audit":
        agent_prompt = (
            f"Use the research_{language} agent to audit dependencies in this project "
            f"for known vulnerabilities, outdated versions, and license issues."
        )
    else:
        print(f"Unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)

    async for message in query(prompt=agent_prompt, options=options):
        if hasattr(message, "content"):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
