import globals
import pymysql.cursors
import time
import datetime
import classes
import tts
from threading import Thread


def checkCall():
    time.sleep(1)
    print("Starting Thread")
    while globals.offRunning is True:
        if globals.screens[2].ids.type.text == ' ':
            cnx = getCNX()
            cursor = cnx.cursor()
            cursor.execute("select * from calls where officer_id = %s and active = True", globals.info[1])
            for row in cursor:
                print(row)
                ttsp = []
                globals.screens[2].ids.type.text = row["type"]
                ttsp.append(row["type"])
                globals.screens[2].ids.addr.text = row["street_address"]
                ttsp.append(row["street_address"])
                globals.screens[2].ids.city.text = row["city"]
                globals.screens[2].ids.zip.text = str(row["zip"])
                globals.screens[2].ids.place.text = row["place"]
                ttsp.append(row["place"])
                globals.screens[2].ids.phone.text = row["phone"]
                globals.screens[2].ids.desc.text = row["description"]
                ttsp.append(row["description"])
                globals.cur_call = row["call_id"]
                cursor.execute('update officer set cur_call = %s where officer_id = %s', (globals.cur_call, globals.info[1]))
                cnx.commit()
                Thread(target=tts.build(ttsp)).start()
            cnx.close()
            cursor.close()
        else:
            cnx = getCNX()
            cursor = cnx.cursor()
            cursor.execute("select status from officer where officer_id = %s", globals.info[1])
            for row in cursor:
                if row['status'] is 1:
                    globals.screens[2].clear()
                    cursor.execute('update officer set cur_call = NULL where officer_id = %s', globals.info[1])
                    cursor.execute('update calls set active = False and time_end = %s where call_id = %s',
                                   (datetime.datetime.now(), globals.cur_call))
                    cnx.commit()
        time.sleep(.25)
    print("Stopping Thread")

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

