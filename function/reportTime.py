from datetime import datetime, timedelta
import time
import tkinter as tk


def what_is_time():
    s = "现在是"+datetime.strftime(datetime.now(), '%Y年%m月%d日%H时%M分')
    return s


def countdown(h=0, m=0, s=0):
    countdownWindow = tk.Tk()
    timeLabel = tk.Label(countdownWindow, font=('Times', 100))
    timeLabel.pack(expan='yes', fill='both')
    t = datetime(1900, 1, 1, 0, 0, 0)+timedelta(hours=h, minutes=m, seconds=s)
    timeString = t.strftime("%H:%M:%S")
    timeLabel.configure(text=timeString)
    timeLabel.update()
    aSecond = timedelta(seconds=1)
    while t.hour != 0 or t.minute != 0 or t.second != 0:
        time.sleep(1)
        t = t-aSecond
        timeString = t.strftime("%H:%M:%S")
        timeLabel.configure(text=timeString)
        timeLabel.update()
    countdownWindow.destroy()
