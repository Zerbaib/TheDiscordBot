import os
from data.var import *
from src.utils.logger import *

class Creator:
    def __init__(self):
        self.log_file()
        self.config_folder()

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