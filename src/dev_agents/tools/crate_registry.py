"""crates.io lookup tools."""

from __future__ import annotations

import httpx

_CRATES_BASE = "https://crates.io/api/v1/crates"
_HEADERS = {"User-Agent": "dev-agents/0.1.0 (https://github.com/stevefulme1/dev-agents)"}


def search_crates(query: str, limit: int = 5) -> list[dict]:
    """Search crates.io."""
    try:
        resp = httpx.get(f"{_CRATES_BASE}", params={"q": query, "per_page": limit}, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
    except httpx.HTTPError:
        return []
    return [
        {
            "name": c.get("name", ""),
            "version": c.get("max_version", ""),
            "description": c.get("description", ""),
            "downloads": c.get("downloads", 0),
            "documentation": c.get("documentation", ""),
        }
        for c in resp.json().get("crates", [])
    ]


def get_crate_info(crate_name: str) -> dict:
    """Get detailed crate info."""
    try:
        resp = httpx.get(f"{_CRATES_BASE}/{crate_name}", headers=_HEADERS, timeout=15)
        resp.raise_for_status()
    except httpx.HTTPError:
        return {"error": f"Crate '{crate_name}' not found"}
    crate = resp.json().get("crate", {})
    return {
        "name": crate.get("name", ""),
        "version": crate.get("max_version", ""),
        "description": crate.get("description", ""),
        "repository": crate.get("repository", ""),
        "documentation": crate.get("documentation", ""),
        "downloads": crate.get("downloads", 0),
        "categories": crate.get("categories", []),
    }
