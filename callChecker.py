# callChecker.py
# Threaded script that checks for a current call to display to the officer, changes their availability, checks
#   if their availability has changed, and ends the call, also checks for their state, and changes it depending
#   on what the database has for their current state
# Kyle  Venenga

import globals
import time
import datetime
import tts
from threading import Thread
import db
import dbCred

# checkCall
# main function for checking
def checkCall():
    time.sleep(2)
    print("Starting Call Check Thread")
    # While the officer screen is open/logged in
    checkState()
    while globals.offRunning is True:
        checkState()
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
                # Change Status'
                flipState('tenSeven', '')
                # Build the gTTS and play it
                Thread(target=tts.build(ttsp)).start()
            cnx.close()
            cursor.close()
        # If in a current call, check if their status is available then end call
        else:
            cnx = dbCred.getCNX()
            cursor = cnx.cursor()
            # Get current status
            cursor.execute("select * from officer where officer_id = %s", globals.info[1])
            for row in cursor:
                # Check if available, if so end the call, change database information
                if row['status'] is 1:
                    flipState('tenEight', 'twentyThreeN')
                    globals.screens[2].clear()
                    now = datetime.datetime.now()
                    cursor.execute('update officer set cur_call = NULL where officer_id = %s', globals.info[1])
                    cursor.execute('update calls set active = False , time_end = %s where call_id = %s',
                                   (now, globals.cur_call))
                    print(globals.cur_call)
                    cnx.commit()
        time.sleep(.25)
    print("Stopping Thread")

# checkState
# Checks the state of the officer, returns their status/on scene
def checkState():
    cursor = db.getCursor()
    cursor.execute("select * from officer where officer_id = %s", globals.info[1])
    for row in cursor:
        scene = None
        if row['on_scene'] is 1:
            scene = 'twentyThreeD'
        if row['on_scene'] is 0:
            scene = 'twentyThreeN'
        if row['status'] is 0:
            flipState('tenSeven', scene)
        if row['status'] is 1:
            scene = None
            flipState('tenEight', scene)


# flipState
# Changes the officers buttons according to their states
def flipState(state, scene):
    if state == 'tenSeven':
        globals.screens[2].ids.tenSeven.state = 'normal'
        globals.screens[2].ids.tenEight.state = 'down'
    if scene == 'twentyThreeN':
        globals.screens[2].ids.tenTwentyThree.state = 'down'
        globals.screens[2].ids.status.text = '10-7 Out of Service'
    if scene == 'twentyThreeD':
        globals.screens[2].ids.tenTwentyThree.state = 'normal'
        globals.screens[2].ids.status.text = '10-7 10-23'
    if state == 'tenEight':
        globals.screens[2].ids.tenSeven.state = 'down'
        globals.screens[2].ids.tenEight.state = 'normal'
        globals.screens[2].ids.tenTwentyThree.state = 'down'
        globals.screens[2].ids.status.text = '10-8 in service'

