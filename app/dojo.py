
from os.path import isfile, getsize

from termcolor import cprint

from .room import LivingSpace, Office
from .person import Fellow, Staff
from random import choice


class Dojo:
    """
    A class that contains the methods to create a new room and to add new persons to the
    Dojo."""

    def __init__(self):
        self.rooms = []
        self.persons = []

    def create_room(self, name, category):
        name = str(name).capitalize()
        category = str(category).capitalize()
        room_is_invalid = self.check_room_invalidity(name, category)

        if room_is_invalid:
            cprint(room_is_invalid, "magenta")
            return room_is_invalid
        else:
            if category == "Office": 
                room = Office(name)
            else:
                room = LivingSpace(name)
        
        self.rooms.append(room)
        cprint("\nSuccessfully added %s %s\n" % (category,
               name), "yellow")
        self.allocate_the_unallocated(category)

    def check_room_invalidity(self, name, category):

        if category.lower() not in ("office", "livingspace"):
            return ("\n '%s' is an invalid room type\n"
                            "Room not added\n" % category)
            
        if not name.isalpha():
            return ("\n room name contains"
             "non-alphabets\nRoom not added\n")

        room_exists = self.check_if_room_exists(name)

        if room_exists != "No such room exists":
            return("\n The name '%s' already exists\n"
                "Room not added\n" % name)
        else:
            return False

    def check_if_room_exists(self, name):        
        try:
            check = [room for room in self.rooms if room.name == name][0]
        except IndexError:
            check = "No such room exists"
        return check

    def allocate_the_unallocated(self, category):

        if category == "Office":
            for person in self.persons:
                if person.office == "Unallocated":
                    self.allocate_office(person)

        else:
            for person in self.persons:
                if person.accomodation == "Unallocated":
                    self.allocate_livingspace(person)

    def allocate_office(self, person):

        available_office = self.check_room_availability("Office")       

        if available_office:
            person.office = available_office
            available_office.occupants.append(person)
            available_office.available_capacity -= 1
            cprint("\n %s will occupy office %s\n"
                % (str(person), str(available_office)), "green")

        elif person.office == "Pending":
            person.office = "Unallocated"
            cprint("\n %s has not been allocated to"
                 " an office" % (str(person)), "magenta")
        else:
            pass

    def allocate_livingspace(self, person):
        available_livingspace = self.check_room_availability("Living Space")        

        if available_livingspace:
            person.accomodation = available_livingspace
            available_livingspace.occupants.append(person)
            available_livingspace.available_capacity -= 1
            cprint("\n %s will reside in %s\n" 
                % (str(person), str(available_livingspace)), "green")

        elif person.accomodation == "Pending":
            person.accomodation = "Unallocated"
            cprint("\n %s has not been allocated to"
                 "a living space" % (str(person)), "magenta")
        else:
            pass
        
    def check_room_availability(self, category):
        try:
            available_room = choice(
                    [room for room in self.rooms if room.category == category and room.available_capacity])
        except IndexError:
            available_room = False
        return available_room

    def add_person(self, category, name, surname, accomodation="N"):
        name = str(name).capitalize() + " " + str(surname).capitalize()
        accomodation = str(accomodation).capitalize() if accomodation else "N"
        category = str(category).capitalize()
        person_is_invalid = self.check_person_invalidity(name, accomodation, category)

        if person_is_invalid:
            cprint(person_is_invalid, "magenta")
            return person_is_invalid

        else:
            office = "Pending"
            accomodation = "Pending" if accomodation == "Y" and category == "Fellow" else ""

        if category == "Fellow":
            person = Fellow(name, office, accomodation)

        else:
            person = Staff(name, office)

        self.persons.append(person)
        cprint("\n %s has been added to the Dojo as a %s" % (name, category), "green")
        self.allocate_office(person)

        if accomodation == "Pending":
            self.allocate_livingspace(person)

    def check_person_invalidity(self, name, accomodation, category):
        name_split = name.split(" ")
        
        if not name_split[0].isalpha() or not name_split[1].isalpha():
            return ("\n %s contains non-alphabets\n"
                "Person not added\n" % name)

        name_already_exists = name in [
            person.name for person in self.persons]

        if name_already_exists:
            return ("\n %s already exists\n"
            "Person not added\n" % name)

        if accomodation not in ("N","Y"):
            return ("Choose either 'Y' or 'N' for accomodation")

        if category not in ("Fellow", "Staff"):
            return "Invalid person category"

        return False

    def print_room(self, name):
        name = name.capitalize()
        room = self.check_if_room_exists(name)
        if room != "No such room exists":
            cprint("\nROOM NAME: %s\tROLE\n" % name.upper(), "yellow")
            for occupant in room.occupants:
                print(str(occupant) + " \t\t" + occupant.category.upper())
        else:
            cprint(room, "magenta")

    def print_allocations(self, filename=""):
        heading_office = "\nALLOCATIONS - OFFICES"
        sub_heading_office = "\nROOM NAME: %s\tROLE\t\tACCOMODATION\n"
        heading_livingspace = "\nALLOCATIONS - LIVING SPACES"
        sub_heading_livingspace = "\nROOM NAME: %s\tROLE\t\tOFFICE\n"
        
        allocations = self.get_allocations()
        offices = allocations[0]
        livingspaces = allocations[1]

        cprint(heading_office, "blue")
        for room, occupants in offices.items():
            cprint(sub_heading_office % room.name.upper(),  "yellow")
            print(occupants)

        cprint(heading_livingspace, "blue")
        for room, occupants in livingspaces.items():
            cprint(sub_heading_livingspace % room.name.upper(),  "yellow")
            print(occupants)
                            
        if filename:
            with open(filename, "w") as outputfile:
                outputfile.write(heading_office)
                for room, occupants in offices.items():
                     outputfile.write(sub_heading_office % room.name.upper())
                     outputfile.write(occupants)
                outputfile.write(heading_livingspace)
                for room, occupants in livingspaces.items():
                    outputfile.write(sub_heading_livingspace % room.name.upper())
                    outputfile.write(occupants)

    def print_unallocated(self, filename=""):
        heading_office = "\nUNALLOCATED - OFFICES"
        heading_livingspace = "\nUNALLOCATED - LIVING SPACES"
        sub_heading = "\nPERSON NAME\t\tROLE\n"
        unallocated_livingspace = ""
        unallocated_office = ""

        for person in self.persons:
            if person.office == "Unallocated":
                unallocated_office += ("%s\t\t%s\n" % (person.name, person.category.upper()))

            if person.accomodation == "Unallocated":
                unallocated_livingspace += ("%s\t\t%s\n" % (person.name, person.category.upper()))

        cprint(heading_office,  "blue")
        cprint(sub_heading,  "yellow")
        print(unallocated_office)

        cprint(heading_livingspace,  "blue")
        cprint(sub_heading,  "yellow")
        print(unallocated_livingspace)

        if filename:
            with open(filename, "w") as outputfile:
                outputfile.write("%s\n%s" %(heading_office, sub_heading))
                outputfile.write(unallocated_office)
                outputfile.write("%s\n%s" %(heading_livingspace, sub_heading))
                outputfile.write(unallocated_livingspace)

    def get_allocations(self):
        offices = {}
        livingspaces = {}
        for room in self.rooms:
            if room.category == "Office":
                allocations_office = ""
                for occupant in room.occupants:
                     allocations_office += ("%s \t\t%s\t\t%s\n" %(str(occupant), 
                        occupant.category.upper(), str(occupant.accomodation)))
                offices[room] = allocations_office
            else:
                allocations_livingspace = ""
                for occupant in room.occupants:
                    allocations_livingspace += ("%s \t\t%s\t\t%s\n" %(str(occupant), 
                        occupant.category.upper(), str(occupant.office)))
                livingspaces[room] = allocations_livingspace
        return(offices, livingspaces)



