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
            userS = ctx.author
            guild = ctx.guild
            presision = [f"userID = {userS.id}", f"guildID = {guild.id}"]

            if userS == user:
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

            if not Saver.fetch(self.dataTable, presision, "coins"):
                data = {
                    "userID": userS.id,
                    "guildID": guild.id,
                    "coins": 0,
                    "cooldown": 0
                }
                Saver.save(self.dataTable, data)
                embed = disnake.Embed(
                    title="❌ Error",
                    description="You don't have enough coins.",
                    color=disnake.Color.red()
                )
                pass
            if not Saver.fetch(self.dataTable, [f"userID = {user.id}", f"guildID = {guild.id}"], "coins"):
                Saver.save(self.dataTable, {"userID": user.id, "guildID": guild.id, "coins": 0, "cooldown": 0})
                pass

            userSBal = Saver.fetch(self.dataTable, presision, "coins")[0][0]
            userBal = Saver.fetch(self.dataTable, [f"userID = {user.id}", f"guildID = {guild.id}"], "coins")[0][0]

            if userSBal < amount:
                embed = disnake.Embed(
                    title="❌ Error",
                    description="You don't have enough coins.",
                    color=disnake.Color.red()
                )
                return
            try:
                userSBal -= amount
                userBal += amount
                Saver.update(self.dataTable, presision, {"coins": userSBal})
                Saver.update(self.dataTable, [f"userID = {user.id}", f"guildID = {guild.id}"], {"coins": userBal})

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
            Log.log(f"COINS on {guild.id} user {userS.id} [{userSBal} - {amount}] to {user.id} -> {userBal}")
        except Exception as e:
            Log.error(e)
            await ctx.send(embed=error("An error occurred."))
            return

def setup(bot):
    bot.add_cog(Pay(bot))