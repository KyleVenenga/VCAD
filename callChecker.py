import globals
import pymysql.cursors
import time
import classes

def checkCall():
    time.sleep(1)
    print("Starting Thread")
    while globals.offRunning is True:
        if globals.screens[2].ids.type.text == ' ':
            cursor = getCursor()
            cursor.execute("select * from calls where officer_id = %s and active = True", globals.info[1])
            for row in cursor:
                print(row)
                globals.screens[2].ids.type.text = row["type"]
                globals.screens[2].ids.addr.text = row["street_address"]
                globals.screens[2].ids.city.text = row["city"]
                globals.screens[2].ids.zip.text = str(row["zip"])
                globals.screens[2].ids.place.text = row["place"]
                globals.screens[2].ids.phone.text = row["phone"]
                globals.screens[2].ids.desc.text = row["description"]
            cursor.close()
        time.sleep(.25)
    print("Stopping Thread")

def getCursor():
    cnx = pymysql.connect(user='vcad',
                          password='vcad123',
                          host='localhost',
                          database='vcad',
                          cursorclass=pymysql.cursors.DictCursor)

    cursor = cnx.cursor()
    return cursor

