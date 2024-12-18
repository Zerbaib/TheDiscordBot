configFolder = "./config/"
cogsFolder = "./src/modules/"
logFolder = "./logs/"
dataFolder = "./src/data/"
assetsFolder = "./assets/"
imgFolder = f"{assetsFolder}img/"

dbInstructionsFile = f"{dataFolder}structure.sql"

policeFile = f"{assetsFolder}arialbd.ttf"
dbFile = f"{dataFolder}bdd.db"
configFile = f"{configFolder}config.json"
emojiFile = f"{configFolder}emojis.json"
rankWallpaperFile = f"{imgFolder}wallpaper.png"
rankWallpaperFinishedFile = f"{imgFolder}wallpaper_finished.png"
logFile = f"{logFolder}.log"

coinEarn = 100
rateLimitXpDaily = 300

class Color():
    reset = "\033[0m"
    red = "\033[31m"
    orange = "\033[33m"
    green = "\033[32m"
    blue = "\033[34m"
def load_config():
    try:
        with open(configFile, 'r') as f:
            import json
            data = json.load(f)
            token = data['token']
            prefix = data['prefix']
            return token, prefix
    except Exception as e:
        print(e)
        return None, None
def load_ownerID():
    try:
        with open(configFile, 'r') as f:
            import json
            data = json.load(f)
            ownerID = int(data['ownerId'])
            return ownerID
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
    "Bronze I": 0,
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
emojisID = {
    "bronze1": 1318555597993410600,
    "bronze2": 1318555647863816254,
    "bronze3": 1318555696282730536,
    "silver1": 1318556065092079687,
    "silver2": 1318556134147231795,
    "silver3": 1318556211498717286,
    "gold1": 1318558600825929798,
    "gold2": 1318558661504798771,
    "gold3": 1318558775245803520,
    "diamond1": 1318560168690061332,
    "diamond2": 1318560260558163968,
    "diamond3": 1318560342728773695,
    "platinium1": 1318559481696620545,
    "platinium2": 1318559687008063599,
    "platinium3": 1318559810874249337,
    "champion1": 1318560751769616407,
    "champion2": 1318560818635472927,
    "champion3": 1318560853624098876,
    "grandchampion": 1318560972478349352
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