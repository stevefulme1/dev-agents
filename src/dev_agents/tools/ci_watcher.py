"""GitHub Actions CI watcher."""

from __future__ import annotations

import json
import subprocess
import time


def watch_ci(repo: str, branch: str, poll_interval: int = 30, max_wait: int = 600) -> dict:
    """Poll GitHub Actions CI until complete or timeout."""
    elapsed = 0
    while elapsed < max_wait:
        result = subprocess.run(
            [
                "gh",
                "run",
                "list",
                "--repo",
                repo,
                "--branch",
                branch,
                "--limit",
                "1",
                "--json",
                "status,conclusion,databaseId,url",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        runs = json.loads(result.stdout)
        if not runs:
            time.sleep(poll_interval)
            elapsed += poll_interval
            continue
        run = runs[0]
        if run["status"] == "completed":
            return {
                "status": run["status"],
                "conclusion": run["conclusion"],
                "url": run["url"],
                "run_id": run["databaseId"],
            }
        time.sleep(poll_interval)
        elapsed += poll_interval
    return {"error": "Timeout waiting for CI", "elapsed": elapsed}


def get_ci_failure_logs(repo: str, run_id: int) -> str:
    """Fetch failure logs from a CI run."""
    result = subprocess.run(
        ["gh", "run", "view", str(run_id), "--repo", repo, "--log-failed"],
        capture_output=True,
        text=True,
    )
    output = result.stdout if result.returncode == 0 else result.stderr
    lines = output.strip().splitlines()
    return "\n".join(lines[-100:]) if len(lines) > 100 else output.strip()
