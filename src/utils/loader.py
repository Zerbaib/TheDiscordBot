import disnake
import os
from data.var import *

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
                                print(f"Loaded {filename}")
                            except Exception as e:
                                print(f"Failed to load {filename}")
                                print(e)
            except Exception as e:
                print(e)
                return