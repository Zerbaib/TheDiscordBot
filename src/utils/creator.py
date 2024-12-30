import json
import os

from src.data.var import data, emojisID, folders, files
import src.data.var as var
from src.utils.logger import Log

class Creator:
    def __init__(self):
        self.log_file()
        self.config_file()
        from src.utils.saver import Saver
        Saver()

    def config_folder(self):
        if os.path.exists(folders['config']):
            Log.log("Config folder already exists")
            return
        else:
            try:
                os.makedirs(folders['config'])
                Log.info("Config folder created")
            except Exception as e:
                Log.error("Failed to create config folder")
                Log.error(e)
                return

    def config_file(self):
        if os.path.exists(files["config"]):
            with open(files["config"], 'r') as f:
                dataConf = json.load(f)
                pass

            missing_or_default_keys = [key for key, default_value in data.items() if key not in dataConf or dataConf[key] == default_value]
            if missing_or_default_keys:
                Log.warn(f"Missing or default keys in config file: {', '.join(missing_or_default_keys)}")
                exit()

            Log.log("Config file already exists")
            pass
        else:
            try:
                self.config_folder()
                with open(files["emojis"], 'w') as f:
                    json.dump(data, f, indent=4)
                Log.info("Config file created")
            except Exception as e:
                Log.error("Failed to create config file")
                Log.error(e)
                return
        if not os.path.exists(files["emojis"]):
            try:
                with open(files["emojis"], 'w') as f:
                    json.dump(emojisID, f, indent=4)
                Log.info("Emoji file created")
            except Exception as e:
                Log.error("Failed to create emoji file")
                Log.error(e)

    def log_folder(self):
        if os.path.exists(folders['logs']):
            Log.log("Log folder already exists")
            return
        else:
            try:
                os.makedirs(folders['logs'])
                Log.info("Log folder created")
            except Exception as e:
                Log.error("Failed to create log folder")
                Log.error(e)
                return

    def log_file(self):
        if os.path.exists(var.logFile):
            Log.log("Log file already exists")
            return
        else:
            try:
                self.log_folder()
                with open(var.logFile, 'w') as f:
                    Log.info("Log file created")
            except Exception as e:
                Log.error("Failed to create log file")
                Log.error(e)
                return