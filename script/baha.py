from user_agent import generate_user_agent
from traceback import print_exc
from bs4 import BeautifulSoup
import requests
import json
import re

from models import BahaDB

class BaHa:
    def __init__(self, name, id, init_txt="", gp=50, subsection=""):
        self.name = name
        self.url = f"https://forum.gamer.com.tw/B.php?page=1&bsn={id}{subsection}"
        self.pre_url = f"https://forum.gamer.com.tw/C.php?bsn={id}&snA="
        self.init_txt = init_txt
        self.gp = gp
        self.pre_send_txt_ls = [init_txt] if init_txt else []

        self.session = requests.Session()

        self.db = BahaDB()

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

    def get_article_soup_ls(self, url):
        res = self.get_res(url)
        soup = self.get_soup(res)

        return soup.select('tr.b-list__row')

    def get_gp(self, soup):
        try:
            gp = int(soup.find('td', class_='b-list__summary').span.text)
        except AttributeError:
            gp = 0
        
        return gp

    def get_title(self, soup):
        try:
            title = soup.find('p', class_='b-list__main__title').text
        except:
            title = soup.find('a', class_='b-list__main__title')
            if title:
                title = title.text
            else:
                title = ""

        return title.strip()

    def get_link_id(self, soup):
        try:
            link_id = soup.find('td', class_='b-list__main')
            link_id = link_id.a['href']
            link_id = re.findall(r'snA=(\d+)', link_id)   
            
        except AttributeError: # Triggering condition is advertisement crawling.
            return
        except TypeError: # Maybe triggering condition is advertisement crawling.
            return

        return link_id[0]

    def get_post_time(self, url):
        res = self.get_res(url)
        soup = self.get_soup(res)

        return soup.select("div .c-post__header__info > a")[0].text

    def main_process(self):
        record_ls = self.db.get_record(self.name)

        page = 1
        FLAG = False
        url = self.url

        while page<5 and not FLAG:

            for ele in  self.get_article_soup_ls(url):
                gp = self.get_gp(ele)
                title = self.get_title(ele)
                if title=="本討論串已無文章" or title=="首篇已刪":
                    continue

                link_id = self.get_link_id(ele)

                if not link_id: # cause advertisement.
                    continue

                if gp<self.gp:
                    continue

                link = f"{self.pre_url + link_id}"

                if link in record_ls:
                    continue
                
                post_time = self.get_post_time(link)

                self.db.add_article(title, link, 1 if gp>2000 else 0, self.name)
                self.pre_send_txt_ls.append(f"{title}\n{post_time}\n<{link}>\n{gp}")
                FLAG = True # break while loop
                break # break for loop

            url = self.url.replace(f"page={page}", f"page={page+1}")
            page += 1

    def run(self):
        try:
            self.main_process()

        except Exception as e:
            print_exc()
            self.pre_send_txt_ls.append(f'{e}')

        return '\n'.join(self.pre_send_txt_ls)
