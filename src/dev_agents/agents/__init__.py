"""Agent definitions and factory."""

from __future__ import annotations


def build_agent_options(model_override: str | None = None):
    """Build ClaudeAgentOptions with all agents registered."""
    try:
        from claude_agent_sdk import ClaudeAgentOptions
    except ImportError:
        return None

    from dev_agents.agents.coding.python import get_agent as get_code_python
    from dev_agents.agents.coding.rust import get_agent as get_code_rust
    from dev_agents.agents.coding.yaml import get_agent as get_code_yaml
    from dev_agents.agents.research.python import get_agent as get_research_python
    from dev_agents.agents.research.rust import get_agent as get_research_rust
    from dev_agents.agents.research.yaml import get_agent as get_research_yaml

    agents = {
        "research_python": get_research_python(model_override),
        "research_yaml": get_research_yaml(model_override),
        "research_rust": get_research_rust(model_override),
        "code_python": get_code_python(model_override),
        "code_yaml": get_code_yaml(model_override),
        "code_rust": get_code_rust(model_override),
    }

    return ClaudeAgentOptions(agents=agents, permission_mode="acceptEdits")
