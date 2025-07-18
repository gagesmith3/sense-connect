# dashboard.py - Sense-Connect CLI Dashboard
from rich.console import Console
from rich.live import Live
from rich.table import Table
import time
import json
import os

# Path to cache file written by main.py
HARD_COUNT_CACHE = 'hard_count_cache.json'

console = Console()

def get_status():
    # Try to read latest status from cache
    if os.path.exists(HARD_COUNT_CACHE):
        with open(HARD_COUNT_CACHE, 'r') as f:
            cache = json.load(f)
        if cache:
            latest = cache[-1]
            return {
                'machine_id': latest.get('machine_id', '-'),
                'count': latest.get('count', '-'),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest.get('timestamp', time.time())))
            }
    return {'machine_id': '-', 'count': '-', 'timestamp': '-'}

def show_dashboard():
    logo = '''
   __________________________________________
  / ____/ __ \/ | / / | / / ____/ ____/_  __/
 / /   / / / /  |/ /  |/ / __/ / /     / /   
/ /___/ /_/ / /|  / /|  / /___/ /___  / /    
\____/\____/_/ |_/_/ |_/_____/\____/ /_/     
                                             
    '''
    console.clear()
    console.print(logo, style="bold purple")
    table = Table(title="Sense-Connect CLI Dashboard")
    table.add_column("Machine ID", justify="center")
    table.add_column("Count", justify="center")
    table.add_column("Last Update", justify="center")
    with Live(table, refresh_per_second=2):
        while True:
            status = get_status()
            table.rows.clear()
            table.add_row(
                str(status['machine_id']),
                str(status['count']),
                status['timestamp']
            )
            time.sleep(1)

if __name__ == "__main__":
    show_dashboard()
