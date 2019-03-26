from TTS import baiduTTS
import random


def who_are_you():
    message = ["我叫小明，我是你的个人助理。", "我就是我，小明", "我叫小明"]
    s = random.choice(message)
    vpaSay(s)


def who_am_i(name):
    s = "你是"+name
    vpaSay(s)


def how_are_u():
    s = "我很好，谢谢。"
    vpaSay(s)


def undefined():
    message = ["我不知道你在说什么。", "我无法理解你所说的。", "你这个问题太深奥了，超出我能理解的范围。"]
    s = random.choice(message)
    vpaSay(s)


def vpaSay(speech):
    print(speech)
    baiduTTS(speech)
