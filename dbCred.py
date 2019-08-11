# dbCred.py
# Kyle Venenga
# Holds database information, allows connection object to be returned with the information
# In another file for security.

import cryptography
import pymysql


# getCNX
# Builds a connection object for the database and returns it
def getCNX():
    cnx = pymysql.connect(user='vcad',
                          password='vcad123',
                          host='192.168.1.170',
                          database='vcad',
                          cursorclass=pymysql.cursors.DictCursor)
    return cnx


