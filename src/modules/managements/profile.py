import disnake
from disnake.ext import commands
from src.data.var import *
from src.utils.error import error_embed as error
from src.utils.logger import Log
import requests


class ProfileCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /profile has been loaded')
        pass

    @commands.slash_command(name="profile", description="Costomize the bot")
    async def profile(self, ctx, setting: str = None, value: str = None):
        user = ctx.author
        guild = ctx.guild
        if not user.guild_permissions.administrator:
            embed = disnake.Embed(
                title='Error',
                description='You must be the owner of the server to use this command.',
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return
        try:
            if setting not in key_profile:
                embed = disnake.Embed(
                    title='Error',
                    description=f'Invalid key. Available keys: {", ".join(key_profile.keys())}\nExample: `/profile avatarURL https://example.com/image.png`',
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return
                
            if setting == "avatarURL":
                if not value.startswith("http") or not value.endswith((".png", ".jpg", ".jpeg")):
                    embed = disnake.Embed(
                        title='Error',
                        description='The avatar URL must be a link to an image (png, jpg, jpeg).',
                        color=disnake.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return
                await self.bot.user.edit(avatar=requests.get(value).content)
                embed = disnake.Embed(
                    title='Success',
                    description=f'Avatar has been updated.',
                    color=disnake.Color.green()
                )
                Log.info(f'PROFILE BOT avatar has been updated by {user.name} in {guild.name}')
                await ctx.send(embed=embed)
            elif setting == "nickname":
                await ctx.guild.me.edit(nick=value)
                embed = disnake.Embed(
                    title='Success',
                    description=f'Nickname has been updated.',
                    color=disnake.Color.green()
                )
                Log.info(f'PROFILE BOT nickname has been updated by {user.name} in {guild.name}')
                await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title='Error',
                    description='An error occured.',
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            Log.error("Failed to execute /profile")
            Log.error(e)
            await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(ProfileCommand(bot))