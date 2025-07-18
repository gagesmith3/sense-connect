# wrapper.py
import subprocess
from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()

def run_counting_app():
    # Start main.py in the background
    return subprocess.Popen(['python3', 'main.py'])

def show_dashboard():
    logo = '''

   __________________________________________
  / ____/ __ \/ | / / | / / ____/ ____/_  __/
 / /   / / / /  |/ /  |/ / __/ / /     / /   
/ /___/ /_/ / /|  / /|  / /___/ /___  / /    
\____/\____/_/ |_/_/ |_/_____/\____/ /_/     
                                             

    '''
    console.print(logo, style="bold magenta")
    table = Table(title="Sense-Connect Debug Dashboard")
    table.add_column("Status")
    table.add_row("Running")
    with Live(table, refresh_per_second=2):
        while True:
            # Update table with logs, status, etc.
            pass

if __name__ == "__main__":
    proc = run_counting_app()
    try:
        show_dashboard()
    except KeyboardInterrupt:
        proc.terminate()