from aip import AipSpeech
from os import system
from pydub import AudioSegment
import pyaudio
import wave
from database.DBOperation import connectTODB, getBaiduSpeechAPIMsg

baiduSpeechAPIMsg = getBaiduSpeechAPIMsg(connectTODB())
APP_ID = baiduSpeechAPIMsg[0]  # appid
API_KEY = baiduSpeechAPIMsg[1]  # ak
SECRET_KEY = baiduSpeechAPIMsg[2]   # sk


def baiduTTS(strToConvert):
    # convert text to speech use baidu TTS api, write into a mp3 file
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(strToConvert, 'zh', 1, {'per': 1, })
    if not isinstance(result, dict):
        with open('audio/audio.mp3', 'wb') as f:
            f.write(result)
        convertMP3toWAV("audio/audio.mp3", "audio/audio.wav")
        playWAV("audio/audio.wav")
    return result


def convertMP3toWAV(mp3FilePath, wavFilePath):
    # convert mp3 file to wav file
    audio = AudioSegment.from_mp3(mp3FilePath)
    audio.export(wavFilePath, format="wav")


def playWAV(wavFilePath):
    # play wav audio file
    CHUNK = 1024

    wf = wave.open(wavFilePath, 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()


def espeakTTS(strToConvert):
    # conver text to speech use espeak
    system("espeak -v zh "+strToConvert)


def tts(strToConvert, debugMode=False):
    if debugMode == False:
        return baiduTTS(strToConvert)
    else:
        return espeakTTS(strToConvert)
