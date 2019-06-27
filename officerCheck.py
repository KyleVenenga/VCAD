from threading import Thread
import globals
import pymysql.cursors
import time
import classes




proc = None

def startProcess():
    proc = Thread(target=checkOnline).start()


def checkOnline():
    print(globals.running)
    while globals.running is True:

        create = True
        cursor = getCursor()
        cursor.execute("select * from officer where  on_duty = True")
        checkOffline()
        for row in cursor:
            if len(globals.onlineOfficers) is 0:
                cur = [int(row["officer_id"]), str(row["last_name"]), bool(row["status"]), bool(row["on_duty"])]
                officer = classes.officer(cur)
                globals.onlineOfficers.append(officer)
                globals.screens[2].ids.ob.addOfficer(officer)
                print("cccccccccccccccccccccccccccccccccccccccc")
            else:
                for off in globals.onlineOfficers:
                    print(row["officer_id"], str(off.id))
                    if row["officer_id"] == int(off.id):
                        off.active = row["status"]
                        create = False
                        print("sssssssssssssssssssssssssssssssssss")
                print(create)
                if create is True:
                    cur = [int(row["officer_id"]), str(row["last_name"]), bool(row["status"]), bool(row["on_duty"])]
                    print(cur)
                    officer = classes.officer(cur)
                    globals.onlineOfficers.append(officer)
                    globals.screens[2].ids.ob.addOfficer(officer)
                    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
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
        print(off.id, off.last)
        cursor.execute("select on_duty from officer where officer_id = %s", off.id)
        for row in cursor:
            print(row['on_duty'])
            if row['on_duty'] is 0:
                globals.onlineOfficers.remove(off)
                globals.screens[2].ids.ob.deleteOfficer(off.id)
                print("dddddddddddddddddddddddddddddddddddddd")

