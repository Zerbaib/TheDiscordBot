import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "economy"

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /balance has been loaded')
        pass

    @commands.slash_command(name="balance", description="Check your balance")
    async def balance(self, ctx):
        try:
            user = ctx.author
            guild = ctx.guild
            presision = [f"userID = {user.id}", f"guildID = {guild.id}"]

            if not Saver.fetch(self.dataTable, presision):
                data = {
                    "userID": user.id,
                    "guildID": guild.id,
                    "coins": 0,
                    "cooldown": 0
                }
                Saver.save(self.dataTable, data)
                pass

            userBal = Saver.fetch(self.dataTable, presision, "coins")[0][0]

            embed = disnake.Embed(
                title="💰 Balance 💰",
                description=f"Your balance is `{userBal}` coins",
                color=disnake.Color.blurple()
                )
            await ctx.send(embed=embed)
        except Exception as e:
            Log.error("Failed to execute /balance")
            Log.error(e)
            return await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(Balance(bot))