"""Auto-detect project language from marker files."""

from __future__ import annotations

from pathlib import Path


def detect_languages(path: str = ".") -> list[str]:
    """Detect project languages by looking for marker files."""
    p = Path(path)
    langs = []
    # Python
    if any((p / f).exists() for f in ("pyproject.toml", "setup.py", "setup.cfg", "requirements.txt")):
        langs.append("python")
    elif list(p.glob("*.py")):
        langs.append("python")
    # Rust
    if (p / "Cargo.toml").exists():
        langs.append("rust")
    # YAML/Ansible
    if any((p / f).exists() for f in ("galaxy.yml", "galaxy.yaml", "ansible.cfg")):
        langs.append("yaml")
    elif (p / "roles").is_dir() or (p / "playbooks").is_dir():
        langs.append("yaml")
    return langs or ["unknown"]


def is_rust_workspace(path: str = ".") -> bool:
    """Check if the Rust project is a Cargo workspace."""
    cargo = Path(path) / "Cargo.toml"
    if not cargo.exists():
        return False
    content = cargo.read_text()
    return "[workspace]" in content


def load_config(path: str = ".") -> dict:
    """Load .dev-agents.toml if exists, otherwise auto-detect."""
    config_file = Path(path) / ".dev-agents.toml"
    if config_file.exists():
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        return tomllib.loads(config_file.read_text())
    return {"project": {"languages": detect_languages(path)}}
