#Joke scripts
import threading, sys, time
from rich.live import Live
from rich.text import Text
from rich.console import Console

stop_event = threading.Event()
console = Console()

def loading_animation(teks):
    i = 0
    with Live(refresh_per_second=10, console=console, transient=True) as live:
        while not stop_event.is_set():
            dot = '.' * (i % 5)
            live.update(Text(f"\r {teks}{dot:<5}"))
            time.sleep(0.3)
            i += 1

def run_with_animation(func, teks):
    global loading_thread
    stop_event.clear()
    loading_thread = threading.Thread(target=loading_animation, args=(teks,))
    loading_thread.start()
    try:
        func()
    except ImportError:
        stop_event.set()
        sys.exit()
    finally:
        stop_event.set()
        loading_thread.join()
    stop_event.set()
    loading_thread.join()
    
