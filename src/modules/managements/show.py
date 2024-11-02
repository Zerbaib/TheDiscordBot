import disnake
from disnake.ext import commands
from src.data.var import keys
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

class Show(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /show has been loaded')
        pass
    
    @commands.slash_command(name="show", description="Show the bot's configuration")
    async def show(self, ctx):
        try:
            user = ctx.author
            guild = ctx.guild
            
            if not Saver.fetch(f"SELECT * FROM guilds WHERE guild_id = {guild.id}"):
                Saver.save(f"INSERT INTO guilds (guild_id, ticket_category, support_role, welcome_channel, leave_channel) VALUES ({guild.id}, 0, 0, 0, 0)")
            
            config = Saver.fetch(f"SELECT * FROM guilds WHERE guild_id = {guild.id}")[0]
            
            server_name = guild.name
            ticket_category = guild.get_channel(config[2]).mention if config[2] else '``None``'
            support_role = guild.get_role(config[3]).mention if config[3] else '``None``'
            welcome_channel = guild.get_channel(config[4]).mention if config[4] else '``None``'
            leave_channel = guild.get_channel(config[5]).mention if config[5] else '``None``'
            
            message = f"**Server Name:** {server_name}\n**Ticket Category:** {ticket_category}\n**Support Role:** {support_role}\n**Welcome Channel:** {welcome_channel}\n**Leave Channel:** {leave_channel}"
            
            embed = disnake.Embed(
                title="🔧 Configuration",
                description=message,
                color=disnake.Color.blurple()
            )
            embed.set_thumbnail(url=guild.icon.url)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error(e)
            Log.error("Failed to execute /show")
            Log.error(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Show(bot))