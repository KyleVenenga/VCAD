# db.py
# Holds all of the database functions

import dbCred


# getCurCall
# Gets the current call ID for the officer id.
def getCurCall(id):
    cursor = dbCred.getCursor()
    cursor.execute("select cur_call from calls where officer_id = %s", id)
    for call in cursor:
        return call["cur_call"]


# setCallInactive
# Changes a call from active to inactive in the database.
def setCallInactive(id):
    print("setting active to false")
    cnx = dbCred.getCNX()
    cursor = cnx.cursor()
    cursor.execute("update calls set active = False where call_id = %s", id)
    cnx.commit()
    cursor.close()
    cnx.close()


# updateOnScene
# Changes an officer on scene state in the database.
def updateOnScene(id, onScene):
    cnx = dbCred.getCNX()
    cursor = cnx.cursor()
    cursor.execute("update officer set on_scene = %s where officer_id = %s", (onScene, id))
    cnx.commit()
    cnx.close()


# getCursor
# Gets a cursor object from a connection object for the database.
def getCursor():
    cnx = dbCred.getCNX()
    cursor = cnx.cursor()
    return cursor
