import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.support_role_id = 1301779175849463840  # Remplace par l'ID de ton rôle support
        self.ticket_category_id = 1301782400170201160  # ID de la catégorie pour les tickets

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /ticket has been loaded')
        pass

    @commands.slash_command(name="ticket", description="Ouvre un ticket d'assistance")
    async def ticket(self, ctx):
        user = ctx.author
        guild = ctx.guild
        support_role = guild.get_role(self.support_role_id)
        category = guild.get_channel(self.ticket_category_id)

        # Vérifie si l'utilisateur a déjà un ticket ouvert
        for channel in category.channels:
            if channel.name == f"ticket-{user.id}":
                await ctx.send("Vous avez déjà un ticket ouvert.", ephemeral=True)
                return

        # Crée un canal pour le ticket
        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            user: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
            support_role: disnake.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            category=category,
            overwrites=overwrites
        )
        await ticket_channel.send(f"{user.mention} Merci d'avoir ouvert un ticket ! Un membre du support vous répondra sous peu.")
        await ctx.send(f"Votre ticket a été créé : {ticket_channel.mention}", ephemeral=True)

def setup(bot):
    bot.add_cog(TicketSystem(bot))