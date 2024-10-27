import disnake
from disnake.ext import commands
from src.utils.logger import Log

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /ping has been loaded')

    @commands.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx):
        try:
            embed = disnake.Embed(
                title="🏓 Pong!",
                description=f"Latency: {round(self.bot.latency * 1000)}ms",
                color=disnake.Color.blurple()
                )
            await ctx.response.defer()
            await ctx.send(ephemeral=True, embed=embed)
        except Exception as e:
            #embed = error.error_embed(e)
            Log.error(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PingCommand(bot))