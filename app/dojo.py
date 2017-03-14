
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
        
        if category == "Office": 
            room = Office(name)
        else:
            room = LivingSpace(name)        
        
        self.rooms.append(room)
        cprint("\nSuccessfully added %s %s\n" % (category,
               name), "yellow")
        self.allocate_the_unallocated(category)

    def check_room_invalidity(self, name, category):
        """checks if room to be added is has invalid arguments
        and returns the error when it is"""
        if category.lower() not in ("office", "livingspace"):
            return ("\n '%s' is an invalid room type\n"
                            "Room not added\n" % category)            
        if not name.isalpha():
            return ("\n room name contains"
             "non-alphabets\nRoom not added\n")
        room_exists = self.check_if_room_exists(name)
        if room_exists != "\nNo such room exists\n":
            return("\n The name '%s' already exists\n"
                "Room not added\n" % name)
        
    def check_if_room_exists(self, name):
        """Receives a room_name as argument 
        and returns the room object"""        
        try:
            check = [room for room in self.rooms if room.name == name][0]
        except IndexError:
            check = "\nNo such room exists\n"
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
                 " a living space" % (str(person)), "magenta")
        else:
            pass
        
    def check_room_availability(self, category):
        """Finds and return a random room that's not yet full"""
        try:
            available_room = choice(
                    [room for room in self.rooms
                     if room.category == category and room.available_capacity])
        except IndexError:
            return
        return available_room

    def add_person(self, category, name, surname, accomodation="N"):
        name = str(name).capitalize() + " " + str(surname).capitalize()
        accomodation = str(accomodation).capitalize() if accomodation else "N"
        category = str(category).capitalize()
        person_is_invalid = self.check_person_invalidity(name, accomodation, category)
        
        if person_is_invalid:
            cprint(person_is_invalid, "magenta")
            return person_is_invalid
        
        office = "Pending"
        accomodation = "Pending" if accomodation == "Y" and category == "Fellow" else ""
        
        if category == "Fellow":
            person = Fellow(name, office, accomodation)
        else:
            person = Staff(name, office)
        
        person.idno = str(len(self.persons) + 1)
        self.persons.append(person)
        cprint("\n %s has been added to the Dojo as a %s" % (name, category), "green")
        self.allocate_office(person)
        if accomodation == "Pending":
            self.allocate_livingspace(person)

    def check_person_invalidity(self, name, accomodation, category):
        """Checks whether a new person has invalid arguments and 
        returns an explantion"""
        name_split = name.split(" ")        
        if not name_split[0].isalpha() or not name_split[1].isalpha():
            return ("\n %s contains non-alphabets\n"
                "Person not added\n" % name)
        if self.get_person_by_attribute(name, "name") != "Invalid name":
            return ("\n %s already exists\n"
            "Person not added\n" % name)
        if accomodation not in ("N","Y"):
            return ("\nChoose either 'Y' or 'N' for accomodation\n")
        if category not in ("Fellow", "Staff"):
            return "Invalid person category"
        
    def get_person_by_attribute(self, var, attr):
        """This function receives two argument the attribute(attr - eg "name") and the
        specific attribute of the person eg "George Bush" It returns the person object
        It allows for flexibility since a one can request with any valid unique attr such as 
        idno"""
        try:
            person = [person for person in self.persons if getattr(person, attr) == var][0]
        except IndexError:
            return "Invalid %s" % attr
        return person

    def print_room(self, name):
        name = name.capitalize()
        room = self.check_if_room_exists(name)
        if room != "\nNo such room exists\n":
            cprint("\nROOM NAME: %s\tROLE\n" % name.upper(), "yellow")
            for occupant in room.occupants:
                print(str(occupant) + " \t\t" + occupant.category.upper())
        else:
            cprint(room, "magenta")

    def print_allocations(self, filename=""):
        heading_office = "\nALLOCATIONS - OFFICES\n"
        sub_heading_office = "\nROOM NAME \t\tROLE"
        heading_livingspace = "\nALLOCATIONS - LIVING SPACES\n"
        sub_heading_livingspace = "\nROOM NAME \t\tROLE" 
        offices_string = ""
        livingspaces_string = ""

        for room in self.rooms:
            if room.category == "Office" and room.occupants:
                offices_string += ("\n%s\n%s\n" %(room.name.upper(),
                "=" * 30) + "".join(["%s \t\t%s\n" %(str(occupant), 
                occupant.category.upper()) for occupant in room.occupants]))

            elif room.category == "Living Space" and room.occupants:
                livingspaces_string  += ("\n%s\n%s\n" %(room.name.upper(),
                "=" * 30) + "".join(["%s \t\t%s\n" %(str(occupant), 
                occupant.category.upper()) for occupant in room.occupants]))

        if filename:
            with open(filename, "w") as outputfile:
                outputfile.write("%s%s%s%s%s%s" %(heading_office, sub_heading_office, offices_string,
                heading_livingspace, sub_heading_livingspace, livingspaces_string))
            cprint("\nSuccessfully printed the output to file %s\n" %filename, "yellow")
        else:
            cprint("%s%s" %(heading_office, sub_heading_office), "yellow")
            print(offices_string)
            cprint("%s%s" %(heading_livingspace, sub_heading_livingspace), "yellow")
            print(livingspaces_string)
        
    def print_unallocated(self, filename=""):
        """Prints the list of unallocated people on the screen or 
        outputs a txt file with the names"""
        heading_office = "\nUNALLOCATED - OFFICES"
        heading_livingspace = "\nUNALLOCATED - LIVING SPACES"
        sub_heading = "\nPERSON NAME\t\tROLE\n"
        
        unallocated_office = "\n".join (["%s\t\t%s" % (person.name, 
            person.category.upper()) for person in self.persons if person.office == "Unallocated"])
        
        unallocated_livingspace = "\n".join (["%s\t\t%s" % (person.name, 
            person.category.upper()) for person in self.persons if person.accomodation == "Unallocated"])
        
        complete_string = ("%s\n%s%s%s\n%s%s" %(heading_office, sub_heading, 
            unallocated_office, heading_livingspace, sub_heading, unallocated_livingspace))        
        
        if filename:
            with open(filename, "w") as outputfile:
                outputfile.write(complete_string)
            cprint("\Successfully printed the output to file %s\n" %filename, "yellow")
        else:
            cprint(heading_office,  "blue")
            cprint(sub_heading,  "yellow")
            print(unallocated_office)
            cprint(heading_livingspace,  "blue")
            cprint(sub_heading,  "yellow")
            print(unallocated_livingspace)
                        
   