import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

class Server:
    DIRECTORY_TO_WATCH = "."

    def __init__(self, target):
        self.observer = Observer()
        self.target = target
        self.process = None  # To store the running subprocess

    def run(self):
        event_handler = Handler(self.target, self)
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
        initial_file = self.get_initial_file()
        if initial_file:
            print(f"Live server for {initial_file} ...")
            self.process = subprocess.Popen(["python", initial_file])

    def get_initial_file(self):
        if self.target == "test":
            initial_file = "test/test.py"
        elif self.target == "main":
            initial_file = "main/main.py"
        else:
            print(f"Invalid target '{self.target}'. Use 'test' or 'main'.")
            return None

        return initial_file

    def restart_script(self, script_path):
        if self.process:
            self.process.terminate()
            print("Previous process terminated")
        print(f"Re-Running {script_path}...")
        self.process = subprocess.Popen(["python", script_path])

class Handler(FileSystemEventHandler):
    def __init__(self, target, server):
        self.target = target
        self.server = server

    def on_modified(self, event):
        if self.should_rerun(event.src_path):
            print(f"Detected change in {event.src_path}. Rerunning script...")
            self.server.restart_script(self.get_script_path())

    def should_rerun(self, src_path):
        if self.target == "test":
            test_files = ["test.py", "meta_test.yaml", "gemini_test.py"]
            return any(src_path.endswith(file) for file in test_files)
        elif self.target == "main":
            main_files = ["main.py", "meta_main.yaml", "gemini_main.py"]
            return any(src_path.endswith(file) for file in main_files)
        return False

    def get_script_path(self):
        if self.target == "test":
            return "test/test.py"
        elif self.target == "main":
            return "main/main.py"
        return None

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python server.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    if target not in ["test", "main"]:
        print(f"Invalid target '{target}'. Use 'test' or 'main'.")
        sys.exit(1)

    server = Server(target)
    server.run()
