import asyncio
import datetime
import random
from json import load

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
        self.bot.loop.create_task(self.resetRateDaly())
        pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            guild = member.guild

            if not Saver.fetch(f"SELECT * FROM ranking WHERE userID = {member.id} AND guildID = {guild.id}"):
                Saver.save(f"INSERT IGNORE INTO ranking (userID, guildID, xp, level, rate) VALUES ({member.id}, {guild.id}, 0, 0, {rateLimitXpDaily})")
                pass

            oldRate = Saver.fetch(f"SELECT rate FROM ranking WHERE userID = {member.id} AND guildID = {guild.id}")[0][0]
            if oldRate == None:
                Saver.save(f"UPDATE ranking SET rate = {rateLimitXpDaily} WHERE userID = {member.id} AND guildID = {guild.id}")
                oldRate = rateLimitXpDaily
            while True:
                oldRate = Saver.fetch(f"SELECT rate FROM ranking WHERE userID = {member.id} AND guildID = {guild.id}")[0][0]
                xp = Saver.fetch(f"SELECT xp FROM ranking WHERE userID = {member.id} AND guildID = {guild.id}")[0][0]
                rate = oldRate - 5
                newXP = xp + 5
                Saver.save(f"UPDATE ranking SET xp = {newXP} WHERE userID = {member.id} AND guildID = {guild.id}")
                Saver.save(f"UPDATE ranking SET rate = {rate} WHERE userID = {member.id} AND guildID = {guild.id}")

                highest_grade = None
                for grade, value in rankGrade.items():
                    if newXP >= value:
                        highest_grade = grade
                if highest_grade:
                    oldGrade = Saver.fetch(f"SELECT grade FROM ranking WHERE userID = {member.id} AND guildID = {guild.id}")[0][0]
                    if oldGrade != highest_grade:
                        Saver.save(f"UPDATE ranking SET grade = '{highest_grade}' WHERE userID = {member.id} AND guildID = {guild.id}")

                        with open(emojiFile, 'r') as f:
                            rankGradeEmoji = load(f)

                        liaison_name = tableLiaison.get(highest_grade)
                        if liaison_name:
                            emoji_id = rankGradeEmoji.get(liaison_name)
                        else:
                            Log.warn(f"Failed to get emoji id {highest_grade}")

                        mess = f"Congratulations {member.mention} :fire:, you have been promoted to grade **{highest_grade}** <:{liaison_name}:{emoji_id}> ! in {guild.name}."
                        await member.send(mess)
                        Log.log(f"GRADE on {guild.id} user {member.id} [+] {oldGrade} -> {highest_grade}")

                if rate <= 0:
                    rate = 0
                    Log.log(f"RATE LIMIT on {guild.id} user {member.id} [+] {oldRate} -> {rate}")
                    break
                Log.log(f"XP on {guild.id} user {member.id} [+] 5 -> {newXP}")
                await asyncio.sleep(60)
                if member.voice is None:
                    break
        except Exception as e:
            Log.warn("Failed to add XP on voice channel")
            Log.warn(e)
            return

    @commands.Cog.listener()
    async def resetRateDaly(self):
        try:
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                await asyncio.sleep(30)
                current_time = datetime.datetime.now().time()
                if current_time.hour == 00 and current_time.minute == 40:
                    print("Resetting rate limit")
                    Saver.save(f"UPDATE ranking SET rate = {rateLimitXpDaily}")
                    Log.log(f"RATE LIMIT RESET")
                    pass
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
                    Saver.save(f"UPDATE ranking SET rate = {rate} WHERE userID = {user.id} AND guildID = {guild.id}")
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

                        with open(emojiFile, 'r') as f:
                            rankGradeEmoji = load(f)

                        liaison_name = tableLiaison.get(highest_grade)
                        if liaison_name:
                            emoji_id = rankGradeEmoji.get(liaison_name)
                        else:
                            Log.warn(f"Failed to get emoji id {highest_grade}")

                        mess = f"Congratulations {user.mention} :fire:, you have been promoted to grade **{highest_grade}** <:{liaison_name}:{emoji_id}> !"
                        await message.channel.send(mess)
                        Log.log(f"GRADE on {guild.id} user {user.id} [+] {oldGrade} -> {highest_grade}")

                if newXP > nextLevelXP:
                    newLevel = oldLevel + 1
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