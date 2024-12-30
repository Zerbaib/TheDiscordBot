import disnake
from disnake.ext import commands
from src.data.var import keys, keys_values
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
    async def set(self, inter: disnake.ApplicationCommandInteraction, key=None, value=None):
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
        try:
            key = str(key)
        except:
            embed = disnake.Embed(
                title='Error',
                description='Key must be a string.',
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed)
            return
        try:
            user = inter.author
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

            if not Saver.fetch("guilds", [f"guild_id = {inter.guild.id}"]):
                data = {
                    "guild_id": inter.guild.id,
                    "ticket_category": 0,
                    "support_role": 0,
                    "welcome_channel": 0,
                    "leave_channel": 0,
                    "voice_table_channel": 0
                }
                Saver.save("guilds", data)

            Saver.update(f"guilds", [f"guild_id = {inter.guild.id}"], {key: value})
            embed = disnake.Embed(
                title='Success',
                description=f'{keys[key]} has been set to ``{value}``.',
                color=disnake.Color.green()
            )

            guild = inter.guild
            config = Saver.fetch("guilds", [f"guild_id = {guild.id}"])[0]
            categoryName = guild.get_channel(config[keys_values["ticket_category"]]).name if config[keys_values["ticket_category"]] else 'None'
            supportRole = guild.get_role(config[keys_values["support_role"]])
            supportRoleName = supportRole.mention if supportRole else '``None``'
            welcomeChannelName = guild.get_channel(config[keys_values["welcome_channel"]]).mention if config[keys_values["welcome_channel"]] else '``None``'
            leaveChannelName = guild.get_channel(config[keys_values["leave_channel"]]).mention if config[keys_values["leave_channel"]] else '``None``'
            voiceTableChannelName = guild.get_channel(config[keys_values["voice_table_channel"]]).mention if config[keys_values["voice_table_channel"]] else '``None``'
            embed.add_field(name='Configuration', value=f"Ticket Category: {categoryName}\nSupport Role: {supportRoleName}\nWelcome Channel: {welcomeChannelName}\nLeave Channel: {leaveChannelName}\nVoice Table Channel: {voiceTableChannelName}")
            await inter.response.send_message(embed=embed, ephemeral=True)
            Log.log(f'SETTING on {inter.guild.id} [+] {keys[key]} has been set to {value}.')
        except Exception as e:
            Log.error("Failed to execute /set")
            Log.error(e)
            await inter.response.send_message(embed=error(e))

def setup(bot):
    bot.add_cog(Set(bot))