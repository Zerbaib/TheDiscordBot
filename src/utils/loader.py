import os

from data.var import *
from src.utils.logger import Log


class Loader():
    def __init__(self, bot):
        self.bot = bot
        self.load_cogs()

    def load_cogs(self):
        for element in os.listdir(cogsFolder):
            try:
                elementDir = f"{cogsFolder}{element}"
                if os.path.isdir(elementDir):
                    for filename in os.listdir(elementDir):
                        if filename.endswith(".py"):
                            cogName = filename[:-3]
                            try:
                                self.bot.load_extension(f'src.modules.{element}.{cogName}')
                                Log.info(f"Loaded {filename}")
                            except Exception as e:
                                Log.error(f"Failed to load {filename}")
                                Log.error(e)
                                exit()
            except Exception as e:
                Log.error(f"Failed to load {element}")
                Log.error(e)
                exit()