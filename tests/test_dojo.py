import sys
import os
from io import StringIO

import unittest

from app.dojo import Dojo

class TestCreateRoom(unittest.TestCase):
	def setUp(self):
		self.dojo = Dojo()
		

	def test_rejects_invalid_room_type(self):
		self.assertEqual((self.dojo.create_room("Spooky", "Scary")), "Invalid room type")

	def test_rejects_invalid_room_name(self):
		self.dojo.create_room("Scary34", "Office")
		self.assertTrue("Scary34" not in [room.room_name for room in self.dojo.rooms])

	def test_create_office_room_successfully(self):
		self.dojo.create_room("Japan", "Office")
		self.assertTrue("Japan" in [room.room_name for room in self.dojo.rooms])

	def test_create_living_space_successfully(self):
		self.dojo.create_room("Hopewell", "livingspace")
		self.assertTrue("Hopewell" in [room.room_name for room in self.dojo.rooms])

	def test_rejects_duplicate_room_name(self):
		self.dojo.create_room("Jamaica", "Office")
		self.dojo.create_room("Jamaica", "livingspace")
		self.assertTrue("Jamaica" in [room.room_name for room in self.dojo.rooms if room.category == "Office"])
		self.assertFalse("Jamaica" in [room.room_name for room in self.dojo.rooms if room.category == "Living Space"])


class TestAddPerson(unittest.TestCase):
	
	def setUp(self):
		self.dojo = Dojo()

	def test_rejects_invalid_person_name(self):
		self.dojo.add_person("fellow", "John3", "Spike")
		self.assertTrue("John3 Spike" not in [person.full_name for person in self.dojo.people])

	def test_rejects_invalid_person_name_non_strings(self):
		self.assertEqual(self.dojo.add_person("fellow", 125, 58888), 'Names in strings only')

	
	def test_adds_fellow_succesfully(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.add_person("fellow", "johny", "bravo")
		self.assertTrue("Johny Bravo" in [person.full_name for person in self.dojo.people])

	def test_adds_fellow_succesfully_with_accomadation(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.create_room("Hunteress", "livingspace")
		self.dojo.add_person("fellow", "John", "Ngravo", "Y")
		self.assertTrue("John Ngravo" in [person.full_name for person in self.dojo.people])

	def test_adds_fellow_and_has_received_accomodation(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.create_room("Hunteress", "livingspace")
		self.dojo.add_person("fellow", "John", "Ngravo", "Y")
		self.assertTrue(self.dojo.people[0].accomodation.room_name == "Hunteress")

	def test_adds_fellow_and_staff_received_offices(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.add_person("fellow", "johny", "bravo")
		self.dojo.add_person("staff", "John", "Ngravo")
		self.assertTrue(self.dojo.people[0].office.room_name == "Hunter")
		self.assertTrue(self.dojo.people[1].office.room_name == "Hunter")

	def test_adds_staff_succesfully(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.add_person("staff", "John", "Ngravo")
		self.assertTrue("John Ngravo" in [person.full_name for person in self.dojo.people])
		
	def test_raise_error_on_duplicate_persons(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.add_person("staff", "John", "Ngravo")
		self.assertEqual(self.dojo.add_person("staff", "John", "Ngravo"), "Person already exists")

class TesstPrintFunctions(unittest.TestCase):
	"""A class to test the print functionalities in v1"""

	def setUp(self):
		self.dojo = Dojo()

	def test_print_names_of_people_in_room(self):
		#create rooms and add persons
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("fellow", "ernest", "achesa", "N")
		self.dojo.add_person("staff", "george", "wanjala")
		#snapshot to store sys.stdout
		temp = sys.stdout
		#capture will hold the output being printed
		capture = StringIO()
		sys.stdout = capture
		#call functions
		self.dojo.print_room("Nairobi")
		#end functions
		#revert to snapshot of sys.stdout
		sys.stdout = temp
		#the printed value that was captured
		output = capture.getvalue()
		heading = "\x1b[33m\nROOM NAME: NAIROBI\tROLE\n"
		expected_output = heading + "\x1b[0m\nErnest Achesa \t\tFELLOW\nGeorge Wanjala \t\tSTAFF\n"
		self.assertEqual(output, expected_output)

	def test_print_allocations_on_screen(self):
		#create rooms and add persons
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.create_room("Chetambe", "livingspace")
		self.dojo.add_person("staff", "george", "wanjala", "Y")
		#snapshot to store sys.stdout
		temp = sys.stdout
		capture = StringIO()
		sys.stdout = capture
		#call functions
		self.dojo.print_allocations()
		#end functions
		#revert to snapshot of sys.stdout
		sys.stdout = temp
		output = capture.getvalue()
		heading_1 = "\x1b[34m\nALLOCATIONS - OFFICES\x1b[0m\n"
		heading_2 = "\x1b[33m\nROOM NAME: NAIROBI\tROLE\t\tACCOMODATION\n"
		Office_occupants = "\x1b[0m\nGeorge Wanjala \t\tSTAFF\t\t\n"
		heading_3 = "\x1b[34m\nALLOCATIONS - LIVING SPACES\x1b[0m\n"
		heading_4 = "\x1b[33m\nROOM NAME: CHETAMBE\tROLE\t\tOFFICE\n\x1b[0m\n"
		expected_output = heading_1 + heading_2 + Office_occupants + heading_3 + heading_4
		self.assertEqual(output, expected_output)

	def  test_print_allocations_with_output_file(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.create_room("Chetambe", "livingspace")
		self.dojo.add_person("staff", "george", "wanjala", "Y")
		self.dojo.print_allocations("test_allocations.txt")
		self.assertTrue(os.path.exists("test_allocations.txt"))
		with open("test_allocations.txt") as outputfile:
			lines = [line.rstrip('\n') for line in outputfile]
			self.assertTrue("ROOM NAME: CHETAMBE\tROLE\t\tOFFICE" in lines)
			self.assertTrue("George Wanjala \t\tSTAFF\t\t" in lines)
		os.remove("test_allocations.txt")

	def test_print_unallocated_on_screen(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("fellow", "george", "wanjala", "Y")
		#snapshot to store sys.stdout
		temp = sys.stdout
		capture = StringIO()
		sys.stdout = capture
		#call functions
		self.dojo.print_unallocated()
		#end functions
		sys.stdout = temp
		output = capture.getvalue()
		heading_1 = "\x1b[34m\nUNALLOCATED - OFFICES\x1b[0m\n"
		heading_2 = "\x1b[33m\nPERSON NAME\t\tROLE\n\x1b[0m\n"
		heading_3 = "\x1b[34m\nUNALLOCATED - LIVING SPACES\x1b[0m\n"
		heading_3 = "\x1b[34m\nUNALLOCATED - LIVING SPACES\x1b[0m\n"
		heading_4 = "\x1b[33m\nPERSON NAME\t\tROLE\n\x1b[0m\n"
		unallocated_persons = "George Wanjala \t\tFELLOW\n"
		expected_output = heading_1 + heading_2 + heading_3 + heading_4 +unallocated_persons
		self.assertEqual(output, expected_output)

	def  test_print_uanllocated_with_output_file(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("fellow", "george", "wanjala", "Y")
		self.dojo.print_unallocated("test_unallocated.txt")
		self.assertTrue(os.path.exists("test_unallocated.txt"))
		with open("test_unallocated.txt", "r") as outputfile:
			lines = [line.rstrip('\n') for line in outputfile]
			self.assertTrue("PERSON NAME\t\tROLE" in lines)
			self.assertTrue("George Wanjala \t\tFELLOW" in lines)
		os.remove("test_unallocated.txt")

 

if __name__ == "__main__":
	unittest.main()
