import socket
import asyncio
from disnake.ext import tasks, commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

class Monitoring(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.previous_status = {}

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.monitor_servers.is_running():
            self.monitor_servers.start(self.bot)
            Log.info('🧰 Monitoring system has been loaded')
    
    async def check_server_status(self,ip, port, timeout=5):
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                return "online"
        except (socket.timeout, ConnectionRefusedError, OSError):
            return "offline"
        
    def fetch_servers_and_users(self):
        return Saver.fetch("SELECT userID, server_ip, server_port FROM servers")

    async def notify_user(self, bot, user_id, message):
        user = await bot.fetch_user(user_id)
        if user:
            try:
                await user.send(message)
            except Exception as e:
                Log.error(f"Erreur lors de l'envoi du message à {user_id}: {e}")

    @tasks.loop(minutes=0.01)
    async def monitor_servers(self,bot):

        # Récupérer les serveurs et utilisateurs depuis la base de données
        servers = self.fetch_servers_and_users()
        for server in servers:
            user_id, ip, port = server
            if user_id==None:
                pass
            else:
                status = await self.check_server_status(ip, port)
                
                # Si le statut du serveur a changé, notifie l'utilisateur associé
                if self.previous_status.get((ip,port)) != status:
                    if status == "offline":
                        await self.notify_user(bot, user_id, f"🚨 Le serveur {ip}:{port} est hors ligne !")
                    elif status == "online":
                        await self.notify_user(bot, user_id, f"✅ Le serveur {ip}:{port} est à nouveau en ligne.")
                    
                    # Met à jour le statut précédent pour éviter les notifications répétées
                    self.previous_status[(ip, port)] = status

            await asyncio.sleep(1)  # Attendre 5 minutes avant la prochaine vérification

def setup(bot):
    bot.add_cog(Monitoring(bot))