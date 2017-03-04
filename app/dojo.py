
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

    def create_room(self, room_name, room_type):

        if not isinstance(room_type, str) or not isinstance(room_name, str):
            cprint('\n' + '"' +  room_name + '"' + ' contains non-alphabets', 'magenta')
            cprint("Room not added\n", "magenta")
            return 'Room names in strings only'

        room_name = room_name.capitalize()
        room_type = room_type.capitalize()

        if room_type.lower() not in ['office', 'livingspace']:
            cprint('\n' + '"' +  room_type + '"' + ' is an invalid room type', 'magenta')
            cprint("Room not added\n", "magenta")
            return 'Invalid room type'

        if not room_name.isalpha() or not room_type.isalpha():
            cprint('\n' + '"' +  room_name + '"' + ' contains non-alphabets', 'magenta')
            cprint("Room not added\n", "magenta")
            return 'Room names in strings only'

        check_in_offices = room_name in [existing_room.room_name for existing_room in self.offices]
        check_in_livingspaces = room_name in [existing_room.room_name for existing_room in self.livingspaces]

        if check_in_offices or check_in_livingspaces:
            cprint('\n' + '"' +  room_name + '"' + ' already exists', 'magenta')
            cprint("Room not added\n", "magenta")
            return 'Name already exists'

        if room_type.lower() == "office":
            new_office = Office(room_name)
            self.offices.append(new_office)
            self.available_offices.append(new_office)
            cprint("\nSuccessfully added Office " + room_name + "\n", "yellow")

        else:
            new_livingspace = LivingSpace(room_name)
            self.livingspaces.append(new_livingspace)
            self.available_livingspaces.append(new_livingspace)
            cprint("\nSuccessfully added Livingspace " + room_name + "\n", "yellow")
         
    def add_person(self, category, name, surname, accomodation="N"):
        """Add a new member to the Dojo"""
        if not isinstance(name, str) or not isinstance(surname, str):
            cprint('\n' + '"' +  str(name) + ' ' + str(surname) + '"' + ' contains non-alphabets', 'magenta')
            cprint("Person not added\n", "magenta")
            return 'Names in strings only'

        if not name.isalpha() or not surname.isalpha():
            cprint('\n' + '"' +  name + ' ' + surname + '"' + ' contains non-alphabets', 'magenta')
            cprint("Person not added\n", "magenta")
            return 'Names must not contain non-alphabetic characters'
        
        full_name = name.capitalize() + " " + surname.capitalize()
                
        check_in_fellows = full_name in [existing_person.full_name for existing_person in self.fellows]
        check_in_staff = full_name in [existing_person.full_name for existing_person in self.staff]

        if check_in_fellows or check_in_staff:
            cprint('\n' + '"' +  full_name + '"' + ' already exists', 'magenta')
            cprint("Person not added\n", "magenta")
            return "Person already exists" 

        try:
            allocated_office = choice(self.available_offices)
            
        except IndexError:
            cprint("\nNo available ofice at the Dojo", "magenta")
            cprint("Please create a new office\n", "magenta")
            return "No available office"

        if category.lower() == "fellow":

            new_fellow = Fellow(full_name, allocated_office, accomodation)
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
                    cprint("\nThe Dojo lacks an available livingspace", "magenta")
                    cprint("Please add a Livingspace and then add a person\n", "magenta")
                    return "No available office"
                
                allocated_livingspace.occupants.append(new_fellow)
                new_fellow.accomodation = allocated_livingspace

                if len(allocated_livingspace.occupants) == allocated_livingspace.capacity:
                    self.available_livingspaces.remove(allocated_livingspace)
                cprint(new_fellow.full_name + " will reside in " + allocated_livingspace.room_name + "\n", "green")

        elif category.lower() == "staff":
            
            new_staff = Staff(full_name, allocated_office)
            self.staff.append(new_staff)
            allocated_office.occupants.append(new_staff)
            
            if len(allocated_office.occupants) == allocated_office.capacity:
                self.available_offices.remove(allocated_office)
            cprint("\nStaff " + new_staff.full_name + " has been added to the Dojo:", "green")
            cprint(new_staff.full_name + " will occupy office " + allocated_office.room_name + "\n", "green")

