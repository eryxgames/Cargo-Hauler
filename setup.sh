#!/bin/bash

echo "===========================================
    Cargo Hauler - Game Setup Script
==========================================="

# Check Python installation
if ! command -v python3 &> /dev/null
then
    echo "Python not found. Please install Python 3.8+"
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv cargo_hauler_venv

echo "Activating virtual environment..."
source cargo_hauler_venv/bin/activate

echo "Installing required dependencies..."
pip install -r requirements.txt

echo "Verifying installations..."
pip list

echo "Setup complete! Use 'cargo.sh' to start the game."