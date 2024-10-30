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
            userID = user.id
            guild = ctx.guild
            guildID = guild.id

            if not Saver.fetch(f"SELECT coins FROM economy WHERE userID = {userID} AND guildID = {guildID}"):
                Saver.save(f"INSERT INTO economy (userID, guildID, coins, cooldown) VALUES ({userID}, {guildID}, 0, 0)")
                pass

            userBal = Saver.fetch(f"SELECT coins FROM economy WHERE userID = {userID} AND guildID = {guildID}")[0][0]

            message = f"Your balance is `{userBal}` coins"
            embed = disnake.Embed(
                title="💰 Balance",
                description=message,
                color=disnake.Color.blurple()
                )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error(e)
            Log.error("Failed to execute /balance")
            Log.error(e)
            await ctx.send(embed=embed)
            return

def setup(bot):
    bot.add_cog(Balance(bot))