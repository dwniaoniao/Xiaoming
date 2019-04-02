from function.conversations import vpaSay
from database.DBOperation import connectTODB
from datetime import datetime


def createNote(title, content, user):
    dateAndTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    connection = connectTODB()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("select id from users where name = '"+user+"'")
            for x in cursor:
                userID = x[0]
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


def getNote(user):
    connection = connectTODB()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("select id from users where name = '"+user+"'")
            for x in cursor:
                userID = x[0]
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


def exportNote(user):
    notes = getNote(user)[0]
    if notes:
        with open('notes/notes.txt', 'w') as f:
            f.write(notes)
        vpaSay("笔记导出成功。")
    else:
        vpaSay("笔记导出失败。")
    pass
