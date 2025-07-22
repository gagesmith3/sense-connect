import socketio
import threading
import time
import jwt

class SocketIOClient:
    def __init__(self, config):
        self.config = config
        self.sio = socketio.Client(
            reconnection=True,
            reconnection_attempts=5,
            reconnection_delay=2,
            reconnection_delay_max=10,
            logger=True,
            engineio_logger=True
        )
        self.server_url = getattr(config, 'socketio_server_url', 'http://192.168.1.6:3000')
        self.jwt_secret = getattr(config, 'jwt_token', '2b1e4f8c9d6a7b3e5c1f0a8d7e6b4c2a1f9e8d7c6b5a4e3d2c1b0a9e8d7c6b5')
        self.connected = False
        self.last_connection_error_logged = False
        self.emit_lock = threading.Lock()
        self._setup_handlers()
        self._connect()

    def _setup_handlers(self):
        @self.sio.event
        def connect():
            self.connected = True
            self.last_connection_error_logged = False
            print(f"[SocketIO] Connected to {self.server_url}")
            self.sio.emit('test', {'message': 'Hello from RPi'})
            self.send_header_status('ONLINE')
            self.send_header_update(0)

        @self.sio.event
        def disconnect():
            self.connected = False
            print(f"[SocketIO] Disconnected from {self.server_url}")
            self.send_header_status('OFFLINE')

        @self.sio.event
        def connect_error(data):
            print(f"[SocketIO] Connection error: {data}")
            self.last_connection_error_logged = True

        @self.sio.on('config_update')
        def on_config_update(data):
            print(f"[SocketIO] Received config update: {data}")
            self.config.update_from_server(data)

    def _connect(self):
        def run():
            delay = 2
            while True:
                try:
                    payload = {'machine_id': getattr(self.config, 'machine_id', 'test-machine')}
                    token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
                    print(f"[SocketIO] Attempting connection to {self.server_url} with JWT: {token}")
                    self.sio.connect(
                        self.server_url,
                        auth={'token': token},
                        transports=['websocket'],  # Use only websocket transport
                        wait_timeout=10
                    )
                    print(f"[SocketIO] Connection established.")
                    break
                except Exception as e:
                    print(f"[SocketIO] Connection failed: {e}")
                    time.sleep(delay)
                    delay = min(delay * 2, 30)  # Exponential backoff up to 30s
        threading.Thread(target=run, daemon=True).start()

    def send_header_status(self, status):
        machine_id = int(self.config.machine_id)
        if self.connected:
            try:
                with self.emit_lock:
                    self.sio.emit('header-status', {
                        'machine_id': machine_id,
                        'status': status
                    })
            except Exception as e:
                print(f"[SocketIO] Emit error (header-status): {e}")
        elif not self.last_connection_error_logged:
            self.last_connection_error_logged = True
            print("[SocketIO] Not connected, cannot emit header-status.")

    def send_header_update(self, count, extra_data=None):
        machine_id = int(self.config.machine_id)
        data = {'count': count}
        if extra_data:
            data.update(extra_data)
        if self.connected:
            try:
                with self.emit_lock:
                    self.sio.emit('header-update', {
                        'machine_id': machine_id,
                        'data': data
                    })
            except Exception as e:
                print(f"[SocketIO] Emit error (header-update): {e}")
        elif not self.last_connection_error_logged:
            self.last_connection_error_logged = True
            print("[SocketIO] Not connected, cannot emit header-update.")

    def send_live_count(self, count):
        if self.connected:
            try:
                with self.emit_lock:
                    self.sio.emit('live_count', {'count': count})
                self.send_header_update(count)
            except Exception as e:
                print(f"[SocketIO] Emit error (live_count): {e}")
        elif not self.last_connection_error_logged:
            self.last_connection_error_logged = True
            print("[SocketIO] Not connected, cannot emit live_count.")

    def is_connected(self):
        return self.connected

    def disconnect(self):
        try:
            self.sio.disconnect()
            print("[SocketIO] Manual disconnect called.")
        except Exception as e:
            print(f"[SocketIO] Disconnect error: {e}")