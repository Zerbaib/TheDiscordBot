import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /stats has been loaded')
        pass

    @commands.slash_command(name="stats", description="Stats of the bot")
    @commands.is_owner()
    async def stats(self, ctx, request: str):
        try:
            numberOfGuilds = len(self.bot.guilds)
            numberOfUsers = len(self.bot.users)
            numberOfCommands = len(self.bot.commands)
            
            numberofUserInRankingDB = Saver.fetch("SELECT COUNT(*) FROM ranking")
            numberOfUsersInEconomyDB = Saver.fetch("SELECT COUNT(*) FROM economy")
            numberOfGuildInSettingsDB = Saver.fetch("SELECT COUNT(*) FROM guilds")
            
            msg = f"**Guilds:** {numberOfGuilds}\n**Users:** {numberOfUsers}\n**Commands:** {numberOfCommands}\n**Users in Ranking DB:** {numberofUserInRankingDB}\n**Users in Economy DB:** {numberOfUsersInEconomyDB}\n**Guilds in Settings DB:** {numberOfGuildInSettingsDB}"
            
            embed = disnake.Embed(
                title="📊 Stats",
                description=msg,
                color=disnake.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            Log.error("Failed to execute /query")
            Log.error(e)
            return await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(Stats(bot))