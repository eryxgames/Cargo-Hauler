@echo off
TITLE Cargo Hauler - Space Trading Adventure

echo ===========================================
echo    Cargo Hauler - Game Launcher
echo ===========================================

echo Activating virtual environment...
call cargo_hauler_venv\Scripts\activate

echo Verifying Python installation...
python --version

REM echo Checking Python executable path...
REM where python

REM echo Listing installed packages...
REM pip list

set PYTHON_EXE=cargo_hauler_venv\Scripts\python.exe
echo Using Python executable: %PYTHON_EXE%

set SCRIPT_PATH=%~dp0src\main.py
echo Running: "%PYTHON_EXE%" "%SCRIPT_PATH%"

"%PYTHON_EXE%" "%SCRIPT_PATH%"

echo Game session ended.
pause