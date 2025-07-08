import random
import time

import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver
from src.utils.lang import get_language_file


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "economy"

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /dice has been loaded')
        pass

    @commands.slash_command(name="dice", description="Roll a dice")
    async def dice(self, ctx, bet: int):
        try:
            lang = get_language_file(ctx.guild.preferred_locale)
            user = ctx.author
            guild = ctx.guild
            presision = [f"userID = {user.id}", f"guildID = {guild.id}"]

            if bet < 1:
                embed = disnake.Embed(
                    title=lang["Casino"]["dice"]["errors"]["title"],
                    description=lang["Casino"]["dice"]["errors"]["invalidAmount"],
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            if not Saver.fetch(self.dataTable, presision):
                data = {
                    "guildID": guild.id,
                    "userID": user.id,
                    "coins": 0
                }
                Saver.save(self.dataTable, data)
                embed = disnake.Embed(
                    title=lang["Casino"]["created"]["title"],
                    description=lang["Casino"]["created"]["description"],
                    color=disnake.Color.green()
                )
                await ctx.send(embed=embed)
                return

            userBal = Saver.fetch(self.dataTable, presision, "coins")[0][0]

            if userBal < bet:
                embed = disnake.Embed(
                    title=lang["Casino"]["dice"]["errors"]["title"],
                    description=lang["Casino"]["dice"]["errors"]["noCoins"],
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)

            embed = disnake.Embed(
                title=lang["Casino"]["dice"]["title"],
                description=". . .",
                color=disnake.Color.blurple()
            )
            embed.set_image(url=f"https://media1.tenor.com/m/jby_bYZfACwAAAAd/the-weeknd-run-it-up.gif")

            await ctx.send(embed=embed, delete_after=2)

            if dice1 == dice2:
                multiplier = dice1
                embed = disnake.Embed(
                    title=lang["Casino"]["dice"]["win"]["title"],
                    description=lang["Casino"]["dice"]["win"]["description"].format(dice1=dice1, dice2=dice2, win=bet*multiplier),
                    color=disnake.Color.green()
                )
                embed.set_image(url="https://media.tenor.com/ljG-wtgMFd0AAAAi/rollbit-stake.gif")
                userBal += bet * multiplier
            else:
                embed = disnake.Embed(
                    title=lang["Casino"]["dice"]["lose"]["title"],
                    description= lang["Casino"]["dice"]["lose"]["description"].format(dice1=dice1, dice2=dice2, bet=bet),
                    color=disnake.Color.red()
                )
                embed.set_image(url="https://media1.tenor.com/m/F1srlDHEYlEAAAAd/luigi-casino.gif")
                userBal -= bet

            Saver.update(self.dataTable, presision, {"coins": userBal})
            time.sleep(2)

            embed.set_footer(text=f"User: {user.display_name} | Balance: {userBal} coins")
            await ctx.send(embed=embed)
            Log.log(f"CASINO on {guild.id} by {user.id} - {dice1} and {dice2} - {userBal}")
        except Exception as e:
            Log.error(e)
            await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(Dice(bot))