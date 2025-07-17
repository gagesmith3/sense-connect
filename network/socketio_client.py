import socketio
import threading
import time
import jwt

class SocketIOClient:
    def send_header_status(self, status):
        if self.connected:
            try:
                self.sio.emit('header-status', {
                    'machine_id': self.config.machine_id,
                    'status': status
                })
                print(f"SocketIOClient: Sent header-status: {status}")
            except Exception as e:
                print(f"SocketIOClient: Emit error (header-status): {e}")
        elif not self.last_connection_error_logged:
            print("SocketIOClient: Not connected, cannot send header-status.")
            self.last_connection_error_logged = True

    def send_header_update(self, data):
        if self.connected:
            try:
                self.sio.emit('header-update', {
                    'machine_id': self.config.machine_id,
                    'data': data
                })
                print(f"SocketIOClient: Sent header-update: {data}")
            except Exception as e:
                print(f"SocketIOClient: Emit error (header-update): {e}")
        elif not self.last_connection_error_logged:
            print("SocketIOClient: Not connected, cannot send header-update.")
            self.last_connection_error_logged = True
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
            print("SocketIOClient: Connected to server.")
            self.sio.emit('test', {'message': 'Hello from RPi'})

        @self.sio.event
        def disconnect():
            self.connected = False
            print("SocketIOClient: Disconnected from server.")

        @self.sio.event
        def connect_error(data):
            if not self.last_connection_error_logged:
                print(f"SocketIOClient: Connection failed: {data}")
                self.last_connection_error_logged = True

        @self.sio.on('config_update')
        def on_config_update(data):
            print(f"SocketIOClient: Received config update: {data}")
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
                    print(f"SocketIOClient: Connection error, retrying in 5s. Error: {e}")
                    time.sleep(5)
        threading.Thread(target=run, daemon=True).start()

    def send_live_count(self, count):
        if self.connected:
            try:
                self.sio.emit('live_count', {'count': count})
                print(f"SocketIOClient: Sent live count {count}")
            except Exception as e:
                print(f"SocketIOClient: Emit error: {e}")
        # Only log not connected once per disconnect
        elif not self.last_connection_error_logged:
            print("SocketIOClient: Not connected, cannot send count.")
            self.last_connection_error_logged = True
