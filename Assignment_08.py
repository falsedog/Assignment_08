# Title: Assignment08.py
# Desc: Assignment 08 - Working with classes
# Change Log: (Who, When, What)
# Rain Doggerel, 2022-Dec-03, bug hunting
# Rain Doggerel, 2022-Dec-02, general class and main scaffolding
# Rain Doggerel, 2022-Nov-28, first interaction
# DBiesinger, 2030-Jan-01, created file
# DBiesinger, 2030-Jan-01, added pseudocode to complete assignment 08

# -- IMPORTS -- #
import pickle
import sys

# -- DATA -- #
listOfCDObjects = []  # Leaving this for future archaeologists


class CD:
    """Stores data about a CD:

    properties:
        id: (int) reference index of CD entry
        title: (string) title of the CD
        artist: (string) artist of the CD
    methods:
        init? str? constructor?
    """
    # -- Fields -- #
    cdTotal = 0  # Initialize

    def __init__(self, passed_id, passed_title, passed_artist):  # Should we have overloaded versions?
        # -- Attributes -- #
        self.id = passed_id
        self.title = passed_title
        self.artist = passed_artist
        CD.increase_total()
        listOfCDObjects.append(self)

    def __str__(self):  # TODO dress this up a little more
        return str(self.id) + ' ' + self.title + " by " + self.artist + '\n'

    @staticmethod  # These may be more for practice than it being the worthwhile way to do it right now
    def increase_total():
        CD.cdTotal += 1

    @staticmethod
    def decrease_total():
        CD.cdTotal -= 1

    # def __del__(self): # Apparently we won't be using deconstructors
        # decrease_total()


# -- PROCESSING -- #
class FileIO:
    """Processes data to and from file:

    properties:
        file_name

    methods:
        save_inventory(file_name, list_Inventory): -> None
        load_inventory(file_name): -> (a list of CD objects)
        file_mgmt(): -> updates Filename or creates a file

    """
    accessFileName = 'cdInventory.dat'

    @staticmethod
    def save_inventory(file_name, list_inventory):
        print("Saving automatically overwrites and creates the file")
        print("Enter 'y' to continue or any other key to return")
        save_choice = input().strip().lower()
        if save_choice == 'y':
            try:
                with open(file_name, 'wb+') as writingTo:  # Overwrites and creates if not present
                    pickle.dump(list_inventory, writingTo)
            except Exception as e:  # Generic catch
                print('File access error of some kind\n' + str(e))
        else:
            return

    @staticmethod
    def load_inventory(file_name, quiet):
        if not quiet:
            print("Loading REPLACES the inventory in memory! Enter y to continue")
            load_choice = input().lower().strip()
        else:
            load_choice = 'y'  # A good candidate for a settings or options menu
        if load_choice == 'y':
            try:
                with open(file_name, 'rb') as readingFrom:  # Does NOT create if not present
                    loaded_data = pickle.load(readingFrom)
            except Exception as e:  # Generic catch
                print('File access error of some kind\n' + str(e))
                FileIO.file_mgmt()
            else:
                return loaded_data  # Is Else best here?
        else:
            return

    @staticmethod
    def file_mgmt():
        print('I could not access the file ' + FileIO.accessFileName)
        print('Would you like to create the file (c) or change the filename (f) used?')
        while True:
            file_choice = input().lower().strip()
            if file_choice == 'c':
                FileIO.file_create()
            elif file_choice == 'f':
                FileIO.file_name()  # Sneaky that exiting is possible before it's explained, but it's worth it imo
            elif file_choice == 'x':
                IO.exit()
            else:
                print('Please enter one of those two choices or exit (x)')
                continue

    @staticmethod
    def file_create():
        with open(FileIO.accessFileName, 'wb+') as touch_this:  # The '+' means create if not found
            pickle.dump(None, touch_this)  # Using None... is this the right idea? Haven't had errors yet...

    @staticmethod
    def file_name():
        print('What would you like to change the filename to?')
        print('Conventionally it is something like inventory.dat')
        print('Extensions are optional but preferred')  # It would be good to use a library aware of filename limits...
        FileIO.accessFileName = input()  # ...to check this input, but, scope
        print('The filename is changed, going to the menu')
        print('Please retry accessing the file there')


# -- PRESENTATION (Input/Output) -- #
class IO:
    # TODO add docstring
    """
    """
    @staticmethod
    def menu_display():
        print("Would you like to...\nShow Inventory (i)  Add CD (a)  "
              + "Delete CD (d)  Save (s)  Load (l)  Exit (x)")

    @staticmethod
    def user_choice():
        while True:
            print()
            choice = input().lower().strip()
            global listOfCDObjects  # This list should exist in FileIO or here most likely
            if choice == 'i':
                IO.inventory_display()
                break
            if choice == 'a':
                IO.new_cd()
                break
            if choice == 'd':
                IO.del_cd()
                break
            if choice == 's':
                FileIO.save_inventory(FileIO.accessFileName, listOfCDObjects)
                break
            if choice == 'l':
                listOfCDObjects = FileIO.load_inventory(FileIO.accessFileName, False)
                break
            if choice == 'x':
                IO.exit()
            else:
                print("Please input a valid option")
                continue

    @staticmethod
    def inventory_display():
        for item in listOfCDObjects:
            print(str(item))  # This requires a CD object string method for user-friendly display

    @staticmethod
    def new_cd():
        while True:
            new_id = input("What's the album ID?").strip()
            try:
                int_new_id = int(new_id)
            except ValueError:
                print("Please enter an integer")
                continue
            else:
                break
        new_title = input("What's the album title?")
        new_artist = input("Who's the album artist?")
        CD(int_new_id, new_title, new_artist)  # There's a warning about reference before assignment which isn't true

    @staticmethod
    def del_cd():
        while True:
            print("What is the index of the CD you want to remove from the inventory?")
            del_choice = input()
            if del_choice.lower() == 'x':
                IO.exit()  # Another unspoken but useful chance to exit before it's mentioned
            try:
                int_del_choice = int(del_choice)
            except ValueError:
                print("Please enter an integer number or exit with (x)")
                continue
            else:
                pass
            for index, cd_object in enumerate(listOfCDObjects):  # Cool python trick I thought might exist and it DID
                if int_del_choice == cd_object.id:  # It keeps a loop index without additional hassle
                    del listOfCDObjects[index]
                    CD.decrease_total()  # Important to have this without it being part of a custom deconstructor
                    return
            else:  # This is supposed to fire only if the for+if don't succeed, but it may be bad form
                print("Did not find it, sorry")
                return

    @staticmethod
    def exit():
        sys.exit()


# -- Main Body of Script -- #
listOfCDObjects = FileIO.load_inventory(FileIO.accessFileName, True)  # Make this a choice?
while True:
    IO.menu_display()
    IO.user_choice()
