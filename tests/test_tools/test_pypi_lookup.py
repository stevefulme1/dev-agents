"""Tests for PyPI lookup."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx

from dev_agents.tools.pypi_lookup import search_pypi


def test_search_pypi_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "info": {
            "name": "httpx",
            "version": "0.27.0",
            "summary": "HTTP client",
            "requires_python": ">=3.8",
            "home_page": "",
            "license": "BSD",
        }
    }
    mock_resp.raise_for_status = MagicMock()
    with patch("dev_agents.tools.pypi_lookup.httpx.get", return_value=mock_resp):
        result = search_pypi("httpx")
        assert result["name"] == "httpx"
        assert result["version"] == "0.27.0"


def test_search_pypi_not_found():
    with patch("dev_agents.tools.pypi_lookup.httpx.get", side_effect=httpx.HTTPError("404")):
        result = search_pypi("nonexistent-pkg-xyz")
        assert "error" in result
