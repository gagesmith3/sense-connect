#!/bin/bash
# sense-connect setup script for Raspberry Pi

set -e

# Update system packages
sudo apt update
sudo apt install -y git python3 python3-pip libpq-dev

# Navigate to project directory (edit path if needed)
cd "$(dirname "$0")"

# Pull latest code from GitHub
if [ -d .git ]; then
    git pull
fi


# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies in the virtual environment
pip install --upgrade pip
pip install python-socketio==5.11.2
pip install PyJWT
pip install -r requirements.txt

# Optionally, run main.py after setup (in the virtual environment)
python main.py

echo "Setup complete."