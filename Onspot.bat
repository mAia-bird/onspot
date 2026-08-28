@echo off
REM Double-click this on Windows to run Onspot — no terminal knowledge needed.
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
    python run.py %*
    goto :end
)
where py >nul 2>nul
if %errorlevel%==0 (
    py run.py %*
    goto :end
)

echo.
echo   Python 3 is not installed yet.
echo   Python 3 eshche ne ustanovlen.
echo.
echo   Install it from:  https://www.python.org/downloads/
echo   (During install, tick "Add Python to PATH".)
echo   Then double-click this file again.
echo.

:end
pause
