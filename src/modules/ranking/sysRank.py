import random

import disnake
from disnake.ext import commands
from src.data.var import *
from src.utils.logger import Log
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

                oldXP = Saver.fetch(f"SELECT xp FROM ranking WHERE userID = {userID} AND guildID = {guildID}")[0][0]
                oldLevel = Saver.fetch(f"SELECT level FROM ranking WHERE userID = {userID} AND guildID = {guildID}")[0][0]
                xpWin = random.randint(1, 5)
                newXP = oldXP + xpWin

                nextLevelXP = 5 * (oldLevel ** 2) + 10 * oldLevel + 10

                if newXP > nextLevelXP:
                    newLevel = oldLevel + 1
                    nextLevelXP = 5 * (newLevel ** 2) + 10 * newLevel + 10
                    mess = f"Congratulations {user.mention}, you have leveled up to level `{newLevel}`!\nneed `{newXP}/{nextLevelXP}` XP to level up again."
                    embed = disnake.Embed(
                        title="🎉 Level Up",
                        description=mess,
                        color=disnake.Color.blurple()
                        )
                    await message.channel.send(embed=embed, delete_after=10)

                    Saver.save(f"UPDATE ranking SET level = {newLevel} WHERE userID = {userID} AND guildID = {guildID}")
                    Log.log(f"LEVEL on {guildID} user {userID} [+] {oldLevel} -> {newLevel}")
                    pass

                Saver.save(f"UPDATE ranking SET xp = {newXP} WHERE userID = {userID} AND guildID = {guildID}")
                Log.log(f"XP on {guildID} user {userID} [+] {xpWin} -> {newXP}")
            except Exception as e:
                Log.warn("Failed to update user xp")
                Log.warn(e)
                return
        except Exception as e:
            Log.error("Failed to execute ranking system")
            Log.error(e)
            return


def setup(bot):
    bot.add_cog(sysRank(bot))