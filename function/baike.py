from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup


def baike(word):
    try:
        url = "http://www.baike.com/wiki/" + quote(word)
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
        x = bs.find('div', {'class': 'summary'})
        speechText = x.p.get_text()
    except Exception as e:
        print(e)
        speechText = "未找到与”" + word + "“相关词条"
    finally:
        return speechText
