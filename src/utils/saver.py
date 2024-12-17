import mysql.connector
from tabulate import tabulate
import json

import mysql.connector
from src.data.var import *
from src.utils.logger import Log
from tabulate import tabulate

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
    table_data = []
    for table in tables:
        table_data.append([table["table"]] + table["columns"])

    # Transpose the table data
    transposed_data = list(zip(*table_data))

    # Adjust headers to match the transposed data
    headers = [f"Table {i+1}" for i in range(len(transposed_data[0]))] + ["Table"]

    print(tabulate(transposed_data, headers=headers, tablefmt="grid"))


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
        cur.execute(dbInstructions, multi=True)
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

            conn.commit()
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
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            Log.error("Failed to save data")
            Log.error(e)
            return

    def close(self):
        self.conn.close()