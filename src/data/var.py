folders = {
    "config": "./config/",
    "cogs": "./src/modules/",
    "logs": "./logs/",
    "data": "./src/data/",
    "assets": "./assets/",
    "img": "./assets/img/"
}
files = {
    "config": f"{folders['config']}config.json",
    "emojis": f"{folders['config']}emojis.json",
    "instructions": f"{folders['data']}structure.sql",
    "police": f"{folders['assets']}arialbd.ttf",
    "wallpaper": f"{folders['img']}wallpaper.png",
    "wallpaper_finished": f"{folders['img']}wallpaper_finished.png"
}

coinEarn = 100
rateLimitXpDaily = 300

def initTime(value):
    global startTimestamp
    global logFile
    startTimestamp = value.strftime("%Hh%M_%d-%m-%Y")
    logFile = f"{folders['logs']}{startTimestamp}.log"

class Color():
    reset = "\033[0m"
    red = "\033[31m"
    orange = "\033[33m"
    green = "\033[32m"
    blue = "\033[34m"
def load_config(value):
    try:
        if value not in ["token", "prefix", "ownerId"]:
            raise ValueError("Invalid value. Expected 'token' or 'prefix' or 'ownerId'.")
        with open(files["config"], 'r') as f:
            import json
            data = json.load(f)
            if value == "ownerId":
                return int(data.get(value))
            return data.get(value)
    except Exception as e:
        print(e)
        return None
class Git():
    from subprocess import check_output
    link = "https://github.com"
    rawLink = "https://raw.githubusercontent.com"
    branch = f"/{check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()}"
    repos = "/Zerbaib/TheDiscordBot"
class Version():
    fileName = "version"
    localVersionFile = f"./{fileName}"
    onlineVersionFile = f"{Git.rawLink}{Git.repos}{Git.branch}/{fileName}"

    def getLocal():
        with open(Version.localVersionFile, 'r') as f:
            localVer = f.read()
        return localVer

    def getOnline():
        import requests
        from src.utils.logger import Log
        try:
            response = requests.get(Version.onlineVersionFile)
            response.raise_for_status()
            onlineVer = response.text
            return onlineVer
        except requests.RequestException as e:
            Log.warn("Can't open online version")
            Log.warn(e)
            return

rankGrade = {
    "Bronze I": 6,
    "Bronze II": 150,
    "Bronze III": 300,
    "Silver I": 375,
    "Silver II": 450,
    "Silver III": 550,
    "Gold I": 700,
    "Gold II": 850,
    "Gold III": 1000,
    "Diamond I": 1150,
    "Diamond II": 1300,
    "Diamond III": 1500,
    "Platinium I": 1750,
    "Platinium II": 1900,
    "Platinium III": 2100,
    "Champion I": 2300,
    "Champion II": 2600,
    "Champion III": 2900,
    "Grand Champion": 4000
}
tableLiaison = {
    "Bronze I": "bronze1",
    "Bronze II": "bronze2",
    "Bronze III": "bronze3",
    "Silver I": "silver1",
    "Silver II": "silver2",
    "Silver III": "silver3",
    "Gold I": "gold1",
    "Gold II": "gold2",
    "Gold III": "gold3",
    "Diamond I": "diamond1",
    "Diamond II": "diamond2",
    "Diamond III": "diamond3",
    "Platinium I": "platinium1",
    "Platinium II": "platinium2",
    "Platinium III": "platinium3",
    "Champion I": "champion1",
    "Champion II": "champion2",
    "Champion III": "champion3",
    "Grand Champion": "grandchampion"
}
keys = {
    'ticket_category': 'Ticket Category',
    'support_role': 'Support Role',
    'welcome_channel': 'Welcome Channel',
    'leave_channel': 'Leave Channel',
    'voice_table_channel': 'Voice Table Channel',
}
keys_values = {
    'ticket_category': 2,
    'support_role': 3,
    'welcome_channel': 4,
    'leave_channel': 5,
    'voice_table_channel': 6,
}
key_profile = {
    'avatarURL': 'Avatar URL',
    'nickname': 'Nickname'
}
key_profile_values = {
    'avatarURL': 2,
    'nickname': 3
}
data = {
    "token": "your_token",
    "prefix": "your_prefix",
    "ownerId": "your_owner_id",
    "dbUser": "your_db_user",
    "dbPass": "your_db_pass",
    "dbHost": "your_db_host",
    "dbPort": "your_db_port",
    "dbName": "your_db_name"
}