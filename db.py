# db.py
# Holds all of the database functions

import dbCred
import pymysql


def getCurCall(id):
    cursor = dbCred.getCursor()
    cursor.execute("select cur_call from calls where officer_id = %s", id)
    for call in cursor:
        return call["cur_call"]


def setCallInactive(id):
    print("setting active to false")
    cnx = dbCred.getCNX()
    cursor = cnx.cursor()
    cursor.execute("update calls set active = False where call_id = %s", id)
    cnx.commit()
    cursor.close()
    cnx.close()


def updateOnScene(id, onScene):
    cnx = dbCred.getCNX()
    cursor = cnx.cursor()
    cursor.execute("update officer set on_scene = %s where officer_id = %s", (onScene, id))
    cnx.commit()
    cnx.close()


def getCursor():
    cnx = dbCred.getCNX()
    cursor = cnx.cursor()
    return cursor
