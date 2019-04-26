from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
from function.conversations import vpaSay


def baike(word):
    try:
        url = "http://www.baike.com/wiki/" + quote(word)
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
        x = bs.find('div', {'class': 'summary'})
        vpaSay(x.p.get_text())
    except Exception as e:
        print(e)
        vpaSay("未找到与”" + word + "“相关词条")
