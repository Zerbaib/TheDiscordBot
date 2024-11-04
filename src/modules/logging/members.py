import disnake
from disnake.ext import commands
from src.data.var import *
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

class Members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🧰 Members log has been loaded')
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        Log.log(f'MEMBER [+] {member.name} (ID: {member.id}) | Now: {len(member.guild.members)} members on {member.guild.name} (ID: {member.guild.id})')
        guild = member.guild
        if get_guild_config(guild.id):
            join_channel = guild.get_channel(get_guild_config(guild.id)[4])
            if join_channel:
                embed = disnake.Embed(
                    title='Member Joined',
                    description=f'{member.mention} has joined the server!',
                    color=disnake.Color.green()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await join_channel.send(embed=embed)
                pass
            pass
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        Log.log(f'MEMBER [-] {member.name} (ID: {member.id}) | Now: {len(member.guild.members)} members on {member.guild.name} (ID: {member.guild.id})')
        guild = member.guild
        if get_guild_config(guild.id):
            leave_channel = guild.get_channel(get_guild_config(guild.id)[5])
            if leave_channel:
                embed = disnake.Embed(
                    title='Member Left',
                    description=f'{member.mention} has left the server!',
                    color=disnake.Color.red()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await leave_channel.send(embed=embed)
                pass
        pass

def setup(bot):
    bot.add_cog(Members(bot))