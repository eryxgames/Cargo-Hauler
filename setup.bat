@echo off
TITLE Cargo Hauler Game Setup

echo ===========================================
echo    Cargo Hauler - Game Setup Script
echo ===========================================

echo Checking for Python installation...
python --version
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b
)

echo Creating virtual environment...
python -m venv cargo_hauler_venv

echo Activating virtual environment...
call cargo_hauler_venv\Scripts\activate

echo Installing required dependencies...
pip install -r requirements.txt

echo Verifying installations...
pip list

echo Setup complete! Use 'cargo.bat' to start the game.
pause