import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


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
            userSender = ctx.author
            userReciever = user
            guild = ctx.guild
            precisionSender = [f"userID = {userSender.id}", f"guildID = {guild.id}"]
            precisionReciever = [f"userID = {userReciever.id}", f"guildID = {guild.id}"]

            if userSender == userReciever:
                embed = disnake.Embed(
                    title="❌ Error",
                    description="You can't pay yourself.",
                    color=disnake.Color.red()
                )
                return
            if amount < 1:
                embed = disnake.Embed(
                    title="❌ Error",
                    description="You can't pay less than 1 coin.",
                    color=disnake.Color.red()
                )
                return

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
                    title="❌ Error",
                    description="You don't have enough coins.",
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
                userRecieverBal = userRecieverAccount[0]
            else:
                userRecieverBal = userRecieverAccount[0][0]

            userSenderBal = userSenderAccount[0][0]

            if userSenderBal < amount:
                embed = disnake.Embed(
                    title="❌ Error",
                    description="You don't have enough coins.",
                    color=disnake.Color.red()
                )
                return
            try:
                userSBal -= amount
                userBal += amount
                Saver.update(self.dataTable, precisionSender, {"coins": userSenderBal})
                Saver.update(self.dataTable, precisionReciever, {"coins": userRecieverBal})

                embed = disnake.Embed(
                    title="💸 Paid",
                    description=f"You paid {user.mention} `{amount}` coins!\nYour balance: `{userSBal}`\n{user.mention}'s balance: `{userBal}`",
                    color=disnake.Color.blurple()
                )
            except Exception as e:
                Log.warn("Failed to update user coins")
                Log.warn(e)
                embed = error(e)
                return
            await ctx.send(embed=embed)
            Log.log(f"COINS on {guild.id} user {userSender.id} [{userSenderBal} - {amount}] to {user.id} -> {userRecieverBal}")
        except Exception as e:
            Log.error(e)
            await ctx.send(embed=error("An error occurred."))
            return

def setup(bot):
    bot.add_cog(Pay(bot))