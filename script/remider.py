from traceback import print_exc
from datetime import datetime

from models import RemiderDB, RemiderContent

class Remider():
    def __init__(self):
        self.pre_send_txt_ls = list()

        self.db = RemiderDB()
    
    def process_one(self, remider_content):
        time_ls = remider_content.start_time.split(",")

        for time in time_ls:
            self.pre_send_txt_ls.append(
                RemiderContent(
                    remider_content.title,
                    remider_content.content,
                    datetime.today().replace(hour=int(time.split(":")[0]), minute=int(time.split(":")[1]))
                )
            )

    def main_process(self):
        remider_content_ls = self.db.get_record()     
        
        list(map(self.process_one, remider_content_ls))

    def run(self):
        try:
            self.main_process()

        except Exception as e:
            print_exc()
            self.pre_send_txt_ls.append(f'{e}')

        return self.pre_send_txt_ls