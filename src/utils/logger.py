from datetime import datetime

from src.data.var import *


def write(cat, message):
    with open(logFile, 'a', encoding="utf-8") as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - {cat} - {message}\n")

class Log():
    def __init__(self):
        pass

    def error(message):
        cat = "[ERROR]"
        print(f"{Color.red}{cat}{Color.reset} {message}")
        write(cat, message)

    def warn(message):
        cat = "[WARN] "
        print(f"{Color.orange}{cat}{Color.reset} {message}")
        write(cat, message)

    def info(message):
        cat = "[INFO] "
        print(f"{Color.green}{cat}{Color.reset} {message}")
        write(cat, message)

    def log(message):
        cat = "[LOG]  "
        print(f"{Color.reset}{cat}{Color.reset} {message}")
        write(cat, message)

    def sql(message):
        cat = "[SQL]  "
        print(f"{Color.blue}{cat}{Color.reset} {message}")
        write(cat, message)