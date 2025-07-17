import psycopg2
import time

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self._connect()

    def _connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.config.db_host,
                port=5432,
                user=self.config.db_user,
                password=self.config.db_password,
                dbname=self.config.db_name
            )
            print("DatabaseManager: Connected to PostgreSQL server.")
        except Exception as e:
            print(f"DatabaseManager: Connection failed: {e}")
            self.conn = None

    def insert_sensor_data(self, machine_id, count, timestamp=None):
        if not self.conn:
            print("DatabaseManager: No connection available.")
            return
        if not timestamp:
            timestamp = int(time.time())
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO sensor_data (machine_id, count, timestamp) VALUES (%s, %s, to_timestamp(%s))",
                    (machine_id, count, timestamp)
                )
                self.conn.commit()
                print(f"DatabaseManager: Inserted count {count} for {machine_id} at {timestamp}.")
        except Exception as e:
            print(f"DatabaseManager: Insert failed: {e}")
            self.conn.rollback()

    def update_status(self, machine_id, status):
        if not self.conn:
            print("DatabaseManager: No connection available.")
            return
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "UPDATE machine_status SET status = %s, last_update = NOW() WHERE machine_id = %s",
                    (status, machine_id)
                )
                self.conn.commit()
                print(f"DatabaseManager: Updated status to {status} for {machine_id}.")
        except Exception as e:
            print(f"DatabaseManager: Status update failed: {e}")
            self.conn.rollback()
