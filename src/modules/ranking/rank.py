import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /rank has been loaded')

    @commands.slash_command(name="rank", description="Check your rank")
    async def rank(self, ctx):
        try:
            user = ctx.author
            userID = user.id
            guild = ctx.guild
            guildID = guild.id

            xp = Saver.fetch(f"SELECT xp FROM ranking WHERE userID = {userID} AND guildID = {guildID}")[0][0]
            level = Saver.fetch(f"SELECT level FROM ranking WHERE userID = {userID} AND guildID = {guildID}")[0][0]

            nextLevelXP = 5 * (level ** 2) + 10 * level + 10
            message = f"Your rank is level `{level}` with `{xp}` XP ```{xp}/{nextLevelXP} XP```"

            embed = disnake.Embed(
                title="📊 Rank",
                description=message,
                color=disnake.Color.blurple()
                )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error(e)
            Log.error("Failed to execute /rank")
            Log.error(e)
            await ctx.send(embed=embed)
            return



def setup(bot):
    bot.add_cog(Rank(bot))