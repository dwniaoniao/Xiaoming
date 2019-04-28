from TTS import tts
import random
from database.DBOperation import connectTODB
import random

def who_are_you():
    message = ["我叫小明，我是你的个人助理。", "我就是我，小明。", "我叫小明。"]
    s = random.choice(message)
    vpaSay(s)


def who_am_i(name):
    s = "你是"+name
    vpaSay(s)


def how_are_u():
    s = "我很好，谢谢。"
    vpaSay(s)

def say_a_word():
    connection = connectTODB()
    i = random.randint(1,6908)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("select word from words where id = "+str(i))
            for x in cursor:
                vpaSay(x[0])
        except Exception as e:
            print(e)
        finally:
            connection.close()

def recite_a_poetry():
    connection = connectTODB()
    i = random.randint(1,311829)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("select content, title, author from poetry where id = "+str(i))
            for x in cursor:
                vpaSay(x[0]+"《"+x[1]+"》"+"————"+x[2])
        except Exception as e:
            print(e)
        finally:
            connection.close()

def undefined():
    message = ["我不知道你在说什么。", "我无法理解你所说的。", "你这个问题太深奥了，超出我能理解的范围。"]
    s = random.choice(message)
    vpaSay(s)


def vpaSay(speech):
    print("小明：" + speech)
    tts(speech, debugMode=False)

