from datetime import datetime
import socket
import threading

import src.data.var as var
from src.data.var import Color, load_config

cat = ["[ERROR]", "[WARN] ", "[INFO] ", "[LOG]  ", "[SQL]  "]

clients = []

def client_handler(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
        except:
            break
    client_socket.close()
    clients.remove(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server started on port 9999")
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=client_handler, args=(client_socket,)).start()

def write(cat, message):
    """
    Write log message to log file and send to connected clients

    Args:
        cat (str): category of the log message
        message (str): log message
    """
    with open(var.logFile, 'a', encoding="utf-8") as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {cat} - {message}\n"
        f.write(log_message)
        for client in clients:
            try:
                client.send(log_message.encode('utf-8'))
            except:
                clients.remove(client)

def check_leveling_log(cate):
    """
    Check the level of loggings (all, info, warn, error, sql, none)

    Args:
        cate (str): category of the log message

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