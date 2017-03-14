
class Room:
	"""A class for the class Room"""

	def __init__(self, name):

		self.name = name
		self.occupants = []
		
	def __repr__(self):
 		return self.name

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


 		