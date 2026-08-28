"""The run loop: read the inbox, classify each file, file it away.

``python run.py``            — sort the inbox once
``python run.py --dry-run``  — show the plan, change nothing
``python run.py --watch``    — keep watching the inbox
"""
from __future__ import annotations

import time
from pathlib import Path

from .classify import classify
from .config import Settings
from .extract import extract_preview
from .i18n import t
from .organizer import Organizer
from .telegram_notify import notify

_SKIP_SUFFIXES = {".crdownload", ".part", ".tmp", ".download"}


def _inbox_files(inbox: Path) -> list[Path]:
    if not inbox.exists():
        return []
    files = []
    for p in sorted(inbox.iterdir()):
        if p.is_file() and not p.name.startswith(".") and p.suffix.lower() not in _SKIP_SUFFIXES:
            files.append(p)
    return files


def scan_once(settings: Settings, organizer: Organizer, dry_run: bool = False) -> list[dict]:
    files = _inbox_files(settings.inbox)
    records = []
    for path in files:
        preview = extract_preview(path)
        decision = classify(settings, path, preview)
        rec = organizer.place(path, decision, dry_run=dry_run)
        records.append(rec)
        icon = {"filed": "📁", "review": "🔎", "duplicate": "♻️"}.get(rec["action"], "•")
        arrow = "→ (dry-run) " if dry_run else "→ "
        print(f"  {icon} {Path(rec['src']).name}  {arrow}{Path(rec['dest']).parent.name}/"
              f"{Path(rec['dest']).name}")
    return records


def _summary(settings: Settings, records: list[dict], dry_run: bool) -> str:
    filed = sum(1 for r in records if r["action"] == "filed")
    review = sum(1 for r in records if r["action"] == "review")
    dups = sum(1 for r in records if r["action"] == "duplicate")
    return t("summary", settings.lang, total=len(records), filed=filed, review=review,
             dups=dups, dry=" (dry-run)" if dry_run else "")


def run(dry_run: bool = False, watch: bool = False, interval: int = 30) -> None:
    settings = Settings()
    if not settings.configured:
        raise SystemExit("Not configured yet. Run:  python run.py setup")
    settings.archive.mkdir(parents=True, exist_ok=True)
    settings.inbox.mkdir(parents=True, exist_ok=True)
    organizer = Organizer(settings)

    print(t("run_header", settings.lang, inbox=str(settings.inbox), archive=str(settings.archive),
            engine=_engine_label(settings)))

    def one_pass() -> None:
        records = scan_once(settings, organizer, dry_run=dry_run)
        summary = _summary(settings, records, dry_run)
        if records:
            print(summary)
            if not dry_run:
                notify(settings, summary)
        else:
            print(t("inbox_empty", settings.lang))

    if not watch:
        one_pass()
        return

    print(t("watching", settings.lang, interval=interval))
    while True:
        one_pass()
        time.sleep(interval)


def _engine_label(settings: Settings) -> str:
    if settings.llm_enabled and settings.llm_model:
        return f"{settings.llm_provider}:{settings.llm_model}"
    return "rules-only"
