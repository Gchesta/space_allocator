class Person:
	"""An overall class for person"""

	def __init__(self, name, office, idno, accomodation=""):

		self.name = name
		self.accomodation = accomodation
		self.office = office
		self.idno = idno

	def __repr__(self):
		
 		return self.name

class Fellow(Person):
	"""A class for fellows"""
	
	def __init__(self, *args):
		self.category = "Fellow"
		super().__init__(*args)


class Staff(Person):
	""""A class for staff"""
	
	def __init__(self, *args):
		self.category = "Staff"
		super().__init__(*args)
	