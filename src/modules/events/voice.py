import asyncio

import disnake
from disnake.ext import commands
from src.data.var import *
from src.utils.logger import Log
from src.utils.saver import Saver


class CustomVoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = {}
    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🧰 CustomVoice has been loaded')
        self.bot.loop.create_task(self.delete_temporary_channels())
        pass
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            target_channel = Saver.fetch("guilds", [f"guild_id = {member.guild.id}"], "voice_table_channel")[0][0]
        except IndexError:
            return
        channel = self.bot.get_channel(int(target_channel))
        if after.channel and after.channel.id == target_channel:
            guild = member.guild
            category = after.channel.category
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(connect=True),
                member: disnake.PermissionOverwrite(connect=True, manage_channels=True)
            }
            channel = await category.create_voice_channel(name=member.display_name, overwrites=overwrites, user_limit=10)
            Log.log(f'TEMPORARY CHANNEL CREATED: {channel.name} (ID: {channel.id}) on {guild.name} (ID: {guild.id})')
            await member.move_to(channel)
            self.temp_channels[channel.id] = asyncio.get_event_loop().time()
    async def delete_temporary_channels(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            current_time = asyncio.get_event_loop().time()
            for channel_id, created_time in list(self.temp_channels.items()):
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    self.temp_channels.pop(channel_id)
                    continue
                if len(channel.members) == 0 and current_time - created_time >= 3:
                    await channel.delete()
                    Log.log(f'TEMPORARY CHANNEL DELETED: {channel.name} (ID: {channel.id}) on {channel.guild.name} (ID: {channel.guild.id})')
                    self.temp_channels.pop(channel_id)
            await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(CustomVoiceCog(bot))