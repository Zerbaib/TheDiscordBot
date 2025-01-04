import datetime

import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver
from src.utils.lang import get_language_file

class Earn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "economy"

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /earn has been loaded')

    @commands.slash_command(name="earn", description="Earn some coins")
    async def earn(self, ctx):
        try:
            lang = get_language_file(ctx.guild.preferred_locale)
            user = ctx.author
            guild = ctx.guild
            presision = [f"userID = {user.id}", f"guildID = {guild.id}"]

            coinEarn = 100

            try:
                data = Saver.fetch(self.dataTable, presision)
                if not data:
                    data = {
                        "userID": user.id,
                        "guildID": guild.id,
                        "coins": 0,
                        "cooldown": 0
                    }
                    Saver.save(self.dataTable, data)
                    pass
            except Exception as e:
                Log.warn("Failed to insert user into economy table")
                Log.warn(e)
                return await ctx.send(embed=error(e))

            userData = Saver.fetch(self.dataTable, presision)[0]
            userBal = userData[3]
            userLastEarn = userData[4]
            timeNow = int(datetime.datetime.now().timestamp())
            cooldownPeriod = 2 * 60 * 60

            if timeNow - userLastEarn < cooldownPeriod:
                remainingTime = cooldownPeriod - (timeNow - userLastEarn)
                hours, remainder = divmod(remainingTime, 3600)
                minutes, seconds = divmod(remainder, 60)
                embed = disnake.Embed(
                    title=lang["Economy"]["earn"]["cooldown"]["title"],
                    description=lang["Economy"]["earn"]["cooldown"]["description"].format(hours=hours, minutes=minutes, seconds=seconds),
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            if userBal is None:
                userBal = 0

            userBal += coinEarn

            try:
                Saver.update(self.dataTable, presision, {"coins": userBal, "cooldown": timeNow})
                embed = disnake.Embed(
                    title=lang["Economy"]["earn"]["title"],
                    description=lang["Economy"]["earn"]["description"].format(coinEarn=coinEarn, userBal=userBal),
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
