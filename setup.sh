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
pip install requests
pip install rich
pip install -r requirements.txt

#setup systemd service
chmod +x /home/iwt/sense-connect/launcher.sh
# Create systemd service file
sudo tee /etc/systemd/system/sense-connect.service > /dev/null <<EOL
[Unit]
Description=Sense Connect Service
After=network.target
[Service]
ExecStart=/bin/bash /home/iwt/sense-connect/launcher.sh
WorkingDirectory=/home/iwt/sense-connect
Restart=always
User=iwt
Group=iwt
[Install]
WantedBy=multi-user.target
EOL
# Enable and start the service
sudo systemctl enable sense-connect
sudo systemctl start sense-connect

echo "Setup complete."

python wrapper.py

