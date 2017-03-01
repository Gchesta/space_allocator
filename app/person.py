class Person:
	"""An overal class for person"""

	def __init__(self, person_name):

		self.person_name = person_name

	def __repr__(self):
 		return self.person_name


class Fellow(Person):
	"""A class for fellows"""

	def __init__(self, person_name):
		super().__init__(person_name)


class Staff(Person):
	""""A class for staff"""

	def __init__(self, person_name):
		super().__init__(person_name)
	