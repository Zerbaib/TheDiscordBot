import sqlite3
from data.var import *
from src.utils.logger import Log

with open(dbInstuctionsFile, 'r') as f:
    dbInstructions = f.read()

def connectDB():
    try:
        conn = sqlite3.connect(dbFile)
        cur = conn.cursor()
        return cur, conn
    except Exception as e:
        Log.error("Failed to connect to database")
        Log.error(e)
        exit()

def createDB():
    try:
        conn = sqlite3.connect(dbFile)
        cur = conn.cursor()
        cur.execute(dbInstructions)
        conn.commit()
        conn.close()
        return cur, conn
    except Exception as e:
        Log.error("Failed to initialize database")
        Log.error(e)
        exit()

class Saver():
    def __init__(self):
        self.cursor, self.conn = createDB()
        self.initDB()

    def initDB(self):
        try:
            cur, conn = connectDB()
            cur.execute(dbInstructions)
            conn.commit()
            conn.close()
            Log.info("Database initialized")
        except Exception as e:
            Log.error("Failed to initialize database")
            Log.error(e)
            exit()

    def close(self):
        self.conn.close()