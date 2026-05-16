"""Unified lint, test, and build runner."""

from __future__ import annotations

import subprocess


def run_linter(language: str, path: str = ".") -> dict:
    """Run the appropriate linter."""
    cmds = {
        "python": [
            (["ruff", "check", path], "ruff check"),
            (["ruff", "format", "--check", path], "ruff format"),
        ],
        "yaml": [
            (["yamllint", "."], "yamllint"),
            (["ansible-lint", "--profile", "production"], "ansible-lint"),
        ],
        "rust": [
            (["cargo", "clippy", "--all-targets", "--", "-D", "warnings"], "cargo clippy"),
            (["cargo", "fmt", "--check"], "cargo fmt"),
        ],
    }
    results = []
    for cmd, label in cmds.get(language, []):
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=path if path != "." else None)
        results.append({"tool": label, "passed": r.returncode == 0, "output": (r.stdout + r.stderr).strip()[-500:]})
    passed = all(r["passed"] for r in results)
    return {"passed": passed, "results": results}


def run_tests(language: str, path: str = ".", test_filter: str | None = None) -> dict:
    """Run the appropriate test suite."""
    cmds = {
        "python": ["pytest", "-v", "--tb=short"],
        "yaml": ["ansible-test", "sanity", "-v", "--color", "yes"],
        "rust": ["cargo", "test"],
    }
    cmd = cmds.get(language, [])
    if not cmd:
        return {"passed": False, "output": f"Unknown language: {language}"}
    if test_filter and language == "python":
        cmd.extend(["-k", test_filter])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=path if path != "." else None)
    return {"passed": r.returncode == 0, "output": (r.stdout + r.stderr).strip()[-1000:]}


def run_build(language: str, path: str = ".") -> dict:
    """Run the build step."""
    cmds = {
        "rust": ["cargo", "build"],
        "python": ["python", "-m", "build"],
    }
    cmd = cmds.get(language)
    if not cmd:
        return {"passed": True, "output": "No build step needed"}
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=path if path != "." else None)
    return {"passed": r.returncode == 0, "output": (r.stdout + r.stderr).strip()[-500:]}
