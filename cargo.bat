@echo off
TITLE Cargo Hauler - Space Trading Adventure

echo ===========================================
echo    Cargo Hauler - Game Launcher
echo ===========================================

echo Activating virtual environment...
call cargo_hauler_venv\Scripts\activate

echo Starting Cargo Hauler...
python src\main.py

echo Game session ended.
pause