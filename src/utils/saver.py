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
        if self.initDB():
            display_table(self.initDB())
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
    def fetch(dataTable, presision, dataFetch = "*"):
        """
        Fetch data from the database

        Parameters:
            dataTable (str): The table to fetch data from
            presision (dict): The conditions to fetch data
            dataFetch (list): The data to fetch

        Returns:
            data (list): The fetched data
        """
        try:
            if type(dataFetch) == list:
                dataFetch = ", ".join(dataFetch)
            query = f"SELECT {dataFetch} FROM {dataTable}"
            if presision:
                query += f" WHERE"
                for item in presision:
                    query += f" {item} AND"
                query = query[:-4]
            Log.sql(query)
            sql_cur_fetchall(query)
        except Exception as e:
            if "list index out of range" in str(e):
                Log.warn(e)
            Log.error("Failed to fetch data")
            Log.error(e)
            return
    def save(dataTable, data):
        """
        Save data to the database

        Parameters:
            dataTable (str): The table to save data to
            data (dict): The data to save

        Returns:
            None
        """
        try:
            query = f"INSERT INTO {dataTable}"
            query += " ("
            for item in data:
                query += f"{item}, "
            query = query[:-2]
            query += ") VALUES ("
            for item in data:
                query += f"{data[item]}, "
            query = query[:-2]
            query += ")"
            Log.sql(query)

            cur, conn = connectDB()
            cur.execute(query)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            Log.error("Failed to save data")
            Log.error(e)
            return
    def update(dataTable, presision, data):
        """
        Update data in the database
        
        Parameters:
            dataTable (str): The table to update data in
            presision (dict): The conditions to update data
            data (dict): The data to update
        
        Returns:
            None
        """
        try:
            query = f"UPDATE {dataTable} SET"
            for item in data:
                if data[item] == str(data[item]):
                    query += f" {item} = '{data[item]}',"
                else:
                    query += f" {item} = {data[item]},"
            query = query[:-1]
            if presision:
                query += " WHERE"
                for item in presision:
                    query += f" {item} AND"
                query = query[:-4]
            Log.sql(query)

            cur, conn = connectDB()
            cur.execute(query)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            Log.error("Failed to update data")
            Log.error(e)
            return
    def query(query):
        """
        Execute a query

        Parameters:
            query (str): The query to execute

        Returns:
            data (list): The fetched data
        """
        try:
            Log.sql(query)
            sql_cur_fetchall(query)
        except Exception as e:
            Log.error("Failed to execute query")
            Log.error(e)
            return

    def close(self):
        self.conn.close()

def sql_cur_fetchall(query):
    cur, conn = connectDB()
    cur.execute(query)
    data = cur.fetchall()
    conn.close()
    return data