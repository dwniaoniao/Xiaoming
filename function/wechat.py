import itchat
from function.conversations import vpaSay
from database.DBOperation import connectTODB


def sendMessage(userID, name, message):
    # send a text message to a wechat user named 'name'
    connection = connectTODB()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "select wechatNickName from contacts where id = %s and name =%s", (str(userID), name))
        for x in cursor:
            wechatUserName = itchat.search_friends(x[0])[0].userName
        if itchat.send_msg(toUserName=wechatUserName, msg=message)['BaseResponse']['Ret'] == 0:
            r = "消息发送成功。"
        else:
            r = "消息发送失败。"
    except Exception as e:
        print(e)
        r = "消息发送失败。"
    finally:
        vpaSay(r)
        connection.close()
