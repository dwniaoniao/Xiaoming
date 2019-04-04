from function import conversations, note, reportTime, translate, weather, wechat, contact
import jieba
import re
import itchat


def brain(userID, name, speechText, cityName, cityCode):
    def checkMessage(textToCheck):
        # check if the speech text match the keyword
        if cutText(textToCheck).issubset(cutText(speechText)):
            return True
        else:
            return False

    if checkMessage("你是谁"):
        conversations.who_are_you()
    elif checkMessage("我是谁"):
        conversations.who_am_i(name)
    elif checkMessage("你好吗"):
        conversations.how_are_u()
    elif checkMessage("现在时间") or checkMessage("现在几点"):
        reportTime.what_is_time()
    elif checkMessage("天气如何") or checkMessage("天气怎样") or checkMessage("当前天气") or checkMessage("现在天气"):
        # weather.weather(cityName, cityCode)
        weather.heWeatherNow(cityName)
    elif "用英语怎么说" in speechText:
        speechText = speechText.replace('用英语怎么说', '')
        translate.inEnglish(speechText)
    elif checkMessage("笔记"):
        if re.search("创建名为\w+的笔记", speechText):
            match = re.search("创建名为\w+的笔记", speechText)
            title = match.group().replace("创建名为", "").replace("的笔记", "")
            note.createNote(title, userID)
        elif checkMessage("获取笔记") or checkMessage("查看笔记"):
            conversations.vpaSay(note.getNote(userID)[1])
        elif checkMessage("导出笔记"):
            note.exportNote(userID)
        elif re.search("删除名为\w+的笔记", speechText):
            title = re.search(
                "删除名为\w+的笔记", speechText).group().replace("删除名为", "").replace("的笔记", "")
            note.deleteNote(userID, title)
        else:
            conversations.undefined()
    elif checkMessage("联系人"):
        if checkMessage("创建") or checkMessage("新建"):
            contact.createContact(userID)
        elif checkMessage("获取") or checkMessage("查看"):
            print(contact.getContact(userID))
        elif re.search("删除名为\w+的联系人", speechText):
            name = re.search(
                "删除名为\w+的联系人", speechText).group().replace("删除名为", "").replace("的联系人", "")
            contact.deleteContact(userID, name)
        else:
            conversations.undefined()
    elif re.search("微信(告诉|给|问){0,1}\w+说\w+", speechText):
        s = re.search("微信(告诉|给|问){0,1}\w+说\w+", speechText).group()
        s = re.sub("微信(告诉|给|问){0,1}", "", s)
        contactName = re.search("^\w+说", s).group().replace("说", "")
        message = s.replace(re.search("^\w+说", s).group(), "")
        wechat.sendMessage(userID, contactName, message)
    else:
        conversations.undefined()


def cutText(textToCut):
    # cut a Chinese string into tokens
    return set(','.join(jieba.cut(textToCut)).split(','))
