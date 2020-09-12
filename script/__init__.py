from datetime import datetime

from .book import BooksDiscount, TaazeDiscount, SanminDiscount, MomoDiscount, TenlongNewBook, Hyread
from .ptt_article import PTTArticle, PTTGamesaleArticles
from models import NotifyDB, MainDB, NewsDB, BahaDB
from .news import NoRSSNews, RSSNews
from .remider import Remider
from .baha import BaHa
from .decorator import log

db = NotifyDB()
m_db = MainDB()

# ========== NEWS ==========
@log
def job_NoRSSNews():
    n = NoRSSNews()
    msg = n.run()
    print(msg)
    db.add_notify(msg, m_db.get_channel(job_NoRSSNews.__name__))

    del n

@log
def job_RSSNews():
    n = RSSNews()
    msg = n.run()
    db.add_notify(msg, m_db.get_channel(job_RSSNews.__name__))

    del n

# ========== Baha Article ==========
@log
def job_baha_off_site():
    b = BaHa("Baha:Off-site", "60076")
    msg = b.run()
    db.add_notify(msg, m_db.get_channel(job_baha_off_site.__name__))

    del b

@log
def job_baha_MS():
    b = BaHa("Baha:MS", "25052")
    msg = b.run()
    db.add_notify(msg, m_db.get_channel(job_baha_MS.__name__))

    del b

@log
def job_baha_translate():
    b = BaHa("Baha:translate", "60508", gp=0, subsection="&subbsn=11")
    msg = b.run()
    db.add_notify(msg, m_db.get_channel(job_baha_translate.__name__))

    del b

@log
def job_baha_NS():
    b = BaHa("Baha:NS", "31587", gp=0)
    msg = b.run()
    db.add_notify(msg, m_db.get_channel(job_baha_NS.__name__))

    del b

@log
def job_baha_news():
    b = BaHa("Baha:Off-site-News", "60076", subsection="&subbsn=16")
    msg = b.run()
    db.add_notify(msg, m_db.get_channel(job_baha_news.__name__))

    del b

@log
def job_baha_political():
    b = BaHa("Baha:Off-site-political", "60076", gp=10, subsection="&subbsn=15")
    msg = b.run()
    db.add_notify(msg, m_db.get_channel(job_baha_political.__name__))

    del b

@log
def job_baha_FA():
    b = BaHa("Baha:FA", "7287")
    msg = b.run()
    db.add_notify(msg, m_db.get_channel(job_baha_FA.__name__))

    del b

# ========== Book Discount ==========
@log
def job_book_discount():
    b = BooksDiscount("https://activity.books.com.tw/crosscat/ajaxinfo/getBooks66OfTheDayAjax/P?uniqueID=E180629000000001_94", "柏克萊")

    msg = b.run()
    db.add_notify(msg, m_db.get_channel(job_book_discount.__name__))

    del b

@log
def job_taaze_discount():
    a = TaazeDiscount("https://www.taaze.tw/index.html", "讀冊")
    msg = a.run()

    db.add_notify(msg, m_db.get_channel(job_taaze_discount.__name__))

    del a

@log
def job_sanmin_discount():
    new_book = SanminDiscount("https://activity.sanmin.com.tw/Today66", "三民")
    msg = new_book.run()

    db.add_notify(msg, m_db.get_channel(job_sanmin_discount.__name__))

    del new_book

@log
def job_momo_discount():
    momo = MomoDiscount("https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=4099900000&mdiv=1099700000-bt_0_957_01-&ctype=B", "MOMO")
    msg = momo.run()

    db.add_notify(msg, m_db.get_channel(job_momo_discount.__name__))

    del momo

@log
def job_tenlong_discount():
    t = TenlongNewBook("https://www.tenlong.com.tw/zh_tw/recent?stock=available", "天龍")
    msg = t.run()

    db.add_notify(msg, m_db.get_channel(job_tenlong_discount.__name__))

    del t

@log
def job_hyread_recommend():
    t = Hyread("https://taichunggov.ebook.hyread.com.tw/", "台中 - Hyread推薦")
    msg = t.run()

    db.add_notify(msg, m_db.get_channel(job_hyread_recommend.__name__))

    t = Hyread("https://ntledu.ebook.hyread.com.tw/", "台灣 - Hyread推薦")
    msg = t.run()

    db.add_notify(msg, m_db.get_channel(job_hyread_recommend.__name__))

    t = Hyread("https://tpml.ebook.hyread.com.tw/", "台北 - Hyread推薦")
    msg = t.run()

    db.add_notify(msg, m_db.get_channel(job_hyread_recommend.__name__))

    del t

# ========== PTT Article ==========
@log
def job_PTT_article():
    b = PTTArticle()
    msg = b.run()

    db.add_notify(msg, m_db.get_channel(job_PTT_article.__name__))

    del b

@log
def job_PTT_gamesale_articles():
    b = PTTGamesaleArticles()
    msg = b.run()

    for m in msg.split("，"):
        db.add_notify(m, m_db.get_channel(job_PTT_gamesale_articles.__name__))

    del b

# ========== Another ==========
@log
def job_clean():
    n = NewsDB()
    msg = n.clean()

    db.add_notify(msg, m_db.get_channel(job_clean.__name__))

    b = BahaDB()
    msg = b.clean()

    db.add_notify(msg, m_db.get_channel(job_clean.__name__))
    
    del n, b

@log
def job_remider():
    b = Remider()
    content_ls = b.run()

    for content in content_ls:
        db.add_notify(
            f"{content.title}\n{content.content}",
            m_db.get_channel(job_remider.__name__),
            content.start_time
        )

    del b

