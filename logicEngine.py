from function import conversations, note, reportTime, translate, weather, wechat, contact, baike, news
import jieba
import jieba.posseg as pseg
import re
import itchat
import _thread


def brain(userID, name, speechText, cityName, cityCode):
    def cutText(textToCut):
        # cut a Chinese string into tokens
        return set(','.join(jieba.cut(textToCut)).split(','))

    def checkMessage(textToCheck):
        # check if the speech text match the keyword
        if cutText(textToCheck).issubset(cutText(speechText)):
            return True
        else:
            return False

    def chineseToArabic(s):
        # convert string s which contain some numbers write in Chinese to Arabic
        # number like "一" is "1"
        # number like "两万" is "20000"
        d = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6,
             "七": 7, "八": 8, "九": 9, "十": 10, "百": 100, "千": 1000, "万": 10000}
        u = ['十', '百', '千', '万']
        d2 = {}

        def getNumber(s):
            l = []
            numberString = ''
            for c in s:
                if c in d.keys():
                    numberString += c
                elif numberString:
                    l.append(numberString)
                    numberString = ''
            if numberString:
                l.append(numberString)
            return l

        def convertToArabic(s):
            if len(s) == 1:
                return d.get(s)
            elif len(s) == 2 and s[1] in u:
                return d.get(s[0])*d.get(s[1])
            else:
                pass
        for i in getNumber(s):
            d2[i] = convertToArabic(i)
        for k in d2.keys():
            s = s.replace(k, str(d2.get(k)))

        return s

    if checkMessage("你是谁"):
        return conversations.who_are_you()
    elif checkMessage("我是谁"):
        return conversations.who_am_i(name)
    elif checkMessage("你好吗"):
        return conversations.how_are_u()
    elif checkMessage("背诗") or checkMessage("来首诗"):
        return conversations.recite_a_poetry()
    elif checkMessage("时间") or checkMessage("几点"):
        return reportTime.what_is_time()
    elif checkMessage("倒计时"):
        speechText = chineseToArabic(speechText)
        match = re.search('[0-9]+\w{0,1}时', speechText)
        if match:
            h = int(re.search('[0-9]*', match.group()).group())
        else:
            h = 0
        match = re.search('[0-9]+分', speechText)
        if match:
            m = int(re.search('[0-9]*', match.group()).group())
        else:
            m = 0
        match = re.search('[0-9]+秒', speechText)
        if match:
            s = int(re.search('[0-9]*', match.group()).group())
        else:
            s = 0
        _thread.start_new_thread(reportTime.countdown, (), {
                                 'h': h, 'm': m, 's': s})
    elif checkMessage("天气"):
        return weather.heWeatherNow(cityName)
    elif "用英语怎么说" in speechText:
        speechText = speechText.replace('用英语怎么说', '')
        return translate.inEnglish(speechText)
    elif checkMessage("笔记"):
        if checkMessage("创建") or checkMessage("新建"):
            note.createNote(userID)
            return ''
        elif checkMessage("获取笔记") or checkMessage("查看笔记"):
            note.getNote(userID)
            return ''
        elif checkMessage("导出笔记"):
            return note.exportNote(userID)
        elif re.search("删除名为\w+的笔记", speechText):
            title = re.search(
                "删除名为\w+的笔记", speechText).group().replace("删除名为", "").replace("的笔记", "")
            return note.deleteNote(userID, title)
        else:
            return conversations.undefined()
    elif checkMessage("联系人"):
        if checkMessage("创建") or checkMessage("新建"):
            contact.createContact(userID)
            return ''
        elif checkMessage("获取") or checkMessage("查看"):
            contact.getContact(userID)
            return ''

        elif re.search("删除名为\w+的联系人", speechText):
            name = re.search(
                "删除名为\w+的联系人", speechText).group().replace("删除名为", "").replace("的联系人", "")
            return contact.deleteContact(userID, name)
        else:
            return conversations.undefined()
    elif re.search("微信(告诉|给|问){0,1}\w+说\w+", speechText):
        s = re.search("微信(告诉|给|问){0,1}\w+说\w+", speechText).group()
        s = re.sub("微信(告诉|给|问){0,1}", "", s)
        contactName = re.search("^\w+说", s).group().replace("说", "")
        message = s.replace(re.search("^\w+说", s).group(), "")
        return wechat.sendMessage(userID, contactName, message)

    elif checkMessage("解释"):
        words = pseg.cut(speechText)
        for word in words:
            if word.word != "解释" and word.flag != "x":
                return baike.baike(word.word)

    elif checkMessage("新闻"):
        l = news.getNews()
        s = ''
        for i in l:
            s += i + '\n'
        return s

    else:
        return conversations.undefined()
