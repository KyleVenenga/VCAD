# VCAD
###### Computer Aided Dispatch system (CAD) for a security company.

## Features

* Account verification for dispatchers and officers
* Dispatcher screen to monitor officers
* Officer screen to aid in patrol
* Data stored in a database

## Dispatcher Features

* View all currently online officers
* Write out a call information and send it to an officer
* Dynamically check the officer's status' such as busy, on scene, and available
* Error handling such as:
  - Checking for 5 digits and digits only in zip code
  - Checking if an officer is busy before sending the officer a call
  - Checking if any fields are empty before submitting a call
  - Not allowing the dispatcher to mark an officer on screen if they are available for a call
* Change any online officer's status (On scene, busy, available)
* Pages for online officers by multiple of 10s to clear clutter

## Officer Features

* Dynamically checks for new calls 
* Dynamically shows current status (If the dispatcher changes status it will appear changed to the officer)
* Allows officer to change status
* View information about the current call
* Night mode for ease of use while driving at night
* Previous calls section for all previous calls from newest to oldest
* Previous calls section displays 10 at a time, with multiple pages to clear clutter
* Google text to speech when a new call is registered. (Dings, call type, street address, building type, description)


## Technologies 
* Google Text To Speech
* Kivy - Python GUI framework that allows for cross-platform support
* Threading
* MySQL / PySQL
* PyGame
* Google Translator - Reads Av. as Avenue, St. as Street etc.
* Tempfile - For current text to speech audio, then deletes


## Languages
* Python - PyCharm
* Kivy
* SQL - MySQL


# Installation - Client
##### If you want to test the system follow instructions, if you want to see videos there are links below 

1. Open the folder 'Build' and download VCAD-1.0-LH.zip
2. Open the folder 'Database File' and download the DB file
3. Import the DB file into a local MySQL database
4. Ensure that there is an account named 'vcad' with the password 'vcad123' 
5. Start the server
6. Extract the zip
7. Navigate and run VCAD-1.0-LH/dist/VCAD/vcad.exe
8. You may want to run two instances
9. Login to these accounts: (Account Type: Username password)
- Officer: venenga1001 venenga
- Officer: schilling1002 schilling
- Officer: stevens1003 stevens
- Officer: anderson1004 anderson
- Officer: houser1006 houser
- Officer: lincoln1007 lincoln
- Officer: young1008 young
- Dispatcher: paterson1005 paterson

# Installation - Development 
1. Open the folder 'Database File' and download the DB file
2. Import the DB file into a local MySQL database
3. Ensure that there is an account named 'vcad' with the password 'vcad123' 
4. Start the server
5. Clone/Download all of the python files, 'Audio' and 'Kivy Files' folders. 
6. Ensure that all import dependencies are installed on local workstation

# [Video Walkthrough](https://drive.google.com/open?id=1bcmTM_wS1g6w5fqnwAujCVLIQ79yMMRF)
