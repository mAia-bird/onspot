"""Optional one-way Telegram notifications (stdlib only).

If configured, Onspot sends a single short summary DM after a run. Completely
optional — leave it off and everything prints to the console instead.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request


class Telegram:
    def __init__(self, token: str) -> None:
        self.base = f"https://api.telegram.org/bot{token}"

    def _call(self, method: str, params: dict, timeout: int = 20) -> dict:
        data = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}).encode()
        req = urllib.request.Request(f"{self.base}/{method}", data=data)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                payload = json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{method} HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:150]}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"{method} network error: {e.reason}")
        if not payload.get("ok"):
            raise RuntimeError(f"{method}: {payload.get('description')}")
        return payload.get("result")

    def get_me(self) -> dict:
        return self._call("getMe")

    def get_updates(self, offset=None, timeout: int = 0) -> list:
        return self._call("getUpdates", {"offset": offset, "timeout": timeout}, timeout=timeout + 10)

    def send(self, chat_id, text: str) -> dict:
        return self._call("sendMessage", {"chat_id": chat_id, "text": text,
                                          "disable_web_page_preview": "true"})


def notify(settings, text: str) -> None:
    """Best-effort: send a DM if Telegram is configured, else do nothing."""
    if not (settings.notify_telegram and settings.telegram_token and settings.telegram_chat_id):
        return
    try:
        Telegram(settings.telegram_token).send(settings.telegram_chat_id, text)
    except Exception:  # noqa: BLE001 - a failed notification must not fail the run
        pass
