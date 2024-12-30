from datetime import datetime

import src.data.var as var
from src.data.var import Color


def write(cat, message):
    """
    Write log message to log file

    Args:
        cat (str): category of the log message
        message (str): log message
    """
    with open(var.logFile, 'a', encoding="utf-8") as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - {cat} - {message}\n")

class Log():
    def __init__(self):
        pass

    def error(message):
        """
        Print error message with red color

        Args:
            message (str): error message
        """
        cat = "[ERROR]"
        print(f"{Color.red}{cat}{Color.reset} {message}")
        write(cat, message)

    def warn(message):
        """
        Print warning message with orange color

        Args:
            message (str): warning message
        """
        cat = "[WARN] "
        print(f"{Color.orange}{cat}{Color.reset} {message}")
        write(cat, message)

    def info(message):
        """
        Print info message with green color

        Args:
            message (str): info message
        """
        cat = "[INFO] "
        print(f"{Color.green}{cat}{Color.reset} {message}")
        write(cat, message)

    def log(message):
        """
        Print log message with white color

        Args:
            message (str): log message
        """
        cat = "[LOG]  "
        print(f"{Color.reset}{cat}{Color.reset} {message}")
        write(cat, message)

    def sql(message):
        """
        Print sql message with blue color

        Args:
            message (str): sql message
        """
        cat = "[SQL]  "
        print(f"{Color.blue}{cat}{Color.reset} {message}")
        write(cat, message)