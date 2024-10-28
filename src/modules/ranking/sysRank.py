import disnake
import random
from disnake.ext import commands
from src.utils.logger import Log
from data.var import *
from src.utils.saver import Saver

class sysRank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info("🧰 Ranking system has been loaded")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return

            if message.guild is None:
                return

            try:
                user = message.author
                userID = user.id
                guild = message.guild
                guildID = guild.id

                if not Saver.fetch(f"SELECT * FROM ranking WHERE userID = {userID} AND guildID = {guildID}"):
                    Saver.save(f"INSERT OR IGNORE INTO ranking (userID, guildID, xp, level) VALUES ({userID}, {guildID}, 0, 0)")
                    pass

                oldXP = Saver.fetch(f"SELECT xp FROM ranking WHERE userID = {userID} AND guildID = {guildID}")
                xpWin = random.randint(1, 15)
                newXP = oldXP + xpWin

                Saver.save(f"UPDATE ranking SET xp = {newXP} WHERE userID = {userID} AND guildID = {guildID}")
                Log.log(f"XP on {guildID} user {userID} [+] {xpWin} -> {newXP}")
            except Exception as e:
                Log.error("Failed to update user xp")
                Log.error(e)
                return
        except Exception as e:
            Log.error("Failed to execute ranking system")
            Log.error(e)
            return


def setup(bot):
    bot.add_cog(sysRank(bot))