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
            ownerID = data['ownerId']
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
        from src.utils.logger import Log
        import requests
        try:
            response = requests.get(Version.onlineVersionFile)
            response.raise_for_status()
            onlineVer = response.text
            return onlineVer
        except requests.RequestException as e:
            Log.warn("Can't open online version")
            Log.warn(e)
            return

keys = {
    'ticket_category': 'Ticket Category',
    'support_role': 'Support Role',
    'welcome_channel': 'Welcome Channel',
    'leave_channel': 'Leave Channel'
}
keys_values = {
    'ticket_category': 2,
    'support_role': 3,
    'welcome_channel': 4,
    'leave_channel': 5
}