import pymysql

def getCNX():
    cnx = pymysql.connect(user='vcad',
                          password='vcad123',
                          host='localhost',
                          database='vcad',
                          cursorclass=pymysql.cursors.DictCursor)
    return cnx


def getCursor():
    cnx = getCNX()
    cursor = cnx.cursor()
    return cursor