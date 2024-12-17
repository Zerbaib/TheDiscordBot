import random

import disnake
from disnake.ext import commands
from src.utils.logger import Log


class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jokes = [
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why don’t scientists trust atoms? Because they make up everything!",
    "I would tell you a construction pun, but I’m still working on it.",
    "Have you heard about the restaurant on the moon? Great food, no atmosphere.",
    "Did you hear about the mathematician who’s afraid of negative numbers? He'll stop at nothing to avoid them!",
    "Parallel lines have so much in common… it’s a shame they’ll never meet.",
    "What do you call fake spaghetti? An impasta!",
    "Want to hear a joke about paper? Never mind, it’s tearable.",
    "I only know 25 letters of the alphabet. I don’t know y.",
]

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /joke has been loaded')
        pass

    @commands.slash_command(name="joke", description="Get a random joke !")
    async def joke(self, ctx):
        random_joke = random.choice(self.jokes)
        embed = disnake.Embed(
            title="🃏 Joke",
            description=random_joke,
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Joke(bot))