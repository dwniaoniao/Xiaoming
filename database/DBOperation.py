import mysql.connector as mariadb


def connectTODB():
    # connect to the database, if success, return the connection, else, return None
    user = 'root'
    password = 'password'
    database = 'XIAOMING'
    try:
        connection = mariadb.connect(
            user=user, password=password, database=database)
    except Exception as e:
        print(e)
        return None
    else:
        return connection


def getBaiduSpeechAPIMsg(connection):
    # get baidu speech API message(appid, apikey,secretkey)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("select * from baiduSpeech")
            for appid, apikey, secretkey in cursor:
                return appid, apikey, secretkey
        except Exception as e:
            print(e)
        finally:
            connection.close()


def getBaiduTranslateAPIMsg(connection):
    # get baidu translate API message(appid,secretkey)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("select * from baiduTranslate")
            for appid, secretkey in cursor:
                return appid, secretkey
        except Exception as e:
            print(e)
        finally:
            connection.close()


def getHeWeatherAPIMsg(connection):
    # get heWeather API message(apikey)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("select * from heWeather")
            for apikey in cursor:
                return apikey
        except Exception as e:
            print(e)
        finally:
            connection.close()


# print(getBaiduSpeechAPIMsg(connectTODB()))
# print(getBaiduTranslateAPIMsg(connectTODB()))
