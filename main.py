from datetime import datetime

import disnake
import src.utils.creator
import src.utils.loader
import src.utils.starter
from disnake.ext import commands
from src.data.var import initTime, load_config
from src.utils.logger import Log

prefix = load_config("prefix")
ownerID = load_config("ownerId")

bot = commands.Bot(
    command_prefix=prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True,
    owner_id=ownerID
)

class main():
    def __init__(self):
        initTime(datetime.now())
        self.bot = bot
        src.utils.creator.Creator()
        src.utils.loader.Loader(self.bot)
        src.utils.starter.Launch(self.bot)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        Log.error("Failed to start bot")
        Log.error(e)
        exit()