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

# Launch dashboard.py in tmux session (if not already running)

# Start dashboard in tmux if not running
if ! tmux has-session -t dashboard 2>/dev/null; then
  tmux new-session -d -s dashboard "$VENV_PY dashboard.py > dashboard.log 2>&1"
  echo "[LAUNCHER] Dashboard launched in tmux session."
fi

# Attach to the dashboard tmux session
tmux attach-session -t dashboard