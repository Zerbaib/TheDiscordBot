import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

class ServerList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /serverlist has been loaded')
        pass

    @commands.slash_command(name="serverlist", description="Get the list of servers where the bot is in")
    @commands.is_owner()
    async def serverlist(self, ctx):
        try:
            servers = self.bot.guilds
            serverList = []
            for server in servers:
                serverList.append(f"{server.name} - {server.id} - {server.member_count} members")
            if len(serverList) > 10:
                embed = disnake.Embed(
                    title="📜 Server List",
                    description="There are too many servers to display. Please check the console for the list.",
                    color=disnake.Color.green()
                )
                await ctx.send(embed=embed, ephemeral=True)
                Log.info("Server List:")
                for server in serverList:
                    Log.info(server)
            else:
                embed = disnake.Embed(
                    title="📜 Server List",
                    description="\n".join(serverList),
                    color=disnake.Color.green()
                )
                await ctx.send(embed=embed, ephemeral=True)
        except Exception as e:
            Log.error("Failed to execute /serverlist")
            Log.error(e)
            return await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(ServerList(bot))