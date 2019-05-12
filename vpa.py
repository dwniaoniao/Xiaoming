#!/usr/bin/python3
from STT import stt
from TTS import tts
from logicEngine import brain
from function.conversations import say_a_word, recite_a_poetry
import sys
from userManagement import userManagement
import random
import tkinter as tk
import tkinter.messagebox

if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    debugMode = True
else:
    debugMode = False

root = tk.Tk()
loginWindow = tk.Tk()
tk.Label(loginWindow, text='用户名').grid(row=0, sticky='w')
tk.Label(loginWindow, text='密码').grid(row=1, sticky='w')
nameEntry = tk.Entry(loginWindow)
nameEntry.grid(row=0, column=1, sticky='e')
passwordEntry = tk.Entry(loginWindow, show='*')
passwordEntry.grid(row=1, column=1, sticky='e')


def login():
    name = nameEntry.get()
    password = passwordEntry.get()
    r = userManagement.userLogin(name, password)
    if r:
        userID = r[0]
        cityName = r[2]
        email = r[3]
        cityCode = ''
        loginWindow.destroy()
        menuBar = tk.Frame(root, relief='raised', bd=2)
        menuBar.pack(fill='x')

        aboutMsg = """
具备背诵古诗、天气查询、文本翻译、百科知识、新闻查询、联系人管理、笔记、代发微信消息等功能。

你可以这样说：
来首李白的诗。
广州的天气？
我必须努力学习用英语怎么说？
解释人工智能。
有什么新闻吗？
查看联系人。
查看所有笔记。
现在几点？
开始一分钟倒计时。
发微信告诉小红说今天晚上来吃饭。
        """
        def aboutButtonCommand():
            tkinter.messagebox.showinfo("About",aboutMsg)

        def exitButtonCommand():
            exit()

        def vpaSay(speechText, debugMode):
            if debugMode == False:
                tts(speechText)
            return speechText

        def welcome():
            # f = random.choice((say_a_word, recite_a_poetry))
            # s = f()
            s = say_a_word()
            s += "\n你好,"+name + ",我可以为你做些什么?\n"
            return s

        aboutButton = tk.Button(menuBar, text='帮助',
                                command=aboutButtonCommand)
        exitButton = tk.Button(menuBar, text='结束', command=exitButtonCommand)
        aboutButton.pack(side='left')
        exitButton.pack(side='left')

        dialogueText = tk.Text(root)
        dialogueText.pack(expand='yes', fill='both')
        scrollBar = tk.Scrollbar(dialogueText)
        dialogueText.configure(yscrollcommand=scrollBar.set)
        scrollBar.config(command=dialogueText.yview)
        scrollBar.pack(side='right', fill='y')

        def clearScreenButtonCommand():
            dialogueText.delete(1.0, 'end')
            dialogueText.update()
        clearScreenButton = tk.Button(
            menuBar, text='清空屏幕', command=clearScreenButtonCommand)
        clearScreenButton.pack(side='left')
        s = welcome()
        dialogueText.insert('end', "小明："+s)
        dialogueText.update()
        vpaSay(s, debugMode)

        if debugMode == True:
            def sendButtonCommand():
                speechText = inputText.get(1.0, 'end').strip()
                if speechText:
                    inputText.delete(1.0, 'end')
                    dialogueText.insert('end', "我："+speechText+'\n')
                    dialogueText.update()
                    speechText = brain(
                        userID, name, speechText, cityName, cityCode)
                    if speechText:
                        dialogueText.insert('end', "小明："+speechText+'\n')
                        # vpaSay(speechText,debugMode)

            def enterCommand(event):
                sendButtonCommand()
            inputText = tk.Text(root, height=5)
            inputText.pack(side='left', expand='yes', fill='both')
            sendButton = tk.Button(
                root, text='Send', command=sendButtonCommand)
            sendButton.pack(side='right', fill='both')
            sendButton.bind_all('<Return>', enterCommand)
        else:
            saySthLabel = tk.Label(
                root, text='按Enter键开始说话', bg='green')
            saySthLabel.pack()

            def speak():
                saySthLabel.config(bg='red')
                saySthLabel.update()
                speechText = stt(debugMode)
                if speechText:
                    dialogueText.insert('end', "我："+speechText+'\n')
                    dialogueText.update()
                    speechText = brain(
                        userID, name, speechText, cityName, cityCode)
                    if speechText:
                        dialogueText.insert('end', "小明："+speechText+'\n')
                        dialogueText.update()
                        vpaSay(speechText, debugMode)
                saySthLabel.config(bg='green')
                saySthLabel.update()

            def enterCommand(event):
                speak()
            root.bind_all('<Return>', enterCommand)
    else:
        tkinter.messagebox.showerror('error', '用户名或密码错误。')


def signUp():
    signUpWindow = tk.Tk()
    tk.Label(signUpWindow, text='用户名').grid(row=0, sticky='w')
    tk.Label(signUpWindow, text='密码').grid(row=1, sticky='w')
    tk.Label(signUpWindow, text='确认密码').grid(row=2, sticky='w')
    tk.Label(signUpWindow, text='所在城市').grid(row=3, sticky='w')
    tk.Label(signUpWindow, text='邮箱').grid(row=4, sticky='w')
    nameEntry = tk.Entry(signUpWindow)
    passwordEntry = tk.Entry(signUpWindow, show='*')
    confirmPasswordEntry = tk.Entry(signUpWindow, show='*')
    cityEntry = tk.Entry(signUpWindow)
    emailEntry = tk.Entry(signUpWindow)
    nameEntry.grid(row=0, column=1, sticky='e')
    passwordEntry.grid(row=1, column=1, sticky='e')
    confirmPasswordEntry.grid(row=2, column=1, sticky='e')
    cityEntry.grid(row=3, column=1, sticky='e')
    emailEntry.grid(row=4, column=1, sticky='e')

    def signUpButtonCommand():
        if passwordEntry.get() != confirmPasswordEntry.get():
            tk.messagebox.showerror(title='Error', message='两次输入的密码不匹配，请重新输入。')
        else:
            name = nameEntry.get()
            password = passwordEntry.get()
            city = cityEntry.get()
            email = emailEntry.get()
            r = userManagement.createUser(name, password, city, email)
            if r == 'success':
                tk.messagebox.showinfo(title='Success', message='创建用户成功。')
                signUpWindow.destroy()
            else:
                tk.messagebox.showerror(title='Error', message='创建用户失败。')

    tk.Button(signUpWindow, text='确认', command=signUpButtonCommand).grid(
        row=5, column=1, sticky='e')
    pass


tk.Button(loginWindow, text='新的用户', command=signUp).grid(
    row=2, column=1, sticky='w')
tk.Button(loginWindow, text='确认', command=login).grid(
    row=2, column=1, sticky='e')
root.mainloop()
