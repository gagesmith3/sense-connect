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

# Install Python dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Optionally, run main.py after setup
python3 main.py

echo "Setup complete."