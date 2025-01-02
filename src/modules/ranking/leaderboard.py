from json import load

import disnake
from disnake.ext import commands
from src.data.var import files, tableLiaison
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


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
            await inter.response.defer()
            guild = inter.guild

            embed = disnake.Embed(
                title=f"📊 Leaderboard",
                color=disnake.Color.blurple()
                )

            query = f"SELECT userID, xp, level, grade FROM ranking WHERE guildID = {str(guild.id)} ORDER BY xp DESC LIMIT 10"
            sortedUser = Saver.query(query)

            if not sortedUser:
                embed.add_field(name="📊 Leaderboard", value="No user found", inline=False)
                return await inter.edit_original_response(embed=embed)

            users = await self.bot.fetch_users([int(userData[0]) for userData in sortedUser])
            for i, (userData, user) in enumerate(zip(sortedUser, users)):
                try:
                    user = await self.bot.fetch_user(int(userData[0]))

                    usrData = sortedUser[i]
                    xp = usrData[1]
                    level = usrData[2]
                    grade = usrData[3]

                    with open(files["emojis"], 'r') as f:
                        rankGradeEmoji = load(f)

                    liaison_name = tableLiaison.get(grade)
                    if liaison_name:
                        emoji_id = rankGradeEmoji.get(liaison_name)

                    title = f"{i+1}. "
                    if liaison_name and emoji_id:
                        title += f"<:{liaison_name}:{emoji_id}>"
                    title += f" {user.display_name}"

                    embed.add_field(name=title, value=f"Level `{level}` with `{xp}` XP", inline=False)

                    if user == user.bot:
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