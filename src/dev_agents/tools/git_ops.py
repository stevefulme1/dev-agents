"""Git operations via gh CLI."""

from __future__ import annotations

import subprocess


def git_commit(message: str, files: list[str] | None = None) -> str:
    """Stage and commit changes."""
    if files:
        subprocess.run(["git", "add"] + files, check=True, capture_output=True)
    else:
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()


def git_push(branch: str | None = None) -> str:
    """Push to origin."""
    cmd = ["git", "push", "origin"]
    if branch:
        cmd.append(branch)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip() or result.stderr.strip()


def create_pr(title: str, body: str, base: str = "main") -> str:
    """Create a GitHub PR via gh CLI."""
    result = subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body", body, "--base", base],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
