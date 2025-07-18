#!/bin/bash
cd /home/pi/sense-connect

# Pull latest code
if [ -d .git ]; then
    git pull
fi

# Activate virtual environment
source venv/bin/activate

# Launch wrapper (which launches main.py)
python wrapper.py