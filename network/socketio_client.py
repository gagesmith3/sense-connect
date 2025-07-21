import socketio
import threading
import time
import jwt

class SocketIOClient:
    def send_header_status(self, status):
        machine_id = int(self.config.machine_id)
        if self.connected:
            try:
                self.sio.emit('header-status', {
                    'machine_id': machine_id,
                    'status': status
                })
            except Exception as e:
                pass
        elif not self.last_connection_error_logged:
            self.last_connection_error_logged = True
            pass

    def send_header_update(self, count, extra_data=None):
        machine_id = int(self.config.machine_id)
        data = {'count': count}
        if extra_data:
            data.update(extra_data)
        if self.connected:
            try:
                self.sio.emit('header-update', {
                    'machine_id': machine_id,
                    'data': data
                })
            except Exception as e:
                pass
        elif not self.last_connection_error_logged:
            self.last_connection_error_logged = True
            pass
    def __init__(self, config):
        self.config = config
        self.sio = socketio.Client()
        self.server_url = getattr(config, 'socketio_server_url', 'http://192.168.1.6:3000')
        self.jwt_secret = getattr(config, 'jwt_token', '2b1e4f8c9d6a7b3e5c1f0a8d7e6b4c2a1f9e8d7c6b5a4e3d2c1b0a9e8d7c6b5')
        self.connected = False
        self.last_connection_error_logged = False
        self._setup_handlers()
        self._connect()

    def _setup_handlers(self):
        @self.sio.event
        def connect():
            self.connected = True
            self.last_connection_error_logged = False
            self.sio.emit('test', {'message': 'Hello from RPi'})
            self.send_header_status('ONLINE')
            self.send_header_update(0)

        @self.sio.event
        def disconnect():
            self.connected = False
            self.send_header_status('OFFLINE')

        @self.sio.event
        def connect_error(data):
            if not self.last_connection_error_logged:
                self.last_connection_error_logged = True

        @self.sio.on('config_update')
        def on_config_update(data):
            self.config.update_from_server(data)

    def _connect(self):
        def run():
            while True:
                try:
                    payload = {'machine_id': getattr(self.config, 'machine_id', 'test-machine')}
                    token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
                    self.sio.connect(self.server_url, auth={'token': token})
                    break
                except Exception as e:
                    pass
                    time.sleep(5)
        threading.Thread(target=run, daemon=True).start()

    def send_live_count(self, count):
        if self.connected:
            try:
                self.sio.emit('live_count', {'count': count})
                self.send_header_update(count)
            except Exception as e:
                pass
        elif not self.last_connection_error_logged:
            self.last_connection_error_logged = True
            pass
    def is_connected(self):
        return self.connected