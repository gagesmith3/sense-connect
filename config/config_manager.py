import json
import os

class ConfigManager:
    def __init__(self, config_path='config/config.json'):
        self.config_path = config_path
        self.sensor_pin = 17
        self.backup_increment = 1
        self.socketio_server_url = 'http://localhost:3000'
        self.sensor_poll_interval = 1
        self.config_update_interval = 60
        self.db_host = 'localhost'
        self.db_user = 'user'
        self.db_password = 'password'
        self.db_name = 'database'
        self.machine_id = 'default-machine'
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                self.sensor_pin = data.get('sensor_pin', self.sensor_pin)
                self.backup_increment = data.get('backup_increment', self.backup_increment)
                self.socketio_server_url = data.get('socketio_server_url', self.socketio_server_url)
                self.sensor_poll_interval = data.get('sensor_poll_interval', self.sensor_poll_interval)
                self.config_update_interval = data.get('config_update_interval', self.config_update_interval)
                self.db_host = data.get('db_host', self.db_host)
                self.db_user = data.get('db_user', self.db_user)
                self.db_password = data.get('db_password', self.db_password)
                self.db_name = data.get('db_name', self.db_name)
                self.machine_id = data.get('machine_id', self.machine_id)

    def update_from_server(self, new_config=None):
        # This method can be called by Socket.IO event or HTTP request
        if new_config:
            self.sensor_pin = new_config.get('sensor_pin', self.sensor_pin)
            self.backup_increment = new_config.get('backup_increment', self.backup_increment)
            self.socketio_server_url = new_config.get('socketio_server_url', self.socketio_server_url)
            self.sensor_poll_interval = new_config.get('sensor_poll_interval', self.sensor_poll_interval)
            self.config_update_interval = new_config.get('config_update_interval', self.config_update_interval)
            self.db_host = new_config.get('db_host', self.db_host)
            self.db_user = new_config.get('db_user', self.db_user)
            self.db_password = new_config.get('db_password', self.db_password)
            self.db_name = new_config.get('db_name', self.db_name)
            self.machine_id = new_config.get('machine_id', self.machine_id)
            self.save()
            print('ConfigManager: Config updated from server.')

    def save(self):
        data = {
            'sensor_pin': self.sensor_pin,
            'backup_increment': self.backup_increment,
            'socketio_server_url': self.socketio_server_url,
            'sensor_poll_interval': self.sensor_poll_interval,
            'config_update_interval': self.config_update_interval,
            'db_host': self.db_host,
            'db_user': self.db_user,
            'db_password': self.db_password,
            'db_name': self.db_name,
            'machine_id': self.machine_id
        }
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=2)
