#!/usr/bin/python3
from STT import stt
from logicEngine import brain
from function.conversations import vpaSay
import sys
import itchat
from userManagement import userManagement

while True:
    r = userManagement.userLogin()
    if r:
        userID = r[0]
        name = r[1]
        cityName = r[2]
        emailt = r[3]
        cityCode = ''
        break
    print("用户名或密码错误。")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debugMode = True
    else:
        debugMode = False
    speechText = stt(debugMode)
    if speechText:
        print("我："+speechText)
        brain(userID, name, speechText, cityName, cityCode)


def welcome():
    vpaSay("你好,"+name + ",我可以为你做些什么?")

# try:
#     itchat.login()
# except Exception as e:
#     print("无法登陆微信。")
#     print(e)
# finally:
#     pass


welcome()

while True:
    main()
