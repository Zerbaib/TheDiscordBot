from src.utils.logger import Log
from data.var import token
import disnake
from disnake.ext import commands

class Launch():
    def __init__(self, bot):
        self.bot = bot
        self.setup_events()
        self.start()

    def setup_events(self):
        @self.bot.event
        async def on_ready():
            Log.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
            Log.info('------')

    def start(self):
        try:
            self.bot.run(token)
        except Exception as e:
            Log.error("Failed to start bot")
            Log.error(e)
            exit()
