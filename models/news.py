from pathlib import Path
import datetime
import sqlite3

from config import Config

class ConfigContent:
    def __init__(self, job_name: str, weekday: str, time: list):
        self.job_name = job_name
        self.weekday = weekday
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

class NewsDB:  
    def __init__(self):
        self.db = DBHandler()
        self.table_name = "News"

    def create_table(self):
        with self.db:
            sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                id integer PRIMARY KEY,
                title string(32) NOT NULL,
                website string(16) NOT NULL,
                date date DEFAULT (date()),
                seen integer DEFAULT 0,
                link string(256)
                );
                """
            
            self.db.cur.execute(sql)

    def get_record(self, website):
        with self.db:
            sql = f"""
                SELECT link FROM {self.table_name} WHERE website='{website}' ORDER BY date DESC, id DESC;
            """

            self.db.cur.execute(sql)
            
            rows = self.db.cur.fetchall()

        return rows[0][0] if rows else ""

    def insert(self, ls):
        with self.db:
            for ele in ls:
                ele.title = ele.title.replace("'", "''")
                ele.link = ele.link.replace("'", "''")

                sql = f"""
                    INSERT INTO {self.table_name} (title, website, link) VALUES 
                    ('{ele.title}', '{ele.website}', '{ele.link}')
                """
                self.db.cur.execute(sql)
            self.db.conn.commit()

    def clean(self):
        with self.db:
            sql = f"""
                DELETE FROM {self.table_name} WHERE id NOT IN (SELECT Max(id) From {self.table_name} Group By link);
            """
            self.db.cur.execute(sql)

            self.db.cur.execute("SELECT changes()")
            number_of_deleted = self.db.cur.fetchall()[0][0]

            self.db.conn.commit()
            
        return f"新聞 - 刪除了 {number_of_deleted} 筆重複內容"
            
if __name__ == "__main__":
    pass
    