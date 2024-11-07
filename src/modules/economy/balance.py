import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /balance has been loaded')
        pass

    @commands.slash_command(name="balance", description="Check your balance")
    async def balance(self, ctx):
        try:
            user = ctx.author
            guild = ctx.guild

            if not Saver.fetch(f"SELECT coins FROM economy WHERE userID = {user.id} AND guildID = {guild.id}"):
                Saver.save(f"INSERT INTO economy (userID, guildID, coins, cooldown) VALUES ({user.id}, {guild.id}, 0, 0)")
                pass

            userBal = Saver.fetch(f"SELECT coins FROM economy WHERE userID = {user.id} AND guildID = {guild.id}")[0][0]

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