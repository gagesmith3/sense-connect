#!/bin/bash
cd /home/iwt/sense-connect
echo "[LAUNCHER] Starting Sense Connect..."

# Pull latest code
if [ -d .git ]; then
    git pull
fi
echo "[LAUNCHER] Git updated."

# Activate virtual environment
source venv/bin/activate
echo "[LAUNCHER] Virtual environment activated."

# Run main.py
python main.py &
echo "[LAUNCHER] main.py started."

# Launch dashboard.py in tmux session (if not already running)
if ! tmux has-session -t dashboard 2>/dev/null; then
  tmux new-session -d -s dashboard "source venv/bin/activate && python dashboard.py"
fi
echo "[LAUNCHER] Dashboard launched in tmux session."