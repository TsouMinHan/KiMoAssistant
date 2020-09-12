from script import job_baha_MS, job_baha_news, job_baha_NS, job_baha_off_site, job_baha_political, job_baha_translate, job_baha_FA
from script import job_book_discount, job_taaze_discount, job_sanmin_discount, job_momo_discount, job_tenlong_discount, job_hyread_recommend
from script import job_NoRSSNews, job_RSSNews
from script import job_PTT_article, job_PTT_gamesale_articles
from script import job_clean, job_remider
from models import MainDB, NewsDB, BahaDB, RemiderDB
from config import Config

baha_ls = [job_baha_MS, job_baha_news, job_baha_NS, job_baha_off_site, job_baha_political, job_baha_translate, job_baha_FA]
book_ls = [job_book_discount, job_taaze_discount, job_sanmin_discount, job_momo_discount, job_tenlong_discount, job_hyread_recommend]
news_ls = [job_NoRSSNews, job_RSSNews]
ptt_ls = [job_PTT_article, job_PTT_gamesale_articles]

# for func in baha_ls:
#     print(func.__name__)
#     func()

if __name__ == "__main__":
    job_RSSNews()
    job_NoRSSNews()
    # db = NewsDB()
    # db.modify()
    # print(a)
    # import requests
    # res = requests.get('https://en.wikipedia.org/wiki/Monty_Python')
    # print(res)
    # print(res.headers)
    # print(res.request.headers)
    pass