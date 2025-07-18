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

# Make launcher.sh executable
chmod +x /home/iwt/sense-connect/launcher.sh
# Add cron @reboot job to auto-launch launcher.sh on boot
(crontab -l 2>/dev/null; echo "@reboot /bin/bash /home/iwt/sense-connect/launcher.sh") | crontab -

echo "Setup complete."


# Enable console auto-login for user 'iwt'
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d
sudo tee /etc/systemd/system/getty@tty1.service.d/autologin.conf > /dev/null <<EOL
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin iwt --noclear %I $TERM
EOL
sudo systemctl daemon-reload
sudo systemctl restart getty@tty1

python wrapper.py

