import disnake
from disnake.ext import commands
from src.utils.logger import Log


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🧰 Guilds log has been loaded')
        pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        Log.log(f'GUILD [+] {guild.name} (ID: {guild.id}) with {len(guild.members)} members | Guilds: {len(self.bot.guilds)}')
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        Log.log(f'GUILD [-] {guild.name} (ID: {guild.id}) with {len(guild.members)} members | Guilds: {len(self.bot.guilds)}')
        pass

def setup(bot):
    bot.add_cog(Server(bot))