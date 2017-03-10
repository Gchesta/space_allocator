
from termcolor import cprint

from .room import LivingSpace, Office
from .person import Fellow, Staff
from random import choice


class Dojo:
    """
    A class that contains the methods to create a new room and to add new persons to the
    Dojo.

    """

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

        room_already_exists = self.check_if_room_exists(name)

        if room_already_exists:
            return("\n The name '%s' already exists\n"
                "Room not added\n" % name)
        else:
            return False

    def check_if_room_exists(self, name):
        for room in self.rooms:
            if room.name == name:
                return True
        return False


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
                 "an office" % (str(person)), "magenta")
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
        accomodation = accomodation.capitalize()
        category = category.capitalize()
        person_is_invalid = self.check_person_invalidity(name, accomodation)

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

        person.idno = len(self.persons) + 1    
        self.persons.append(person)
        cprint("\n %s has been added to the Dojo as a %s" % (name, category), "green")
        self.allocate_office(person)

        if accomodation == "Pending":
            self.allocate_livingspace(person)

    def check_person_invalidity(self, name, accomodation="N"):
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

        return False

    def print_room(self, name):
        name = name.capitalize()
        room_exists = self.check_if_room_exists(name)
        if room_exists:
            for room in self.rooms:
                if room.name == name:
                    cprint("\nROOM NAME: %s\tROLE\n" % name.upper(), "yellow")
                    for occupant in room.occupants:
                        print(str(occupant) + " \t\t" + occupant.category.upper())

        else:
            cprint("Room does not exists", "magenta")

    def choose_headings(self, origin):
        #headings and sub_headings for print_allocations
        heading_allocations_offices = "\nALLOCATIONS - OFFICES"
        subheading_allocations_offices = "\nROOM NAME: %s\tROLE\t\tACCOMODATION\n"
        heading_allocations_livingspaces = "\nALLOCATIONS - LIVING SPACES"
        sub_heading_allocations_livingspaces = "\nROOM NAME: %s\tROLE\t\tOFFICE\n"

        if origin == "print_allocations":
            return(heading_allocations_offices, subheading_allocations_offices,
                heading_allocations_livingspaces, sub_heading_allocations_livingspaces)

        #if origin is not print_allocations, it is print_unallocated
        #headings and sub_headings for print_unallocations
        heading_unallocated_offices = "\nUNALLOCATED - OFFICES"
        heading_unallocated_livingspaces = "\nUNALLOCATED - LIVING SPACES"
        sub_heading_unallocated = "\nPERSON NAME\t\tROLE\n"

        return(heading_unallocated_offices, heading_unallocated_livingspaces,
         sub_heading_unallocated)

    def print_allocations(self, filename=""):
        headings = self.choose_headings("print_allocations")
        heading_office = headings[0]
        sub_heading_office = headings[1]
        heading_livingspace = headings[2]
        sub_heading_livingspace = headings[3]

        cprint(heading_office,  "blue")
        for room in self.rooms:
            if room.category == "Office":
                cprint(sub_heading_office % room.name.upper(), "yellow")
                for occupant in room.occupants:
                    print("%s \t\t%s\t\t%s" %(str(occupant), 
                        occupant.category.upper(), str(occupant.accomodation)))

        cprint(heading_livingspace, "blue")
        for room in self.rooms:
            if room.category == "Living Space":
                cprint(sub_heading_livingspace % room.name.upper(),  "yellow")
                for occupant in room.occupants:
                    print("%s \t\t%s\t\t%s" %(str(occupant), 
                        occupant.category.upper(), str(occupant.office)))
                            
        if filename:
            with open(filename, "w") as outputfile:
                outputfile.write(heading_office)
                for room in self.rooms:
                    if room.category == "Office":
                        outputfile.write(sub_heading_office % room.name.upper())
                        for occupant in room.occupants:
                            outputfile.write("%s \t\t%s\t\t%s\n" %(str(occupant), 
                        occupant.category.upper(), str(occupant.accomodation)))

                outputfile.write(heading_livingspace)
                for room in self.rooms:
                    if room.category == "Living Space":
                        outputfile.write(sub_heading_livingspace % room.name.upper())
                        for occupant in room.occupants:
                            outputfile.write("%s \t\t%s\t\t%s\n" % (str(occupant), 
                        occupant.category.upper(), str(occupant.office)))


    def print_unallocated(self, filename=""):
        headings = self.choose_headings("print_unallocated")
        heading_office = headings[0]
        heading_livingspace = headings[1]
        sub_heading = headings[2]

        cprint(heading_office,  "blue")
        cprint(sub_heading,  "yellow")
        for person in self.persons:
            if person.office == "Unallocated":
                print("%s\t\t%s" % (person.name, person.category.upper()))

        cprint(heading_livingspace,  "blue")
        cprint(sub_heading,  "yellow")
        for person in self.persons:
            if person.accomodation == "Unallocated":
                print("%s\t\t%s" % (person.name, person.category.upper()))

        if filename:
            with open(filename, "w") as outputfile:
                outputfile.write(heading_office + "\n")
                outputfile.write(sub_heading)
                for person in self.persons:
                    if person.office == "Unallocated":
                        outputfile.write("%s\t\t%s\n" %(person.name, person.category.upper()))

                outputfile.write(heading_livingspace)
                outputfile.write(sub_heading)
                for person in self.persons:
                    if person.accomodation == "Unallocated":
                        outputfile.write("%s\t\t%s\n" % (person.name, person.category.upper()))


    