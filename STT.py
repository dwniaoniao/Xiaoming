import speech_recognition as sr
from aip import AipSpeech
from function import conversations
import sys
import os
from database.DBOperation import connectTODB, getBaiduSpeechAPIMsg
# import requests
# from ASRT.general_function.file_wav import *

baiduSpeechAPIMsg = getBaiduSpeechAPIMsg(connectTODB())
APP_ID = baiduSpeechAPIMsg[0]  # appid
API_KEY = baiduSpeechAPIMsg[1]  # ak
SECRET_KEY = baiduSpeechAPIMsg[2]   # sk

# close the stderr file descriptor, prevent the error message from frushing the screen.
# os.close(sys.stderr.fileno())


def recordAudio():
    # record audio from the microphone into a wav file
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print("Say something!")
        audio = r.listen(source=source, phrase_time_limit=45)

    with open("audio/recording.wav", "wb") as f:
        f.write(audio.get_wav_data(convert_rate=16000))


def recognizeSpeech():
    # recognize speech using baidu speech API
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    recordAudio()
    result = client.asr(get_file_content('audio/recording.wav'),
                        'wav', 16000, {'dev_pid': 1537, })
    if result['err_msg'] == "success.":
        return result['result'][0]
    else:
        conversations.undefined()
        return None


def get_file_content(filePath):
    # read file
    with open(filePath, 'rb') as fp:
        return fp.read()


def stt(debugMode=False):
    if debugMode == True:
        print("Say something!")
        return input()
    else:
        return recognizeSpeech()

# def recognizeSpeech2():
#     # recognize speech using ASRT speech recognition server
#     url = 'http://127.0.0.1:20000/'
#     token = 'qwertasd'
#     recordAudio()
#     wavsignal, fs = read_wav_data(
#         'audio/recording.wav')
#     datas = {'token': token, 'fs': fs, 'wavs': wavsignal}
#     r = requests.post(url, datas)
#     r.encoding = 'utf-8'
#     return r.text
