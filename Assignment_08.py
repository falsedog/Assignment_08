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
class CD:
    """Stores data about a CD:

    properties:
        id: (int) reference index of CD entry
        title: (string) title of the CD
        artist: (string) artist of the CD
    methods:
        init/constructor: (object) takes int, str, str to create a CD object
        str: (str) returns a nicely formatted string of the album information
        increase_total: increases cd class variable for number of objects
        decrease_total: decreases cd class variable for number of objects
    """
    # -- Fields -- #
    cdTotal = 0  # Initialize

    def __init__(self, passed_id, passed_title, passed_artist):  # Should we have overloaded versions?
        # -- Attributes -- #
        self.id = passed_id
        self.title = passed_title
        self.artist = passed_artist
        CD.increase_total()
        FileIO.listOfCDObjects.append(self)

    def __str__(self):
        return str(self.id) + '\t' + "Title: " + self.title + "\n\tArtist: " + self.artist

    @staticmethod  # These may be more for practice than it being the worthwhile way to do it right now
    def increase_total():
        CD.cdTotal += 1

    @staticmethod
    def decrease_total():
        CD.cdTotal -= 1


# -- PROCESSING -- #
class FileIO:  # Because these are all static it's not really that vital that this be a class...
    """Processes data to and from file:

    properties:
        file_name: the filename used

    methods:
        save_inventory(file_name, list_Inventory): -> None
        load_inventory(file_name): -> Fills list of CD Objects if possible, clears on empty file, returns nothing
        file_mgmt(): -> flows to creating or modifying filename variable
        file_create(): -> creates the file with user approval if possible
        file_name(): -> changes the name of the filename to be loaded or created

    """
    accessFileName = 'cdInventory.dat'
    listOfCDObjects = []  # Initialize

    @staticmethod
    def save_inventory(file_name, list_inventory):
        print("Saving automatically overwrites (or creates) the file")
        print("Enter 'y' to continue or any other key to return to menu ")
        save_choice = input().strip().lower()
        if save_choice == 'y':
            try:
                with open(file_name, 'wb+') as writingTo:  # Overwrites and creates if not present
                    pickle.dump(list_inventory, writingTo)
                print("Saved data")
                return
            except Exception as e:  # Generic catch
                print('File access error of some kind\n' + str(e))
                return

    @staticmethod
    def load_inventory(file_name, quiet):
        if not quiet:
            print("Loading REPLACES the inventory in memory! Enter y to continue\n")
            load_choice = input().lower().strip()
        else:
            load_choice = 'y'  # A good candidate for a settings or options menu
        if load_choice == 'y':
            try:
                with open(file_name, 'rb') as readingFrom:  # Does NOT create if not present
                    FileIO.listOfCDObjects = pickle.load(readingFrom)
                print("Loaded data")
            except EOFError:
                print("No data in file, proceeding with blank inventory")
                FileIO.listOfCDObjects = []
            except Exception as e:  # Generic catch
                print('File access error of some kind\n' + str(e))
                FileIO.file_mgmt()

    @staticmethod
    def file_mgmt():
        print("I could not access the file " + FileIO.accessFileName)
        print("Would you like to create the file (c) or change the filename (f) used?\n")
        while True:
            file_choice = input().lower().strip()
            if file_choice == 'c':
                FileIO.file_create()
            elif file_choice == 'f':
                FileIO.file_name()
            elif file_choice == 'x':  # Sneaky that exiting is possible before it's explained, but it's worth it imo
                IO.exit()
            else:
                print('Please enter one of those two choices or exit (x)\n')
                continue

    @staticmethod
    def file_create():
        try:
            with open(FileIO.accessFileName, 'wb+') as touch_this:  # The '+' means create if not found
                pickle.dump(None, touch_this)  # Using None... is this the right idea? Haven't had errors yet...
        except Exception:
            print("Can't create file, something is too wrong for me to address, sorry")

    @staticmethod
    def file_name():
        print("What would you like to change the filename to?")
        print("Conventionally it is something like inventory.dat")
        print("Extensions are optional but preferred\n")  # I want to use a library aware of filename limits...
        FileIO.accessFileName = input()  # ...to check this input, but, scope
        print("The filename is changed, going to the menu")
        print("Please retry accessing the file there")


# -- PRESENTATION (Input/Output) -- #
class IO:
    """Most general user interface functions:

    properties: None

    methods:
        menu_display(): -> Displays the list of choices to a user
        user_choice(): -> Fields and flows to the user choice
        inventory_display(): -> Uses object function to display a complete CD object inventory
        new_cd(): -> User interface for collecting and passing information to generate a new CD object
        del_cd(): -> Queries user for index of object in inventory to loop to find and delete
            Is not smart enough to distinguish between objects with shared indexes
        exit(): -> Asks about saving before exiting
    """
    @staticmethod
    def menu_display():
        print()
        print("Would you like to...\nShow Inventory (i)  Add CD (a)  "
              + "Delete CD (d)  Save (s)  Load (l)  Exit (x)")

    @staticmethod
    def user_choice():
        while True:
            print()
            choice = input().lower().strip()
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
                FileIO.save_inventory(FileIO.accessFileName, FileIO.listOfCDObjects)
                break
            if choice == 'l':
                loaded_check = FileIO.load_inventory(FileIO.accessFileName, False)
                if loaded_check is not None:  # To safely allow for backing out
                    FileIO.load_inventory(FileIO.accessFileName, False)
                break
            if choice == 'x':
                IO.exit()
            else:
                print("Please input a valid option")
                continue

    @staticmethod
    def inventory_display():
        for item in FileIO.listOfCDObjects:
            print(str(item))  # This requires a CD object string method for user-friendly display

    @staticmethod
    def new_cd():
        while True:  # A version differently informed by the past might never ask for a user provided ID number...
            new_id = input("What's the album ID?\t").strip()  # ...Meaning less chance for duplicates when deleting
            try:
                int_new_id = int(new_id)
                break
            except ValueError:  # It might also be nice to use a library for generic input validation
                print("Please enter an integer")
                continue
        new_title = input("What's the album title?\t")
        new_artist = input("Who's the album artist?\t")
        CD(int_new_id, new_title, new_artist)  # There's a warning about reference before assignment which isn't true

    @staticmethod
    def del_cd():
        while True:
            print("What is the index of the CD you want to remove from the inventory? ")
            del_choice = input()
            if del_choice.lower() == 'x':
                IO.exit()  # Another unspoken but useful chance to exit before it's mentioned
            try:
                int_del_choice = int(del_choice)
            except ValueError:
                print("Please enter an integer number or exit with (x) ")
                continue
            else:
                pass
            for index, cd_object in enumerate(FileIO.listOfCDObjects):  # Nice python trick I thought might exist...
                if int_del_choice == cd_object.id:
                    del FileIO.listOfCDObjects[index]  # ...and it DID! It keeps a loop index without additional hassle
                    CD.decrease_total()  # Important to have this without it being part of a custom deconstructor
                    return
            else:  # This is supposed to fire only if the for+if don't succeed, but it may be bad form...
                print("Did not find it, sorry")
                return

    @staticmethod
    def exit():
        print("Would you like to save before exiting? Press 'y' for yes \n")
        save_first = input().lower().strip()
        if save_first == 'y':
            FileIO.save_inventory(FileIO.accessFileName, FileIO.listOfCDObjects)
            sys.exit()
        else:
            print("Ok byyyeee")
            sys.exit()


# -- Main Body of Script -- #
try:
    FileIO.load_inventory(FileIO.accessFileName, True)  # Make this a choice? A flag?
except Exception:  # Broad exception but this is just in case of truly weird things
    print("Could not load from file, continuing with blank ")
    FileIO.listOfCDObjects = []  # Maybe a second initialization but if it errors here then why not be careful
while True:
    IO.menu_display()
    IO.user_choice()
