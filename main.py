import src.utils.creator
import src.utils.loader
from src.utils.logger import Log

class main():
    def __init__(self):
        src.utils.creator.Creator()
        src.utils.loader.Loader()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        Log.error("Failed to start bot")
        Log.error(e)
        exit()