"""Research pipeline."""

from __future__ import annotations


async def run_research(language: str, prompt: str, options) -> None:
    """Run a research query through the appropriate agent."""
    from claude_agent_sdk import query

    agent_prompt = f"Use the research_{language} agent to research: {prompt}"
    async for message in query(prompt=agent_prompt, options=options):
        if hasattr(message, "content"):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="", flush=True)
    print()
