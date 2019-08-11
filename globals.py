# globals.py
# Holds all of the projects global variables
# Kyle Venenga

# True if app is running
appRunning = True

# Last Name, Badge_Num (all .py)
info = ['', None]

# List of online officers (officerCheck.py)
onlineOfficers = []

# True if dispatcher screen is running (officerCheck.py)
dispRunning = False

# True if officer screen is running (callChecker.py)
offRunning = False

# List of screen objects [Splash, Login, None/Disp/Admin/Off] (all .py)
screens = []

# Current officer ID (callChecker.py)
curOff = ''

# Current Call ID (all .py)
cur_call = 0