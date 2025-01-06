import disnake
from disnake.ext import commands
from src.utils.logger import Log
from src.utils.saver import Saver
from PIL import Image, ImageChops, ImageDraw, ImageFont
from src.data.var import files, folders


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

    def circle(self, pfp, size=(125, 125)):
        pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(pfp.size, Image.LANCZOS)
        mask = ImageChops.darker(mask, pfp.split()[-1])
        pfp.putalpha(mask)
        return pfp
    
    def gen_banner(self, member):
        try:
            banner = Image.open(files["join_banner"])
            pfp = member.avatar.with_size(125)
            pfp = self.circle(pfp)
            banner.paste(pfp, (25, 25), pfp)
            banner.save(files["join_banner_finished"])
            draw = ImageDraw.Draw(banner)
            font = ImageFont.truetype(files["police"], 20)
            draw.text((160, 60), member.display_name, font=font, fill="black")
            draw.text((160, 90), "Welcome to the server!", font=font, fill="black")
            return True
        except Exception as e:
            Log.error(e)
            return False

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🧰 Members log has been loaded')
        pass

    @commands.Cog.slash_command(name="members", description="Check the number of members in the server")
    async def members(self, inter):
        try:
            await inter.response.defer()
            guild = inter.guild
            members = len(guild.members)
            if self.gen_banner(inter.author):
                await inter.channel.send(file=disnake.File(files["join_banner_finished"]))
            
            embed = disnake.Embed(
                title="Members",
                description=f"The server has {members} members.",
                color=disnake.Color.blue()
            )
            await inter.edit_original_response(embed=embed)
        except Exception as e:
            Log.error(e)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        Log.log(f'MEMBER [+] {member.name} (ID: {member.id}) | Now: {len(member.guild.members)} members on {member.guild.name} (ID: {member.guild.id})')
        guild = member.guild
        if get_guild_config(guild.id):
            join_channel = guild.get_channel(get_guild_config(guild.id)[4])
            if join_channel:
                if self.gen_banner(member):
                    await join_channel.send(file=disnake.File(files["join_banner_finished"]))
                
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