import pywapi
from function.translate import translate
import signal
import httplib2
import urllib
import json
from database.DBOperation import connectTODB, getHeWeatherAPIMsg
import pysnooper


def handler(signum, frame):
    raise AssertionError


def weather(cityName, cityCode):
    # get wether from Weather.com, cityCode is the city zip code, 5s timeout
    try:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5)
        w = pywapi.get_weather_from_weather_com(cityCode)
        speechText = cityName+"当前天气情况：" + \
            translate(w['current_conditions']['text'], 'en', 'zh') + "，气温：" + \
            w['current_conditions']['temperature']+"摄氏度，体感温度：" + \
            w['current_conditions']['feels_like']+"摄氏度，湿度："+w['current_conditions']['humidity']+"%，能见度：" + \
            w['current_conditions']['visibility']+"公里，风力：" + \
            w['current_conditions']['wind']['speed']+"公里每小时。"
        signal.alarm(0)
    except AssertionError:
        speechText = "获取天气失败。"
    finally:
        return speechText


@pysnooper.snoop()
def heWeatherNow(city):
    # get current weather from heweather.com
    key = getHeWeatherAPIMsg(connectTODB())[0]
    url = "https://free-api.heweather.net/s6/weather?"
    myurl = url+"&location="+urllib.parse.quote(city)+"&key="+key
    try:
        httpClient = httplib2.Http()
        response, content = httpClient.request(myurl)
        result = json.loads(content)
        now = result['HeWeather6'][0]['now']
        lifestyle = result['HeWeather6'][0]['lifestyle'][0]['txt']
        forecast = result['HeWeather6'][0]['daily_forecast'][0]
        forecast2 = result['HeWeather6'][0]['daily_forecast'][1]
        forecast3 = result['HeWeather6'][0]['daily_forecast'][2]
        speechText1 = city+"当前天气情况：" + \
            now['cond_txt']+"，气温："+now['tmp']+"摄氏度，体感温度："+now['fl']+"摄氏度，湿度："+now['hum'] + \
            "%，能见度："+now['vis']+"公里，"+now['wind_dir'] + \
            "，风力："+now['wind_spd']+"公里每小时。"+lifestyle
        speechText2 = "今天降水概率：" + \
            forecast['pop']+"%，白天"+forecast['cond_txt_d'] + \
            "，夜间"+forecast['cond_txt_n'] + "；"
        speechText3 = "明天降水概率：" + \
            forecast2['pop']+"%，白天"+forecast2['cond_txt_d'] + \
            "，夜间"+forecast2['cond_txt_n'] + "；"
        speechText4 = "后天降水概率：" + \
            forecast3['pop']+"%，白天"+forecast3['cond_txt_d'] + \
            "，夜间"+forecast3['cond_txt_n'] + "。"
        speechText = speechText1 + "未来3天天气预报：" + \
            speechText2 + speechText3 + speechText4
    except:
        speechText = "获取天气失败。"
    finally:
        return speechText
