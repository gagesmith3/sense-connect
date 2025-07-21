
# Sense-Connect CLI Dashboard (refactored)
import time
import json
import os
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

HARD_COUNT_CACHE = 'hard_count_cache.json'
console = Console()

def get_status():
    try:
        if os.path.exists(HARD_COUNT_CACHE):
            with open(HARD_COUNT_CACHE, 'r') as f:
                cache = json.load(f)
            if cache and isinstance(cache, list) and len(cache) > 0:
                latest = cache[-1]
                return {
                    'machine_id': latest.get('machine_id', '-'),
                    'count': latest.get('count', '-'),
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest.get('timestamp', time.time())))
                }
    except Exception as e:
        return {'machine_id': 'ERROR', 'count': 'ERROR', 'timestamp': str(e)}
    return {'machine_id': '-', 'count': '-', 'timestamp': '-'}

def get_connection_status():
    # Replace with real checks if available
    return {
        "DB": True,
        "WebSocket": False,
    }

def show_dashboard():
    logo = '''
   __________________________________________
  / ____/ __ \/ | / / | / / ____/ ____/_  __/
 / /   / / / /  |/ /  |/ / __/ / /     / /   
/ /___/ /_/ / /|  / /|  / /___/ /___  / /    
\____/\____/_/ |_/_/ |_/_____/______//_/     
                                             
    '''
    logo_panel = Panel(Text(logo, style="bold purple"), border_style="purple")

    with Live(console=console, refresh_per_second=2, screen=False) as live:
        while True:
            try:
                # Connection status panel
                conn_status = get_connection_status()
                status_text = ""
                for name, connected in conn_status.items():
                    indicator = "🟢" if connected else "🔴"
                    style = "bold green" if connected else "bold red"
                    status_text += f"[{style}]{indicator} {name}[/]  "
                status_panel = Panel(Text(status_text, justify="center"), title="Connection Status", border_style="magenta")

                # Main data table
                status = get_status()
                table = Table(title="Sense-Connect CLI Dashboard")
                table.add_column("Machine ID", justify="center")
                table.add_column("Count", justify="center")
                table.add_column("Last Update", justify="center")
                table.add_row(
                    str(status['machine_id']),
                    str(status['count']),
                    status['timestamp']
                )

                # Stack logo, status panel, and table vertically
                live.update([logo_panel, status_panel, table])
            except Exception as e:
                error_panel = Panel(Text(f"[DASHBOARD ERROR] {e}", style="bold red"), border_style="red")
                live.update([logo_panel, error_panel])
            time.sleep(1)

if __name__ == "__main__":
    show_dashboard()
