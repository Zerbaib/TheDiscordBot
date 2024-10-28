import src.utils.creator
import src.utils.loader
from src.utils.logger import Log
from src.utils.starter import Launch
from data.var import load_config
import disnake
from disnake.ext import commands

t, prefix = load_config()

bot = commands.Bot(
    command_prefix=prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True
)

class main():
    def __init__(self):
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