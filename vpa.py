#!/usr/bin/python3
from STT import stt
from logicEngine import brain
from function.conversations import vpaSay, say_a_word, recite_a_poetry
import sys
from userManagement import userManagement
import random

def checkUser(debugMode):
    if debugMode == False:
        while True:
            r = userManagement.userLogin()
            if r:
                return (r[0], r[1], r[2], r[3], '')
            print("用户名或密码错误。")
    else:
        return (7, "佳炜", "广州", "", "")


def main(debugMode):
    speechText = stt(debugMode)
    if speechText:
        print("我："+speechText)
        brain(userID, name, speechText, cityName, cityCode)


def welcome():
    f = random.choice((say_a_word, recite_a_poetry))
    f()
    vpaSay("你好,"+name + ",我可以为你做些什么?")


if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    debugMode = True
else:
    debugMode = False

t = checkUser(debugMode)
userID = t[0]
name = t[1]
cityName = t[2]
email = t[3]
cityCode = t[4]

welcome()

while True:
    main(debugMode)
