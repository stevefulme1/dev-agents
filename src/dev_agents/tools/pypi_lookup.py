"""PyPI package lookup tools."""

from __future__ import annotations

import httpx

_PYPI_BASE = "https://pypi.org/pypi"


def search_pypi(package_name: str) -> dict:
    """Get info about a PyPI package."""
    try:
        resp = httpx.get(f"{_PYPI_BASE}/{package_name}/json", timeout=15)
        resp.raise_for_status()
    except httpx.HTTPError:
        return {"error": f"Package '{package_name}' not found on PyPI"}
    info = resp.json().get("info", {})
    return {
        "name": info.get("name", ""),
        "version": info.get("version", ""),
        "summary": info.get("summary", ""),
        "requires_python": info.get("requires_python", ""),
        "home_page": info.get("home_page", ""),
        "license": info.get("license", ""),
    }
