#!/usr/bin/python3
from STT import recognizeSpeech
from TTS import baiduTTS
from logicEngine import brain
from function.conversations import vpaSay
import sys
import itchat

name = "佳炜"
cityName = "广州"
cityCode = "CHXX0037"


def main():
    if len(sys.argv) == 1:
        speechText = recognizeSpeech()
        if speechText:
            print("我："+speechText)
            brain(name, speechText, cityName, cityCode)
        itchat.logout()
    else:
        speechText = sys.argv[1]
        print("我："+speechText)
        brain(name, speechText, cityName, cityCode)
        exit()


def welcome():
    vpaSay("你好,"+name + ",我可以为你做些什么?")

try:
    itchat.login()
except Exception as e:
    print("无法登陆微信。")
    print(e) 
finally:
    pass

welcome()

while True:
    main()
