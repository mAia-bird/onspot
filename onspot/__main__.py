"""``python -m onspot`` — same behavior as ``python run.py``."""
import json
import sys
from pathlib import Path

from .config import Settings


def _cmd_list_inbox() -> None:
    """Print the inbox files, one path per line (used by the Skill)."""
    from .sorter import _inbox_files
    for p in _inbox_files(Settings().inbox):
        print(p)


def _cmd_place(raw: list[str]) -> None:
    """Safely file ONE already-classified document. The decision (category + name)
    comes from the caller — a person, or Claude running the Skill — while the safe
    move/copy, dedup, and never-overwrite guarantees stay here.

    usage: place <file> --category "01 Taxes" [--name "clean name"] [--dry-run]
    """
    from .organizer import Organizer
    s = Settings()
    if not s.configured:
        raise SystemExit("Not configured. Run:  python3 run.py setup")
    file = category = name = None
    dry = False
    it = iter(raw)
    for a in it:
        if a == "--category":
            category = next(it, None)
        elif a == "--name":
            name = next(it, None)
        elif a == "--dry-run":
            dry = True
        elif not a.startswith("--") and file is None:
            file = a
    if not file:
        raise SystemExit('usage: place <file> --category "NAME" [--name "NAME"] [--dry-run]')
    p = Path(file)
    if not p.is_file():
        raise SystemExit(f"no such file: {file}")
    decision = {"category": category, "filename": name or p.stem, "via": "skill",
                "confidence": 1.0 if category else 0.0}
    rec = Organizer(s).place(p, decision, dry_run=dry)
    print(json.dumps(rec, ensure_ascii=False))


def main() -> None:
    raw = sys.argv[1:]
    cmd = raw[0].lower() if raw else ""

    if cmd in ("list-inbox", "list_inbox"):
        _cmd_list_inbox()
        return
    if cmd == "place":
        _cmd_place(raw[1:])
        return

    args = [a.lower() for a in raw]

    if any(a in ("check", "--check", "doctor") for a in args):
        from .doctor import run_check
        run_check()
        return

    if any(a in ("setup", "--setup", "-s") for a in args):
        from .setup_wizard import main as setup_main
        setup_main()
        return

    if not Settings().configured:
        # First run: nothing configured yet — walk the user through setup.
        from .setup_wizard import main as setup_main
        setup_main()
        return

    dry_run = "--dry-run" in args or "-n" in args
    watch = "--watch" in args or "-w" in args
    interval = 30
    if "--interval" in args:
        try:
            interval = int(args[args.index("--interval") + 1])
        except (ValueError, IndexError):
            pass
    from .sorter import run
    run(dry_run=dry_run, watch=watch, interval=interval)


if __name__ == "__main__":
    main()
