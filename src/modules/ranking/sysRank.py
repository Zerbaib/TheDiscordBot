import datetime
import random

import disnake
from disnake.ext import commands
from src.data.var import *
from src.utils.logger import Log
from src.utils.saver import Saver
import datetime
import asyncio


class sysRank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info("🧰 Ranking system has been loaded")
        self.bot.loop.create_task(self.resetRateDaly())
        pass

    @commands.Cog.listener()
    async def resetRateDaly(self):
        try:
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                current_time = datetime.datetime.now().time()
                if current_time.hour == 00 and current_time.minute == 00:
                    Saver.save(f"UPDATE ranking SET rate = {rateLimitXpDaily}")
                    Log.log(f"RATE LIMIT RESET")
                    pass
                await asyncio.sleep(10)
        except Exception as e:
            Log.warn("Failed to reset rate limit")
            Log.warn(e)
            return

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return
            if message.guild is None:
                return

            try:
                user = message.author
                guild = message.guild

                if not Saver.fetch(f"SELECT * FROM ranking WHERE userID = {user.id} AND guildID = {guild.id}"):
                    Saver.save(f"INSERT IGNORE INTO ranking (userID, guildID, xp, level, rate) VALUES ({user.id}, {guild.id}, 0, 0, {rateLimitXpDaily})")
                    pass

                oldXP = Saver.fetch(f"SELECT xp FROM ranking WHERE userID = {user.id} AND guildID = {guild.id}")[0][0]
                oldLevel = Saver.fetch(f"SELECT level FROM ranking WHERE userID = {user.id} AND guildID = {guild.id}")[0][0]
                oldRate = Saver.fetch(f"SELECT rate FROM ranking WHERE userID = {user.id} AND guildID = {guild.id}")[0][0]
                if oldRate == None:
                    Saver.save(f"UPDATE ranking SET rate = {rateLimitXpDaily} WHERE userID = {user.id} AND guildID = {guild.id}")
                    oldRate = rateLimitXpDaily
                xpWin = random.randint(1, 5)
                rate = oldRate - xpWin
                Saver.save(f"UPDATE ranking SET rate = {rate} WHERE userID = {user.id} AND guildID = {guild.id}")
                if rate <= 0:
                    rate = 0
                    Log.log(f"RATE LIMIT on {guild.id} user {user.id} [+] {oldRate} -> {rate}")
                    return

                newXP = oldXP + xpWin

                nextLevelXP = 5 * (oldLevel ** 2) + 10 * oldLevel + 10

                highest_grade = None
                for grade, value in rankGrade.items():
                    if newXP >= value:
                        highest_grade = grade
                if highest_grade:
                    oldGrade = Saver.fetch(f"SELECT grade FROM ranking WHERE userID = {user.id} AND guildID = {guild.id}")[0][0]
                    if oldGrade != highest_grade:
                        Saver.save(f"UPDATE ranking SET grade = '{highest_grade}' WHERE userID = {user.id} AND guildID = {guild.id}")

                        liaison_name = tableLiaison.get(highest_grade)
                        if liaison_name:
                            emoji_id = rankGradeEmoji.get(liaison_name)
                        else:
                            Log.warn(f"Failed to get emoji id {highest_grade}")

                        mess = f"Congratulations {user.mention} <:fire:>, you have been promoted to grade **{highest_grade}** <{liaison_name}:{emoji_id}> !"
                        await message.channel.send(mess, delete_after=10)
                        Log.log(f"GRADE on {guild.id} user {user.id} [+] {oldGrade} -> {highest_grade}")

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

                    Saver.save(f"UPDATE ranking SET level = {newLevel} WHERE userID = {user.id} AND guildID = {guild.id}")
                    Log.log(f"LEVEL on {guild.id} user {user.id} [+] {oldLevel} -> {newLevel}")
                    pass

                Saver.save(f"UPDATE ranking SET xp = {newXP} WHERE userID = {user.id} AND guildID = {guild.id}")
                Log.log(f"XP on {guild.id} user {user.id} [+] {xpWin} -> {newXP}")
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