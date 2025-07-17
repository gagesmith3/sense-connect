# sense-connect main entry point
import time
import threading
from sensor.sensor import SensorManager
from network.socketio_client import SocketIOClient
from config.config_manager import ConfigManager
from network.alert import AlertManager
from storage.database_manager import DatabaseManager
import subprocess
import json
import os


# Check for code updates from git repo
def update_code():
    try:
        result = subprocess.run(["git", "pull"], cwd=os.path.dirname(__file__), capture_output=True, text=True)
        print(f"Code update: {result.stdout}")
    except Exception as e:
        print(f"Code update failed: {e}")

update_code()

# Initialize config
config = ConfigManager()
config.load()

# Initialize sensor manager
sensor = SensorManager(config)

# Initialize Socket.IO client
socket_client = SocketIOClient(config)

# Initialize alert manager
alert_manager = AlertManager(config)

# Initialize database manager
db_manager = DatabaseManager(config)

# Local cache for hard counts
HARD_COUNT_CACHE = 'hard_count_cache.json'
def cache_hard_count(machine_id, count, timestamp):
    cache = []
    if os.path.exists(HARD_COUNT_CACHE):
        with open(HARD_COUNT_CACHE, 'r') as f:
            cache = json.load(f)
    cache.append({'machine_id': machine_id, 'count': count, 'timestamp': timestamp})
    with open(HARD_COUNT_CACHE, 'w') as f:
        json.dump(cache, f)

def flush_hard_count_cache():
    if os.path.exists(HARD_COUNT_CACHE):
        with open(HARD_COUNT_CACHE, 'r') as f:
            cache = json.load(f)
        for entry in cache:
            db_manager.insert_sensor_data(entry['machine_id'], entry['count'], entry['timestamp'])
        os.remove(HARD_COUNT_CACHE)


def sensor_loop():
    while True:
        sensor.update_count()
        socket_client.send_live_count(sensor.count)
        if not sensor.is_active():
            alert_manager.send_downtime_alert()
        time.sleep(config.sensor_poll_interval)


def config_update_loop():
    while True:
        config.update_from_server()
        time.sleep(config.config_update_interval)

def hard_count_loop():
    while True:
        try:
            db_manager.insert_sensor_data(config.machine_id, sensor.count)
            flush_hard_count_cache()
        except Exception as e:
            print(f"Hard count upload failed, caching locally: {e}")
            cache_hard_count(config.machine_id, sensor.count, int(time.time()))
        sensor.reset_count()
        time.sleep(60)

def health_report_loop():
    while True:
        # Stub: send health/status info to server
        # Example: socket_client.sio.emit('health_report', {...})
        time.sleep(300)


if __name__ == "__main__":
    # Flush any cached hard counts on startup
    flush_hard_count_cache()
    # Start sensor loop in a thread
    threading.Thread(target=sensor_loop, daemon=True).start()
    # Start config update loop in a thread
    threading.Thread(target=config_update_loop, daemon=True).start()
    # Start hard count upload loop in a thread
    threading.Thread(target=hard_count_loop, daemon=True).start()
    # Start health report loop in a thread
    threading.Thread(target=health_report_loop, daemon=True).start()
    # Keep main thread alive
    while True:
        time.sleep(60)
