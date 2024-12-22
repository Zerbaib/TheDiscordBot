import os
import sys

import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log


class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /restart has been loaded')
        pass
    
    @commands.slash_command(name="restart", description="Restart the bot")
    @commands.is_owner()
    async def restart(self, ctx):
        try:
            embed = disnake.Embed(  
                title="🔄 Restarting",
                description="Restarting the bot...",
                color=disnake.Color.green()
            )
            
            await ctx.send(embed=embed, ephemeral=True)
            await self.bot.close()
            
            
            # Restart the bot
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            Log.error("Failed to execute /restart")
            Log.error(e)
            return await ctx.send(embed=error(e))
        
def setup(bot):
    bot.add_cog(Restart(bot))