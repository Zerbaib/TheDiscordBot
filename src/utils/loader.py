import os
from data.var import *
from src.utils.logger import Log

class Loader():
    def __init__(self, bot):
        self.bot = bot

    def load_cogs(self):
        for element in os.listdir(cogsFolder):
            try:
                elementDir = f"{cogsFolder}{element}"
                if os.path.isdir(elementDir):
                    for filename in os.listdir(elementDir):
                        if filename.endswith(".py"):
                            cogName = filename[:-3]
                            try:
                                self.bot.load_extension(f'cogs.{element}.{cogName}')
                                Log.info(f"Loaded {filename}")
                            except Exception as e:
                                Log.error(f"Failed to load {filename}")
                                Log.error(e)
            except Exception as e:
                print(e)
                return