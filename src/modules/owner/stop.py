import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log

class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /stop has been loaded')
        pass
    
    @commands.slash_command(name="stop", description="Stop the bot")
    async def stop(self, ctx):
        try:
            if ctx.author is not self.bot.owner:
                embed = disnake.Embed(
                    title="❌ Permission Denied",
                    description="You do not have permission to execute this command.",
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed, ephemeral=True)
            embed = disnake.Embed(
                title="🛑 Stopping",
                description="Stopping the bot...",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed, ephemeral=True)
            await self.bot.close()
        except Exception as e:
            Log.error("Failed to execute /stop")
            Log.error(e)
            return await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(Stop(bot))