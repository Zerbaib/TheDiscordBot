import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver


class Query(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /query has been loaded')
        pass

    @commands.slash_command(name="query", description="Query the database")
    @commands.is_owner()
    async def query(self, ctx, request: str):
        try:
            query = request
            result = Saver.query(query)
            embed = disnake.Embed(
                description=f"```{result}```" if result else f"```sql\n{query}```",
                color=disnake.Color.green()
            )
            
            if not result:
                embed.description = f"```sql\n{query}```\n*Query executed successfully*"
                embed.color = disnake.Color.blurple()
                embed.title = "🔍 Query (No return)"
            else:
                embed.description = f"```{result}```\n*Query executed successfully*"
                embed.color = disnake.Color.blurple()
                embed.title = "🔍 Query"
            
            await ctx.send(embed=embed, ephemeral=True)
        except Exception as e:
            Log.error("Failed to execute /query")
            Log.error(e)
            return await ctx.send(embed=error(e))

def setup(bot):
    bot.add_cog(Query(bot))