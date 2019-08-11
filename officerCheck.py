# officerCheck.py
# Script that runs in thread to check for online/offline officers and display them, as well as checking status
#   and changing various variables and database entries accordingly.
# Kyle Venenga

import globals
import time
import classes
import db


# checkOnline
# Main function for checking if an officer is online
def checkOnline():
    time.sleep(.25)
    print("starting thread")
    # Run while dispatcher screen is running
    while globals.dispRunning is True:
        # Build database information for all on duty officers
        cursor = db.getCursor()
        cursor.execute("select * from officer where  on_duty = True")
        checkOffline() # Check to see if any officers previously online have gone offline
        # Cycle through all the online officers
        for row in cursor:
            create = True   # If True at the end, we will create new officer
            # If length of online officers is 0, we do not need to check if all status', can assume offline prior
            if len(globals.onlineOfficers) is 0:
                #  Build the officer
                cur = [int(row["officer_id"]), str(row["last_name"]), bool(row["status"]), bool(row["on_duty"])]
                curOff = classes.officer(cur)
                globals.screens[2].ids.ob.putOfficerIn(curOff.id) # Run disp screens add officer to screen function
                globals.onlineOfficers.append(curOff)
            # If the list of online officers is not 0 (Online officers prior to current loop)
            else:
                # Run through all officers
                for off in globals.onlineOfficers:
                    # If the officer was previously online prior to loop, update their status
                    if row["officer_id"] == int(off.id):
                        off.active = row["status"]
                        off.onScene = row["on_scene"]
                        # Update their buttons
                        globals.screens[2].ids.ob.getOfficer(row["officer_id"]).change23Button(row["on_scene"])
                        globals.screens[2].ids.ob.getOfficer(row["officer_id"]).changeStatusButton(row["status"])
                        if off.active is True:
                            db.setCallInactive(db.getCurCall(row["officer_id"]))
                            globals.screens[2].ids.ob.getOfficer(row["officer_id"]).change23Button(False)
                            db.updateOnScene(row["officer_id"], False)
                        # No need to create this officer, they were previously online
                        create = False
                # If we are creating a new officer, new one came online, build officer much like if list was 0
                if create is True:
                    cur = [int(row["officer_id"]), str(row["last_name"]), bool(row["status"]), bool(row["on_duty"])]
                    curOff = classes.officer(cur)
                    globals.screens[2].ids.ob.putOfficerIn(curOff.id)
                    globals.onlineOfficers.append(curOff)
        cursor.close()
        time.sleep(.25)
    print("stopping thread")


# checkOffline
# Checks if there were any previously online officers that have now gone offline
def checkOffline():
    cursor = db.getCursor()
    for off in globals.onlineOfficers:
        cursor.execute("select on_duty from officer where officer_id = %s", off.id)
        for row in cursor:
            if row['on_duty'] is 0:
                globals.onlineOfficers.remove(off)
                globals.screens[2].ids.ob.deleteOfficer(off.id)

