from datetime import datetime


def what_is_time():
    s = "现在是"+datetime.strftime(datetime.now(), '%Y年%m月%d日%H时%M分')
    return s
