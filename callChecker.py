# callChecker.py
# Threaded script that checks for a current call to display to the officer, changes their availability, checks
#   if their availability has changed, and ends the call
# Kyle  Venenga

import globals
import pymysql.cursors
import time
import datetime
import classes
import tts
from threading import Thread
import db
import dbCred

# checkCall
# main function for checking
def checkCall():
    time.sleep(5)
    print("Starting Call Check Thread")
    # While the officer screen is open/logged in
    while globals.offRunning is True:
        # If there is no current call - Text should be blank (' ' for aesthetic purposes)
        if globals.screens[2].ids.type.text == ' ':
            # Build cursor object with the call info
            cnx = dbCred.getCNX()
            cursor = cnx.cursor()
            cursor.execute("select * from calls where officer_id = %s and active = True", globals.info[1])
            # Run through each item in the cursor, print it to the screen, build array for gTTS
            for row in cursor:
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
                # Change availability
                cursor.execute('update officer set cur_call = %s where officer_id = %s', (globals.cur_call, globals.info[1]))
                cnx.commit()
                globals.screens[2].ids.cb.buildCall(row['time_start'], row['street_address'], row['call_id'])

                # Build the gTTS and play it
                Thread(target=tts.build(ttsp)).start()
            cnx.close()
            cursor.close()
        # If in a current call, check if their status is available then end call
        else:
            cnx = dbCred.getCNX()
            cursor = cnx.cursor()
            # Get current status
            cursor.execute("select status from officer where officer_id = %s", globals.info[1])
            for row in cursor:
                # Check if available, if so end the call, change database information
                if row['status'] is 1:
                    globals.screens[2].clear()
                    now = datetime.datetime.now()
                    cursor.execute('update officer set cur_call = NULL where officer_id = %s', globals.info[1])
                    cursor.execute('update calls set active = False , time_end = %s where call_id = %s',
                                   (now, globals.cur_call))
                    print(globals.cur_call)
                    cnx.commit()
        time.sleep(.25)
    print("Stopping Thread")


