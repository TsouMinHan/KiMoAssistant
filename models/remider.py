from models import MainDB

class RemiderContent():
    def __init__(self, title, content, start_time):
        self.title = title
        self.content = content
        self.start_time = start_time

class RemiderDB(MainDB):
    def __init__(self):
        super().__init__()
        self.table_name = "remider"
    
    def create_table(self):
        with self.db:
            sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                id integer PRIMARY KEY,
                title string(8) NOT NULL,
                content string(64) NOT NULL,
                start_time string(64) NOT NULL,
                weekday string(8) NOT NULL
                );
            """

            self.db.cur.execute(sql)
        
    def get_record(self):
        with self.db:
            sql = f"""
                SELECT * FROM {self.table_name}
                WHERE weekday LIKE '%' || (strftime('%w', date('now'))) || '%';
            """

            self.db.cur.execute(sql)

            rows = self.db.cur.fetchall()

        return [ RemiderContent(row[1], row[2], row[3]) for row in rows ]