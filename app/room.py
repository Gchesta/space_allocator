class Room:
	"""A class for the class Room"""

	def __init__(self, room_name):

		self.room_name = room_name

	def __repr__(self):
 		return self.room_name

class Office(Room):
 	"""A class for Office which inherits from Room"""
 	def __init__(self, room_name):
 		self.residents = {"Fellows":[], "Staff":[]}
 		super().__init__(room_name)

 

class LivingSpace(Room):
 	"""A class for LivingSace which inherits from Room"""
 	def __init__(self, room_name):
 		self.residents = []
 		super().__init__(room_name)

 	
 		
 		