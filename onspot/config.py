"""Configuration: taxonomy + behavior in ``config.json``, secrets in ``.env``.

Standard library only. ``config.json`` is safe to keep in the repo (it holds no
secrets — just your folders and categories). ``.env`` holds the LLM API key and
optional Telegram token and is git-ignored.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.json"
ENV_PATH = ROOT / ".env"


# --- .env (secrets) --------------------------------------------------------
def load_env(path: Path = ENV_PATH) -> dict:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        data[key.strip()] = value
        os.environ.setdefault(key.strip(), value)
    return data


def write_env(values: dict, path: Path = ENV_PATH) -> None:
    lines = ["# Onspot secrets — never commit this file (it is in .gitignore).", ""]
    for key, value in values.items():
        if value:
            lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


# --- config.json (taxonomy + behavior) -------------------------------------
def load_config(path: Path = CONFIG_PATH) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_config(cfg: dict, path: Path = CONFIG_PATH) -> None:
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class Settings:
    """A read-only snapshot: config.json merged with .env secrets."""

    def __init__(self) -> None:
        load_env()
        c = load_config()
        self.raw = c
        self.lang = c.get("lang", "en")
        self.inbox = Path(os.path.expanduser(c.get("inbox", "inbox")))
        self.archive = Path(os.path.expanduser(c.get("archive", "archive")))
        self.mode = c.get("mode", "move")  # "move" | "copy"
        self.min_confidence = float(c.get("min_confidence", 0.6))
        self.duplicates_dir = c.get("duplicates_dir", "_Duplicates")
        self.review_dir = c.get("review_dir", "_Review")
        self.categories = c.get("categories", [])
        self.notify_telegram = bool(c.get("notify_telegram", False))

        # Secrets / LLM from environment.
        self.llm_enabled = os.environ.get("LLM_ENABLED", "").lower() in ("1", "true", "yes")
        self.llm_provider = os.environ.get("LLM_PROVIDER", "openai")
        self.llm_base = os.environ.get("LLM_API_BASE", "https://api.openai.com/v1")
        self.llm_key = os.environ.get("LLM_API_KEY", "")
        self.llm_model = os.environ.get("LLM_MODEL", "")
        self.llm_vision = os.environ.get("LLM_VISION", "").lower() in ("1", "true", "yes")
        self.telegram_token = os.environ.get("TELEGRAM_TOKEN", "")
        self.telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    @property
    def configured(self) -> bool:
        return bool(self.raw) and self.inbox and self.archive

    def category_names(self) -> list[str]:
        return [c["name"] for c in self.categories if c.get("name")]
