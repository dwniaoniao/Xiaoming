from database.DBOperation import connectTODB
from function.conversations import vpaSay


def createContact(userID):
    connection = connectTODB()
    name = input("名称： ")
    phone = input("电话： ")
    email = input("邮件地址： ")
    wechatNickName = input("微信昵称： ")
    try:
        cursor = connection.cursor()
        cursor.execute("insert into contacts value (default,%s,%s,%s,%s,%s)",
                       (name, phone, email, wechatNickName, str(userID)))
    except Exception as e:
        r = "联系人创建失败。"
        print(e)
    else:
        connection.commit()
        r = "联系人创建成功。"
    finally:
        connection.close()
        vpaSay(r)


def getContact(userID):
    connection = connectTODB()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "select name,phone,email,wechatNickName from contacts where id = "+str(userID))
        r = []
        for x in cursor:
            r.append(x)
    except Exception as e:
        speechText = "获取联系人失败。"
        r = None
    else:
        speechText = "获取联系人成功。"
    finally:
        connection.close()
        vpaSay(speechText)
        return r


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
        vpaSay(r)
