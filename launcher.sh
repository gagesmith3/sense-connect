#!/bin/bash
cd /home/iwt/sense-connect

# Pull latest code
if [ -d .git ]; then
    git pull
fi

# Activate virtual environment
source venv/bin/activate

# Launch main.py
python main.py

sleep 10

python dashboard.py