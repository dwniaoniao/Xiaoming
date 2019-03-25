import pywapi
from function.conversations import vpaSay
import signal


def handler(signum, frame):
    raise AssertionError


def weather(cityName, cityCode):
    # get wether from Weather.com, cityCode is the city zip code, 5s timeout
    try:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5)
        w = pywapi.get_weather_from_weather_com(cityCode)
        speechText = cityName+"当前天气情况：" + \
            w['current_conditions']['text']+"，气温：" + \
            w['current_conditions']['temperature']+"摄氏度，体感温度：" + \
            w['current_conditions']['feels_like']+"摄氏度，湿度："+w['current_conditions']['humidity']+"%，能见度：" + \
            w['current_conditions']['visibility']+"公里，风力：" + \
            w['current_conditions']['wind']['speed']+"公里每小时。"
        signal.alarm(0)
    except AssertionError:
        speechText = "获取天气失败。"
    finally:
        vpaSay(speechText)
