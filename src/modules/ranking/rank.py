import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log

class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /rank has been loaded')

def setup(bot):
    bot.add_cog(Rank(bot))