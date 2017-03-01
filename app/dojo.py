from room import LivingSpace, Office
from person import Fellow, Staff
from random import choice

class Dojo:
	"""
	A class that contains the methods to create a new room and to add new people to the 
	Dojo. 

	"""

	def __init__(self):

		self.living_spaces = {"Amugune": ["Jonathan Swift", "Tom Jones"]}
		self.offices = {"Saitoti": { "Fellows":["Jonathan Swift", "Tom Jones"], "Staff":[]}, "Sahari": {"Staff":["William Jakoyo", "Franklin Barasa"], "Fellows":[]} }
		self.fellows = ["Jonathan Swift", "Tom Jones"]
		self.staff = ["William Jakoyo", "Franklin Barasa"]

	def create_room(self, room_type, room_name_list):
		"""Create a new room."""

		self.room_type = room_type

		if self.room_type not in ["Office", "Living-space"]:
			print("The Dojo doesn't have the room type you've entred")

		else:
			
			for room_name in room_name_list:
				self.room_name = room_name

				"""Check whether the room already exists"""
				if self.room_name in self.offices or self.room_name in self.living_spaces:
					print("There is already a room with the name " + self.room_name + ". Please try again")
					raise ValueError
				
				elif self.room_type == "Office":
					"""Create room if it doesn't exists"""
			
					new_office = Office(self.room_name)
					self.offices[str(new_office)] = new_office.residents

				else:
					
					new_living_space = LivingSpace(self.room_name)
					self.living_spaces[str(new_living_space)] = new_living_space.residents

	def add_new_member(self, person_category, person_name, wants_accomodation="N"):
		"""Add a new member to the Dojo"""

		self.person_name = person_name
		self.person_category = person_category
		self.wants_accomodation = wants_accomodation

		"""Check if the person already exists"""
		if self.person_name in self.fellows or self.person_name in self.staff:

			print("There is already a person with with the name " + self.person_name + ". Please try again")
			raise ValueError

		
		elif self.person_category not in ["Staff", "Fellow"]:
			"""Check if the category is valid"""

			print("The Dojo doesn't have the membership you've entred")

		
		elif self.wants_accomodation == "Y":
		#Allocate accomodation to Fellows only and offices to Fellows and Staff
			if self.person_category == "Fellow":
				
				new_fellow = Fellow(self.person_name)
				allocated_office = choice([key for key, value in self.offices.items()])
				allocated_living_space = choice([key for key, value in self.living_spaces.items()])
				self.fellows.append(str(new_fellow))
				self.offices[allocated_office]['Fellows'].append(str(new_fellow))
				self.living_spaces[allocated_living_space].append(str(new_fellow))

			else:

				new_staff = Staff(self.person_name)
				allocated_office = choice([key for key, value in self.offices.items()])
				self.staff.append(str(new_staff))
				self.offices[allocated_office]['Staff'].append(str(new_staff))
				print("Living Spaces are only available for fellows. No room was allocated to " + self.person_name)
				raise ValueError

		else:

		#offices to Staff and to Fellows who don't want accomodation"""
			if self.person_category == "Fellow":
				
				new_fellow = Fellow(self.person_name)
				allocated_office = choice([key for key, value in self.offices.items()])
				self.fellows.append(str(new_fellow))
				self.offices[allocated_office]['Fellows'].append(str(new_fellow))
				
			else:

				new_staff = Staff(self.person_name)
				allocated_office = choice([key for key, value in self.offices.items()])
				self.staff.append(str(new_staff))
				self.offices[allocated_office]['Staff'].append(str(new_staff))
								



       


"""dojo = Dojo()
dojo.create_room("Living-space", ["Chetambe"])
dojo.create_room("Office", ["Harambee", "Nyayo"])
dojo.create_room("Office", ["Harambee", "Nyayo"])
print(dojo.offices)
print(dojo.living_spaces)
dojo.add_new_member("Fellow", "George wekesa")
dojo.add_new_member("Staff", "Wawire Nyongesa")
dojo.add_new_member("Staff", "Wawire Nyongesa")
print(dojo.fellows)
print(type(dojo.staff[2]))
print(dojo.offices)"""

	
	
	



