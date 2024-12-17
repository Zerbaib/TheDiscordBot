import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver
from src.data.var import *
from json import load


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
            grade = Saver.fetch(f"SELECT grade FROM ranking WHERE userID = {userID} AND guildID = {guildID}")[0][0]

            with open(emojiFile, 'r') as f:
                rankGradeEmoji = load(f)

            liaison_name = tableLiaison.get(grade)
            if liaison_name:
                emoji_id = rankGradeEmoji.get(liaison_name)
            else:
                Log.warn(f"Failed to get emoji id {grade}")

            nextLevelXP = 5 * (level ** 2) + 10 * level + 10
            mess = f"Your grade is **{grade}** \n\nwith ``{xp}`` XP and ``{level}`` level\nNext level at ```{xp}/{nextLevelXP} XP```"

            embed = disnake.Embed(
                title="📊 Rank Information 📊",
                description=mess,
                color=disnake.Color.blurple()
            )
            imageFileLink = disnake.File(f"./img/{liaison_name}.png")
            embed.set_thumbnail(file=imageFileLink)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error(e)
            Log.error("Failed to execute /rank")
            Log.error(e)
            await ctx.send(embed=embed)
            return



def setup(bot):
    bot.add_cog(Rank(bot))