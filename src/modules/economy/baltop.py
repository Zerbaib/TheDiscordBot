import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


class Baltop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /baltop has been loaded')
        pass

    @commands.slash_command(name="baltop", description="See the top 10 users with the highest balances")
    async def baltop(self, ctx):
            try:
                guildID = ctx.guild.id
                topUsers = Saver.fetch(f"SELECT userID, coins FROM economy WHERE guildID = {guildID} ORDER BY coins DESC LIMIT 10")

                message = "\n".join([f"**#{i+1}** <@{user[0]}> - **{user[1]}** coins" for i, user in enumerate(topUsers)])

                embed = disnake.Embed(
                    title="🏆 Top 10 Balances 🏆",
                    description=message if message else "No users found.",
                    color=disnake.Color.gold()
                )
                await ctx.send(embed=embed)
            except Exception as e:
                Log.error("Failed to execute /baltop")
                Log.error(e)
                return await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(Baltop(bot))