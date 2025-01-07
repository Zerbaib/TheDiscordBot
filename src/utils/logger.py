from datetime import datetime

from src.data.var import Color, load_config

cat = ["[ERROR]", "[WARN] ", "[INFO] ", "[LOG]  ", "[SQL]  "]

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
def check_leveling_log(cate):
        """
        Check the level of loggings (all, info, warn, error, sql, none)

        Returns:
            bool: True if need to log, False id not log
        """
        config = load_config("logLevel")
        if config == "all":
            return True
        elif config == "info":
            if cate == cat[0] or cate == cat[1] or cate == cat[2]:
                return True
            else:
                return False
        elif config == "warn":
            if cate == cat[0] or cate == cat[1]:
                return True
            else:
                return False
        elif config == "error" and cate == cat[0]:
            return True
        elif config == "sql" and cate == cat[3] or cate == cat[4]:
            return True
        else:
            return False

class Log():
    def __init__(self):
        pass

    def error(message):
        """
        Print error message with red color

        Args:
            message (str): error message
        """
        if check_leveling_log(cat[0]):
            print(f"{Color.red}{cat[0]}{Color.reset} {message}")
            write(cat[0], message)

    def warn(message):
        """
        Print warning message with orange color

        Args:
            message (str): warning message
        """
        if check_leveling_log(cat[1]):
            print(f"{Color.orange}{cat[1]}{Color.reset} {message}")
            write(cat[1], message)

    def info(message):
        """
        Print info message with green color

        Args:
            message (str): info message
        """
        if check_leveling_log(cat[2]):
            print(f"{Color.green}{cat[2]}{Color.reset} {message}")
            write(cat[2], message)

    def log(message):
        """
        Print log message with white color

        Args:
            message (str): log message
        """
        if check_leveling_log(cat[3]):
            print(f"{Color.reset}{cat[3]}{Color.reset} {message}")
            write(cat[3], message)

    def sql(message):
        """
        Print sql message with blue color

        Args:
            message (str): sql message
        """
        if check_leveling_log(cat[4]):
            print(f"{Color.blue}{cat[4]}{Color.reset} {message}")
            write(cat[4], message)