#!/bin/bash

echo "===========================================
    Cargo Hauler - Game Launcher
==========================================="

echo "Activating virtual environment..."
source cargo_hauler_venv/bin/activate

echo "Starting Cargo Hauler..."
python3 src/main.py

echo "Game session ended."