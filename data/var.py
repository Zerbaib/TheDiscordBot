configFolder = "./config/"
cogsFolder = "./src/modules/"
logFolder = "./logs/"
dataFolder = "./data/"

dbInstuctionsFile = f"{dataFolder}structure.sqlite"

dbFile = f"{dataFolder}bdd.db"
configFile = f"{configFolder}config.json"
logFile = f"{logFolder}log.txt"

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
        return

#token, prefix = load_config()