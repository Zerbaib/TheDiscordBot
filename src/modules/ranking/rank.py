from json import load

import disnake
from disnake.ext import commands
from src.data.var import *
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
            grade = Saver.fetch(f"SELECT grade FROM ranking WHERE userID = {userID} AND guildID = {guildID}")[0][0]

            with open(emojiFile, 'r') as f:
                rankGradeEmoji = load(f)

            liaison_name = tableLiaison.get(grade)
            if liaison_name:
                emoji_id = rankGradeEmoji.get(liaison_name)
            else:
                Log.warn(f"Failed to get emoji id {grade}")

            progress_bar = ""
            
            actualGrade = grade
            nextGrade = list(rankGrade.keys())[list(rankGrade.keys()).index(grade) + 1] if grade in rankGrade else None
            actualGradeXp = rankGrade[actualGrade]
            nextGradeXp = rankGrade[nextGrade] if nextGrade else None
            if nextGradeXp:
                progress = (xp - actualGradeXp) / (nextGradeXp - actualGradeXp)
                progress_bar = "█" * int(progress * 20) + "░" * (20 - int(progress * 20))
            else:
                progress_bar = "█" * 20

            nextLevelXP = 5 * (level ** 2) + 10 * level + 10
            mess = f"Your grade is **{grade}**"
            mess += f"\n\n[{progress_bar}] {round(progress*100)}%\n\n"
            mess += f"with ``{xp}`` XP and ``{level}`` level\nNext level at ```{xp}/{nextLevelXP} XP```"

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