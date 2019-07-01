from threading import Thread
import globals
import pymysql.cursors
import time
import classes


def startProcess():
    proc = Thread(target=checkOnline).start()
    

def checkOnline():
    time.sleep(2)
    print("starting thread")
    while globals.dispRunning is True:


        cursor = getCursor()
        cursor.execute("select * from officer where  on_duty = True")
        checkOffline()
        for row in cursor:
            create = True
            if len(globals.onlineOfficers) is 0:
                cur = [int(row["officer_id"]), str(row["last_name"]), bool(row["status"]), bool(row["on_duty"])]
                curOff = classes.officer(cur)
                globals.addOff = True
                globals.screens[2].ids.ob.putOfficerIn(curOff.id)
                globals.onlineOfficers.append(curOff)
            else:
                for off in globals.onlineOfficers:
                    if row["officer_id"] == int(off.id):
                        off.active = row["status"]
                        create = False
                print(create)
                if create is True:
                    cur = [int(row["officer_id"]), str(row["last_name"]), bool(row["status"]), bool(row["on_duty"])]
                    curOff = classes.officer(cur)
                    globals.addOff = True
                    globals.screens[2].ids.ob.putOfficerIn(curOff.id)
                    globals.onlineOfficers.append(curOff)
        cursor.close()
        time.sleep(1)
    print("stopping thread")


def getCursor():
    cnx = pymysql.connect(user='vcad',
                          password='vcad123',
                          host='localhost',
                          database='vcad',
                          cursorclass=pymysql.cursors.DictCursor)

    cursor = cnx.cursor()
    return cursor


def checkOffline():
    cursor = getCursor()
    for off in globals.onlineOfficers:
        #print(off.id, off.last)
        cursor.execute("select on_duty from officer where officer_id = %s", off.id)
        for row in cursor:
            #print(row['on_duty'])
            if row['on_duty'] is 0:
                globals.onlineOfficers.remove(off)
                globals.screens[2].ids.ob.deleteOfficer(off.id)
                #print("dddddddddddddddddddddddddddddddddddddd")

