# classes.py
# File that holds all of the global classes
# Kyle Venenga


class officer():
    def __init__(self, list):
        # list: badge_num/id, last name, active, online
        self.id = list[0]
        self.last = list [1]
        self.active = list[2]
        self.online = list[3]

    def print(self):
        print("ID: ", self.id, "\nLast: ", self.last, "\nActive: ", self.active, "\nOnline: ", self.online)
