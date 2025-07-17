#!/bin/bash
# sense-connect setup script for Raspberry Pi

set -e

# Update system packages
sudo apt update
sudo apt install -y git python3 python3-pip libpq-dev

# Navigate to project directory (edit path if needed)
cd "$(dirname "$0")"

# Check for code updates from git repo
def update_code():
    try:
        result = subprocess.run(["git", "pull"], cwd=os.path.dirname(__file__), capture_output=True, text=True)
        print(f"Code update: {result.stdout}")
    except Exception as e:
        print(f"Code update failed: {e}")

update_code()

# Install Python dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Optionally, run main.py after setup
python3 main.py

echo "Setup complete."
