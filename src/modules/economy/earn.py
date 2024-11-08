import datetime

import disnake
from disnake.ext import commands
from src.data.var import *
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver
from src.modules.managements.userinfo import Userinfo
from main import bot


class Earn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /earn has been loaded')

    @commands.slash_command(name="earn", description="Earn some coins")
    async def earn(self, ctx):
        try:
            user = ctx.author
            guild = ctx.guild

            coinEarn = 100

            try:
                data = Saver.fetch(f"SELECT * FROM economy WHERE userID = {user.id} AND guildID = {guild.id};")
                if not data:
                    Saver.save(f"INSERT INTO economy (guildID, userID, coins, cooldown) VALUES ({guild.id}, {user.id}, 0, 0);")
                    pass
            except Exception as e:
                Log.warn("Failed to insert user into economy table")
                Log.warn(e)
                return await ctx.send(embed=error(e))

            userData = Saver.fetch(f"SELECT * FROM economy WHERE userID = {user.id} AND guildID = {guild.id};")[0]
            userBal = userData[3]
            userLastEarn = userData[4]
            timeNow = int(datetime.datetime.now().timestamp())
            cooldownPeriod = 2 * 60 * 60

            if timeNow - userLastEarn < cooldownPeriod:
                remainingTime = cooldownPeriod - (timeNow - userLastEarn)
                hours, remainder = divmod(remainingTime, 3600)
                minutes, seconds = divmod(remainder, 60)
                embed = disnake.Embed(
                    title="⏳ Cooldown",
                    description=f"You need to wait `{int(hours)}h {int(minutes)}m {int(seconds)}s` before earning again.",
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            if userBal is None:
                userBal = 0

            userBal += coinEarn

            try:
                Saver.save(f"UPDATE economy SET coins = {userBal}, cooldown = {timeNow} WHERE userID = {user.id} AND guildID = {guild.id};")
                embed = disnake.Embed(
                    title="💸 Earn Coins 💸",
                    description=f"You earned `{coinEarn}` coins! 💰\nTotal coins: `{userBal}`",
                    color=disnake.Color.blurple()
                )
                await ctx.send(embed=embed)
            except Exception as e:
                Log.warn("Failed to update user coins")
                Log.warn(e)
                return await ctx.send(embed=error(e))
            Log.log(f"COINS on {guild.id} user {user.id} [+] {coinEarn} -> {userBal}")
        except Exception as e:
            Log.error("An error occurred while executing /earn command")
            Log.error(e)
            embed = error(e)
            await ctx.send(embed=embed)
            return

def setup(bot):
    bot.add_cog(Earn(bot))
