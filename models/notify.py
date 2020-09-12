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

class NotifyDB:  
    def __init__(self):
        self.db = DBHandler()
        self.table_name = "notify"

    def create_table(self):
        with self.db:
            sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                id integer PRIMARY KEY,
                msg text NOT NULL,
                time datetime DEFAULT (datetime('now', 'localtime')),
                channel integer NOT NULL
                );
                """
            
            self.db.cur.execute(sql)

    def add_notify(self, msg, channel, time=""):
        if not msg:
            return

        msg = msg.replace("'", "''")

        with self.db:
            if time:
                sql = f"""
                    INSERT INTO {self.table_name} (msg, time, channel)
                    VALUES ('{msg}', '{time}', '{channel}');
                """
            else:
                sql = f"""
                    INSERT INTO {self.table_name} (msg, channel)
                    VALUES ('{msg}', '{channel}');
                """

            self.db.cur.execute(sql)
            self.db.conn.commit()

    def get_record(self):
        with self.db:
            sql = f"""
                SELECT * FROM {self.table_name}
            """

            self.db.cur.execute(sql)

            rows = self.db.cur.fetchall()
            
        ls = [NotifyContent(row[1], row[2], row[3]) for row in rows]

        return ls

if __name__ == "__main__":
    pass

    