configFolder = "./config/"
cogsFolder = "./src/modules/"
logFolder = "./logs/"
dataFolder = "./src/data/"

dbInstructionsFile = f"{dataFolder}structure.sql"

dbFile = f"{dataFolder}bdd.db"
configFile = f"{configFolder}config.json"
logFile = f"{logFolder}.log"

coinEarn = 100

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
    "Bronze I": 50,
    "Bronze II": 75,
    "Bronze III": 100,
    "Silver I": 150,
    "Silver II": 200,
    "Silver III": 250,
    "Gold I": 300,
    "Gold II": 375,
    "Gold III": 450,
    "Platinum I": 500,
    "Platinum II": 600,
    "Platinum III": 700,
    "Diamond I": 800,
    "Diamond II": 900,
    "Diamond III": 1000,
    "Champion I": 1250,
    "Champion II": 1500,
    "Champion III": 2000,
    "Grand Champion": 3000
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