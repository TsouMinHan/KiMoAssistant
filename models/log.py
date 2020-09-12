from .main import MainDB

class LogDB(MainDB):
    def __init__(self):
        super().__init__()
        self.table_name = "log"

    def create_table(self):
        with self.db:
            sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id integer PRIMARY KEY,
                    title string(32) NOT NULL,
                    msg txt,
                    datetime datetime DEFAULT (datetime('now', 'localtime'))
                );
            """

            self.db.cur.execute(sql)
    
    def add_log(self, title, msg):
        with self.db:
            sql = f"""
                INSERT INTO {self.table_name} (title, msg)
                VALUES (
                    '{title}', '{msg}'
                );
            """

            self.db.cur.execute(sql)
            self.db.conn.commit()