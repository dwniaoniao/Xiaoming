from function.conversations import vpaSay
from database.DBOperation import connectTODB
from datetime import datetime
from STT import recognizeSpeech
import re


def createNote(title, userID):
    vpaSay("请录入内容：")
    content = ''
    while True:
        paragragh = recognizeSpeech()
        if not re.match("^录入结束\w*", paragragh):
            content += paragragh + '\n'
        else:
            break
    dateAndTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    connection = connectTODB()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("insert into notes value (default,%s,%s,%s,%s)",
                           (title, content, dateAndTime, userID))
        except Exception as e:
            print(e)
            vpaSay("笔记创建失败。")
        else:
            connection.commit()
            vpaSay("笔记创建成功。")
        finally:
            connection.close()

    pass


def getNote(userID):
    connection = connectTODB()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("select * from notes where id = "+str(userID))
            r = ''
            for x in cursor:
                dateAndTime = x[3].strftime("%Y-%m-%d %H:%M:%S")
                r += "标题："+x[1]+'\n'+"创建时间："+dateAndTime+'\n'+"正文："+x[2]+'\n\n'
        except Exception as e:
            print(e)
            speechText = "获取笔记失败。"
            r = None
        else:
            speechText = "获取笔记成功。"
            print(r)
        finally:
            connection.close()
            return(r, speechText)
    pass


def exportNote(userID):
    notes = getNote(userID)[0]
    if notes:
        with open('notes/notes.txt', 'w') as f:
            f.write(notes)
        vpaSay("笔记导出成功。")
    else:
        vpaSay("笔记导出失败。")
    pass
