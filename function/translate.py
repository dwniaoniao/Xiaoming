import httplib2
from hashlib import md5
import urllib
import random
import json
from function.conversations import vpaSay
from database.DBOperation import connectTODB,getBaiduTranslateAPIMsg

baiduTranslateAPIMsg = getBaiduTranslateAPIMsg(connectTODB())

APP_ID = baiduTranslateAPIMsg[0]
SECRET_KEY = baiduTranslateAPIMsg[1]


def translate(text, srcLanguge, dstLanguage):
    # translate text from source language into destination language use baidu translate api
    httpClien = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = APP_ID+text+str(salt)+SECRET_KEY
    m1 = md5(bytes(sign, 'utf-8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+APP_ID+'&q=' + \
        urllib.parse.quote(text)+'&from='+srcLanguge+'&to=' + \
        dstLanguage + '&salt='+str(salt)+'&sign='+sign

    try:
        httpClient = httplib2.Http()
        response, content = httpClient.request(
            'http://api.fanyi.baidu.com'+myurl)
        result = json.loads(content)
        return result['trans_result'][0]['dst']
    except Exception as e:
        return None


def inEnglish(text):
    # tranlate Chinese txt into English
    speechText = translate(text, 'zh', 'en')
    vpaSay(speechText)

# print(translate("programming",'en','zh'))
# print(translate("中华人民共和国",'zh','en'))
