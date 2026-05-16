"""Tests for crates.io lookup."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from dev_agents.tools.crate_registry import get_crate_info, search_crates


def test_search_crates_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "crates": [
            {
                "name": "serde",
                "max_version": "1.0.0",
                "description": "Serialization",
                "downloads": 1000,
                "documentation": "https://docs.rs/serde",
            }
        ]
    }
    mock_resp.raise_for_status = MagicMock()
    with patch("dev_agents.tools.crate_registry.httpx.get", return_value=mock_resp):
        result = search_crates("serde")
        assert len(result) == 1
        assert result[0]["name"] == "serde"


def test_get_crate_info_not_found():
    with patch("dev_agents.tools.crate_registry.httpx.get", side_effect=Exception("404")):
        result = get_crate_info("nonexistent-crate")
        assert "error" in result
