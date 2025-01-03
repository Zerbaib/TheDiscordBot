import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver
from src.utils.lang import get_language_file


class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "economy"

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /pay has been loaded')

    @commands.slash_command(name="pay", description="Pay someone")
    async def pay(self, ctx, user: disnake.User, amount: int):
        try:
            lang = get_language_file(ctx.guild.preferred_locale)
            userSender = ctx.author
            userReciever = user
            guild = ctx.guild
            precisionSender = [f"userID = {userSender.id}", f"guildID = {guild.id}"]
            precisionReciever = [f"userID = {userReciever.id}", f"guildID = {guild.id}"]

            if userSender == userReciever:
                embed = disnake.Embed(
                    title=lang["Economy"]["pay"]["errors"]["title"],
                    description=lang["Economy"]["pay"]["errors"]["selfPay"],
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)
            if amount < 1:
                embed = disnake.Embed(
                    title=lang["Economy"]["pay"]["errors"]["title"],
                    description=lang["Economy"]["pay"]["errors"]["invalidAmount"],
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            userSenderAccount = Saver.fetch(self.dataTable, precisionSender)
            userRecieverAccount = Saver.fetch(self.dataTable, precisionReciever)

            if not userSenderAccount:
                userSenderAccount = {
                    "userID": userSender.id,
                    "guildID": guild.id,
                    "coins": 0,
                    "cooldown": 0
                }
                Saver.save(self.dataTable, userSenderAccount)
                embed = disnake.Embed(
                    title=lang["Economy"]["pay"]["errors"]["title"],
                    description=lang["Economy"]["pay"]["errors"]["noCoins"],
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)
            if not userRecieverAccount:
                userRecieverAccount = {
                    "userID": userReciever.id,
                    "guildID": guild.id,
                    "coins": 0,
                    "cooldown": 0
                }
                Saver.save(self.dataTable, userRecieverAccount)
                userRecieverBal = userRecieverAccount["coins"]
            else:
                userRecieverBal = userRecieverAccount[0][3]
            userSenderBal = userSenderAccount[0][3]

            if userSenderBal < amount:
                embed = disnake.Embed(
                    title=lang["Economy"]["pay"]["errors"]["title"],
                    description=lang["Economy"]["pay"]["errors"]["noCoins"],
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            try:
                Saver.query(f"UPDATE {self.dataTable} SET coins = CASE WHEN userID = {userSender.id} THEN coins - {amount} WHEN userID = {userReciever.id} THEN coins + {amount} END WHERE userID IN ({userSender.id}, {userReciever.id}) AND guildID = {guild.id}")

                embed = disnake.Embed(
                    title=lang["Economy"]["pay"]["title"],
                    description=lang["Economy"]["pay"]["description"].format(userR=user.mention, amount=amount, userSBal=userSenderBal-amount, userBal=userRecieverBal+amount),
                    color=disnake.Color.blurple()
                )
                await ctx.send(embed=embed)
            except Exception as e:
                Log.warn("Failed to update user coins")
                Log.warn(e)
                embed = error(e)
                return await ctx.send(embed=embed)
            Log.log(f"COINS on {guild.id} user {userSender.id} [{userSenderBal} - {amount}] to {user.id} -> {userRecieverBal}")
        except Exception as e:
            Log.error(e)
            await ctx.send(embed=error("An error occurred."))
            return

def setup(bot):
    bot.add_cog(Pay(bot))