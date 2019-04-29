from function import conversations, note, reportTime, translate, weather, wechat, contact, baike, news
import jieba
import jieba.posseg as pseg
import re
import itchat


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
