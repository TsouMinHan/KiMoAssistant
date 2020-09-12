from pathlib import Path
import datetime
import sqlite3

from config import Config

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

class BahaDB:  
    def __init__(self):
        self.db = DBHandler()
        self.table_name = "baha"

    def create_table(self):
        with self.db:
            sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                id integer PRIMARY KEY,
                title string(32) NOT NULL,
                link string(64) NOT NULL,
                special string(1) NOT NULL,
                name string(16) NOT NULL
                );
                """
            
            self.db.cur.execute(sql)

    def add_article(self, title, link, special, name):
        with self.db:
            title = title.replace("'", "''")
            
            sql = f"""
                INSERT INTO {self.table_name} (title, link, special, name) VALUES 
                ('{title}', '{link}', '{special}', '{name}');
            """

            self.db.cur.execute(sql)
            self.db.conn.commit()

    def get_record(self, name):
        with self.db:
            sql = f"""
                SELECT link FROM {self.table_name} WHERE name='{name}'
            """

            self.db.cur.execute(sql)

            rows = self.db.cur.fetchall()
            
        ls = [row[0] for row in rows]

        return ls

    def check_record(self, link):
        with self.db:
            sql = f"""
                SELECT link FROM {self.table_name} WHERE link='{link}'
            """

            self.db.cur.execute(sql)

            rows = self.db.cur.fetchall()
            
        ls = [row[0] for row in rows]

        return ls

    def clean(self):
        with self.db:
            sql = f"""
                DELETE FROM {self.table_name}
                WHERE name in 
                (
                    SELECT name FROM {self.table_name}
                    WHERE special='0'
                    GROUP BY name
                    HAVING count(*) > 1000
                ) and special='0'
            """
            self.db.cur.execute(sql)

            self.db.cur.execute("SELECT changes()")
            number_of_deleted = self.db.cur.fetchall()[0][0]

            self.db.conn.commit()
        
        return f"巴哈 - 刪除了 {number_of_deleted} 筆重複內容"

if __name__ == "__main__":
    pass