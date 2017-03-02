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

    def create_room(self, args):
        """Create a new room."""

        for room in args["<room_name>"]:
            
            added_room = room.capitalize()
            check_in_offices = added_room in [existing_room.room_name for existing_room in self.offices]
            check_in_livingspaces = added_room in [existing_room.room_name for existing_room in self.livingspaces]

            rooms_not_added = []
            rooms_added = []

            if check_in_offices or check_in_livingspaces:
                room.reason = "Name already exists"
                rooms_not_added.append(room)

            elif not room.isalpha():
                reason = "Contains non-alphabetic characters"
                rooms_not_added.append((added_room, reason))

            elif args["<type_of_room>"].lower() == "office":
                new_office = Office(added_room)
                date_created = new_office.date_created
                rooms_added.append(new_office)
                self.offices.append(new_office)


            else:
                new_livingspace = LivingSpace(added_room)
                room_type = "Livingspace"
                date_created = new_livingspace.date_created
                rooms_added.append(new_office)
                self.livingspaces.append(new_livingspace)

        print(rooms_added)
        if rooms_added:
            print(" ")
            print("The following rooms have been added to the Dojo:\n")
            for room_added in rooms_added:
                print("Room: " + room_added.room_name)
                print("    Type        : " + type(room_added))
                print("    Date Created: " + room_added.date_created)

        if rooms_not_added:
            print("The following rooms have not been added to the Dojo:")
            for room_added in rooms_added:
                print("Room: " + added_room)
                print("    Reason:" + reason)
                

    def add_person(self, args):
        """Add a new member to the Dojo"""

        full_name_split = args["<person_name>"].title().split(" ")

        if not "".join(full_name_split).isalpha():
            return "Names must be made up entirely of letters"

        first_name = full_name_split[0]
        other_names = " ".join(full_name_split[1:])
        full_name = first_name + " " + other_names

        check_in_fellows = full_name in [
            existing_person.full_name for existing_person in self.fellows]
        check_in_staff = full_name in [
            existing_person.full_name for existing_person in self.staff]

        if check_in_fellows or check_in_staff:
            return "There is already a person with the name " + full_name + ". Please try again"

        allocated_office = choice(self.offices)
        allocated_living_space = choice(self.livingspaces)

        if args["FELLOW"]:
            accomodation = allocated_living_space if args[
                "wants_accomodation"] == "Y" else "NONE"
            new_fellow = Fellow(first_name, other_names,
                                accomodation, allocated_office)
            self.fellows.append(new_fellow)
            allocated_office.occupants.append(new_fellow)

            if accomodation != "NONE":
                allocated_living_space.append(new_fellow)
                allocated_living_space.occupants(new_fellow)

        elif args["STAFF"]:
            accomodation = "NONE"
            new_staff = Staff(first_name, other_names,
                              accomodation, allocated_office)
            self.staff.append(new_staff)
            allocated_office.occupants.append(new_staff)
