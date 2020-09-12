from datetime import datetime
import schedule
import time

from script import job_baha_MS, job_baha_news, job_baha_NS, job_baha_off_site, job_baha_political, job_baha_translate, job_baha_FA
from script import job_book_discount, job_taaze_discount, job_sanmin_discount, job_momo_discount, job_tenlong_discount, job_hyread_recommend
from script import job_PTT_article, job_PTT_gamesale_articles
from script import job_NoRSSNews, job_RSSNews
from script import job_clean, job_remider
from models import MainDB

'''If you have new job, remember append to the dictionary.'''
job_dc = {
    "job_NoRSSNews": job_NoRSSNews,
    "job_RSSNews": job_RSSNews,

    "job_baha_translate": job_baha_translate,
    "job_baha_political": job_baha_political,
    "job_baha_off_site": job_baha_off_site,
    "job_baha_news": job_baha_news,
    "job_baha_NS": job_baha_NS,
    "job_baha_MS": job_baha_MS,
    "job_baha_FA": job_baha_FA,

    "job_sanmin_discount": job_sanmin_discount,
    "job_taaze_discount": job_taaze_discount,
    "job_book_discount": job_book_discount,
    "job_momo_discount": job_momo_discount,
    "job_tenlong_discount": job_tenlong_discount,
    "job_hyread_recommend": job_hyread_recommend,

    "job_PTT_gamesale_articles": job_PTT_gamesale_articles,
    "job_PTT_article": job_PTT_article,

    "job_clean": job_clean,
    "job_remider": job_remider,
}

def show_now_time(function_name):
    now_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(f'Start {function_name} at {now_time}')

def set_execution(func, time):
    time_ls = time.split(",")

    print(f"--Set {func.__name__}")
    
    for ti in time_ls:
        schedule.every().day.at(ti).do(func) 
        print(str(datetime.today().weekday()+1), ti)

def set_schedule():
    show_now_time(set_schedule.__name__)
    
    schedule.clear() # clear schedule make sure that schedule is clean before assigning the jobs

    db = MainDB()

    for job in db.get_record():
        func = job_dc[job.name]
        
        set_execution(func, job.time)

    schedule.every().day.at("00:01").do(set_schedule)  

def run():
    show_now_time('Main')

    while True:
        time.sleep(30)
        schedule.run_pending()

if __name__ == '__main__':
    set_schedule()
    run()
