import disnake
import time
import random
from disnake.ext import commands
from src.data.var import *
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /dice has been loaded')
        pass

    @commands.slash_command(name="dice", description="Roll a dice")
    async def dice(self, ctx, bet: int):
        try:
            user = ctx.author
            guild = ctx.guild

            if bet < 1:
                embed = disnake.Embed(
                    title="🚫 Invalid Bet",
                    description="You can't bet less than 1 coin.",
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            if not Saver.fetch(f"SELECT coins FROM economy WHERE userID = {user.id} AND guildID = {guild.id}"):
                Saver.save(f"INSERT INTO economy (userID, guildID, coins, cooldown) VALUES ({user.id}, {guild.id}, 0, 0)")
                embed = disnake.Embed(
                    title="🔩 Economy Account Created",
                    description="You have been registered to the economy system.",
                    color=disnake.Color.green()
                )
                await ctx.send(embed=embed)
                return

            userBal = Saver.fetch(f"SELECT coins FROM economy WHERE userID = {user.id} AND guildID = {guild.id}")[0][0]

            if userBal < bet:
                embed = disnake.Embed(
                    title="🚫 Insufficient Balance",
                    description="You don't have enough coins to bet.",
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)

            embed = disnake.Embed(
                title="🎲 Rolling Dice",
                description=f"Wait for the result...",
                color=disnake.Color.blurple()
            )
            embed.set_image(url=f"https://media1.tenor.com/m/jby_bYZfACwAAAAd/the-weeknd-run-it-up.gif")

            await ctx.send(embed=embed, delete_after=2)

            if dice1 == dice2:
                multiplier = dice1
                embed = disnake.Embed(
                    title="🎲 You Won",
                    description=f"You rolled a {dice1} and a {dice2}. You won {bet * multiplier} coins.",
                    color=disnake.Color.green()
                )
                embed.set_image(url="https://media.tenor.com/ljG-wtgMFd0AAAAi/rollbit-stake.gif")
                userBal += bet * multiplier
            else:
                embed = disnake.Embed(
                    title="🎲 You Lost",
                    description=f"You rolled a {dice1} and a {dice2}. You lost {bet} coins.",
                    color=disnake.Color.red()
                )
                embed.set_image(url="https://media1.tenor.com/m/F1srlDHEYlEAAAAd/luigi-casino.gif")
                userBal -= bet

            Saver.save(f"UPDATE economy SET coins = {userBal} WHERE userID = {user.id} AND guildID = {guild.id}")
            time.sleep(2)
            await ctx.send(embed=embed)
            Log.log(f"CASINO on {guild.id} by {user.id} - {dice1} and {dice2} - {userBal}")
        except Exception as e:
            Log.error(e)
            await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(Dice(bot))