"""``python -m onspot`` — same behavior as ``python run.py``."""
import sys

from .config import Settings


def main() -> None:
    args = [a.lower() for a in sys.argv[1:]]

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
