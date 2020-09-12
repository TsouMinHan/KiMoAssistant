from user_agent import generate_user_agent
from traceback import print_exc
from bs4 import BeautifulSoup
import requests
import json
import re

from models import NewsDB

class Content():
    def __init__(self, title, link, website):
        self.title = title
        self.link = link
        self.website = website

class RSSNews:
    def __init__(self, init_txt=''):
        self.init_txt = init_txt
        self.pre_send_txt_ls = [init_txt] if init_txt else []

        self.session = requests.Session()

        self.db = NewsDB()

        self.website_dc = {
            "Bnext": {
                "url": "https://www.bnext.com.tw/rss",
                "record_url": self.db.get_record("Bnext")
            },
            "Ithome": {
                "url": "https://www.ithome.com.tw/rss",
                "record_url": self.db.get_record("Ithome")
            },
            "Techbang": {
                "url": "https://feeds.feedburner.com/techbang/daily",
                "record_url": self.db.get_record("Techbang")
            },
            "TheNewsLens": {
                "url": "https://feeds.feedburner.com/TheNewsLens",
                "record_url": self.db.get_record("TheNewsLens")
            },
            "businessweekly": {
                "url": "http://cmsapi.businessweekly.com.tw/?CategoryId=24612ec9-2ac5-4e1f-ab04-310879f89b33&TemplateId=8E19CF43-50E5-4093-B72D-70A912962D55",
                "record_url": self.db.get_record("businessweekly")
            },
            "businessweekly-Wealth": {
                "url": "https://www.businessweekly.com.tw/Event/feedsec.aspx?feedid=10&channelid=15",
                "record_url": self.db.get_record("businessweekly-Wealth")
            },
            "chainnews": {
                "url": "https://www.chainnews.com/zh-hant/feeds/articles/",
                "record_url": self.db.get_record("chainnews")
            },
            "abmedia": {
                "url": "https://www.abmedia.io/feed/",
                "record_url": self.db.get_record("abmedia")
            },
            "toy-people": {
                "url": "https://feeds.feedburner.com/toy-people?format=xml",
                "record_url": self.db.get_record("toy-people")
            }
        }

    def get_res(self, url):
        headers = {
            'user-agent': generate_user_agent()
        }
        with self.session.get(url, headers=headers) as res:
            pass
        if res.status_code == 200:
            return res

        self.add_to_pre_send_txt_ls(f'request {url} faild request code : {res.status_code}')
        return None

    def get_soup(self, res):
        if res:
            return BeautifulSoup(res.text, 'html.parser')
        return None

    def main_process(self):
        for website in self.website_dc:
            print(f"開始爬取 {website} 文章")

            res = self.get_res(self.website_dc[website]["url"])
            html = res.text.replace("\n", "")

            item_ls = re.findall(r"<item>(.*?)</item>", html)
            
            ls = []

            for item in item_ls:
                title = re.findall(r"<title>(.*?)</title>", item)[0].strip()
                link = re.findall(r"<link>(.*?)</link>", item)[0].strip()
                
                # if duplicate, end crawler this web site
                if link == self.website_dc[website]["record_url"]:
                    break

                ls.append(
                    Content(
                        title,
                        link,
                        website
                    )
                )

            self.db.insert(ls[::-1])
            self.add_to_pre_send_txt_ls(f"{website} 輸入了 {len(ls)} 筆資料\n")

    def add_to_pre_send_txt_ls(self, msg):
        self.pre_send_txt_ls.append(msg)

    def run(self):
        try:
            self.main_process()

        except Exception as e:
            print_exc()
            self.add_to_pre_send_txt_ls(f'{e}')

        return '\n'.join(self.pre_send_txt_ls)

class NoRSSNews:
    def __init__(self, init_txt=''):
        self.init_txt = init_txt
        self.pre_send_txt_ls = [init_txt] if init_txt else []

        self.session = requests.Session()
        self.db = NewsDB()

        self.website_dc = {
            "Blocktempo": {
                "url": "https://www.blocktempo.com/category/latest-news/",
                "parmas": {"page": 1},
                "record_url": self.db.get_record("Blocktempo"),
                "title_command": "div.jeg_postblock_content > h3",
                "link_command": "div.jeg_postblock_content > h3",
            },
            "Inside": {
                "url": "https://www.inside.com.tw/",
                "parmas": {"page": 1},
                "record_url": self.db.get_record("Inside"),
                "title_command": "h3.post_title",
                "link_command": "h3.post_title",
            },
            "Playpcesor": {
                "url": "https://www.playpcesor.com/",
                "parmas": {"page": 1},
                "record_url": self.db.get_record("Playpcesor"),
                "title_command": "h3.post-title",
                "link_command": "h3.post-title",
            },
            "Daodu": {
                "url": "https://daodu.tech/",
                "parmas": {"page": 0}, # not work, but i think it isn't a problem.
                "record_url": self.db.get_record("Daodu"),
                "title_command": "div.post-list-text-content > div.post-header > h2",
                "link_command": "div.post-list-text-content > div.post-header > h2",
            },
            "Haze": {
                "url": "https://www.chainnews.com/zh-hant/u/295997329585.htm",
                "parmas": {"page": 1},
                "record_url": self.db.get_record("Haze"),
                "title_command": "h2.feed-post-title",
                "link_command": "h2.feed-post-title",
            }
        }

    def get_res(self, url, params={}):
        headers = {
            'user-agent': generate_user_agent()
        }
        with self.session.get(url, headers=headers, params=params) as res:
            pass
        
        if res.status_code == 200:
            return res

        self.pre_send_txt_ls.append(f'request {url} faild request code : {res.status_code}')
        return None

    def get_soup(self, res):
        if res:
            return BeautifulSoup(res.text, 'html.parser')
        return None

    def main_process(self):     

        for website in self.website_dc:
            ls = []
            
            print(f"開始爬取 {website} 文章")

            FLAG = False

            while self.website_dc[website]["parmas"]["page"] < 6 and not FLAG:
                url = self.website_dc[website]["url"]
                parmas = self.website_dc[website]["parmas"]

                res = self.get_res(url, parmas)
                soup = self.get_soup(res)

                if not soup:
                    break

                title_soup = soup.select(self.website_dc[website]["title_command"])
                link_soup = soup.select(self.website_dc[website]["link_command"])

                for i in range(len(title_soup)):
                    title = title_soup[i].text.strip()
                    link = link_soup[i].a['href']
                    
                    if link == self.website_dc[website]["record_url"]:
                        FLAG = True
                        break
                
                    ls.append(
                        Content(
                            title,
                            link,
                            website
                        )
                    )

                self.website_dc[website]["parmas"]["page"] +=1

            self.db.insert(ls[::-1])
            self.pre_send_txt_ls.append(f"{website} 輸入了 {len(ls)} 筆資料\n")

    def run(self):
        try:
            self.main_process()

        except Exception as e:
            print_exc()
            self.pre_send_txt_ls.append(f'{e}')

        return '\n'.join(self.pre_send_txt_ls)

if __name__ == "__main__":
    c = RSSNews()
    c.run()