from json import load

import disnake
from disnake.ext import commands
from src.data.var import files, get_rank_info_config
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver
from src.utils.lang import get_language_file


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "ranking"
        self.tableLiaison = get_rank_info_config("liaison")

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

            query = f"SELECT userID, xp, level, grade FROM ranking WHERE guildID = {str(guild.id)} ORDER BY xp DESC LIMIT 10"
            sortedUser = Saver.query(query)

            if not sortedUser:
                embed.add_field(name="📊 Leaderboard", value="No user found", inline=False)
                return await inter.edit_original_response(embed=embed)

            for i, userData in enumerate(sortedUser):
                try:
                    user = await self.bot.fetch_user(int(userData[0]))

                    usrData = sortedUser[i]
                    xp = usrData[1]
                    level = usrData[2]
                    grade = usrData[3]

                    with open(files["emojis"], 'r') as f:
                        rankGradeEmoji = load(f)

                    liaison_name = self.tableLiaison.get(grade)
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