#!/bin/bash

# validate.sh - Silent system check for dirty-vm runnables
# Runs check/main.py with suppressed output.
# On failure, advises the user to run 'dirty-vm check' for full details.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! python3 "$SCRIPT_DIR/main.py" > /dev/null 2>&1; then
    echo "System check failed. Run 'dirty-vm check' for details."
    exit 1
fi
