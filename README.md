# dev-agents

Research and coding agents for Python, YAML, and Rust — built on the Claude Agent SDK.

## Install

```bash
pip install dev-agents
```

## Usage

```bash
# Research
dev-agents research python "best async HTTP client library"
dev-agents research rust "how to implement custom serde deserializer"
dev-agents research yaml "best practices for Ansible EDA rulebooks"

# Code
dev-agents code python "add a retry decorator with exponential backoff"
dev-agents code rust "add a new crate called utils to the workspace"
dev-agents code yaml "create a role for nginx with molecule tests"

# Full pipeline (code + lint + test + commit + PR + CI watch)
dev-agents pipeline python "add pagination to the API client and ship it"

# Dependency audit
dev-agents audit python

# Detect project languages
dev-agents detect
```

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `research_python` | sonnet | PyPI, docs, codebase analysis, dependency auditing |
| `research_yaml` | sonnet | Ansible Galaxy, docs, collection analysis |
| `research_rust` | sonnet | crates.io, docs.rs, workspace analysis |
| `code_python` | opus | Write Python, run ruff/pytest, fix failures |
| `code_yaml` | opus | Write YAML/Ansible, run linters, fix failures |
| `code_rust` | opus | Write Rust, cargo build/clippy/test, workspaces |

## License

GPL-3.0-or-later
