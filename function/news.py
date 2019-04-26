from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
from function.conversations import vpaSay


def getNews():
    html = urlopen("https://www.thepaper.cn/")
    bs = BeautifulSoup(html, "html.parser")
    news = bs.find_all('div', {'class': 'news_li'})
    for i in random.sample(news, 5):
        if i.h2 and i.p:
            vpaSay(i.h2.get_text().strip() + "：" + i.p.get_text().strip())
