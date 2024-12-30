from json import load

import disnake
from disnake.ext import commands
from src.data.var import files, tableLiaison
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver
from src.utils.lang import get_language_file


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "ranking"

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /leaderboard has been loaded')
        pass

    @commands.slash_command(name="leaderboard", description="Check the leaderboard")
    async def leaderboard(self, inter):
        try:
            lang = get_language_file(inter.guild.preferred_locale)
            await inter.response.defer()
            guild = inter.guild

            embed = disnake.Embed(
                title=lang["Ranking"]["leaderboard"]["title"],
                color=disnake.Color.blurple()
                )

            sortedUser = Saver.query(f"SELECT userID FROM ranking WHERE guildID = {str(guild.id)} ORDER BY xp DESC")

            for i, userData in enumerate(sortedUser[:10]):
                try:
                    user = await self.bot.fetch_user(int(userData[0]))
                    presision = [f"userID = {userData[0]}", f"guildID = {guild.id}"]

                    usrData = Saver.fetch(self.dataTable, presision, ["xp", "level", "grade"])[0]
                    xp = usrData[0]
                    level = usrData[1]
                    grade = usrData[2]

                    with open(files["emojis"], 'r') as f:
                        rankGradeEmoji = load(f)

                    liaison_name = tableLiaison.get(grade)
                    if liaison_name:
                        emoji_id = rankGradeEmoji.get(liaison_name)

                    title = f"{i+1}. "
                    if liaison_name and emoji_id:
                        title += f"<:{liaison_name}:{emoji_id}>"
                    title += f" {user.display_name}"

                    embed.add_field(name=title, value=lang["Ranking"]["leaderboard"]["fields"].format(level=level, xp=xp), inline=False)

                    if user.bot:
                        Saver.query(f"DELETE FROM ranking WHERE userID = {userData[0]} AND guildID = {guild.id}")
                        Log.warn(f"Bot user {user.id} has been removed from leaderboard")
                        continue
                except Exception as e:
                    Log.warn("Failed to fetch user")
                    Log.warn(e)
                    continue
            await inter.edit_original_response(embed=embed)
        except Exception as e:
            embed = error(e)
            Log.error("Failed to execute /leaderboard")
            Log.error(e)
            await inter.send(embed=embed)
            return

def setup(bot):
    bot.add_cog(Leaderboard(bot))