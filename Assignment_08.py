#------------------------------------------#
# Title: Assignmen08.py
# Desc: Assignnment 08 - Working with classes
# Change Log: (Who, When, What)
# Rain Doggerel, 2022-Nov-28, first interaction
# DBiesinger, 2030-Jan-01, created file
# DBiesinger, 2030-Jan-01, added pseudocode to complete assignment 08
#------------------------------------------#

# -- IMPORTS -- #
import pickle
import sys

# -- DATA -- #
accessFileName = 'cdInventory.dat'
listOfCDObjects = []


class CD():
    """Stores data about a CD:

    properties:
        id: (int) reference index of CD entry
        title: (string) title of the CD
        artist: (string) artist of the CD
    methods:
        init? str? constructor?
    """
    def __init__(self, passedID, passedTitle, passedArtist): # Should we have overloaded versions?
        self.id = passedID
        self.title = passedTitle
        self.artist = passedArtist

    def __str__(self): # Am I using self correctly here?
        print(self.id, self.title + " by " + self.artist + '\n')
    # TODO Add Code to the CD class, don't forget a string method
    def __del__(self):
        pass # TODO add deallocation stuff

# -- PROCESSING -- #


class FileIO:
    """Processes data to and from file:

    properties:

    methods:
        save_inventory(file_name, list_Inventory): -> None
        load_inventory(file_name): -> (a list of CD objects)

    """
    # TODO Add code to process data from a file
    # TODO Add code to process data to a file
    @staticmethod
    def save_inventory(file_name, list_Inventory):
        try:
            with open(file_name, 'wb+') as writingTo: # Overwrites and creates if not present
                pickle.dump(list_Inventory, writingTo)
        except Exception as e: # Generic catch
            print('File access error of some kind\n' + e)

    @staticmethod
    def load_inventory(file_name):
        try:
            with open(file_name, 'rb') as readingFrom: # Reads and does not create if not present
                loadedData = pickle.load(readingFrom)
        except Exception as e: # Generic catch
            print('File access error of some kind\n' + e)
            # TODO create file function call here
        else:
            return loadedData # Is Else best here?

    @staticmethod
    def file_mgmt():
        print('I could not access the file ' + accessFileName)
        print('Would you like to create the file or change the filename used?')
# -- PRESENTATION (Input/Output) -- #


class IO:
    # TODO add docstring
    """
    """
    # TODO add code to show menu to user
    @staticmethod
    def menuDisplay():
        print('Would you like to\nDisplay Inventory (d)\tAdd CD(a)\t'
              + 'Delete Entry(d)\tSave (s)\tLoad (l)\tExit (x)')
    # TODO add code to captures user's choice
    @staticmethod
    def userChoice():
        while True:
            choice = input(' ').lower().strip() # For readability but also a test to see if this fixes Spyder's console input problem
            if choice == 'd':
                IO.inventoryDisplay()
            if choice == 'a':
                IO.newCD()
            if choice == 'd':
                IO.delCD()
            if choice == 's':
                FileIO.save_inventory()
            if choice == 'l':
                FileIO.load_inventory()
            if choice == 'x':
                IO.exit()
            else:
                print('Please input a valid option')
                continue

    # TODO add code to display the current data on screen
    @staticmethod
    def inventoryDisplay(): # I think this might shoudl be passed the inventory
        for item in listOfCDObjects:
            print(item) # This requires a CD object string method
    # TODO add code to get CD data from user
    @staticmethod
    def newCD():
        while True:
            newID = input('What\'s the album ID?').strip()
            try:
                intNewID = int(newID)
            except ValueError:
                print('Please enter an integer')
                continue
            else:
                break
        newTitle = input('What\'s the album title?')
        newArtist = input('Who\'s the album artist?')
        CD(intNewID, newTitle, newArtist)
    @staticmethod
    def delCD():
        while True:
            print('What is the index of the CD you want to remove from the inventory?')
            delChoice = input()
            try:
                intDelChoice = int(delChoice)
            except ValueError:
                print('Please enter an integer number')
                continue
            else:
                break
            # There needs to be a function to search and delete
    @staticmethod
    def exit():
        sys.exit()

# -- Main Body of Script -- #
# TODO Add Code to the main body
# Load data from file into a list of CD objects on script start
FileIO.load_inventory(accessFileName) # Make this a choice
# Display menu to user
    # show user current inventory
IO.menuDisplay()
    # let user add data to the inventory
    # let user save inventory to file
    # let user load inventory from file
    # let user exit program