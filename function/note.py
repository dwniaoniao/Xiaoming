from database.DBOperation import connectTODB
from datetime import datetime
from STT import stt
import re
import tkinter as tk
import tkinter.messagebox
import pysnooper


def createNote(userID):
    createNoteWindow = tk.Tk()
    tk.Label(createNoteWindow, text='title').pack()
    titleEntry = tk.Entry(createNoteWindow)
    titleEntry.pack(expand='yes', fill='x')
    tk.Label(createNoteWindow, text='content').pack()
    contentText = tk.Text(createNoteWindow)
    contentText.pack(expand='yes', fill='both')

    def createNoteButtonCommand():
        title = titleEntry.get()
        content = contentText.get(1.0, 'end')
        dateAndTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        connection = connectTODB()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("insert into notes value (default,%s,%s,%s,%s)",
                               (title, content, dateAndTime, userID))
            except Exception as e:
                print(e)
                s = "笔记创建失败。"
                tkinter.messagebox.showerror(title='Error', message=s)
            else:
                connection.commit()
                s = "笔记创建成功。"
                tkinter.messagebox.showinfo(title='Success', message=s)
                createNoteWindow.destroy()
            finally:
                connection.close()
    tk.Button(createNoteWindow, text='Create',
              command=createNoteButtonCommand).pack()


def getNote(userID):
    getNoteWindow = tk.Tk()
    noteText = tk.Text(getNoteWindow)
    noteText.pack(expand='yes', fill='both')
    scrollBar = tk.Scrollbar(noteText)
    noteText.configure(yscrollcommand=scrollBar.set)
    scrollBar.pack(side='right', fill='y')

    def closeButtonCommand():
        getNoteWindow.destroy()

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
            r = None
            speechText = "获取笔记失败。"
            tkinter.messagebox.showerror(title='Error', message=speechText)
            getNoteWindow.destroy()
        else:
            speechText = "获取笔记成功。"
            noteText.insert(1.0, r)
            noteText.update()
        finally:
            connection.close()
    tk.Button(getNoteWindow, text='Ok', command=closeButtonCommand).pack()
    return r


def exportNote(userID):
    notes = getNote(userID)
    if notes:
        with open('notes/notes.txt', 'w') as f:
            f.write(notes)
        return "笔记导出成功。"
    else:
        return "笔记导出失败。"
    pass


@pysnooper.snoop()
def deleteNote(userID, title):
    connection = connectTODB()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "delete from notes where title = %s and id = %s", (title, userID))
    except Exception as e:
        r = "删除笔记失败。"
        print(e)
    else:
        connection.commit()
        r = "删除笔记成功。"
    finally:
        connection.close()
        return r
