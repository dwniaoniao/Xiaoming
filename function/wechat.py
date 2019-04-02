import itchat
from function.conversations import vpaSay


def sendMessage(name, message):
    # send a text message to a wechat user named 'name'
    try:
        if itchat.send_msg(toUserName=name, msg=message)['BaseResponse']['Ret'] == 0:
            r = "消息发送成功。"
        else:
            r = "消息发送失败。"
    except Exception as e:
        print(e)
        r = "消息发送失败。"
    finally:
        vpaSay(r)
