import disnake
from disnake.ext import commands
from src.utils.logger import Log
from src.utils.saver import Saver
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
from src.data.var import files
import os


def get_guild_config(guild_id):
    try:
        data = Saver.fetch("guilds", [f"guild_id = {guild_id}"])
        if data:
            return data[0]
        return False
    except Exception as e:
        Log.error(e)
        return

class Members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def circle(self, pfp, size=(250, 250)):
        pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(pfp.size, Image.LANCZOS)
        mask = ImageChops.darker(mask, pfp.split()[-1])
        pfp.putalpha(mask)
        return pfp
    
    async def gen_banner(self, member):
        try:
            banner = Image.open(files["join_banner"])
            avatar_bytes = await member.avatar.read()
            pfp = Image.open(BytesIO(avatar_bytes))
            pfp = self.circle(pfp)
            banner.paste(pfp, (175, 50), pfp)
            banner.save(files["join_banner_finished"])
            draw = ImageDraw.Draw(banner)
            font = ImageFont.truetype(files["police"], 60)
            draw.text((475, 95), member.display_name, font=font, fill="#4f5053")
            font = ImageFont.truetype(files["police"], 40)
            text = f'Welcome on {member.guild.name}'
            text2 = f'You are the {len(member.guild.members)}th member'
            draw.text((475, 180), text, font=font, fill="#4f5053")
            draw.text((475, 220), text2, font=font, fill="#4f5053")
            banner.save(files["join_banner_finished"])
            return True
        except Exception as e:
            Log.error(e)
            return False

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
                if await self.gen_banner(member):
                    await join_channel.send(member.mention, file=disnake.File(files["join_banner_finished"]))
                    try:
                        os.remove(files["join_banner_finished"])
                    except Exception as e:
                        Log.warn(e)
                else:
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

