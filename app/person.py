class Person:
	"""An overall class for person"""

	def __init__(self, first_name, other_names, living_place, office):

		self.first_name = first_name
		self.other_names = other_names
		self.full_name = first_name + " " + other_names
		self.living_place = living_place
		self.office = office

	def __repr__(self):
		
 		return self.full_name


class Fellow(Person):
	"""A class for fellows"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


class Staff(Person):
	""""A class for staff"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	