from database.DBOperation import connectTODB
import tkinter as tk
import tkinter.messagebox


def createContact(userID):
    createContactWindow = tk.Tk()
    tk.Label(createContactWindow, text='名称').grid(row=0, sticky='w')
    tk.Label(createContactWindow, text='电话').grid(row=1, sticky='w')
    tk.Label(createContactWindow, text='邮箱地址').grid(row=2, sticky='w')
    tk.Label(createContactWindow, text='微信昵称').grid(
        row=3, sticky='w')
    nameEntry = tk.Entry(createContactWindow)
    phoneEntry = tk.Entry(createContactWindow)
    emailEntry = tk.Entry(createContactWindow)
    wechatNickNameEntry = tk.Entry(createContactWindow)
    nameEntry.grid(row=0, column=1, sticky='e')
    phoneEntry.grid(row=1, column=1, sticky='e')
    emailEntry.grid(row=2, column=1, sticky='e')
    wechatNickNameEntry.grid(row=3, column=1, sticky='e')

    def createContactButtonCommand():
        name = nameEntry.get()
        phone = phoneEntry.get()
        email = emailEntry.get()
        wechatNickName = wechatNickNameEntry.get()
        connection = connectTODB()
        try:
            cursor = connection.cursor()
            cursor.execute("insert into contacts value (default,%s,%s,%s,%s,%s)",
                           (name, phone, email, wechatNickName, str(userID)))
        except Exception as e:
            r = "联系人创建失败。"
            tkinter.messagebox.showerror(title='Error', message=r)
            print(e)
        else:
            connection.commit()
            r = "联系人创建成功。"
            tkinter.messagebox.showinfo(title='Success', message=r)
            createContactWindow.destroy()
        finally:
            connection.close()
    tk.Button(createContactWindow, text='创建',
              command=createContactButtonCommand).grid(row=4, column=1, sticky='e')


def getContact(userID):
    getContactWindow = tk.Tk()
    contactText = tk.Text(getContactWindow)
    contactText.pack(expand='yes', fill='both')
    scrollBar = tk.Scrollbar(contactText)
    contactText.configure(yscrollcommand=scrollBar.set)
    scrollBar.pack(side='right', fill='y')

    def closeButtonCommand():
        getContactWindow.destroy()

    connection = connectTODB()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "select name,phone,email,wechatNickName from contacts where id = "+str(userID))
        r = ''
        for x in cursor:
            r += '姓名：'+'\t'+x['name']+'\n' + \
                '电话：'+'\t'+x['phone']+'\n' +\
                '邮箱地址：'+'\t'+x['email']+'\n' +\
                '微信昵称：'+'\t'+x['wechatNickName']+'\n'
    except Exception as e:
        speechText = "获取联系人失败。"
        r = None
        tkinter.messagebox.showerror(title='Error', message=speechText)
        getContactWindow.destroy()
    else:
        speechText = "获取联系人成功。"
        contactText.insert(1.0, r)
        contactText.update()

    finally:
        connection.close()
    tk.Button(getContactWindow, text='ok', command=closeButtonCommand).pack()
    return r, speechText


def deleteContact(userID, name):
    # delete a contact, the contact name is 'name'
    connection = connectTODB()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "delete from contacts where name = %s and id = %s", (name, userID))
    except Exception as e:
        r = "删除联系人失败。"
        print(e)
    else:
        connection.commit()
        r = "删除联系人成功。"
    finally:
        connection.close()
        return r
