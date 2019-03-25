from function import conversations,reportTime
import jieba


def brain(name, speechText):
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
    else:
        conversations.undefined()


def cutText(textToCut):
    # cut a Chinese string into tokens
    return set(','.join(jieba.cut(textToCut)).split(','))

# brain('fuck',"现在时间。")