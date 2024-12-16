import disnake
from disnake.ext import commands
from src.data.var import keys, keys_values
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

            if not user.guild_permissions.administrator:
                embed = disnake.Embed(
                    title='Error',
                    description='You must have the `Administrator` permission to use this command.',
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed, ephemeral=True)

            if not Saver.fetch(f"SELECT * FROM guilds WHERE guild_id = {guild.id}"):
                Saver.save(f"INSERT INTO guilds (guild_id, ticket_category, support_role, welcome_channel, leave_channel) VALUES ({guild.id}, 0, 0, 0, 0)")

            config = Saver.fetch(f"SELECT * FROM guilds WHERE guild_id = {guild.id}")[0]

            server_name = guild.name
            ticket_category = guild.get_channel(config[keys_values["ticket_category"]]).name if config[keys_values["ticket_category"]] and guild.get_channel(config[keys_values["ticket_category"]]) else 'None'
            supportRole = guild.get_role(config[keys_values["support_role"]])
            support_role = supportRole.mention if supportRole else '``None``'
            welcome_channel = guild.get_channel(config[keys_values["welcome_channel"]]).mention if config[keys_values["welcome_channel"]] and guild.get_channel(config[keys_values["welcome_channel"]]) else '``None``'
            leave_channel = guild.get_channel(config[keys_values["leave_channel"]]).mention if config[keys_values["leave_channel"]] and guild.get_channel(config[keys_values["leave_channel"]]) else '``None``'
            voice_table_channel = guild.get_channel(config[keys_values["voice_table_channel"]]).mention if config[keys_values["voice_table_channel"]] and guild.get_channel(config[keys_values["voice_table_channel"]]) else '``None``'
            message = f"**Server Name:** ``{server_name}``\n**Ticket Category:** ``#{ticket_category}``\n**Support Role:** {support_role}\n**Welcome Channel:** {welcome_channel}\n**Leave Channel:** {leave_channel}\n**Voice Table Channel:** {voice_table_channel}"

            embed = disnake.Embed(
                    title="🔧 Configuration",
                    description=message,
                    color=disnake.Color.blurple()
            )
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
            await ctx.send(embed=embed)
        except Exception as e:
            Log.error("Failed to execute /show")
            Log.error(e)
            await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(Show(bot))