from pathlib import Path
import datetime
import sqlite3

from config import Config

class JobContent:
    def __init__(self, name: str, time: str):
        self.name = name
        self.time = time

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

class MainDB:  
    def __init__(self):
        self.db = DBHandler()
        self.table_name = "job"

    def create_table(self):
        with self.db:
            sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                id integer PRIMARY KEY,
                name string(8) NOT NULL,
                start_time string(64) NOT NULL,
                weekday string(8) NOT NULL,
                channel integer NOT NULL,
                execution BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY (channel) REFERENCES channel(id)
                );
                """
            
            self.db.cur.execute(sql)

    def add_job(self, name, start_time, weekday):
        with self.db:
            sql = f"""
                INSERT INTO {self.table_name} (name, start_time, weekday) VALUES 
                ('{name}', '{start_time}', '{weekday}');
            """

            self.db.cur.execute(sql)
            self.db.conn.commit()

    def get_record(self):
        with self.db:
            sql = f"""
                SELECT name, start_time 
                FROM {self.table_name}
                WHERE execution=1 and weekday LIKE '%' || (strftime('%w', date('now'))) || '%';
            """

            self.db.cur.execute(sql)

            rows = self.db.cur.fetchall()
            
        ls = [JobContent(row[0], str(row[1])) for row in rows]

        return ls
    
    def get_channel(self, name):
        with self.db:
            sql = f"""
                SELECT (channel) FROM channel
                WHERE id IN
                (
                    SELECT (channel) FROM {self.table_name}
                WHERE name='{name}'
                )
            """

            self.db.cur.execute(sql)

            rows = self.db.cur.fetchall()

        return rows[0][0]

class ChannelDB(MainDB):
    def __init__(self):
        super().__init__()

    def create_table(self):
        with self.db:
            sql = f"""
                CREATE TABLE IF NOT EXISTS channel (
                id integer PRIMARY KEY,
                name string(16),
                channel integer NOT NULL
                );
                """
            
            self.db.cur.execute(sql)

if __name__ == "__main__":
    m = MainDB()
    m.create_table()