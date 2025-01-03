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
            userS = ctx.author
            guild = ctx.guild
            presision = [f"userID = {userS.id}", f"guildID = {guild.id}"]

            if userS == user:
                embed = disnake.Embed(
                    title=lang["Economy"]["pay"]["errors"]["title"],
                    description=lang["Economy"]["pay"]["errors"]["selfPay"],
                    color=disnake.Color.red()
                )
                return

            if amount < 1:
                embed = disnake.Embed(
                    title=lang["Economy"]["pay"]["errors"]["title"],
                    description=lang["Economy"]["pay"]["errors"]["invalidAmount"],
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
                    title=lang["Economy"]["pay"]["errors"]["title"],
                    description=lang["Economy"]["pay"]["errors"]["noCoins"],
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
                    title=lang["Economy"]["pay"]["errors"]["title"],
                    description=lang["Economy"]["pay"]["errors"]["noCoins"],
                    color=disnake.Color.red()
                )
                return
            try:
                userSBal -= amount
                userBal += amount
                Saver.update(self.dataTable, presision, {"coins": userSBal})
                Saver.update(self.dataTable, [f"userID = {user.id}", f"guildID = {guild.id}"], {"coins": userBal})

                embed = disnake.Embed(
                    title=lang["Economy"]["pay"]["title"],
                    description=lang["Economy"]["pay"]["description"].format(userR=user.mention, amount=amount, userSBal=userSBal, userBal=userBal),
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