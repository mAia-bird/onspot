#!/bin/bash
# Double-click this on macOS to run Onspot — no terminal knowledge needed.
# It finds Python 3 for you and gives a clear message if it's missing.
cd "$(dirname "$0")" || exit 1

if command -v python3 >/dev/null 2>&1; then
  python3 run.py "$@"
else
  echo ""
  echo "  Python 3 is not installed yet."
  echo "  Python 3 ещё не установлен."
  echo ""
  echo "  Install it from:  https://www.python.org/downloads/"
  echo "  Поставь его отсюда: https://www.python.org/downloads/"
  echo "  Then double-click this file again."
  echo ""
fi

echo ""
read -n 1 -s -r -p "Press any key to close this window. (Нажми любую клавишу, чтобы закрыть.)"
echo ""
