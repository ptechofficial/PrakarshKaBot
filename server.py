import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Server:
    DIRECTORY_TO_WATCH = "scripts"  # Watching the scripts directory

    def __init__(self):
        self.observer = Observer()
        self.process = None  # To store the running subprocess

    def run(self):
        event_handler = Handler(self)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()

        # Run the specified file immediately
        self.run_initial_file()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Server Stopped")

        self.observer.join()

    def run_initial_file(self):
        initial_file = "scripts/bot.py"  # Update path
        print(f"Live server for {initial_file} ...")
        self.process = subprocess.Popen(["python", initial_file])

    def restart_script(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(["python", "scripts/bot.py"])  # Update path

class Handler(FileSystemEventHandler):
    def __init__(self, server):
        self.server = server
        self.last_triggered = 0  # To track the last triggered time

    def on_modified(self, event):
        current_time = time.time()
        if current_time - self.last_triggered > 1:  # Debounce threshold (1 second)
            print(f"Detected change in {event.src_path}. Rerunning bot.py...")
            self.last_triggered = current_time  # Update last triggered time
            self.server.restart_script()

if __name__ == '__main__':
    server = Server()
    server.run()
