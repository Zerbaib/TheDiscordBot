import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver
from src.utils.lang import get_language_file


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
                lang = get_language_file(ctx.guild.preferred_locale)

                guildID = ctx.guild.id
                topUsers = Saver.query(f"SELECT userID, coins FROM economy WHERE guildID = {guildID} ORDER BY coins DESC LIMIT 10")

                message = "\n".join([lang["Economy"]["baltop"]["fields"].fomat(i=i+1, userId=user[0], userBal=user[1]) for i, user in enumerate(topUsers)])

                embed = disnake.Embed(
                    title=lang["Economy"]["baltop"]["title"],
                    description=message if message else lang["Economy"]["baltop"]["errors"]["noUser"],
                    color=disnake.Color.gold()
                )
                await ctx.send(embed=embed)
            except Exception as e:
                Log.error("Failed to execute /baltop")
                Log.error(e)
                return await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(Baltop(bot))