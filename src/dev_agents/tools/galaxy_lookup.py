"""Ansible Galaxy lookup tools."""

from __future__ import annotations

import httpx

_GALAXY_BASE = "https://galaxy.ansible.com/api"


def search_galaxy(query: str, limit: int = 5) -> list[dict]:
    """Search Ansible Galaxy for collections."""
    try:
        resp = httpx.get(
            f"{_GALAXY_BASE}/v3/plugin/ansible/search/collection-versions/",
            params={"q": query, "limit": limit, "is_highest": True},
            timeout=15,
        )
        resp.raise_for_status()
    except httpx.HTTPError:
        return []
    return [
        {
            "namespace": item.get("namespace", ""),
            "name": item.get("name", ""),
            "version": item.get("version", ""),
            "description": item.get("description", ""),
        }
        for item in resp.json().get("data", [])
    ]
