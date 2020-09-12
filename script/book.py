from user_agent import generate_user_agent
from datetime import datetime, timedelta
from traceback import print_exc
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import json
import re

class BookContent():
    def __init__(self, book_source, book_title, book_link, book_price):
        self.book_source = book_source
        self.book_title = book_title
        self.book_link = f"<{book_link}>"
        self.book_price = book_price

class BooksDiscount:
    def __init__(self, url, init_txt=''):
        self.url = url
        self.init_txt = init_txt
        self.pre_send_txt_ls = [init_txt] if init_txt else []

        self.book_content_ls = []

        self.session = requests.Session()

    def get_res(self, url):
        headers = {
            'user-agent': generate_user_agent()
        }
        with self.session.get(url, headers=headers) as res:
            pass
        if res.status_code == 200:
            return res

        self.pre_send_txt_ls.append(f'request {self.url} faild request code : {res.status_code}')
        return None

    def get_soup(self, res):
        if res:
            return BeautifulSoup(res.text, 'html.parser')
        return None

    def main_process(self):
        res = self.get_res(self.url)
        soup = self.get_soup(res)

        book_title = soup.select("h1 > a")[0].text
        book_link = soup.select("h1 > a")[0]['href']

        book_price = soup.select("ul.price.clearfix > li > b")[1].text # index 0 is "66"(discount rate)

        self.book_content_ls.append(
            BookContent(
                self.init_txt,
                book_title,
                book_link,
                book_price)
        )
        
        self.output_process()

    def output_process(self):
        for book in self.book_content_ls:
            msg = f"{book.book_title}\n{book.book_link}\n{book.book_price}"

            self.pre_send_txt_ls.append(msg)

    def run(self):
        try:
            self.main_process()

        except Exception as e:
            print_exc()
            self.pre_send_txt_ls.append(f'{e}')

        return '\n'.join(self.pre_send_txt_ls)

class TaazeDiscount(BooksDiscount):
    def __init__(self, url, init_txt=''):
        super().__init__(url, init_txt=init_txt)
        self.pre_url = "https://www.taaze.tw/"
    
    def main_process(self):
        res = self.get_res(self.url)
        soup = self.get_soup(res)

        div_soup = soup.select("div.carousel.slide")[0]
        div_soup = soup.select("div.carousel-inner > div.item")

        for n, ele_soup in enumerate(div_soup):
            # i don't know why can't select div block. i can just get first nest soup. than use re to find price.
            temp_soup = ele_soup.select("div.description")[0]
            try:
                book_price = re.findall(r">(\d*?)</span>", str(temp_soup))[1] # index 0 is discount
            except IndexError:
                book_price = re.findall(r">(\d*?)</span>", str(temp_soup))[0] # no discount.

            book_title = re.findall(r";\">(.*?)</strong>", str(temp_soup))[0]
            book_link = self.pre_url + re.findall(r"href='/(.*?)'\">", str(temp_soup))[0]
            
            self.book_content_ls.append(
                BookContent(
                    self.init_txt,
                    book_title,
                    book_link,
                    book_price
                )
            )

            

            if n == 2: # div_soup has catch a lots of data. I just need first three data.
                break
        
        self.output_process()

class SanminDiscount(BooksDiscount):
    def __init__(self, url, init_txt=''):
        super().__init__(url, init_txt=init_txt)
    
    def main_process(self):
        res = self.get_res(self.url)
        soup = self.get_soup(res)

        table_soup = soup.select('div.this66 > table')

        for table_ele in table_soup[:-1]:
            a_soup = table_ele.select("p.PicTd > a")[0]

            book_title = a_soup.text
            book_link = f"https:{a_soup['href']}"
            book_price = table_ele.select("span")[2].text # index 0 and 1 are original price and disscount rate

            if '簡體書' not in book_title:
                self.book_content_ls.append(
                    BookContent(
                        self.init_txt,
                        book_title,
                        book_link,
                        book_price
                    )
                )

        self.output_process()

class MomoDiscount(BooksDiscount):
    def __init__(self, url, init_txt=''):
        super().__init__(url, init_txt=init_txt)

    def main_process(self):
        res = self.get_res(self.url)
        soup = self.get_soup(res)

        div_soup = soup.select('div#bt_2_095_01_small > div.TabContent > div.TabContentD')[:2]
        for ele in div_soup:
            a_soup = ele.find('a')

            book_title = a_soup['title']
            book_link = "https://www.momoshop.com.tw/" + a_soup['href']
            book_price = a_soup.find('b').text

            self.book_content_ls.append(
                BookContent(
                    self.init_txt,
                    book_title,
                    book_link,
                    book_price
                )
            )
        self.output_process()

class TenlongNewBook(BooksDiscount):
    def __init__(self, url, init_txt=""):
        super().__init__(url, init_txt)
        self.pre_url_formula = "https://www.tenlong.com.tw{}"
        self.today_date = datetime.today()

    def main_process(self):
        res = self.get_res(self.url)
        soup = self.get_soup(res)
        
        book_div = soup.select("li.single-book")
        
        for book_ele in book_div:

            book_link = self.pre_url_formula.format(book_ele.a["href"])
            res = self.get_res(book_link)
            soup = self.get_soup(res)

            book_date = soup.select("ul.item-sub-info > li > span.info-content")[1].text
            book_date = datetime.strptime(book_date, "%Y-%m-%d") # str -> datetime

            gap = (self.today_date - book_date).days

            if gap<=7:
                book_title = soup.select("h1.item-title")[0].text.strip()
                book_price = "-".join([ ele.text.strip() for ele in soup.select("span.pricing")])
                self.book_content_ls.append(
                    BookContent(
                        self.init_txt,
                        book_title,
                        book_link,
                        book_price
                    )
                )

        self.output_process()

class Hyread(BooksDiscount):
    def __init__(self, url, init_txt=''):
        super().__init__(url, init_txt=init_txt)

    def process_one(self, soup):
        book_title = soup.select("h6 > a")[0].text
        book_link = self.url + soup.select("h6 > a")[0]['href']

        self.book_content_ls.append(
            BookContent(
                self.init_txt,
                book_title,
                book_link,
                "")
        )

    def main_process(self):
        res = self.get_res(self.url)
        soup = self.get_soup(res)

        div_soup_ls = soup.select("div.item.col-five.col-sm-6.col-xs-6")

        list(map(self.process_one, div_soup_ls))

        self.output_process()