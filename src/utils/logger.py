from datetime import datetime

from src.data.var import Color, load_config


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
        self.config = load_config("logLevel")
        self.cat = ["[ERROR]", "[WARN] ", "[INFO] ", "[LOG]  ", "[SQL]  "]
        pass

    def check_leveling_log(self, cat):
        """
        Check the level of loggings (all, info, warn, error, sql, none)

        Returns:
            bool: True if need to log, False id not log
        """
        if self.config == "all":
            return True
        elif self.config == "info":
            if cat == self.cat[0] or cat == self.cat[1] or cat == self.cat[2]:
                return True
            else:
                return False
        elif self.config == "warn":
            if cat == self.cat[0] or cat == self.cat[1]:
                return True
            else:
                return False
        elif self.config == "error" and cat == self.cat[0]:
            return True
        elif self.config == "sql" and cat == self.cat[3] or cat == self.cat[4]:
            return True
        else:
            return False

    def error(self, message):
        """
        Print error message with red color

        Args:
            message (str): error message
        """
        if self.check_leveling_log(self.cat[0]):
            print(f"{Color.red}{self.cat[0]}{Color.reset} {message}")
            write(self.cat[0], message)

    def warn(self, message):
        """
        Print warning message with orange color

        Args:
            message (str): warning message
        """
        if self.check_leveling_log(self.cat[1]):
            print(f"{Color.orange}{self.cat[1]}{Color.reset} {message}")
            write(self.cat[1], message)

    def info(message):
        """
        Print info message with green color

        Args:
            message (str): info message
        """
        if self.check_leveling_log(self.cat[2]):
            print(f"{Color.green}{self.cat[2]}{Color.reset} {message}")
            write(self.cat[2], message)

    def log(message):
        """
        Print log message with white color

        Args:
            message (str): log message
        """
        if self.check_leveling_log(self.cat[3]):
            print(f"{Color.reset}{self.cat[3]}{Color.reset} {message}")
            write(self.cat[3], message)

    def sql(message):
        """
        Print sql message with blue color

        Args:
            message (str): sql message
        """
        if self.check_leveling_log(self.cat[4]):
            print(f"{Color.blue}{self.cat[4]}{Color.reset} {message}")
            write(self.cat[4], message)