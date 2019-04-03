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
        cursor.execute("insert into contacts value (default,%s,%s,%s,%s,%s)",(name,phone,email,wechatNickName,str(userID)))
    except Exception as e:
        r = "联系人创建失败。"        
        print(e)
    else:
        connection.commit()
        r = "联系人创建成功。"
    finally:
        connection.close()
        vpaSay(r)
