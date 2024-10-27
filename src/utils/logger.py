from data.var import *
from datetime import datetime

class Log():
    def __init__(self):
        pass

    def error(message):
        cat = "[ERROR]"
        print(f"{Color.red}{cat}{Color.reset} {message}")
        with open(logFile, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} - {cat} - {message}\n")

    def warn(message):
        cat = "[WARN]"
        print(f"{Color.orange}{cat}{Color.reset} {message}")
        with open(logFile, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} - {cat}  - {message}\n")

    def info(message):
        cat = "[INFO]"
        print(f"{Color.green}{cat}{Color.reset} {message}")
        with open(logFile, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} - {cat}  - {message}\n")

    def log(message):
        cat = "[LOG]"
        print(f"{Color.reset}{cat}{Color.reset} {message}")
        with open(logFile, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} - {cat}   - {message}\n")