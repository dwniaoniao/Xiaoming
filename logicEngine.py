from function import conversations, reportTime, weather, translate
import jieba


def brain(name, speechText, cityName, cityCode):
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
    else:
        conversations.undefined()


def cutText(textToCut):
    # cut a Chinese string into tokens
    return set(','.join(jieba.cut(textToCut)).split(','))


# brain('test',"能不能告诉我你是谁","","")
# brain('test',"现在时间","","")
# brain('test', "天气如何", "广州", "CHXX0037")
# brain('test', "人工智能用英语怎么说？", '', '')
