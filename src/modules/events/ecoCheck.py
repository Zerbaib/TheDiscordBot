import datetime

import disnake
from disnake.ext import commands
import asyncio
from src.utils.logger import Log
from src.utils.saver import Saver


class ecoCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataTable = "economy"

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /ecoCheck has been loaded')
        self.bot.loop.create_task(self.checkIndex())

    @commands.Cog.listener()
    async def checkIndex(self):
        while True:
            try:
                query = f"SELECT userID, guildID, COUNT(*) FROM {self.dataTable} GROUP BY userID, guildID HAVING COUNT(*) > 1"
                results = Saver.query(query)
                if results:
                    for result in results:
                        user_id, guild_id, count = result
                        Log.warn(f"Duplicate entry found: userID={user_id}, guildID={guild_id}, count={count}")
                        query = f"DELETE FROM {self.dataTable} WHERE userID = {user_id} AND guildID = {guild_id} LIMIT {count - 1}"
                        Saver.query(query)
                        Log.warn(f"Deleted {count - 1} duplicate entries")
            except Exception as e:
                Log.error(f"Error checking index: {e}")
            await asyncio.sleep(3600)

def setup(bot):
    bot.add_cog(ecoCheck(bot))