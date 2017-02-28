
from random import randint

all_rooms_dict = {"Office":{"Speedy":["Robert Wanyama", "JM Kariuki"], "Hopeshut":["William Jakoyo", "Franklin Barasa"], "Kenya":["Sospeter Ojamong", "Lucy Were", "Madam Veronica", "Roberto Tryasu"]}, "LivingSpace":{"Amugune":["Robert Wanyama,", "JM Kariuki"], "Chetambe":["Sospeter Ojamong", "Lucy Were"], "Nairobi":["Madam Veronica", "Roberto Tryasu"]}}
all_members_dict = {"Fellow":["Jonathan Swift", "Tom Jones", "Andrew Bilfil", "Jane Eyre"], "Staff": ["William Jakoyo", "Franklin Barasa"]}

class Dojo:
	def __init__(self, room_type, room_name):
		self.room_type = room_type
		self.room_name = room_name

	def create_room(self):
		offices = [key for key, value in all_rooms_dict["Office"].items()]
		living_spaces = [key for key, value in all_rooms_dict["LivingSpace"].items()]

		if self.room_name in offices + living_spaces:

			print("That room already exists in the Dojo")
			raise ValueError()
		else:

			all_rooms_dict[self.room_type][self.room_name] = []
	
	def all_rooms(self):
		offices = [key for key, value in all_rooms_dict["Office"].items()]
		living_spaces = [key for key, value in all_rooms_dict["LivingSpace"].items()]

		return offices + living_spaces


class Room(Dojo):
	pass

class Office(Room):
	pass
	
class LivingSpace(Room):
	pass

class Person(object):

	def __init__(self, member_category, member_name, wants_accomodation = "N"):
		self.member_category = member_category
		self.member_name = member_name
		self.wants_accomodation = wants_accomodation

	def add_new_member(self):
		fellows = all_members_dict["Fellow"]
		staff = all_members_dict["Staff"]

		if self.member_name in fellows + staff:

			print("We Already have a similar name at Andela")
			raise ValueError()
		else:
			offices = [key for key, value in all_rooms_dict["Office"].items()]
			no_offices = len(offices)
			random_room = randint(0, no_offices - 1)
			all_rooms_dict["Office"][offices[random_room]].append(self.member_name)
			all_members_dict[self.member_category].append(self.member_name)

		if self.member_category == "Fellow" and self.wants_accomodation == "Y":
			living_spaces = [key for key, value in all_rooms_dict["LivingSpace"].items()]
			no_of_living_spaces = len(living_spaces)
			random_living_space = randint(0, no_of_living_spaces - 1)
			all_rooms_dict["LivingSpace"][living_spaces[random_living_space]].append(self.member_name)

	def all_members(self):
		return all_members_dict["Fellow"] + all_members_dict["Staff"]

class Fellow(Person):
	pass

class Staff(Person):
	pass

