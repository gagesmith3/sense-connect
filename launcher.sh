#!/bin/bash
cd /home/iwt/sense-connect
echo "[LAUNCHER] Starting Sense Connect..."

# Pull latest code
if [ -d .git ]; then
    git pull
fi
echo "[LAUNCHER] Git updated."

# Set TERM for rich/console apps
export TERM=xterm

# Use venv's python directly and log output
VENV_PY="$(pwd)/venv/bin/python"

# Run main.py
$VENV_PY main.py > main.log 2>&1 &
echo "[LAUNCHER] main.py started."

#run dashboard.py
$VENV_PY dashboard.py > dashboard.log 2>&1 &

