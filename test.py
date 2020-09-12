from bs4 import BeautifulSoup
import requests
import re
import csv
import json
import time
import fileinput
# import urllib2

url = "https://www.91toy.com.tw/search/?category=new"
# data = urllib2.urlopen(url).read()
res = requests.get(url)
soup = BeautifulSoup(res)

print(soup)