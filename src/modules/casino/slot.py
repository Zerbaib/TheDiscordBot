import random
import time

import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


class Slot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "economy"

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /slot has been loaded')
        pass
    
    @commands.slash_command(name="slot", description="Play a slot machine")
    async def slot(self, ctx, bet: int):
        try:
            user = ctx.author
            guild = ctx.guild
            slotEmojis = ["🍒", "7️⃣", "💰", "💎", "💵", "💳","💿", "📀", "🎉"]
            presision = [f"userID = {user.id}", f"guildID = {guild.id}"]
            
            if bet < 1:
                embed = disnake.Embed(
                    title="🚫 Invalid Bet",
                    description="You can't bet less than 1 coin.",
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
                    title="🔩 Economy Account Created",
                    description="You have been registered to the economy system.",
                    color=disnake.Color.green()
                )
                await ctx.send(embed=embed)
                return

            userBal = Saver.fetch(self.dataTable, presision, "coins")[0][0]

            if userBal < bet:
                embed = disnake.Embed(
                    title="🚫 Insufficient Balance",
                    description="You don't have enough coins to bet.",
                    color=disnake.Color.red()
                )
                return await ctx.send(embed=embed)

            userBal -= bet

            slot1 = random.choice(slotEmojis)
            slot2 = random.choice(slotEmojis)
            slot3 = random.choice(slotEmojis)

            embed = disnake.Embed(
                title="🎰 Slot Machine",
                description=f"It's spinning...",
                color=disnake.Color.blurple()
            )
            embed.set_image(url="https://media.tenor.com/exsQ1OPTGKUAAAAi/maquina-traga-monedas.gif")
            await ctx.send(embed=embed, delete_after=2)

            if slot1 == slot2 == slot3:
                multiplier = 10
                message = f"🎉 You won {bet * multiplier} coins!"
                userBal += bet * multiplier
            elif slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
                multiplier = 3
                message = f"🎉 You won {bet * multiplier} coins!"
                userBal += bet * multiplier
            else:
                message = "🎰 You lost"
            
            Saver.update(self.dataTable, presision, {"coins": userBal})
            
            time.sleep(2)
            
            embed = disnake.Embed(
                title="🎰 Slot Machine",
                description=message,
                color=disnake.Color.blurple()
            )
            embed.add_field(name="Result", value=f"{slot1} {slot2} {slot3}")
            embed.set_image(url="https://media1.tenor.com/m/WUWygJ0Fwz8AAAAd/jago33-slot-machine.gif")
            embed.set_footer(text=f"User: {user.display_name} | Balance: {userBal} coins")
            await ctx.send(embed=embed)
            Log.log(f"CASINO on {guild.id} by {user.id} - {slot1} {slot2} {slot3} - {userBal}")
        except Exception as e:
            embed = error(e)
            Log.error("Failed to execute /slot")
            Log.error(e)
            await ctx.send(embed=embed)
            return


def setup(bot):
    bot.add_cog(Slot(bot))