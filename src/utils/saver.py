import sqlite3
import mysql.connector
import json

from src.data.var import *
from src.utils.logger import Log

with open(dbInstructionsFile, 'r') as f:
    dbInstructions = f.read()
with open(configFile, 'r') as f:
    config = json.load(f)
    dbUser = config["dbUser"]
    dbPass = config["dbPass"]
    dbHost = config["dbHost"]
    dbPort = int(config["dbPort"])
    dbName = config["dbName"]
def display_table(tables):
    print(" | ".join([table["table"] for table in tables]))
    print(" | ".join(["-" * len(table["table"]) for table in tables]))

    # Find the maximum length of each column across all tables
    max_lengths = [max(len(str(col[i])) for table in tables if len(table["columns"]) > i for col in [table["columns"]]) for i in range(max(len(table["columns"]) for table in tables))]

    # Format string to align columns
    format_str = " | ".join(["{:>" + str(length) + "}" for length in max_lengths])

    for i in range(max(len(table["columns"]) for table in tables)):
        row_data = [table["columns"][i] if len(table["columns"]) > i else "" for table in tables]
        print(format_str.format(*row_data))


def connectDB():
    try:
        conn = mysql.connector.connect(
            user=dbUser,
            password=dbPass,
            host=dbHost,
            port=dbPort,
            database=dbName
        )
        cur = conn.cursor()
        return cur, conn
    except Exception as e:
        Log.error("Failed to connect to database")
        Log.error(e)
        exit()

def createDB():
    try:
        cur, conn = connectDB()
        cur.execute(dbInstructions)
        return cur, conn
    except Exception as e:
        Log.error("Failed to create database")
        Log.error(e)
        exit()

class Saver():
    def __init__(self):
        self.cursor, self.conn = createDB()
        table_data = self.initDB()
        if table_data:
            print(table_data)
            display_table(table_data)
        else:
            print("| Aucune donnée trouvée |")

    def initDB(self):
        try:
            cur, conn = connectDB()

            cur.execute("SHOW TABLES")
            tables = [table[0] for table in cur.fetchall()]

            table_data = []
            for table in tables:
                cur.execute(f"DESCRIBE {table}")
                columns = [column[0] for column in cur.fetchall()]
                table_data.append({"table": table, "columns": columns})

            cur.close()
            conn.close()
            Log.info("Database initialized")
            return table_data
        except Exception as e:
            Log.error("Failed to initialize the database")
            Log.error(e)
            exit()

    def fetch(query):
        try:
            cur, conn = connectDB()
            cur.execute(query)
            data = cur.fetchall()
            conn.close()
            return data
        except Exception as e:
            if "list index out of range" in str(e):
                Log.warn(e)
            Log.error("Failed to fetch data")
            Log.error(e)
            return

    def save(query):
        try:
            cur, conn = connectDB()
            cur.execute(query)
            cur.close()
            conn.close()
        except Exception as e:
            Log.error("Failed to save data")
            Log.error(e)
            return

    def close(self):
        self.conn.close()