@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] Creating virtual environment...
    py -m venv .venv
)

echo [SETUP] Installing dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [RUN] Launching SIGNAL_LOSS...
".venv\Scripts\python.exe" visuals.py

endlocal
