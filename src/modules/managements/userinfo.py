from datetime import datetime

import disnake
from disnake import Member
from disnake.ext import commands
from src.utils.logger import Log


class Userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /userinfo has been loaded')
        pass

    @commands.slash_command(name="userinfo", description="Get information about a user")
    async def userinfo(self, ctx, member: Member = None):
        if member is None:
            member = ctx.author

        # Obtenez les informations de l'utilisateur
        embed = disnake.Embed(
            title=f"User Info - {member.display_name}",
            color=member.color,
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick if member.nick else "None", inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Userinfo(bot))