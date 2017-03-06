from datetime import date

class Room:
	"""A class for the class Room"""

	def __init__(self, room_name):

		self.room_name = room_name
		self.occupants = []
		self.date_created = str(date.today())

	def __repr__(self):
 		return self.room_name

class Office(Room):
 	"""A class for Office which inherits from Room"""
 	def __init__(self, args):
 		self.available_capacity = 6
 		self.category = "Office"

 		super().__init__(args)

class LivingSpace(Room):
 	"""A class for LivingSace which inherits from Room"""
 	def __init__(self, args):
 		self.available_capacity = 4
 		self.category = "Living Space"
 		super().__init__(args)


 		