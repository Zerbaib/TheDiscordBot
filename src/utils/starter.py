import disnake
from disnake.ext import commands
from src.data.var import *
from src.utils.logger import Log


class Launch():
    def __init__(self, bot):
        self.token, prefix = load_config()
        self.bot = bot
        self.setup_events()
        self.start()

    def setup_events(self):
        @self.bot.event
        async def on_ready():
            Log.info('------')
            Log.info(f'Version local: {Version.getLocal()}')
            Log.info(f'Version online: {Version.getOnline()}')
            Log.info(f'On {len(self.bot.guilds)} guilds')
            Log.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
            Log.info('------')

    def start(self):
        try:
            self.bot.run(self.token)
        except Exception as e:
            Log.error("Failed to start bot")
            Log.error(e)
            exit()
