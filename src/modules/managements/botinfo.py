from datetime import datetime, timezone
from src.data.var import files
import disnake
from disnake.ext import commands
import src.data.var
from src.utils.error import error_embed as error
from src.utils.logger import Log
from main import bot


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /botinfo has been loaded')
        pass

    @commands.slash_command(name="botinfo", description="Get information about the bot")
    async def botinfo(self, ctx):
        try:
            bot = self.bot
            embed = disnake.Embed(
                title=f"Bot Info - {bot.user.name}",
                color=disnake.Color.blue(),
                timestamp=datetime.now(timezone.utc)
            )

            owner = bot.get_user(bot.owner_id) or await bot.fetch_user(bot.owner_id)
            with open(files["version"], "r") as f:
                version = f.read().strip()

            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.add_field(name="Bot ID", value=f"```{bot.user.id}```", inline=True)
            embed.add_field(name="Bot Version", value=f"```{version}```", inline=True)
            embed.add_field(name="Owner", value=owner.display_name, inline=False)
            embed.add_field(name="Servers", value=f"```{len(bot.guilds)}```", inline=True)
            embed.add_field(name="Users", value=f"```{len(bot.users)}```", inline=True)
            embed.add_field(name="Slash Commands", value=f"```{len(bot.slash_commands)}```", inline=True)
            embed.add_field(name="Created At", value=f"```{bot.user.created_at.strftime("%Y-%m-%d %H:%M:%S")}```", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed, ephemeral=True)
        except Exception as e:
            Log.error("Failed to get server information")
            Log.error(e)
            return await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(BotInfo(bot))