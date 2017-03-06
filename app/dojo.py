
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
        
        self.rooms = []
        self.people = []
               
    def create_room(self, room_name, room_type):

        if not isinstance(room_type, str) or not isinstance(room_name, str):
            cprint('\n' + '"' +  room_name + '"' + ' contains non-alphabets', 'magenta')
            cprint("Room not added\n", "magenta")
            return 'Room names in strings only'

        room_name = room_name.capitalize()
        room_type = room_type.capitalize()

        if room_type.lower() not in ('office', 'livingspace'):
            cprint('\n' + '"' +  room_type + '"' + ' is an invalid room type', 'magenta')
            cprint("Room not added\n", "magenta")
            return 'Invalid room type'

        if not room_name.isalpha() or not room_type.isalpha():
            cprint('\n' + '"' +  room_name + '"' + ' contains non-alphabets', 'magenta')
            cprint("Room not added\n", "magenta")
            return 'Room names in strings only'

        check_in_rooms = room_name in [existing_room.room_name for existing_room in self.rooms]
        
        if check_in_rooms:
            cprint('\n' + '"' +  room_name + '"' + ' already exists', 'magenta')
            cprint("Room not added\n", "magenta")
            return 'Name already exists'

        if room_type.lower() == "office":
            new_room = Office(room_name)

        else:
            new_room = LivingSpace(room_name)
        
        self.rooms.append(new_room)
        cprint("\nSuccessfully added " + new_room.category + " "  + room_name + "\n", "yellow")

                 
    def add_person(self, category, name, surname, accomodation=""):
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
        check_in_people = full_name in [existing_person.full_name for existing_person in self.people]
        
        if check_in_people:
            cprint('\n' + '"' +  full_name + '"' + ' already exists', 'magenta')
            cprint("Person not added\n", "magenta")
            return "Person already exists" 

        try:
            allocated_office = choice([room for room in self.rooms if room.category == "Office" and room.available_capacity])
            
        except IndexError:
            allocated_office = "unallocated"
            cprint('\n' + '"' +  full_name + '"' + ' has not been allocated to an office','magenta')
            
        if category.lower() == "fellow":
            new_person = Fellow(full_name, allocated_office, accomodation)

        else:
            new_person = Fellow(full_name, allocated_office)

        self.people.append(new_person)
        if new_person.office != "unallocated":
            allocated_office.occupants.append(new_person)
            allocated_office.available_capacity -= 1
            cprint("\n" + new_person.category + " " + new_person.full_name + " has been added to the Dojo:", "green")
            cprint(new_person.full_name + " will occupy office " + allocated_office.room_name + "\n", "green")

        if accomodation != "":

            try:
                allocated_livingspace = choice([room for room in self.rooms if room.category == "Living Space" and room.available_capacity])
            except IndexError:
                allocated_livingspace = "unallocated"
                cprint('\n' + '"' +  full_name + '"' + ' has not been allocated to a Living Space','magenta')
            
            new_person.accomodation = allocated_livingspace
            if new_person.accomodation != "unallocated":
                allocated_livingspace.occupants.append(new_person)
                allocated_livingspace.available_capacity -= 1
                cprint(new_person.full_name + " will reside in " + allocated_livingspace.room_name + "\n", "green")

   