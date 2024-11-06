import disnake
from disnake.ext import commands
from datetime import datetime
from src.utils.logger import Log
from src.utils.error import error_embed as error

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /serverinfo has been loaded')
        pass
    
    @commands.slash_command(name="serverinfo", description="Get information about the server")
    async def serverinfo(self, ctx):
        try:
            guild = ctx.guild
            embed = disnake.Embed(
                title=f"Server Info - {guild.name}",
                color=disnake.Color.blue(),
                timestamp=datetime.utcnow()
            )
            
            embed.set_thumbnail(url=guild.icon.url)
            embed.add_field(name="Server ID", value=guild.id, inline=True)
            embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
            embed.add_field(name="Members", value=guild.member_count, inline=True)
            embed.add_field(name="Roles", value=len(guild.roles), inline=True)
            embed.add_field(name="Emojis", value=len(guild.emojis), inline=True)
            embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)
            embed.add_field(name="Region", value=guild.region, inline=True)
            embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed, ephemeral=True)
        except Exception as e:
            Log.error("Failed to get server information")
            Log.error(e)
            return await ctx.send(embed=error(e))
    
def setup(bot):
    bot.add_cog(ServerInfo(bot))