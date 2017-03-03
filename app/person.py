class Person:
	"""An overall class for person"""

	def __init__(self, full_name, office, livingspace=None):

		self.full_name = full_name
		self.livingspace = livingspace
		self.office = office

	def __repr__(self):
		
 		return self.full_name


class Fellow(Person):
	"""A class for fellows"""

	def __init__(self, *args):
		super().__init__(*args)


class Staff(Person):
	""""A class for staff"""

	def __init__(self, *args):
		super().__init__(*args)
	