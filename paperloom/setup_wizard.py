"""Interactive first-run setup for Paperloom.

Walks the user through: language, inbox/archive folders, move-vs-copy, a category
taxonomy (from a template), which AI to connect (local / API / Anthropic / none),
and optional Telegram notifications. Writes ``config.json`` + ``.env``.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from .config import CONFIG_PATH, ENV_PATH, write_config, write_env
from .i18n import t

# --- taxonomy templates (folder names are in the chosen language) -----------
_TEMPLATES = {
    "en": [
        {"name": "01 Taxes", "description": "Tax returns and letters from the tax office",
         "rules": {"text_any": ["tax", "finanzamt", "steuer", "hmrc", "irs"]}},
        {"name": "02 Bank", "description": "Bank statements, cards, loans",
         "rules": {"text_any": ["bank", "iban", "statement", "kontoauszug"]}},
        {"name": "03 Insurance", "description": "Insurance policies and claims",
         "rules": {"text_any": ["insurance", "policy", "versicherung"]}},
        {"name": "04 Housing", "description": "Rent, mortgage, utilities, address",
         "rules": {"text_any": ["rent", "lease", "mortgage", "utility", "miete"]}},
        {"name": "05 IDs & Personal", "description": "Passports, ID cards, certificates",
         "rules": {"filename_any": ["passport", "id"], "text_any": ["passport", "id card"]}},
        {"name": "06 Contracts", "description": "Signed contracts and agreements",
         "rules": {"text_any": ["contract", "agreement", "vertrag"]}},
        {"name": "07 Medical", "description": "Doctors, prescriptions, clinics",
         "rules": {"text_any": ["medical", "doctor", "prescription", "clinic"]}},
        {"name": "08 Invoices & Receipts", "description": "Invoices, receipts, bills",
         "rules": {"text_any": ["invoice", "receipt", "rechnung"]}},
        {"name": "09 Archive", "description": "Older documents that don't fit above", "rules": {}},
    ],
    "ru": [
        {"name": "01 Налоги", "description": "Налоговые декларации и письма из налоговой",
         "rules": {"text_any": ["налог", "фнс", "steuer", "finanzamt", "tax"]}},
        {"name": "02 Банк", "description": "Выписки, карты, кредиты",
         "rules": {"text_any": ["банк", "iban", "выписка", "счёт", "bank"]}},
        {"name": "03 Страховки", "description": "Полисы и страховые случаи",
         "rules": {"text_any": ["страхов", "полис", "versicherung", "insurance"]}},
        {"name": "04 Жильё", "description": "Аренда, ипотека, коммуналка, адрес",
         "rules": {"text_any": ["аренда", "квартир", "ипотек", "miete", "rent"]}},
        {"name": "05 Документы и личное", "description": "Паспорта, удостоверения, свидетельства",
         "rules": {"filename_any": ["passport", "паспорт"], "text_any": ["паспорт", "удостоверение"]}},
        {"name": "06 Договоры", "description": "Подписанные договоры и соглашения",
         "rules": {"text_any": ["договор", "соглашение", "vertrag", "contract"]}},
        {"name": "07 Медицина", "description": "Врачи, рецепты, клиники",
         "rules": {"text_any": ["медиц", "врач", "рецепт", "клиник"]}},
        {"name": "08 Счета и чеки", "description": "Счета, чеки, квитанции",
         "rules": {"text_any": ["счёт", "чек", "квитанц", "invoice", "rechnung"]}},
        {"name": "09 Архив", "description": "Старые документы, не попавшие выше", "rules": {}},
    ],
}
_MINIMAL = {
    "en": [{"name": "Documents", "description": "Everything", "rules": {}},
           {"name": "Archive", "description": "Older stuff", "rules": {}}],
    "ru": [{"name": "Документы", "description": "Всё подряд", "rules": {}},
           {"name": "Архив", "description": "Старое", "rules": {}}],
}


def _ask(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except EOFError:
        raise KeyboardInterrupt


def _choose_language() -> str:
    while True:
        ans = _ask(t("choose_lang")).lower()
        if ans in ("1", "en", "english", ""):
            return "en"
        if ans in ("2", "ru", "russian", "русский"):
            return "ru"


def _setup_folders(lang: str) -> dict:
    print(t("folders_intro", lang))
    inbox = _ask(t("prompt_inbox", lang)) or "inbox"
    archive = _ask(t("prompt_archive", lang)) or "archive"
    mode = _ask(t("prompt_mode", lang)).lower()
    mode = "copy" if mode == "copy" else "move"
    return {"inbox": inbox, "archive": archive, "mode": mode}


def _setup_taxonomy(lang: str) -> list:
    print(t("taxonomy_intro", lang))
    choice = _ask(t("taxonomy_choose", lang))
    cats = _MINIMAL[lang] if choice == "2" else _TEMPLATES[lang]
    print(t("taxonomy_saved", lang, n=len(cats)))
    return cats


def _setup_llm(lang: str) -> dict:
    print(t("llm_intro", lang))
    choice = _ask(t("llm_choose", lang)) or "1"
    if choice == "4":
        print(t("llm_none", lang))
        return {}

    if choice == "3":  # Anthropic
        provider, default_base, example = "anthropic", "https://api.anthropic.com", "claude-haiku-4-5"
    elif choice == "2":  # OpenAI-compatible API
        provider, default_base, example = "openai", "https://api.openai.com/v1", "gpt-4o-mini"
    else:  # Local
        provider, default_base, example = "openai", "http://localhost:11434/v1", "llama3.1"

    base = _ask(t("llm_base", lang, default=default_base)) or default_base
    key = _ask(t("llm_key", lang))
    model = _ask(t("llm_model", lang, example=example))
    vision = _ask(t("llm_vision", lang)).lower() in ("y", "yes", "д", "да")

    env = {"LLM_ENABLED": "true", "LLM_PROVIDER": provider, "LLM_API_BASE": base,
           "LLM_API_KEY": key, "LLM_MODEL": model, "LLM_VISION": "true" if vision else "false"}

    # Try a quick connectivity test (non-fatal).
    print(t("llm_testing", lang))
    try:
        for k, v in env.items():
            os.environ[k] = v
        from .config import Settings
        from .llm import quick_test
        quick_test(Settings())
        print(t("llm_ok", lang))
    except Exception as e:  # noqa: BLE001
        print(t("llm_fail", lang, err=str(e)[:160]))
    return env


def _setup_notify(lang: str) -> tuple[dict, bool]:
    print(t("notify_intro", lang))
    if _ask(t("notify_enable", lang)).lower() not in ("y", "yes", "д", "да"):
        print(t("notify_skip", lang))
        return {}, False
    from .telegram_notify import Telegram
    token = _ask(t("notify_token", lang))
    if not token:
        print(t("notify_skip", lang))
        return {}, False
    tg = Telegram(token)
    try:
        me = tg.get_me()
    except Exception as e:  # noqa: BLE001
        print(t("notify_skip", lang))
        return {}, False
    username = me.get("username", "your_bot")
    print("  " + t("notify_capture", lang, username=username))
    try:
        backlog = tg.get_updates(offset=-1, timeout=0)
    except Exception:  # noqa: BLE001
        backlog = []
    offset = (backlog[-1]["update_id"] + 1) if backlog else None
    deadline = time.time() + 90
    while time.time() < deadline:
        try:
            updates = tg.get_updates(offset=offset, timeout=0)
        except Exception:  # noqa: BLE001
            updates = []
        for upd in updates:
            offset = upd["update_id"] + 1
            sender = upd.get("message", {}).get("from")
            if sender and not sender.get("is_bot"):
                chat = str(sender["id"])
                print(t("notify_ok", lang, name=sender.get("first_name", "you"), chat=chat))
                return {"TELEGRAM_TOKEN": token, "TELEGRAM_CHAT_ID": chat}, True
        time.sleep(2)
    print(t("notify_skip", lang))
    return {}, False


def run() -> None:
    print(t("banner"))
    lang = _choose_language()
    print(t("intro", lang))

    folders = _setup_folders(lang)
    categories = _setup_taxonomy(lang)
    llm_env = _setup_llm(lang)
    notify_env, notify_on = _setup_notify(lang)

    config = {
        "lang": lang,
        "inbox": folders["inbox"],
        "archive": folders["archive"],
        "mode": folders["mode"],
        "min_confidence": 0.6,
        "duplicates_dir": "_Duplicates",
        "review_dir": "_Review",
        "notify_telegram": notify_on,
        "categories": categories,
    }
    write_config(config)
    write_env({**llm_env, **notify_env})

    print(t("done", lang, config=str(CONFIG_PATH), env=str(ENV_PATH),
            inbox=str(Path(os.path.expanduser(folders["inbox"])))))


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        print("\n\n(cancelled — re-run any time with:  python run.py setup)")
        sys.exit(1)
