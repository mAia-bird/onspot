"""Self-check: ``python3 run.py check``.

Prints a plain ✓/✗ checklist so anyone — not just a developer — can see at a
glance whether Onspot is set up correctly and what, if anything, is wrong.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from .config import load_config
from .i18n import t


def _line(ok: bool, text: str) -> bool:
    print(f"  {'✓' if ok else '✗'} {text}")
    return ok


def _folder_ok(path: Path) -> tuple[bool, str]:
    try:
        path.mkdir(parents=True, exist_ok=True)
        # Confirm we can actually write here.
        with tempfile.NamedTemporaryFile(dir=path, delete=True):
            pass
        return True, ""
    except OSError as e:
        return False, e.strerror or str(e)


def run_check() -> None:
    cfg = load_config()
    lang = cfg.get("lang", "en")
    print(t("check_title", lang))
    problems = 0

    # Python (we only get here on 3.9+, but show it).
    _line(True, t("c_python", lang, ver=".".join(map(str, sys.version_info[:3]))))

    # Settings present?
    if not cfg:
        _line(False, t("c_config_missing", lang))
        print(t("c_problems", lang))
        return
    _line(True, t("c_config_ok", lang))

    from .config import Settings
    s = Settings()

    ok, err = _folder_ok(s.inbox)
    if not _line(ok, t("c_inbox_ok" if ok else "c_inbox_bad", lang, path=str(s.inbox), err=err)):
        problems += 1
    ok, err = _folder_ok(s.archive)
    if not _line(ok, t("c_archive_ok" if ok else "c_archive_bad", lang, path=str(s.archive), err=err)):
        problems += 1

    _line(True, t("c_cats", lang, n=len(s.categories)))

    # AI model (optional).
    if s.llm_enabled and s.llm_model:
        try:
            from .llm import quick_test
            quick_test(s)
            _line(True, t("c_llm_ok", lang, model=s.llm_model))
        except Exception as e:  # noqa: BLE001
            _line(False, t("c_llm_bad", lang, err=str(e)[:120]))
            problems += 1
    else:
        _line(True, t("c_llm_off", lang))

    # Telegram (optional).
    if s.notify_telegram and s.telegram_token:
        try:
            from .telegram_notify import Telegram
            me = Telegram(s.telegram_token).get_me()
            ok = bool(s.telegram_chat_id)
            if not _line(ok, t("c_tg_ok" if ok else "c_tg_bad", lang,
                               username=me.get("username", "?"), err="no chat id")):
                problems += 1
        except Exception as e:  # noqa: BLE001
            _line(False, t("c_tg_bad", lang, err=str(e)[:120]))
            problems += 1
    else:
        _line(True, t("c_tg_off", lang))

    print(t("c_all_ok" if problems == 0 else "c_problems", lang))
    if problems:
        os.environ["ONSPOT_CHECK_FAILED"] = "1"
