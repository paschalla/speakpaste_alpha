#!/bin/bash

# This script launches Speakpaste reliably.

# First, get the absolute path to the directory where this script is located.
# This makes the script portable, even if you move the project folder.
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# The command to launch the app inside a Konsole window.
# It first changes to the correct directory, then executes the app.
konsole -e sh -c "cd '$SCRIPT_DIR' && '$SCRIPT_DIR/venv/bin/python' main_app.py"