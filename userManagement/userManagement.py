from database.DBOperation import connectTODB
from hashlib import sha256
import getpass


def createUser(name, password, city, email):
    connection = connectTODB()
    encrypedPassword = sha256(bytes(password, 'utf-8')).hexdigest()
    try:
        cursor = connection.cursor()
        cursor.execute("insert into users value (default,%s,%s,%s,%s)",
                       (name, encrypedPassword, city, email))
    except Exception as e:
        print(e)
        result = "fail"
    else:
        connection.commit()
        result = "success"
    finally:
        connection.close()
        return result


def verifyUser(name, password):
    connection = connectTODB()
    encrypedPassword = sha256(bytes(password, 'utf-8')).hexdigest()
    result = {'result': 'rejected'}
    try:
        cursor = connection.cursor()
        cursor.execute(
            "select * from users where name = %s and password = %s", (name, encrypedPassword))
        for x in cursor:
            if x:
                result['result'] = 'accepted'
                result['userID'] = x[0]
                result['name'] = name
                result['city'] = x[3]
                result['email'] = x[4]
    except Exception as e:
        print(e)
    finally:
        connection.close()
        return result


def userLogin(name, password):
    result = verifyUser(name, password)
    if result['result'] == 'accepted':
        return result['userID'], result['name'], result['city'], result['email']
    else:
        return None
