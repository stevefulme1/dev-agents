"""Tests for project detection."""

from __future__ import annotations

from dev_agents.config import detect_languages, is_rust_workspace


def test_detect_python(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='test'\n")
    assert "python" in detect_languages(str(tmp_path))


def test_detect_rust(tmp_path):
    (tmp_path / "Cargo.toml").write_text("[package]\nname='test'\n")
    assert "rust" in detect_languages(str(tmp_path))


def test_detect_yaml(tmp_path):
    (tmp_path / "galaxy.yml").write_text("namespace: test\n")
    assert "yaml" in detect_languages(str(tmp_path))


def test_detect_unknown(tmp_path):
    assert detect_languages(str(tmp_path)) == ["unknown"]


def test_detect_multi(tmp_path):
    (tmp_path / "pyproject.toml").write_text("")
    (tmp_path / "Cargo.toml").write_text("")
    langs = detect_languages(str(tmp_path))
    assert "python" in langs
    assert "rust" in langs


def test_rust_workspace(tmp_path):
    (tmp_path / "Cargo.toml").write_text("[workspace]\nmembers = ['crate-a']\n")
    assert is_rust_workspace(str(tmp_path))


def test_rust_not_workspace(tmp_path):
    (tmp_path / "Cargo.toml").write_text("[package]\nname='test'\n")
    assert not is_rust_workspace(str(tmp_path))
