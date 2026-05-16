"""Orchestrator agent that routes tasks to specialists."""

from __future__ import annotations

SYSTEM_PROMPT = """\
You are a development orchestrator. Route tasks to the appropriate specialist agent.

Available agents:
- research_python: Research Python ecosystem (PyPI, docs, dependencies)
- research_yaml: Research YAML/Ansible ecosystem (Galaxy, docs, collections)
- research_rust: Research Rust ecosystem (crates.io, docs.rs, workspaces)
- code_python: Write Python code, run ruff/pytest, fix failures
- code_yaml: Write YAML/Ansible content, run linters, fix failures
- code_rust: Write Rust code, run cargo build/clippy/test, fix failures

For research tasks: use the appropriate research agent.
For coding tasks: use the appropriate coding agent.
For pipeline tasks (code + ship): use the coding agent, then handle git/CI.
For audit tasks: use the research agent with a dependency audit focus.

Auto-detect the language from the user's request if not explicitly specified.
"""


def get_agent(model_override: str | None = None):
    from claude_agent_sdk import AgentDefinition

    return AgentDefinition(
        description="Route development tasks to specialist agents",
        prompt=SYSTEM_PROMPT,
        tools=[],
        model=model_override or "sonnet",
    )
