# dashboard.py - Sense-Connect CLI Dashboard
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.group import Group
import time
import json
import os

# Path to cache file written by main.py
HARD_COUNT_CACHE = 'hard_count_cache.json'

console = Console()
console.clear()

def get_status():
    # Try to read latest status from cache
    try:
        if os.path.exists(HARD_COUNT_CACHE):
            with open(HARD_COUNT_CACHE, 'r') as f:
                cache = json.load(f)
            if cache and isinstance(cache, list):
                latest = cache[-1]
                return {
                    'machine_id': latest.get('machine_id', '-'),
                    'count': latest.get('count', '-'),
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest.get('timestamp', time.time())))
                }
    except Exception as e:
        print(f"[DASHBOARD ERROR] get_status: {e}")
    return {'machine_id': '-', 'count': '-', 'timestamp': '-'}

def get_connection_status():
    # Replace these with real checks
    return {
        "DB": True,           # True = connected, False = disconnected
        "WebSocket": False,   # Example status
    }

def render_status_panel(statuses):
    status_text = ""
    for name, connected in statuses.items():
        indicator = "🟢" if connected else "🔴"
        style = "bold green" if connected else "bold red"
        status_text += f"[{style}]{indicator} {name}[/]\n"
    panel = Panel(Text(status_text, justify="center"), title="Connection Status", border_style="magenta")
    return panel

def show_dashboard():
    logo = '''
   __________________________________________
  / ____/ __ \/ | / / | / / ____/ ____/_  __/
 / /   / / / /  |/ /  |/ / __/ / /     / /   
/ /___/ /_/ / /|  / /|  / /___/ /___  / /    
\____/\____/_/ |_/_/ |_/_____/______//_/     
                                             
    '''
    
    

    from rich.group import Group
    with Live(console=console, refresh_per_second=2, screen=False) as live:
        while True:
            try:
                status = get_status()
                conn_status = get_connection_status()
                status_panel = render_status_panel(conn_status)

                table = Table(title="Sense-Connect CLI Dashboard")
                table.add_column("Machine ID", justify="center")
                table.add_column("Count", justify="center")
                table.add_column("Last Update", justify="center")
                table.add_row(
                    str(status['machine_id']),
                    str(status['count']),
                    status['timestamp']
                )

                # Group the logo, status panel, and table together
                group = Group(
                    Text(logo, style="bold purple"),
                    status_panel,
                    table
                )
                live.update(group)
            except Exception as e:
                console.print(f"[DASHBOARD ERROR] {e}", style="bold red")
            time.sleep(1)

if __name__ == "__main__":
    show_dashboard()
