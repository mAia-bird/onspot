#!/usr/bin/env python3
"""Onspot launcher.

    python3 run.py             # first time: runs setup; afterwards: sorts the inbox once
    python3 run.py --dry-run   # show what would happen, change nothing (safe preview)
    python3 run.py --watch     # keep watching the inbox (optional: --interval 30)
    python3 run.py check       # self-check: is everything set up correctly?
    python3 run.py setup       # force the setup wizard
    python3 run.py --help      # this message

(On Windows use `python` instead of `python3`. Prefer double-clicking
Onspot.command on macOS or Onspot.bat on Windows — no terminal needed.)

Requires Python 3.9+ and nothing else — only the standard library.
"""
import sys

if sys.version_info < (3, 9):
    sys.exit("Onspot needs Python 3.9 or newer. Install it from https://www.python.org/downloads/")


def main() -> None:
    argv = sys.argv[1:]
    if any(a in ("-h", "--help", "help") for a in argv):
        print(__doc__)
        return
    debug = "--debug" in argv
    try:
        from onspot.__main__ import main as entry
        entry()
    except KeyboardInterrupt:
        print("\n(stopped)")
        sys.exit(130)
    except SystemExit:
        raise  # clean, intentional exits (e.g. "not configured") pass through
    except Exception as err:  # noqa: BLE001 - turn any crash into a friendly message
        if debug:
            raise
        try:
            from onspot.config import load_config
            from onspot.i18n import t
            lang = load_config().get("lang", "en")
            print(t("crash", lang, err=err))
        except Exception:  # noqa: BLE001 - never let the error handler itself crash
            print(f"\n❌ Something went wrong: {err}\n"
                  "   Report it at https://github.com/mAia-bird/onspot/issues "
                  "(run again with --debug for details).")
        sys.exit(1)


if __name__ == "__main__":
    main()
