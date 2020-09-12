from user_agent import generate_user_agent
from traceback import print_exc
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import re

from models import PTTDB

class Content():
    def __init__(self, title, link):
        self.title = title
        self.link = f"<{link}>"

class PTTArticle:
    def __init__(self, init_txt=''):
        self.url_formula = "https://www.ptt.cc/bbs/{}/index.html"
        self.index_formula = "https://www.ptt.cc/bbs/{}/index{}.html"

        self.section_ls = ["Browsers", "CompBook"]
        
        self.init_txt = init_txt
        self.pre_send_txt_ls = [init_txt] if init_txt else []
        self.content_ls = []

        self.session = requests.Session()

    def get_res(self, url):
        headers = {
            'user-agent': generate_user_agent()
        }
        with self.session.get(url, headers=headers) as res:
            pass
        if res.status_code == 200:
            return res

        self.pre_send_txt_ls.append(f'request {url} faild request code : {res.status_code}')
        return None

    def get_soup(self, res):
        if res:
            return BeautifulSoup(res.text, 'html.parser')
        return None
    
    def get_lastest_page(self, url) -> int:
        res = self.get_res(url)
        soup = self.get_soup(res)

        link = soup.select('div.btn-group.btn-group-paging a')[1]['href']

        return int(re.findall(r'index(\d+).', link)[0]) + 1

    def yield_data(self, soup):
        today = datetime.now()
        day_frame = 7

        for ele in soup:
            date = ele.find('div', class_='date').text.strip()
            date_str = str(today.year)+'/'+date
            date_tiem = datetime.strptime(date_str, "%Y/%m/%d") # EX:2020 + / + 1/2

            if 0<=(today-date_tiem).days <= day_frame or -366<=(today-date_tiem).days<=-358 :
                title_soup = ele.find('div', class_='title')
                
                try:
                    title = date_str + title_soup.find('a').text                    
                    link_url = 'https://www.ptt.cc' + title_soup.find('a')['href']
                    yield [title, link_url]

                except AttributeError:
                    pass

    def stop_check(self, soup):
        '''
        Trough check the first data's date to know this page should stop to not.
        :Return boolean
        '''
        today = datetime.now()
        day_frame=7

        for ele in soup:
            date = ele.find('div', class_='date').text.strip()
            date = datetime.strptime(str(today.year)+'/'+date, "%Y/%m/%d") # EX:2020 + / + 1/2
            
            return not (0<=(today-date).days <= day_frame or -366<=(today-date).days<=-358)

    def main_process(self):
        for section in self.section_ls:
            FLAG = False

            url = self.url_formula.format(section)
            page = self.get_lastest_page(url)

            while not FLAG:
                url = self.index_formula.format(section, page)

                res = self.get_res(url)
                soup = self.get_soup(res)
                div_soup = soup.select('div.r-ent')

                res_ls = list(self.yield_data(div_soup))
                for res in res_ls:
                    self.content_ls.append(
                        Content(
                            res[0],
                            res[1]
                        )
                    )
                
                FLAG = self.stop_check(div_soup)
                page -= 1

        self.output_process()

    def output_process(self):
        for cnt in self.content_ls:
            self.pre_send_txt_ls.append(
                f"{cnt.title}\n{cnt.link}"
            )

    def run(self):
        try:
            self.main_process()

        except Exception as e:
            print_exc()
            self.pre_send_txt_ls.append(f'{e}')

        return '\n'.join(self.pre_send_txt_ls)

class PTTGamesaleArticles:
    def __init__(self, init_txt=''):
        self.url_formula = "https://www.ptt.cc/bbs/{}/index.html"
        self.index_formula = "https://www.ptt.cc/bbs/{}/index{}.html"        

        self.section_ls = ["Gamesale",]
        self.db = PTTDB()
        self.init_txt = init_txt
        self.pre_send_txt_ls = [init_txt] if init_txt else []
        self.content_ls = []

        self.session = requests.Session()

        self.content_keyword = "台中"
        self.title_keyword_ls = self.db.get_keywords()

    def get_res(self, url):
        headers = {
            'user-agent': generate_user_agent()
        }
        with self.session.get(url, headers=headers) as res:
            pass
        if res.status_code == 200:
            return res

        self.pre_send_txt_ls.append(f'request {url} faild request code : {res.status_code}')
        return None

    def get_soup(self, res):
        if res:
            return BeautifulSoup(res.text, 'html.parser')
        return None

    def get_lastest_page(self, url) -> int:
        res = self.get_res(url)
        soup = self.get_soup(res)

        link = soup.select('div.btn-group.btn-group-paging a')[1]['href']

        return int(re.findall(r'index(\d+).', link)[0]) + 1

    def yield_data(self, soup):
        """
        : Return: list of Content(title, link).
        """
        today = datetime.now()
        day_frame = 0

        for ele in soup:
            date = ele.find('div', class_='date').text.strip()
            date_str = str(today.year)+'/'+date
            date_tiem = datetime.strptime(date_str, "%Y/%m/%d") # EX:2020 + / + 1/2

            if 0<=(today-date_tiem).days <= day_frame or -366<=(today-date_tiem).days<=-358 :
                title_soup = ele.find('div', class_='title')
                
                try:
                    title = title_soup.find('a').text.replace(" ", "")                  
                    link_url = 'https://www.ptt.cc' + title_soup.find('a')['href']
                    yield Content(title, link_url)

                except AttributeError:
                    pass

    def content_keyword_check(self, c):
        """
            if it has self.content_keyword in Content.title, add self.content_keyword in title.
        """
        res = self.get_res(c.link[1:-1]) # exclude < and >

        if re.search(self.content_keyword, res.text):
            c.title = self.content_keyword + c.title            
        return c

    def title_keyword_filter(self, c):
        for title_keyword in self.title_keyword_ls:
            if title_keyword in c.title:
                return True
        return False

    def filter_content(self, temp_content_ls, title_keyword_ls=list()):
        """    
            Filter by keywords
            The keywords are group of single or multiple words.

            :Parameters temp_content_ls: list of Contant(title, link).
            example: [Content1, Content2, ...]

            :Parameters title_keywords_ls: 
            example: [ "動物森友會", "OOXX", ... ]

            :Return results: list of Content.
        """
        content_ls = list(filter(lambda c: "NS" in c.title, temp_content_ls))

        if self.title_keyword_ls:
            content_ls = list(filter(self.title_keyword_filter, content_ls))
            content_ls = list(map(self.content_keyword_check, content_ls))
        else:
            content_ls = list(map(self.content_keyword_check, content_ls))

        return content_ls

    def stop_check(self, soup):
        '''
        Trough check the first data's date to know this page should stop to not.
        :Return boolean
        '''
        today = datetime.now()
        day_frame = 0

        for ele in soup:
            date = ele.find('div', class_='date').text.strip()
            date = datetime.strptime(str(today.year)+'/'+date, "%Y/%m/%d") # EX:2020 + / + 1/2
            
            return not (0<=(today-date).days <= day_frame or -366<=(today-date).days<=-358)
    
    def main_process(self):
        for section in self.section_ls:
            self.title_keyword_ls = self.db.get_keywords()

            # init
            url = self.url_formula.format(section)
            FLAG = False
            page = self.get_lastest_page(url)

            while not FLAG:
                url = self.index_formula.format(section, page)
                res = self.get_res(url)
                soup = self.get_soup(res)
                div_soup = soup.select('div.r-ent')

                temp_content_ls = list(self.yield_data(div_soup))

                if self.title_keyword_ls:
                    content_ls = self.filter_content(temp_content_ls, self.title_keyword_ls)
                else:
                    content_ls = self.filter_content(temp_content_ls)
                
                for content in content_ls:
                    self.pre_send_txt_ls.append(f"{content.title}\n{content.link}")

                FLAG = self.stop_check(div_soup)

                page -= 1

    def run(self):
        try:
            self.main_process()

        except Exception as e:
            print_exc()
            self.pre_send_txt_ls.append(f'{e}')

        return '，'.join(self.pre_send_txt_ls)

