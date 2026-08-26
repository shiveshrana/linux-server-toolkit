#!/bin/bash

set -u

SUCCESS=0
GENERAL_ERROR=1
INVALID_INPUT=2
PERMISSION_ERROR=3
DEPENDENCY_ERROR=4

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
REPORT_DIR="$PROJECT_DIR/reports"

echo "=========================================="
echo " Linux Server Toolkit - Setup"
echo "=========================================="

# Check operating system
if [[ "$(uname -s)" != "Linux" ]]; then
    echo "ERROR: This toolkit requires Linux."
    exit 4
fi

echo "[1/5] Checking Python..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 is not installed."
    echo "Install Python 3 and run setup again."
    exit 4
fi

PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"

echo "[2/5] Creating required directories..."

mkdir -p "$LOG_DIR"
mkdir -p "$REPORT_DIR"

if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to create directories."
    exit 1
fi

echo "[3/5] Installing Python dependencies..."

if [[ -f "$PROJECT_DIR/requirements.txt" ]]; then

    python3 -m pip install -r "$PROJECT_DIR/requirements.txt"

    if [[ $? -ne 0 ]]; then
        echo "ERROR: Failed to install Python dependencies."
        exit 4
    fi

else
    echo "WARNING: requirements.txt not found."
fi

echo "[4/5] Setting executable permissions..."

find "$PROJECT_DIR" -type f -name "*.sh" -exec chmod +x {} \;

if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to set script permissions."
    exit 1
fi

echo "[5/5] Running basic validation..."

if ! python3 -m py_compile "$PROJECT_DIR/main.py"; then
    echo "ERROR: Python syntax validation failed."
    exit 1
fi

echo
echo "=========================================="
echo " Setup completed successfully!"
echo "=========================================="
echo
echo "Start the toolkit with:"
echo
echo "    python3 main.py"
echo
echo "Or:"
echo
echo "    ./main.py"
echo