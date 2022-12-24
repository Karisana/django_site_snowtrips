import bs4
from django.test import TestCase
from bs4 import BeautifulSoup
import requests
import cfscrape


# def get_text(url):
#     rs = requests.get(url)
#     root = BeautifulSoup(rs.content, 'html.parser')
#     return root.text.split('\n')


# url = 'https://vk.com/zalesom.trip?w=wall-49741741_3728'
# text = get_text(url)
#
# values = ['', ' ', ]
#
# new_text = [value for value in text if value not in values]
#
#
# max_string = max(new_text, key=len)
# print(max_string)



from lxml import html

# url = 'https://adzhigardak.ru/novosti'
#
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# page = requests.get(url, headers=headers)
# # print(page.content)
# print(page.status_code)
#
# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.title)
# print(soup.title.name)
# print(soup.title.parent.name)
#
# test = soup.find('div', class_ = 't-feed__col-grid__post-wrapper')
# print(test)
#


