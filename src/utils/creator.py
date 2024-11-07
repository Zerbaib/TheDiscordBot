import json
import os

from src.data.var import *
from src.utils.logger import *


class Creator:
    def __init__(self):
        self.log_file()
        self.config_file()
        from src.utils.saver import Saver
        Saver()

    def config_folder(self):
        if os.path.exists(configFolder):
            Log.log("Config folder already exists")
            return
        else:
            try:
                os.makedirs(configFolder)
                Log.info("Config folder created")
            except Exception as e:
                Log.error("Failed to create config folder")
                Log.error(e)
                return

    def config_file(self):
        if os.path.exists(configFile):
            Log.log("Config file already exists")
            return
        else:
            try:
                self.config_folder()
                data = {
                    "token": "your_token",
                    "prefix": "your_prefix",
                    "dbUser": "your_db_user",
                    "dbPass": "your_db_pass",
                    "dbHost": "your_db_host",
                    "dbPort": "your_db_port",
                    "dbName": "your_db_name"
                }
                with open(configFile, 'w') as f:
                    json.dump(data, f, indent=4)
                Log.info("Config file created")
            except Exception as e:
                Log.error("Failed to create config file")
                Log.error(e)
                return

    def log_folder(self):
        if os.path.exists(logFolder):
            Log.log("Log folder already exists")
            return
        else:
            try:
                os.makedirs(logFolder)
                Log.info("Log folder created")
            except Exception as e:
                Log.error("Failed to create log folder")
                Log.error(e)
                return
    
    def log_file(self):
        if os.path.exists(logFile):
            Log.log("Log file already exists")
            return
        else:
            try:
                self.log_folder()
                with open(logFile, 'w') as f:
                    Log.info("Log file created")
            except Exception as e:
                Log.error("Failed to create log file")
                Log.error(e)
                return