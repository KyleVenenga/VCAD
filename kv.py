# VCAD
# Created 2019
# Computer assisted dispatcher for a smaller security company
# Developer: Kyle Venenga

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.graphics import Color
from kivy.uix.popup import Popup
from kivy.graphics import Line
from kivy.uix.anchorlayout import AnchorLayout
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import StringProperty
import time
import datetime
import math
import pymysql
import pymysql.cursors
from kivy.uix.screenmanager import ScreenManager, Screen
import globals
import officerCheck
import callChecker
import classes
import sys
from threading import Thread
import db

# NOTES FOR .KV LANGUAGE
# Padding, left, top, right, bottom

# ----------------------------------------------------------------- #
# IMPORT .kv FILES
Builder.load_file('Kivy Files/VCAD.kv')
Builder.load_file('Kivy Files/DCAD.kv')
Builder.load_file('Kivy Files/Admin.kv')
Builder.load_file('Kivy Files/Login.kv')
Builder.load_file('Kivy Files/splash.kv')
Builder.load_file('Kivy Files/popup.kv')
Builder.load_file('Kivy Files/RoundedButton.kv')

# ----------------------------------------------------------------- #
# CONNECT TO MYSQL DATABASE
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


# ----------------------------------------------------------------- #
# FUNCTIONS
def addNow(id, col):
    cnx = getCNX()
    call_id = 0
    cursor = cnx.cursor()
    cursor.execute("select call_id from calls where officer_id = %s and active = true", id)
    for cur in cursor:
        call_id = cur['call_id']
    now = datetime.datetime.now()
    cursor.execute("select on_scene_time from calls where call_id = %s", call_id)
    for st in cursor:
        if st["on_scene_time"] is not None:
            print("Scene time is not None")
            return
    print("Call Id: ", call_id)
    try:
        cursor.execute("update calls set on_scene_time = %s where call_id = %s", (now, call_id))
        print("We be workin yo!")
    except:
        print("we not be workin yo")
    cnx.commit()
    cnx.close()
    cursor.close()


def printCalls():
    cursor = getCursor()
    cursor.execute("select * from calls;")
    for row in cursor:
        print(row)

def getCallID():
    print("getCallID")
    cursor = getCursor()  # Database cursor object
    top = 0
    #printCalls()
    cursor.execute("select call_id from calls;")
    if cursor.rowcount is 0:
        print("row count 0")
        return 1

    for row in cursor:
        print("Loop")
        if row["call_id"] > top:
            top = row["call_id"]
    cursor.close()
    return top + 1


def updateAvailability(id, avail):
    cnx = getCNX()
    cursor = cnx.cursor()
    cursor.execute("update officer set status = %s where officer_id = %s", (avail, id))
    cnx.commit()
    cnx.close()
    cursor.close()

def updateOnline(id, online):
    cnx = getCNX()
    cursor = cnx.cursor()
    cursor.execute("update officer set on_duty = %s where officer_id = %s", (online, id))
    cnx.commit()
    cnx.close()
    cursor.close()

# ----------------------------------------------------------------- #
# NON GUI CLASSES


class dispatchCall():
    # list [type, addr, city, zip, place, phone, desc, officer_ID]
    def __init__(self, list):
        self.call_id = getCallID()
        self.callType = list[0]
        self.street_address = list[1]
        self.city = list[2]
        self.zip = list[3]
        self.place = list[4]
        self.phone = list[5]
        self.description = list[6]
        self.time_start = datetime.datetime.now()
        self.time_end = None
        self.officer_id = list[7]
        self.report = ""
        self.active = True
        self.on_scene_time = None
        print("created call")

        statement = "INSERT INTO calls VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        print(statement)
        cnx = getCNX()
        cursor = cnx.cursor()
        cursor.execute(statement, (self.call_id, self.callType, self.street_address, self.city, self.zip, self.place,
                                   self.phone, self.description, self.time_start, self.time_end, self.officer_id,
                                   self.report, self.active, self.on_scene_time))
        cnx.commit()
        cursor.execute("update officer set cur_call = %s where officer_id = %s", (self.call_id, self.officer_id))
        cnx.commit()
        cnx.close()
        cursor.close()
        print("finished")



# ----------------------------------------------------------------- #
# WIDGET CLASSES

# NO LOGIC CLASSES (No code)
class RoundedButton(Widget):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)


class popupError(Popup):
    def __init__(self, **kwargs):
        super(popupError, self).__init__(**kwargs)

    def changeText(self, text):
        self.ids.errorMsg.text = text


class CallWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(CallWidget, self).__init__(**kwargs)


class CallsList(GridLayout):
    def __init__(self, **kwargs):
        super(CallsList, self).__init__(**kwargs)


class AnchorWidget(Widget):
    pass


class HBoxWidget(Widget):
    def __init__(self, **kwargs):
        super(HBoxWidget, self).__init__(**kwargs)


class VBoxWidget(Widget):
    def __init__(self, **kwargs):
        super(VBoxWidget, self).__init__(**kwargs)


class DCADOfficerInfo(BoxLayout):
    def __init__(self, **kwargs):
        super(DCADOfficerInfo, self).__init__(**kwargs)
        self.state = False
        self.on_scene = False

    # press107
    # When 10-7 button is pressed, run this, changes state of other button, and changes label
    def press107(self):
        if self.ids.tenSeven.state != "down":
            self.state = False
            self.ids.tenEight.state = "down"
        else:
            self.ids.tenEight.state = "normal"
            self.state = True
        print(self.state)
        updateAvailability(int(self.ids.badgeNum.text), self.state)

    # press108
    # When 10-8 button is pressed, run this, changes state of other button, and changes label
    def press108(self):
        if self.ids.tenEight.state != "down":
            self.state = True
            db.updateOnScene(int(self.ids.badgeNum.text), False)
            self.ids.onScene.state = "down"
            self.ids.tenSeven.state = "down"
        else:
            self.ids.tenSeven.state = "normal"
            self.state = False
        updateAvailability(int(self.ids.badgeNum.text), self.state)

    def press23(self):
        if self.ids.onScene.state == "normal":
            if self.state == True:
                self.ids.onScene.state = "down"
            else:
                addNow(self.ids.badgeNum.text, " ")
                db.updateOnScene(int(self.ids.badgeNum.text), True)
        else:
            db.updateOnScene(int(self.ids.badgeNum.text), False)
        updateAvailability(int(self.ids.badgeNum.text), self.state)

    def change23Button(self, on_scene):
        if on_scene == False:
            self.ids.onScene.state = "down"
        else:
            self.ids.onScene.state = "normal"

    def changeStatusButton(self, status):
        self.state = status
        if status == False:
            self.ids.tenSeven.state = "normal"
            self.ids.tenEight.state = "down"
        else:
            self.ids.tenSeven.state = "down"
            self.ids.tenEight.state = "normal"
        updateAvailability(int(self.ids.badgeNum.text), self.state)

    def sendCall(self):
        self.state = False
        self.changeStatusButton(False)
        updateAvailability(int(self.ids.badgeNum.text), self.state)
        db.updateOnScene(int(self.ids.badgeNum.text), False)

    def sendBut(self, id):
        globals.screens[2].createCall(id)

# ----------------------------------------------------------------- #
# LOGIC CODED WIDGETS

# MyLabel
# Widget (Image) for implementing resizeable text
class MyLabel(Image):
    text = StringProperty('')

    def on_text(self, *_):
        # Just get large texture:
        l = Label(text=self.text)
        l.font_size = '1000dp'  # something that'll give texture bigger than phone's screen size
        l.texture_update()
        # Set it to image, it'll be scaled to image size automatically:
        self.texture = l.texture


# CallBox
# Widget that holds all the information for the call information
# This class required creating things in Python rather than using kivy language
# I also wanted to get familiar with programming these in Python
class CallsBox(BoxLayout):
    def __init__(self, **kwargs):
        super(CallsBox, self).__init__(**kwargs)

        # MEMBER VARIABLES
        self.calls = []                                 # List of saved calls
        self.page = 1                                   # Current page number for calls
        self.pages = math.ceil(len(self.calls) / 10)    # Keeps number of pages of calls

        # THIS SECTION ADDS A LABEL FOR PREVIOUS CALLS
        self.orientation = "vertical"
        self.labBox = AnchorLayout()
        self.labBox.padding = [0, 5, 0, 0]
        self.labBox.size_hint = (1, .083)
        self.lab = MyLabel()
        self.labBox.add_widget(self.lab)
        self.lab.text = "Previous Calls"
        self.lab.size_hint = (1, .75)
        self.labBox.anchor_x = 'center'
        self.add_widget(self.labBox)

        # THIS SECTION ADDS PREVIOUS AND NEXT BUTTONS FOR CALLS
        self.butBox = GridLayout()
        self.butBox.orientation = 'horizontal'
        self.butBox.size_hint = (1, .083)
        self.butBox.padding = [0, 5, 5, 0]
        self.butBox.rows = 1
        self.prev = RoundedButton()
        self.next = RoundedButton()
        self.curPage = MyLabel()
        self.prev.ids.but.text = "Prev"
        self.next.ids.but.text = "Next"
        self.curPage.text = "Page: " + str(self.page)
        self.butBox.add_widget(self.prev)
        self.butBox.add_widget(self.curPage)
        self.butBox.add_widget(self.next)
        # Bind buttons to functions
        self.next.ids.but.bind(on_press=lambda x:self.nextPrev(self.next.ids.but.text))
        self.prev.ids.but.bind(on_press=lambda x: self.nextPrev(self.prev.ids.but.text))
        self.add_widget(self.butBox)

        # ADD BOX FOR PREVIOUS CALLS
        self.prevCalls = BoxLayout()
        self.prevCalls.orientation = 'vertical'
        self.add_widget(self.prevCalls)

        # TESTING (Adds calls to box for testing)
        for x in range(33):
            self.addCall()

        # DISPLAYS ALL CALLS
        self.displayRange()
        globals.offRunning = True


    # displayRange
    # Displays the range of calls.
    # Adds all the calls for the current page of the callBox
    # Displays calls within the range of the current page
    def displayRange(self):
        # Variables
        end = self.page * 10
        start = end - 10
        remain = len(self.calls) % 10
        self.pages = math.ceil(len(self.calls) / 10)

        # If we have no remainder that means we display 10
        if remain is 0 or self.page < self.pages:
            for start in range(start, end):
                self.prevCalls.add_widget(self.calls[start])
        # Otherwise we just show 10 - the amount we have left over
        else:
            for start in range(start, (start + remain)):
                self.prevCalls.add_widget(self.calls[start])
            # Add blank widgets to keep all of the widgets the same size
            for x in range(10-remain):
                self.prevCalls.add_widget(BoxLayout())

    # addCall
    # adds a new call widget to the array
    # CURRENTLY NEEDS WORK THIS IS DEFAULT (Database work)
    def addCall(self):
        self.cur = CallWidget()
        self.cur.padding = [0, self.height / 10, 5, 0]
        self.cur.width = self.width
        self.calls.append(self.cur)

    # nextPrev
    # Function called when the next/prev buttons are hit
    def nextPrev(self, butTxt):
        self.pages = math.ceil(len(self.calls) / 10)

        # Checks the button, if we can go that direction, display range of calls
        if butTxt is "Prev":
            # If the current page is greater than 1, we can go back
            if self.page > 1:
                self.prevCalls.clear_widgets()
                self.page = self.page - 1
                self.displayRange()
            else:
                return
        if butTxt is "Next":
            # If the current page is less than max pages, we can go forward
            if self.page < self.pages:
                self.prevCalls.clear_widgets()
                self.page = self.page + 1
                self.displayRange()
            else:
                return
        self.curPage.text = "Page: " + str(self.page)


# OfficerBox
# Widget that holds all the information for the online officer information
# This class required creating things in Python rather than using kivy language
# I also wanted to get familiar with programming these in Python
class OfficerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(OfficerBox, self).__init__(**kwargs)

        # MEMBER VARIABLES
        self.officers = []                                  # Array of officer widgets
        self.page = 1                                       # Current page number for calls
        self.pages = math.ceil(len(self.officers) / 10)     # Max number of pages
        self.allOfficers = []


        # THIS SECTION ADDS A LABEL FOR PREVIOUS OFFICERS
        self.orientation = "vertical"
        self.labBox = AnchorLayout()
        self.labBox.padding = [0, 5, 0, 0]
        self.labBox.size_hint = (1, .083)
        self.lab = MyLabel()
        self.labBox.add_widget(self.lab)
        self.lab.text = "Online Officers"
        self.lab.size_hint = (1, .75)
        self.labBox.anchor_x = 'center'
        self.add_widget(self.labBox)

        # THIS SECTION ADDS PREVIOUS AND NEXT BUTTONS FOR OFFICERS
        self.page = 1
        self.butBox = GridLayout()
        self.butBox.orientation = 'horizontal'
        self.butBox.size_hint = (1, .083)
        self.butBox.padding = [0, self.height * .05, 5, self.height * .05]
        self.butBox.rows = 1
        self.prev = RoundedButton()
        self.next = RoundedButton()
        self.curPage = MyLabel()
        self.curPage.padding = [self.width * .25, 0, self.width * .25, 0]
        self.prev.ids.but.text = "Prev"
        self.next.ids.but.text = "Next"
        self.curPage.text = "Page: " + str(self.page)
        self.butBox.add_widget(BoxLayout(size_hint=(.5, 1)))
        self.butBox.add_widget(self.prev)
        self.butBox.add_widget(self.curPage)
        self.butBox.add_widget(self.next)
        self.butBox.add_widget(BoxLayout(size_hint=(.5, 1)))
        # Bind buttons to functions
        self.next.ids.but.bind(on_press=lambda x: self.nextPrev(self.next.ids.but.text))
        self.prev.ids.but.bind(on_press=lambda x: self.nextPrev(self.prev.ids.but.text))
        self.add_widget(self.butBox)
        self.orientation = 'vertical'

        # ADD BOX FOR OFFICERS
        self.officersBox = BoxLayout()
        self.officersBox.orientation = 'vertical'
        self.add_widget(self.officersBox)
        self.buildArray()

        # FOR TESTING (adds officer widgets)
        globals.dispRunning = True
        globals.offRunning = True
        Thread(target=officerCheck.checkOnline).start()


    def buildArray(self):
        cursor = getCursor()
        cursor.execute("select * from officer where dispatch = FALSE and officer_id > 1")
        for row in cursor:
            cur = DCADOfficerInfo()
            cur.ids.name.text = str(row["last_name"])
            cur.ids.badgeNum.text = str(row["officer_id"])
            cur.padding = [0, self.height / 10, 5, 0]
            cur.width = self.width
            cur.oid = int(row["officer_id"])
            print("ID: ", cur.oid)
            cur.ids.onScene.state = "down"
            self.allOfficers.append(cur)

        cursor.close()

    def putOfficerIn(self, id):
        for cur in self.allOfficers:
            if str(id) == cur.ids.badgeNum.text:
                self.officers.append(cur)
                self.displayRange()

    # displayRange
    # Displays the range of officers.
    # Adds all the officers for the current page of the officerBox
    # Displays officers within the range of the current page
    def displayRange(self):
        self.officersBox.clear_widgets()
        # VARIABLES
        end = self.page * 10
        start = end - 10
        remain = len(self.officers) % 10
        self.pages = math.ceil(len(self.officers) / 10)
        # If we have no remainder that means we display 10
        if len(self.officers) is not 0:
            if remain is 0 or self.page < self.pages:
                for start in range(start, end):
                    self.officersBox.add_widget(self.officers[start])
            else:
                # If the current page is less than max pages, we can go forward
                for start in range(start, (start + remain)):
                    self.officersBox.add_widget(self.officers[start])
                # Add blank widgets to keep all of the widgets the same size
                for x in range(10 - remain):
                    self.officersBox.add_widget(BoxLayout())

    # addOfficer
    # adds a new officer widget to the array
    # CURRENTLY NEEDS WORK THIS IS DEFAULT (Database work)
    def addOfficer(self, officer):
        print("Adding Officer")
        self.cur = DCADOfficerInfo()
        self.cur.ids.name.text = officer.last
        self.cur.ids.badgeNum.text = str(officer.id)
        self.cur.padding = [0, self.height / 10, 5, 0]
        self.cur.width = self.width
        self.ids.send.bind(on_press=lambda x: globals.screens[2].createCall())
        self.officers.append(self.cur)
        self.displayRange()

    # nextPrev
    # Function called when the next/prev buttons are hit
    def nextPrev(self, butTxt):
        self.pages = math.ceil(len(self.officers) / 10)

        # Checks the button, if we can go that direction, display range of calls
        if butTxt is "Prev":
            # If the current page is greater than 1, we can go back
            if self.page > 1:
                self.officersBox.clear_widgets()
                self.page = self.page - 1
                self.displayRange()
            else:
                return
        if butTxt is "Next":
            # If the current page is less than max pages, we can go forward
            if self.page < self.pages:
                self.officersBox.clear_widgets()
                self.page = self.page + 1
                self.displayRange()
            else:
                return
        self.curPage.text = "Page: " + str(self.page)

    def deleteOfficer(self, badge):
        for officer in self.officers:
            if officer.ids.badgeNum.text == str(badge):
                self.officers.remove(officer)
                self.displayRange()

    def getOfficer(self, id):
        for officer in self.officers:
            if officer.ids.badgeNum.text == str(id):
                return officer




# ----------------------------------------------------------------- #
# SCREENS


# OfficerScreen
# Screen that the officer views
# VCAD.kv
class OfficerScreen(Screen):
    def __init__(self, **kwargs):
        super(OfficerScreen, self).__init__(**kwargs)
        self.ids.logout.bind(on_press=lambda x: self.logout())  # Bind logout button to logout
        self.ids.officerName.text = globals.info[0]             # Set the name to their name
        self.badge = int(globals.info[1])
        updateOnline(self.badge, True)
        globals.screens[2] = self
        print(self)
        print(globals.screens[2].ids.officerName.text)
        Thread(target=callChecker.checkCall).start()

    def clear(self):
        self.ids.type.text, self.ids.addr.text, self.ids.city.text, self.ids.zip.text, \
            self.ids.place.text, self.ids.phone.text, self.ids.desc.text = (' ', ' ', ' ', ' ', ' ', ' ', ' ')


    # press107
    # When 10-7 button is pressed, run this, changes state of other button, and changes label
    def press107(self):
        self.ids.tenEight.state = "down" if self.ids.tenSeven.state != "down" else "normal"
        self.ids.status.text = "10-7 - Out of Service" if self.ids.tenSeven.state == "down" else "10-8 - In Service"

    # press108
    # When 10-8 button is pressed, run this, changes state of other button, and changes label
    def press108(self):
        self.ids.tenSeven.state = "down" if self.ids.tenEight.state != "down" else "normal"
        self.ids.status.text = "10-7 - Out of Service" if self.ids.tenSeven.state == "down" else "10-8 - In Service"

    # logout
    # Logs out of the user account, switches screen, changes info name back to nothing,
    #  and removes screen to save memory
    def logout(self):
        globals.info = [None, None]
        updateOnline(self.badge, False)
        scrn.switch_to(globals.screens[1])
        globals.screens[2] = None
        globals.offRunning = False


# DispatchScreen
# Screen that the dispatcher sees
# DCAD.kv
class DispatchScreen(Screen):
    def __init__(self, **kwargs):
        super(DispatchScreen, self).__init__(**kwargs)
        self.ids.logout.bind(on_press=lambda x: self.logout())  # Bind logout button to logout
        self.ids.dispatcherName.text = globals.info[0]                               # Set the name to users name
        print(self.canvas.children)

    def changeLineColor(self, isZip, text):
        print("text: ", text)
        if text == "" or text == " " or text == "  ":
            print("blank")
            return (1, 1, 1, 1), 1
        if isZip is True:
            try:
                print("is int")
                testInt = int(text)
                if len(text) == 5:
                    return (0, 1, 0, 1), 2
                elif len(text) < 5:
                    return (1, 1, 0, 1), 2
                else:
                    return (1, 0, 0, 1), 2
            except:
                print("is not int")
                return (1, 0, 0, 1), 2
        else:
            print("is something else")
            return (0, 1, 0, 1), 2


    # logout
    # Logs out of the user account, switches screen, changes info name back to nothing,
    #  and removes screen to save memory
    def logout(self):
        globals.dispRunning = False
        globals.info[0] = ''
        globals.screens[2] = None
        scrn.switch_to(globals.screens[1])
        globals.onlineOfficers = []

    def clearFields(self):
        self.ids.callType.text = ""
        self.ids.streetAddr.text = ""
        self.ids.city.text = ""
        self.ids.zip.text = ""
        self.ids.place.text = ""
        self.ids.phone.text = ""
        self.ids.description.text = ""

    def createCall(self, id):
        print("Creating Call")
        # list [type, addr, city, zip, place, phone, desc, officer_ID]
        callList = [self.ids.callType.text, self.ids.streetAddr.text, self.ids.city.text, self.ids.zip.text,
                    self.ids.place.text, self.ids.phone.text, self.ids.description.text, id]
        for item in callList:
            if item is "" or 0:
                scrn.error = "Empty Field: Please fill in all text boxes."
                error = popupError()
                error.open()
                return
        try:
            testInt = int(callList[3])
            if len(callList[3]) != 5:
                scrn.error = "Zip Code Format: Ensure Zip Code is a 5-digit number."
                error = popupError()
                error.open()
                return
        except:
            scrn.error = "Zip Code Format: Ensure Zip Code is a number."
            error = popupError()
            error.open()
            return
        officer = self.ids.ob.getOfficer(id)
        cursor = getCursor()
        cursor.execute("select status from officer where officer_id = %s", id)
        for row in cursor:
            if row["status"] == 0:
                scrn.error = "Officer is not available."
                error = popupError()
                error.open()
                return
        call = dispatchCall(callList)
        self.ids.ob.getOfficer(id).sendCall()
        self.clearFields()


# LoginScreen
# Screen everyone sees to login to their account
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.ids.logBut.bind(on_press=lambda x: self.loginButton())  # Bind login button to login function
        Window.bind(on_key_down=self._on_keyboard_down)              # Bind window to keyboard down

    # _on_keyboard_down
    # Checks if the user hit enter, and runs the loginButton function
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:  # 40 - Enter key pressed
            self.loginButton()

    # clear
    # Clears all of the information
    def clear(self):
        self.ids.password.text = ""
        self.ids.username.text = ""
        self.ids.status.text = " "

    # loginButton
    # Function called to log in the user, and determine which screen they see next
    def loginButton(self,):
        # VARIABLES
        password = str(self.ids.password.text)  # Password the user entered
        username = str(self.ids.username.text)  # Username the user entered
        cursor = getCursor()                   # Database cursor object

        # LOGIC
        cursor.execute("select * from officer;")    # Execute SQL code to gather officer info
        # Check each instance of officer for if the username exists
        for row in cursor:
            # If username exists
            if row["username"] == str(username):
                # If Password matches usernames password
                if row["pass"] == str(password):
                    globals.info[0] = row["last_name"]  # Set global last name to their last name

                    # CHECK WHAT USER TYPE THEY ARE AND LAUNCH THAT SCREEN
                    #   1. Switch screen to splash screen (Currently not working?)
                    #   2. Screen array at bucket 2, create new screen for that type of user
                    #   3. Clear login information stuff
                    #   4. Switch screen to the user's screen
                    #   5. Break out of the function

                    # If they are a dispatcher
                    if row["dispatch"] == 1:
                        scrn.switch_to(globals.screens[0])
                        globals.screens[2] = DispatchScreen()
                        self.clear()
                        scrn.switch_to(globals.screens[2])
                        return
                    # If they are an admin
                    if row["username"] == 'admin':
                        scrn.switch_to(globals.screens[0])
                        globals.screens[2] = AdminScreen()
                        self.clear()
                        scrn.switch_to(globals.screens[2])
                        return
                    # Otherwise they are an officer
                    else:
                        globals.info[1] = row["officer_id"]
                        scrn.switch_to(globals.screens[0])
                        globals.screens[2] = OfficerScreen()
                        self.clear()
                        scrn.switch_to(globals.screens[2])
                        return
                # If password doesn't match the usernames password
                else:
                    self.ids.status.text = "Incorrect Password"
                    return
        # If the username doesn't exist we will have reached here, let the user know it doesn't exist
        self.ids.status.text = "Username doesn't exist!"
        return


# AdminScreen
# Screen admin sees
class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        self.ids.logout.bind(on_press=lambda x: self.logout(scrn))  # Binds the logout button to logout

    # logout
    # Logs out of the user account, switches screen, changes info name back to nothing,
    #  and removes screen to save memory
    def logout(self, scrn):
        globals.info[0] = ''
        globals.screens[2] = None
        scrn.switch_to(globals.screens[1])


# SplashScreen
# Basic screen with logo
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)


class ScreenManagement(ScreenManager):
    error = ""
    running = True


# ----------------------------------------------------------------- #
# SCREEN MANAGER BUILDING
scrn = ScreenManagement()                           # Screen Manager Object
globals.screens = [SplashScreen(), LoginScreen(), None]     # Array of screens
scrn.switch_to(globals.screens[1])                          # Switch screens to login

# ----------------------------------------------------------------- #
# APPLICATION


# Main Application
# Name must be first screen kv file name then App after
class LoginApp(App):

    # build
    # Builds application
    def build(self):
        self.icon = 'VCAD.png'
        self.title = "VCAD"
        self.loading = Screen(name='splash')
        return scrn

    def stop(self):
        if globals.info[1] is not None:
            updateOnline(globals.info[1], False)
        globals.offRunning = False
        globals.dispRunning = False

    # fontsize
    # Sets the fontsize for the application (dynamic)
    def fontsize(self, text):
        length = 80 if len(text) > 100 else len(text)
        dp = 100
        for x in range(1, length):
            dp -= 1

        # print(dp)
        return "{}dp".format(dp)


# ----------------------------------------------------------------- #
# MAIN

if __name__ == '__main__':
    LoginApp().run()
    globals.appRunning = False
    sys.stdout.flush()
    sys.stdout.close()



