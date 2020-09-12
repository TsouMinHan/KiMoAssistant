from models import MainDB, NewsDB, NotifyDB, BahaDB, PTTDB, ChannelDB, RemiderDB, LogDB

db_ls = [MainDB, NewsDB, NotifyDB, BahaDB, PTTDB, ChannelDB, RemiderDB, LogDB]

for db in db_ls:
    a = db()
    a.create_table()
