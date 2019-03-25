from STT import recognizeSpeech
from TTS import baiduTTS
from logicEngine import brain
from function.conversations import vpaSay

name = "佳炜"
city = "广州"


def main():
    speechText = recognizeSpeech()
    if speechText:
        print("我："+speechText)
        brain(name, speechText)


def welcome():
    vpaSay("你好,"+name + ",我可以为你做些什么?")


welcome()

while True:
    main()
