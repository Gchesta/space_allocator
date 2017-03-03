
from termcolor import cprint, colored

from .room import LivingSpace, Office
from .person import Fellow, Staff
from random import choice



class Dojo:
    """
    A class that contains the methods to create a new room and to add new people to the
    Dojo.

    """
    def __init__(self):
        self.livingspaces = []
        self.offices = []
        self.fellows = []
        self.staff = []
        self.available_offices = []
        self.available_livingspaces = []

    def create_room(self, args):
        """Create a new room."""
        rooms_not_added = []
        rooms_added = []

        for room in args["<room_name>"]:
            
            if not isinstance(room, str):
                rooms_not_added.append({"Room": room_to_add, "Reason": "Only strings are allowed"})

            room_to_add = room.capitalize()
            check_in_offices = room_to_add in [existing_room.room_name for existing_room in self.offices]
            check_in_livingspaces = room_to_add in [existing_room.room_name for existing_room in self.livingspaces]

            elif check_in_offices or check_in_livingspaces:
                rooms_not_added.append({"Room": room_to_add, "Reason": "Name already exists"})

            elif not room_to_add.isalpha():
                rooms_not_added.append({"Room": room_to_add, "Reason": "Contains non-alphabetic characters"})

            elif args["<type_of_room>"].lower() == "office":
                new_office = Office(room_to_add)
                rooms_added.append({"Room": new_office.room_name, "Type": "Office", "Date Created": new_office.date_created})
                self.offices.append(new_office)
                self.available_offices.append(new_office)

            elif args["<type_of_room>"].lower() == "livingspace":
                new_livingspace = LivingSpace(room_to_add)
                room_type = "Livingspace"
                rooms_added.append({"Room": new_livingspace.room_name, "Type": "Livingspace", "Date Created": new_livingspace.date_created})
                self.livingspaces.append(new_livingspace)
                self.available_livingspaces.append(new_livingspace)

            else:
                cprint("\nThe Dojo doesn't have that room type", "yellow")
                cprint("Please try again!", "yellow")
                return "The Dojo doesn't have that room type"
                
                
        print("\n")
        if rooms_added:
            print(" ")
            cprint("The following rooms have been added to the Dojo:\n", "green")
            for room_added in rooms_added:
                print("\nRoom: " + room_added["Room"])
                print("    Type        : " + room_added["Type"])
                print("    Date Created: " + room_added["Date Created"])

        if rooms_not_added:
            
            print(" ")
            cprint("The following rooms have NOT been added to the Dojo:\n", "magenta")
            for room_not_added in rooms_not_added:
                print("\nRoom: " + room_not_added["Room"])
                print("    Reason: " + room_not_added["Reason"])
        print("\n")
                

    def add_person(self, args):
        """Add a new member to the Dojo"""
        try:
            full_name = args["<first_name>"].capitalize() + " " + args["<surname>"].capitalize()
            full_name_split = full_name.split(" ")
        except AttributeError:
            
            cprint("\nName contains non-alphabetic characters", "yellow")
            cprint("Please try again!\n", "yellow")
            return "Name contains non-alphabetic characters"


        if not "".join(full_name_split).isalpha():
            cprint("\nName contains non-alphabetic characters", "yellow")
            cprint("Please try again!\n", "yellow")
            return
        
        check_in_fellows = full_name in [existing_person.full_name for existing_person in self.fellows]
        check_in_staff = full_name in [existing_person.full_name for existing_person in self.staff]

        if check_in_fellows or check_in_staff:
        
            cprint("\nThere is already a person with the name " + full_name, "yellow")
            cprint("Please try again!", "yellow")
            return "There is already a person with that name" 

        try:
            allocated_office = choice(self.available_offices)
            
        except IndexError:
            cprint("\nThe Dojo lacks an available office", "yellow")
            cprint("Please add an office and then add a person\n", "yellow")
            return

        

        if args["fellow"]:
            accomodation = allocated_livingspace if args["<wants_accomodation>"] == "Y" else "NONE"
            new_fellow = Fellow(full_name, accomodation, allocated_office)
            self.fellows.append(new_fellow)
            allocated_office.occupants.append(new_fellow)
            if len(allocated_office.occupants) == allocated_office.capacity:
                self.available_offices.remove(allocated_office)
            cprint("\nFellow " + new_fellow.full_name + " has been added to the Dojo:", "green")
            cprint(new_fellow.full_name + " will occupy office " + allocated_office.room_name + "\n", "green")

            if accomodation != "NONE":

                try:
                    allocated_livingspace = choice(self.available_livingspaces)
                except IndexError:
                    cprint("\nThe Dojo lacks an available livingspace", "yellow")
                    cprint("Please add a Livingspace and then add a person\n", "yellow")
                    return
                allocated_livingspace.occupants.append(new_fellow)
                if len(allocated_livingspace.occupants) == allocated_livingspace.capacity:
                    self.available_livingspaces.remove(allocated_livingspace)
                cprint(new_fellow.full_name + " will reside in " + allocated_livingspace.room_name + "\n", "green")

        elif args["staff"]:
            accomodation = "NONE"
            new_staff = Staff(full_name, allocated_office)
            self.staff.append(new_staff)
            allocated_office.occupants.append(new_staff)
            if len(allocated_office.occupants) == allocated_office.capacity:
                self.available_offices.remove(allocated_office)
            cprint("\nStaff " + new_staff.full_name + " has been added to the Dojo:", "green")
            cprint(new_staff.full_name + " will occupy office " + allocated_office.room_name + "\n", "green")

