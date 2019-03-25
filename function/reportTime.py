from datetime import datetime
from function.conversations import vpaSay
# from TTS import baiduTTS
def what_is_time():
    s = "现在是"+datetime.strftime(datetime.now(), '%Y年%m月%d日%H时%M分')
    vpaSay(s)
    # print(s)
    # baiduTTS(s)