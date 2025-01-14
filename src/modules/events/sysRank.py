import asyncio
import datetime
import random
from json import load

import disnake
from disnake.ext import commands
from src.data.var import files, rateLimitXpDaily, get_rank_info_config
from src.utils.logger import Log
from src.utils.saver import Saver


class sysRank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTables = "ranking"
        self.tableLiaison = get_rank_info_config("liaison")
        self.rankGrade = get_rank_info_config("grade")

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info("🧰 Ranking system has been loaded")
        self.bot.loop.create_task(self.resetRateDaly())
        pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if member.bot:
                return
            guild = member.guild
            presision = [f"guildID = {guild.id}", f"userID = {member.id}"]
            channel = after.channel

            if not Saver.fetch(self.dataTables, presision):
                data = {
                    "guildID": guild.id,
                    "userID": member.id,
                    "xp": 0,
                    "level": 0,
                    "rate": rateLimitXpDaily
                }
                Saver.save(self.dataTables, data)
                pass

            oldRate = Saver.fetch(self.dataTables, presision, "rate")[0][0]
            if oldRate == None:
                Saver.update(self.dataTables, presision, {"rate": rateLimitXpDaily})
                oldRate = rateLimitXpDaily
            while True:
                oldRate = Saver.fetch(self.dataTables, presision, "rate")[0][0]
                xp = Saver.fetch(self.dataTables, presision, "xp")[0][0]
                rate = oldRate - 5
                newXP = xp + 5
                Saver.update(self.dataTables, presision, {"rate": rate})

                if rate <= 0:
                    rate = 0
                    Saver.update(self.dataTables, presision, {"rate": rate})
                    Log.log(f"RATE LIMIT on {guild.id} user {member.id} [+] {oldRate} -> {rate}")
                    break
                else:
                    Saver.update(self.dataTables, presision, {"xp": newXP})
                    Log.log(f"XP on {guild.id} user {member.id} [+] 5 -> {newXP}")
                    pass

                highest_grade = None
                for grade, value in self.rankGrade.items():
                    if newXP >= value:
                        highest_grade = grade
                if highest_grade:
                    oldGrade = Saver.fetch(self.dataTables, presision, "grade")[0][0]
                    if oldGrade != highest_grade:
                        Saver.update(self.dataTables, presision, {"grade": highest_grade})

                        with open(files["emojis"], 'r') as f:
                            rankGradeEmoji = load(f)

                        liaison_name = self.tableLiaison.get(highest_grade)
                        if liaison_name:
                            emoji_id = rankGradeEmoji.get(liaison_name)
                        else:
                            Log.warn(f"Failed to get emoji id {highest_grade}")

                        mess = f"Congratulations {member.mention} :fire:, you have been promoted to grade **{highest_grade}** <:{liaison_name}:{emoji_id}> !"
                        await channel.send(mess)
                        Log.log(f"GRADE on {guild.id} user {member.id} [+] {oldGrade} -> {highest_grade}")
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
                await asyncio.sleep(50)
                currentTime = datetime.datetime.now().time()
                if currentTime.hour == 6 and currentTime.minute == 00:
                    usersData = Saver.fetch(self.dataTables, ["userID", "xp", "rate"])
                    for userData in usersData:
                        userId, xp, rate = userData
                        if xp < 50:
                            xp = xp - 0
                        elif xp < 100:
                            xp = xp - 10
                        elif xp < 500:
                            xp = xp - 50
                        elif xp < 1000:
                            xp = xp - 100
                        elif xp < 2500:
                            xp = xp - 150
                        else:
                            xp = xp - 200
                        if xp < 0:
                            xp = 0
                        grade = None
                        for g, value in self.rankGrade.items():
                            if xp >= value:
                                grade = g
                        if grade:
                            Saver.update(self.dataTables, [f"userID = {userId}"], {"grade": grade})
                        Save.update(self.dataTables, [f"userID = {userId}"], {"xp": xp, "rate": rateLimitXpDaily})
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
                presision = [f"guildID = {guild.id}", f"userID = {user.id}"]
                usrData = Saver.fetch(self.dataTables, presision, ["xp", "level", "rate"])

                if not usrData:
                    data = {
                        "guildID": guild.id,
                        "userID": user.id,
                        "xp": 0,
                        "level": 0,
                        "rate": rateLimitXpDaily
                    }
                    Saver.save(self.dataTables, data)
                    oldRate = rateLimitXpDaily
                    oldXP = 0
                    oldLevel = 0
                    pass
                else:
                    oldXP = usrData[0][0]
                    oldLevel = usrData[0][1]
                    oldRate = usrData[0][2]

                if oldRate == None:
                    Saver.update(self.dataTables, presision, {"rate": rateLimitXpDaily})
                    oldRate = rateLimitXpDaily
                xpWin = random.randint(1, 5)
                newXP = oldXP + xpWin
                rate = oldRate - xpWin
                Saver.update(self.dataTables, presision, {"rate": rate, "xp": newXP})
                if rate <= 0:
                    rate = 0
                    Saver.update(self.dataTables, presision, {"rate": rate})
                    Log.log(f"RATE LIMIT on {guild.id} user {user.id} [+] {oldRate} -> {rate}")
                    return


                nextLevelXP = 5 * (oldLevel ** 2) + 10 * oldLevel + 10

                highest_grade = None
                for grade, value in self.rankGrade.items():
                    if newXP >= value:
                        highest_grade = grade
                if highest_grade:
                    oldGrade = Saver.fetch(self.dataTables, presision, "grade")[0][0]
                    if oldGrade != highest_grade:
                        Saver.update(self.dataTables, presision, {"grade": highest_grade})

                        with open(files["emojis"], 'r') as f:
                            rankGradeEmoji = load(f)

                        liaison_name = self.tableLiaison.get(highest_grade)
                        if liaison_name:
                            emoji_id = rankGradeEmoji.get(liaison_name)
                        else:
                            Log.warn(f"Failed to get emoji id {highest_grade}")

                        mess = f"Congratulations {user.mention} :fire:, you have been promoted to grade **{highest_grade}** <:{liaison_name}:{emoji_id}> !"
                        await message.channel.send(mess)
                        Log.log(f"GRADE on {guild.id} user {user.id} [+] {oldGrade} -> {highest_grade}")

                if newXP > nextLevelXP:
                    newLevel = oldLevel + 1
                    Saver.update(self.dataTables, presision, {"level": newLevel})
                    Log.log(f"LEVEL on {guild.id} user {user.id} [+] {oldLevel} -> {newLevel}")
                    pass
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