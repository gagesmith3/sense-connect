
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
    status_file = "connection_status.json"
    if os.path.exists(status_file):
        try:
            with open(status_file, "r") as f:
                status = json.load(f)
            # Ensure both keys exist
            return {
                "DB": status.get("DB", False),
                "WebSocket": status.get("WebSocket", False)
            }
        except Exception as e:
            return {"DB": False, "WebSocket": False}
    return {"DB": False, "WebSocket": False}


def show_dashboard():
    from rich.layout import Layout
    from rich.align import Align
    from rich.box import ROUNDED

    logo = """
   __________________________________________
  / ____/ __ \/ | / / | / / ____/ ____/_  __/
 / /   / / / /  |/ /  |/ / __/ / /     / /   
/ /___/ /_/ / /|  / /|  / /___/ /___  / /    
\____/\____/_/ |_/_/ |_/_____/______//_/     
                                             
    """
    logo_panel = Panel(Align.center(Text(logo, style="bold purple")), border_style="purple", box=ROUNDED)

    def make_sidebar():
        conn_status = get_connection_status()
        status_lines = []
        for name, connected in conn_status.items():
            indicator = "🟢" if connected else "🔴"
            style = "bold green" if connected else "bold red"
            status_lines.append(f"[{style}]{indicator}[/] {name}")
        sidebar_panel = Panel(
            Align.left("\n".join(status_lines)),
            title="Connections",
            border_style="magenta",
            width=22,
            box=ROUNDED,
            padding=(1,2)
        )
        return sidebar_panel

    def make_summary_panel(status):
        summary = f"[bold cyan]Machine:[/] {status['machine_id']}\n[bold yellow]Count:[/] {status['count']}"
        return Panel(Align.center(summary), title="Summary", border_style="cyan", box=ROUNDED, padding=(1,2))

    def make_table(status):
        table = Table(title="Recent Update", box=ROUNDED, pad_edge=True)
        table.add_column("Field", justify="right")
        table.add_column("Value", justify="left")
        table.add_row("Machine ID", str(status['machine_id']))
        table.add_row("Count", str(status['count']))
        table.add_row("Timestamp", status['timestamp'])
        return Panel(table, padding=(1,2))

    def make_raw_output_panel():
        log_file = "main.log"
        lines = []
        if os.path.exists(log_file):
            try:
                with open(log_file, "r") as f:
                    lines = f.readlines()[-10:]
            except Exception as e:
                lines = [f"[ERROR] Could not read log: {e}"]
        else:
            lines = ["[main.log not found]"]
        raw_text = "".join(lines).strip()
        return Panel(Text(raw_text, style="white"), title="Raw Output (main.py)", border_style="blue", box=ROUNDED, padding=(1,2))

    def make_footer():
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return Panel(Align.center(f"[bold white]Sense-Connect Dashboard | Last refresh: {now}"), border_style="grey37", box=ROUNDED)

    with Live(console=console, refresh_per_second=2, screen=True) as live:
        while True:
            try:
                status = get_status()
                layout = Layout()
                layout.split_column(
                    Layout(name="header", size=7),
                    Layout(name="body", ratio=2),
                    Layout(name="raw_output", size=8),
                    Layout(name="footer", size=3)
                )
                layout["body"].split_row(
                    Layout(name="sidebar", size=22),
                    Layout(name="main", ratio=2)
                )
                layout["header"].update(logo_panel)
                layout["sidebar"].update(make_sidebar())
                layout["main"].split_column(
                    Layout(name="summary", size=5),
                    Layout(name="table", ratio=2)
                )
                layout["main"]["summary"].update(make_summary_panel(status))
                layout["main"]["table"].update(make_table(status))
                layout["raw_output"].update(make_raw_output_panel())
                layout["footer"].update(make_footer())
                live.update(layout)
            except Exception as e:
                error_panel = Panel(Text(f"[DASHBOARD ERROR] {e}", style="bold red"), border_style="red", box=ROUNDED)
                live.update(error_panel)
            time.sleep(1)

if __name__ == "__main__":
    show_dashboard()
