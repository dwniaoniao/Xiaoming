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
tk.Label(loginWindow, text='name').grid(row=0, sticky='w')
tk.Label(loginWindow, text='password').grid(row=1, sticky='w')
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

        def aboutButtonCommand():
            tkinter.messagebox.showinfo("About", "about\nabout")

        def exitButtonCommand():
            exit()

        def vpaSay(speechText, debugMode):
            if debugMode == False:
                tts(speechText)
            return speechText

        def welcome():
            f = random.choice((say_a_word, recite_a_poetry))
            s = f()
            s += "\n你好,"+name + ",我可以为你做些什么?\n"
            return s

        aboutButton = tk.Button(menuBar, text='About',
                                command=aboutButtonCommand)
        exitButton = tk.Button(menuBar, text='Exit', command=exitButtonCommand)
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
            menuBar, text='Clear screen', command=clearScreenButtonCommand)
        clearScreenButton.pack(side='left')
        s = welcome()
        dialogueText.insert('end', "小明："+s)
        dialogueText.update()
        vpaSay(s, debugMode)

        if debugMode == True:
            def sendButtonCommand():
                speechText = inputText.get(1.0, 'end')
                if speechText.strip():
                    inputText.delete(1.0, 'end')
                    dialogueText.insert('end', "我："+speechText)
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
                root, text='Press Enter and say something!', bg='green')
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


tk.Button(loginWindow, text='login', command=login).grid(
    row=2, column=1, sticky='e')
root.mainloop()
