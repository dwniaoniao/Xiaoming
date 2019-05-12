import httplib2
from hashlib import md5
import urllib
import random
import json
from database.DBOperation import connectTODB, getBaiduTranslateAPIMsg
import tkinter as tk
import tkinter.messagebox

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
    return speechText


def freeTranslate():
    translateWindow = tk.Tk()
    settingFrame = tk.Frame(translateWindow,relief='raised')
    settingFrame.pack(side='top',fill='x')
    tk.Label(settingFrame,text='From').pack(side='left')
    fromEntry = tk.Entry(settingFrame)
    fromEntry.insert('end','auto')
    fromEntry.pack(side='left')
    tk.Label(settingFrame,text='To').pack(side='left')
    toEntry = tk.Entry(settingFrame)
    toEntry.insert('end','zh')
    toEntry.pack(side='left')

    srcLangugeText = tk.Text(translateWindow)
    srcLangugeText.pack(expand='yes',fill='both')
    dstLanguageText = tk.Text(translateWindow)
    dstLanguageText.pack(expand='yes',fill='both')

    def translateButtonCommand():
        try:
            text = srcLangugeText.get(1.0,'end')
            textList = text.splitlines()
            srcLanguge = fromEntry.get()
            dstLanguage = toEntry.get()
            dstLanguageText.delete(1.0,'end')
            for i in textList:
                if i.strip():
                    dstLanguageText.insert('end',translate(i,srcLanguge,dstLanguage)+'\n')
                    dstLanguageText.update()
        except Exception as e:
            tkinter.messagebox.showerror(title='Error',message=e)
    
    def closeButtonCommand():
        translateWindow.destroy()

    tk.Button(settingFrame,text='Close',command=closeButtonCommand).pack(side='right')
    tk.Button(settingFrame,text='Translate', command=translateButtonCommand).pack(side='right')
    translateWindow.mainloop()
