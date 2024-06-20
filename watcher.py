import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class Watcher:
    DIRECTORY_TO_WATCH = "."

    def __init__(self, file_to_run):
        self.observer = Observer()
        self.file_to_run = file_to_run

    def run(self):
        event_handler = Handler(self.file_to_run)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()

        # Run the specified file immediately
        print(f"Live server for {self.file_to_run} ...")
        subprocess.run(["python", self.file_to_run])

        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, file_to_run):
        self.file_to_run = file_to_run

    def on_modified(self, event):
        if event.src_path.endswith(self.file_to_run):
            print(f"Detected change in {event.src_path}. Rerunning script...")
            subprocess.run(["python", self.file_to_run])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python watcher.py <filename>")
        sys.exit(1)

    file_to_run = sys.argv[1]
    if not file_to_run.endswith(".py"):
        file_to_run += ".py"

    w = Watcher(file_to_run)
    w.run()
