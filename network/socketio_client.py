import socketio
import threading
import time

class SocketIOClient:
    def __init__(self, config):
        self.config = config
        self.sio = socketio.Client()
        self.server_url = getattr(config, 'socketio_server_url', 'http://192.168.1.6:3000')
        self.connected = False
        self._setup_handlers()
        self._connect()

    def _setup_handlers(self):
        @self.sio.event
        def connect():
            self.connected = True
            print("SocketIOClient: Connected to server.")

        @self.sio.event
        def disconnect():
            self.connected = False
            print("SocketIOClient: Disconnected from server.")

        @self.sio.event
        def connect_error(data):
            print(f"SocketIOClient: Connection failed: {data}")

        @self.sio.on('config_update')
        def on_config_update(data):
            print(f"SocketIOClient: Received config update: {data}")
            self.config.update_from_server(data)

    def _connect(self):
        def run():
            while True:
                try:
                    self.sio.connect(self.server_url)
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
        else:
            print("SocketIOClient: Not connected, cannot send count.")
