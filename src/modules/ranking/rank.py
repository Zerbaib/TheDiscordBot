import os
from io import BytesIO

import disnake
from disnake.ext import commands
from PIL import Image, ImageChops, ImageDraw, ImageFont
from src.data.var import rankGrade, tableLiaison, folders, files
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "ranking"

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

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /rank has been loaded')

    @commands.slash_command(name="rank", description="Check your rank")
    async def rank(self, ctx, member: disnake.Member = None):
        try:
            if member:
                user = member
            else:
                user = ctx.author
            if user.bot:
                embed = disnake.Embed(
                    title="📊 Rank Information 📊",
                    description=f"User {user.mention} is a bot",
                    color=disnake.Color.blurple()
                )
                return await ctx.send(embed=embed)
            guild = ctx.guild
            name = user.display_name
            progress=0
            progress_bar = ""
            presision = [f"userID = {user.id}", f"guildID = {guild.id}"]
            try:
                usrData = Saver.fetch(self.dataTable, presision, ["xp", "level", "grade"])[0]
                xp = usrData[0]
                level = usrData[1]
                grade = usrData[2]
            except IndexError:
                embed = disnake.Embed(
                    title="📊 Rank Information 📊",
                    description=f"User {user.mention} is not ranked yet",
                    color=disnake.Color.blurple()
                )
                await ctx.send(embed=embed)
                return
            liaison_name = tableLiaison.get(grade)
            if not liaison_name:
                Log.warn(f"Failed to get emoji id {grade}")

            actualGrade = grade
            if actualGrade is None:
                actualGrade = list(rankGrade.keys())[0]
            nextGrade = list(rankGrade.keys())[list(rankGrade.keys()).index(grade) + 1] if grade in rankGrade else None
            actualGradeXp = rankGrade[actualGrade]
            nextGradeXp = rankGrade[nextGrade] if nextGrade else None
            if nextGradeXp:
                progress = (xp - actualGradeXp) / (nextGradeXp - actualGradeXp)
                if not progress:
                    progress = 0
                progress_bar = "█" * int(progress * 20) + "░" * (20 - int(progress * 20))
            else:
                progress_bar = "█" * 20

            background = Image.open(files["wallpaper"])
            asset = user.display_avatar.with_size(1024)
            data = BytesIO(await asset.read())
            pfp = Image.open(data).convert("RGBA")
            pfp = self.circle(pfp)

            if liaison_name is not None:
                imageFilePath = f"{folders['img']}icon/{liaison_name}.png"
                icon = Image.open(imageFilePath)
                icon = icon.resize((250, 250)).convert("RGBA")
                background.paste(icon, (300, 90), icon)

                draw = ImageDraw.Draw(background)
                font = ImageFont.truetype(files["police"], 24)
                text = grade
                draw.text((370, 380), text, font=font, fill="#3d403e")

            text_overlay = Image.new('RGBA', background.size, (255, 255, 255, 0))
            overlay_draw = ImageDraw.Draw(text_overlay)
            textLvl = f"Level {level}"
            textXp = f"XP {xp}"
            font = ImageFont.truetype(files["police"], 28)
            overlay_draw.text((25, 25), name, font=font, fill=(87, 86, 84, 128))
            font = ImageFont.truetype(files["police"], 24)
            overlay_draw.text((30, 50), textLvl, font=font, fill=(87, 86, 84, 128))
            overlay_draw.text((30, 75), textXp, font=font, fill=(87, 86, 84, 128))

            background = Image.alpha_composite(background.convert('RGBA'), text_overlay)

            font = ImageFont.truetype(files["police"], 20)
            draw = ImageDraw.Draw(background)
            text = f"[{progress_bar}] {round(progress*100)}%"
            draw.text((266, 340), text, font=font, fill="#3d403e")

            background.paste(pfp, (700, 30), pfp)
            background.save(files["wallpaper_finished"], "PNG")

            await ctx.send(file=disnake.File(files["wallpaper_finished"]))

            try:
                os.remove(files["wallpaper_finished"])
            except Exception as e:
                Log.error("Failed to remove rankWallpaperFinishedFile")
                Log.error(e)
        except Exception as e:
            embed = error(e)
            Log.error("Failed to execute /rank")
            Log.error(e)
            await ctx.send(embed=embed)
            return



def setup(bot):
    bot.add_cog(Rank(bot))