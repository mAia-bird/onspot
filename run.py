#!/usr/bin/env python3
"""Onspot launcher.

    python run.py             # first time: runs setup; afterwards: sorts the inbox once
    python run.py --dry-run   # show what would happen, change nothing (safe preview)
    python run.py --watch     # keep watching the inbox (optional: --interval 30)
    python run.py setup       # force the setup wizard
    python run.py --help      # this message

Requires Python 3.9+ and nothing else — only the standard library.
"""
import sys

if sys.version_info < (3, 9):
    sys.exit("Onspot needs Python 3.9 or newer.")


def main() -> None:
    if any(a in ("-h", "--help", "help") for a in sys.argv[1:]):
        print(__doc__)
        return
    from onspot.__main__ import main as entry
    entry()


if __name__ == "__main__":
    main()
