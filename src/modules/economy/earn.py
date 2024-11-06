import datetime

import disnake
from disnake.ext import commands
from src.data.var import *
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


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
            userID = user.id
            try:
                result = Saver.fetch(f"SELECT cooldown FROM economy WHERE userID = {userID} AND guildID = {ctx.guild.id}")
                userLastEarn = result[0][0] if result else 0
            except Exception as e:
                if "list index out of range" in str(e):
                    userLastEarn = 0
            guild = ctx.guild
            guildID = guild.id
            timeNow = int(datetime.datetime.now().timestamp())
            cooldown_period = 2 * 60 * 60

            if not result:
                print("is None")
                Saver.save(f"INSERT INTO economy (guildID, userID, coins, cooldown) VALUES ({guildID}, {userID}, 0, {timeNow})")
                print("inserted")
                userLastEarn = 0

            if timeNow - userLastEarn < cooldown_period:
                remaining_time = cooldown_period - (timeNow - userLastEarn)
                hours, remainder = divmod(remaining_time, 3600)
                minutes, seconds = divmod(remainder, 60)
                embed = disnake.Embed(
                    title="⏳ Cooldown",
                    description=f"You need to wait `{int(hours)}h {int(minutes)}m {int(seconds)}s` before earning again.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            coinEarn = 100
            Saver.save(f"UPDATE economy SET cooldown = {timeNow} WHERE userID = {userID} AND guildID = {guildID}")

            userData = Saver.fetch(f"SELECT * FROM economy WHERE userID = {userID} AND guildID = {guildID}")
            print(userData)
            userBal = Saver.fetch(f"SELECT coins FROM economy WHERE userID = {userID} AND guildID = {guildID}")[0][0]

            userBal += coinEarn

            try:
                Saver.save(f"UPDATE economy SET coins = {userBal} WHERE userID = {userID} AND guildID = {guildID}")
                embed = disnake.Embed(
                    title="💸 Earn Coins 💸",
                    description=f"You earned `{coinEarn}` coins! 💰\nTotal coins: `{userBal}`",
                    color=disnake.Color.blurple()
                )
                await ctx.send(embed=embed)
            except Exception as e:
                Log.warn("Failed to update user coins")
                Log.warn(e)
                embed = error(e)
                await ctx.send(embed=embed)
                return

            Log.log(f"COINS on {guildID} user {userID} [+] {coinEarn} -> {userBal}")

        except Exception as e:
            Log.error("An error occurred while executing /earn command")
            Log.error(e)
            embed = error(e)
            await ctx.send(embed=embed)
            return

def setup(bot):
    bot.add_cog(Earn(bot))
