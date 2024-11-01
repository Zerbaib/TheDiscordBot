import disnake
from disnake.ext import commands
from src.utils.error import error_embed as error
from src.utils.logger import Log
from src.utils.saver import Saver

class server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Log.info('🔩 /server has been loaded')  

    #param,service_name=['add','update','remove','assign','unassign','infot'],['python']
    @commands.slash_command(name="server", description="gere la liste des servers")
    async def server(self, ctx, param: str = None, server_name: str = None, ip: str = None, port: int = None, service_name: str = None, user: disnake.User=None):  # type: ignore
        try:
            if param == 'add':
                if server_name and ip and port and service_name:
                    Saver.save(f"INSERT INTO servers (server_name, server_ip, server_port) VALUES ('{server_name}', '{ip}', {port})")
                    await ctx.send(f"✅ Serveur `{server_name}` ajouté avec succès.")
                else:
                    await ctx.send("⚠️ Paramètres manquants ! Veuillez spécifier `server_name`, `ip`, et `port`.")

            elif param == 'update':
                if server_name and ip and port and service_name:
                    pass
            elif param == 'remove':
                if server_name:
                    Saver.save(f"DELETE FROM servers WHERE server_name = '{server_name}'")
                    await ctx.send(f"❌ Serveur `{server_name}` supprimé avec succès.")
                else:
                    await ctx.send("⚠️ Paramètre manquant ! Veuillez spécifier `server_name`.")

            elif param == 'assign':
                if server_name and user.id:
                    Saver.save(f"UPDATE servers SET userID = {user.id} WHERE server_name = '{server_name}'")
                    await ctx.send(f"🔗 Serveur `{server_name}` assigné à l'utilisateur `{user}`.")
                else:
                    await ctx.send("⚠️ Paramètres manquants ! Veuillez spécifier `server_name` et `user_id`.")

            elif param == 'unassign':
                if server_name:
                    Saver.save(f"UPDATE servers SET userID = NULL WHERE server_name = '{server_name}'")
                    await ctx.send(f"🚫 Serveur `{server_name}` désassigné à {user}")
                else:
                    await ctx.send("⚠️ Paramètre manquant ! Veuillez spécifier `server_name`.")

            elif param == 'infot':
                if server_name:
                    server_info = Saver.fetch(f"SELECT * FROM servers WHERE server_name = '{server_name}'")
                    if server_info:
                        server = server_info[0]
                        user = server[1]
                        ip = server[3]
                        port = server[4]
                        await ctx.send(f"ℹ️ **Informations du serveur**\n**Nom**: {server_name}\n**IP**: {ip}\n**Port**: {port}\n**Assigné à**: {user if user else 'Aucun utilisateur'}")
                    else:
                        await ctx.send("⚠️ Serveur introuvable.")
                else:
                    await ctx.send("⚠️ Paramètre manquant ! Veuillez spécifier `server_name`.")
                    
        except Exception as e:
            embed = error(e)
            Log.error("Une erreur est survenue lors de l'exécution de la commande /server")
            Log.error(e)
            await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(server(bot))