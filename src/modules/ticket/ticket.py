import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

def get_guild_config(guild_id):
    try:
        data = Saver.fetch(f"SELECT * FROM guilds WHERE guild_id = {guild_id}")
        if data:
            return data[0]
        return False
    except Exception as e:
        Log.error(e)
        return

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /ticket has been loaded')
        pass

    @commands.slash_command(name="ticket", description="Open a support ticket")
    async def ticket(self, ctx):
        try:
            user = ctx.author
            guild = ctx.guild
            if not get_guild_config(guild.id):
                embed = disnake.Embed(
                    title='Error',
                    description='The bot has not been configured yet. Use `/set` to configure it.',
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            config = get_guild_config(guild.id)
            support_role = guild.get_role(config[1])  # Assuming 'support_role' is the second element
            category = guild.get_channel(config[2])  # Assuming 'ticket_category' is the third element

            for channel in category.channels:
                if channel.name == f"ticket-{user.id}":
                    await ctx.send("You already have an open ticket.", ephemeral=True)
                    return

            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                user: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                support_role: disnake.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{user.name}",
                category=category,
                overwrites=overwrites
            )
            await ticket_channel.send(f"{user.mention} Thank you for opening a ticket! A support member will respond shortly.")
            await ctx.send(f"Your ticket has been created: {ticket_channel.mention}", ephemeral=True)
            Log.log(f'TICKET on {guild.id} [+] {user.name} has opened a ticket.')
        except Exception as e:
            Log.error(e)
            await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(TicketSystem(bot))