import platform
from datetime import datetime

import disnake
from disnake.ext import commands
from src.data.var import Version, load_config
from src.utils.logger import Log


class Launch():
    def __init__(self, bot):
        self.token = load_config("token")
        self.bot = bot
        self.setup_events()
        self.start()

    def setup_events(self):
        @self.bot.event
        async def on_ready():
            if Version.getLocal() != Version.getOnline():
                Log.warning("🛑 New version available")
                Log.warning("🛑 Please update the bot")
            Log.info('=' * 25)
            Log.info(f'🔱 Python Version {platform.python_version()}')
            Log.info(f'🔱 Disnake Version {disnake.__version__}')
            Log.info(f'🔱 Version local: {Version.getLocal()}')
            Log.info(f'🔱 Version online: {Version.getOnline()}')
            Log.info(f'🔱 On {len(self.bot.guilds)} guilds')
            Log.info(f'🔱 Logged in as {self.bot.user} (ID: {self.bot.user.id})')
            Log.info(f'🔱 Connected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')
            Log.info('=' * 25)

    def start(self):
        try:
            self.bot.run(self.token)
        except Exception as e:
            Log.error("Failed to start bot")
            Log.error(e)
            exit()
