"""Full pipeline: code -> lint -> test -> commit -> PR -> CI watch -> fix."""

from __future__ import annotations


async def run_pipeline(
    language: str,
    prompt: str,
    options,
    no_push: bool = False,
    base: str = "main",
) -> None:
    """Run the full code-and-ship pipeline."""
    from claude_agent_sdk import query

    ship_instruction = ""
    if not no_push:
        ship_instruction = (
            f" Then commit with a descriptive message, push to a feature branch, "
            f"and create a PR against {base}. Watch CI until it passes — if CI fails, "
            f"read the failure logs, fix the issues, push again, and re-check CI. "
            f"Repeat up to 3 times."
        )

    agent_prompt = (
        f"Use the code_{language} agent. "
        f"Implement the following: {prompt}\n\n"
        f"After writing code, run the linter and fix any issues. "
        f"Run the tests and fix any failures. "
        f"Repeat lint+test until everything passes."
        f"{ship_instruction}"
    )

    async for message in query(prompt=agent_prompt, options=options):
        if hasattr(message, "content"):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="", flush=True)
    print()
