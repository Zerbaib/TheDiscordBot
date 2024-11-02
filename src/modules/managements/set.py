import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /set has been loaded')
        pass
    
    @commands.slash_command(name="set", description="Configure the bot")
    async def set(self, inter: disnake.ApplicationCommandInteraction, key: str, value):
        try:
            try:
                value = int(value)
            except:
                embed = disnake.Embed(
                    title='Error',
                    description='Value must be an integer.',
                    color=disnake.Color.red()
                )
                await inter.response.send_message(embed=embed)
                return
            user = inter.author
            keys = {
                'ticket_category': 'Ticket Category',
                'support_role': 'Support Role',
                'welcome_channel': 'Welcome Channel',
                'leave_channel': 'Leave Channel'
            }
            
            if not user.guild_permissions.administrator:
                embed = disnake.Embed(
                    title='Error',
                    description='You must have the `Administrator` permission to use this command.',
                    color=disnake.Color.red()
                )
                await inter.response.send_message(embed=embed, ephemeral=True)
                return
            
            if key not in keys:
                embed = disnake.Embed(
                    title='Error',
                    description=f'Invalid key. Available keys: {", ".join(keys.keys())}\nExample: `/set ticket_category 123456789012345678`',
                    color=disnake.Color.red()
                )
                await inter.response.send_message(embed=embed, ephemeral=True)
                return
            
            if not Saver.fetch(f"SELECT * FROM guilds WHERE guild_id = {inter.guild.id}"):
                Saver.save(f"INSERT INTO guilds (guild_id, ticket_category, support_role, welcome_channel, leave_channel) VALUES ({inter.guild.id}, 0, 0, 0, 0)")
            
            Saver.save(f"UPDATE guilds SET {key} = '{value}'")
            embed = disnake.Embed(
                title='Success',
                description=f'{keys[key]} has been set to ``{value}``.',
                color=disnake.Color.green()
            )
            data = Saver.fetch(f"SELECT * FROM guilds WHERE guild_id = {inter.guild.id}")[0]
            categoryName = inter.guild.get_channel(data[1]).name if data[2] else 'None'
            supportRoleName = inter.guild.get_role(data[2]).name if data[3] else 'None'
            welcomeChannelName = inter.guild.get_channel(data[3]).name if data[4] else 'None'
            leaveChannelName = inter.guild.get_channel(data[4]).name if data[5] else 'None'
            embed.add_field(name='Configuration', value=f"Ticket Category: {categoryName}\nSupport Role: {supportRoleName}\nWelcome Channel: {welcomeChannelName}\nLeave Channel: {leaveChannelName}")
            await inter.response.send_message(embed=embed)
            Log.log(f'SETTING on {inter.guild.id} [+] {keys[key]} has been set to {value}.')
        except Exception as e:
            Log.error("Failed to execute /set")
            Log.error(e)
            await inter.response.send_message(embed=error(e))

def setup(bot):
    bot.add_cog(Set(bot))