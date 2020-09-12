from datetime import datetime
from pathlib import Path
import sqlite3

from config import Config

class NotifyContent:
    def __init__(self, msg: str, time: datetime, channel: int):
        self.msg = msg
        self.time = time
        self.channel = channel

class DBHandler:
    def __init__(self):
        self.db_name = f"{Config.DB}"

    def __enter__(self):
        self.start_database()
        return self

    def __exit__(self, exc_type, ex_value, ex_traceback):
        self.close_database()
    
    def start_database(self,):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

    def close_database(self,):
        """shut down connect to DB
        """
        self.conn.close()

class PTTDB:  
    def __init__(self):
        self.db = DBHandler()
        self.table_name = "PTT"

    def create_table(self):
        with self.db:
            sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                id integer PRIMARY KEY,
                keyword text NOT NULL
                );
                """
            
            self.db.cur.execute(sql)

    def get_keywords(self):
        ls = []
        with self.db:
            sql = f"""
                SELECT keyword FROM {self.table_name}
            """

            self.db.cur.execute(sql)

            rows = self.db.cur.fetchall()
            
        ls = [row[0] for row in rows]

        return ls

if __name__ == "__main__":
    pass