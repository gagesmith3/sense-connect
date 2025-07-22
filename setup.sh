#!/bin/bash
# sense-connect setup script for Raspberry Pi

#set -e

# Update system packages
sudo apt update
sudo apt install -y git python3 python3-pip libpq-dev
# Install tmux for session management
sudo apt install -y tmux

# Navigate to project directory (edit path if needed)
cd "$(dirname "$0")"

# Pull latest code from GitHub
if [ -d .git ]; then
    git pull
fi

### Create Python virtual environment if not exists
if [ ! -d venv ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install Python dependencies in the virtual environment
echo "[SETUP] Upgrading pip..."
pip install --upgrade pip && echo "[SETUP] pip upgraded."
echo "[SETUP] Installing python-socketio..."
pip install python-socketio==5.11.2 && echo "[SETUP] python-socketio installed."
echo "[SETUP] Installing PyJWT..."
pip install PyJWT && echo "[SETUP] PyJWT installed."
echo "[SETUP] Installing requests..."
pip install requests && echo "[SETUP] requests installed."
echo "[SETUP] Installing rich..."
pip install rich && echo "[SETUP] rich installed."
echo "[SETUP] Installing RPi.GPIO..."
pip install RPi.GPIO && echo "[SETUP] RPi.GPIO installed."
echo "[SETUP] Installing python-socketio (again, if needed)..."
pip install python-socketio==5.11.2 && echo "[SETUP] python-socketio (again) installed."
echo "[SETUP] Installing psycopg2..."
pip install psycopg2 && echo "[SETUP] psycopg2 installed."
echo "[SETUP] Installing schedule..."
pip install schedule && echo "[SETUP] schedule installed."

echo "[SETUP] All Python dependencies installed."

# Ensure log files exist and are writable
touch /home/iwt/sense-connect/main.log
touch /home/iwt/sense-connect/dashboard.log
chmod 664 /home/iwt/sense-connect/main.log /home/iwt/sense-connect/dashboard.log
chown $(whoami):$(whoami) /home/iwt/sense-connect/main.log /home/iwt/sense-connect/dashboard.log
echo "[SETUP] Log files main.log and dashboard.log created and permissions set."


### Make launcher.sh executable (use absolute path)
chmod +x /home/iwt/sense-connect/launcher.sh

# Add auto-launch dashboard for SSH users in .bash_profile
USER_HOME=$(eval echo ~$USER)
DASHBOARD_LAUNCH="\n# Auto-run dashboard on SSH login (only for interactive shells)\nif [ -n \"\$SSH_CONNECTION\" ] && [ -t 1 ]; then\n    source /home/iwt/sense-connect/venv/bin/activate\n    python /home/iwt/sense-connect/dashboard.py\nfi\n"
if ! grep -q 'Auto-run dashboard on SSH login' "$USER_HOME/.bash_profile" 2>/dev/null; then
    echo -e "$DASHBOARD_LAUNCH" >> "$USER_HOME/.bash_profile"
    echo "[SETUP] Added dashboard auto-launch to .bash_profile."
else
    echo "[SETUP] Dashboard auto-launch already present in .bash_profile."
fi


# Add cron @reboot job to auto-launch launcher.sh on boot
# Remove any previous @reboot jobs for launcher.sh
crontab -l 2>/dev/null | grep -v 'launcher.sh' > tempcron
# Add launcher.sh to run on boot via cron
echo "@reboot /bin/bash /home/iwt/sense-connect/launcher.sh" >> tempcron
crontab tempcron
rm tempcron
echo "[SETUP] Cron job added to run launcher.sh on boot."


### Enable console auto-login for user 'iwt'
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d
sudo tee /etc/systemd/system/getty@tty1.service.d/autologin.conf > /dev/null <<EOL
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin iwt --noclear %I $TERM
EOL
sudo systemctl daemon-reload
sudo systemctl restart getty@tty1

echo "[SETUP] Setup complete."