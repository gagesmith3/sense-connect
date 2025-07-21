#!/bin/bash
cd /home/iwt/sense-connect

# Pull latest code
if [ -d .git ]; then
    git pull
fi

# Activate virtual environment
source venv/bin/activate

# Run main.py
python main.py &

# Launch dashboard.py in tmux session (if not already running)
if ! tmux has-session -t dashboard 2>/dev/null; then
  tmux new-session -d -s dashboard "source venv/bin/activate && python dashboard.py"
fi