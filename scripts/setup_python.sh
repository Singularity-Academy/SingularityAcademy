#!/bin/bash

# Try to find Python 3 in the following order:
# 1. python3 command
# 2. python command (if it's Python 3)
# If no Python 3 is found, abort with error

if command -v python3 >/dev/null 2>&1; then
    PYTHON=$(command -v python3)
elif command -v python >/dev/null 2>&1; then
    # Check if 'python' is Python 3
    version=$(python -c 'import sys; print(sys.version_info[0])' 2>/dev/null)
    if [ "$version" = "3" ]; then
        PYTHON=$(command -v python)
    else
        echo "Error: Found Python but it's not Python 3" >&2
        exit 1
    fi
else
    echo "Error: No Python interpreter found in PATH" >&2
    exit 1
fi

# Export the variable so it's available to child processes
export PYTHON

# Print the Python path for verification
echo "Using Python interpreter: $PYTHON"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment" >&2
        exit 1
    fi
    echo "Virtual environment created successfully"
else
    echo "Virtual environment already exists"
fi

# Activate the virtual environment
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment" >&2
    exit 1
fi
echo "Virtual environment activated successfully"

echo "Installing dependencies..."

pip3 install -r requirements.txt

echo "Installation complete"