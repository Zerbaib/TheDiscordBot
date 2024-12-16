import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

class InviteGet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /inviteget has been loaded')
        pass

    @commands.slash_command(name="inviteget", description="Get an invite link of a server where the bot is in")
    @commands.is_owner()
    async def inviteget(self, ctx, id: int):
        try:
            getServer = self.bot.get_guild(id)
            invite = await getServer.text_channels[0].create_invite(max_age=0, max_uses=0, unique=False)
            embed = disnake.Embed(
                title="🔗 Invite",
                description=f"Here is the invite link of the server: {invite}",
                color=disnake.Color.green()
            )
        except Exception as e:
            Log.error("Failed to execute /inviteget")
            Log.error(e)
            return await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(InviteGet(bot))