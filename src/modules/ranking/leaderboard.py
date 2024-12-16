import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /leaderboard has been loaded')
        pass
    
    @commands.slash_command(name="leaderboard", description="Check the leaderboard")
    async def leaderboard(self, inter):
        try:
            await inter.response.defer()
            guild = inter.guild
            guildID = guild.id

            embed = disnake.Embed(
                title=f"📊 Leaderboard",
                color=disnake.Color.blurple()
                )

            sortedUser = Saver.fetch(f"SELECT userID FROM ranking WHERE guildID = {str(guildID)} ORDER BY xp DESC")

            for i, userData in enumerate(sortedUser):
                try:
                    user = await self.bot.fetch_user(int(userData[0]))
                    xp = Saver.fetch(f"SELECT xp FROM ranking WHERE userID = {userData[0]} AND guildID = {guildID}")[0][0]
                    level = Saver.fetch(f"SELECT level FROM ranking WHERE userID = {userData[0]} AND guildID = {guildID}")[0][0]
                    embed.add_field(name=f"{i+1}. {user.display_name}", value=f"Level `{level}` with `{xp}` XP", inline=False)
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