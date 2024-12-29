import random
import time

import disnake
from disnake.ext import commands
from src.data.var import *
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


class Caster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "economy"

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /caster has been loaded')
        pass

    @commands.slash_command(name="caster", description="nothing goes anymore")
    async def caster(self, ctx, choice, bet: int):
        try:
            casesP = ["00", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"]
            choices = ["even", "odd", "red", "black", "00", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"]
            user = ctx.author
            guild = ctx.guild
            presision = [f"userID = {user.id}", f"guildID = {guild.id}"]

            if bet < 1:
                embed = disnake.Embed(
                    title="🚫 Invalid Bet",
                    description="You can't bet less than 1 coin.",
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            if not Saver.fetch(self.dataTable, presision):
                data = {
                    "guildID": guild.id,
                    "userID": user.id,
                    "coins": 0
                }
                Saver.save(self.dataTable, data)
                embed = disnake.Embed(
                    title="🔩 Economy Account Created",
                    description="You have been registered to the economy system.",
                    color=disnake.Color.green()
                )
                await ctx.send(embed=embed)
                return

            userBal = Saver.fetch(self.dataTable, presision, "coins")[0][0]

            if userBal < bet:
                embed = disnake.Embed(
                    title="🚫 Insufficient Balance",
                    description="You don't have enough coins to bet.",
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            if not choice.lower() in choices:
                embed = disnake.Embed(
                    title="🚫 Invalid Choice",
                    description="Please choose a valid option.",
                    color=disnake.Color.red()
                )
                embed.add_field(name="Choices", value="even, odd, red, black, 00, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32")
                return await ctx.send(embed=embed)

            if choice.lower() not in casesP:
                if choice.lower() == "odd":
                    cases = ["1", "3", "5", "7", "9", "11", "13", "15", "17", "19", "21", "23", "25", "27", "29", "31"]
                    multiplier = 2
                elif choice.lower() == "even":
                    cases = ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30", "32"]
                    multiplier = 2
                elif choice.lower() == "red":
                    cases = ["1", "3", "5", "7", "9", "12", "14", "16", "18", "19", "21", "23", "25", "27", "30", "32"]
                    multiplier = 2
                elif choice.lower() == "black":
                    cases = ["2", "4", "6", "8", "10", "11", "13", "15", "17", "20", "22", "24", "26", "28", "29", "31"]
                    multiplier = 2
            else:
                multiplier = 36
                cases = [choice.lower()]

            embed = disnake.Embed(
                title="nothing goes anymore",
                description=f"It's turning...",
                color=disnake.Color.blurple()
            )
            embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExczR2ZW1vM2lkeGZmZ2tkMDVmZDQ3azNpZ3Z0ZXpsM2w5MzNhYnNrOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26uf2YTgF5upXUTm0/giphy.gif")
            await ctx.send(embed=embed, delete_after=4)

            userBal -= bet
            result = random.choice(casesP)
            if result in cases:
                userBal += bet * multiplier
                embed = disnake.Embed(
                    title="🎉 You won!",
                    description=f"The result is `{result}`.\nYou won `{bet * multiplier}` coins!\nGongrats {user.mention}!",
                    color=disnake.Color.green()
                )
                embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHNnMXhrMW1yd3R1Z2ltdGEzOW54bHJrOTV3NjR2OHJoamV4M3gweCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o6Mb5XHOPtD2qT4RO/giphy.gif")
            else:
                embed = disnake.Embed(
                    title="🎉 You lost!",
                    description=f"The result is `{result}`.\nYou lost `{bet}` coins!",
                    color=disnake.Color.red()
                )
                embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHJvejVwNjZscnpteWd2YTlpZWczOXY2MzhmeGVleW5nZ3VkMjBraCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26uflBhaGt5lQsaCA/giphy.gif")
            Saver.update(self.dataTable, presision, {"coins": userBal})
            time.sleep(4)

            embed.set_footer(text=f"User: {user.display_name} | Balance: {userBal} coins")
            await ctx.send(embed=embed)
            Log.log(f"CASINO on {guild.id} user {user.id} [{choice}] {result} -> {userBal}")
        except Exception as e:
            await ctx.send(embed=error(e))
            Log.error(e)
            return

def setup(bot):
    bot.add_cog(Caster(bot))