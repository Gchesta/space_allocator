import sys
import os
from io import StringIO

import unittest

from space_allocator.app import Dojo, Staff, Fellow, LivingSpace, Office

class TestCreateRoom(unittest.TestCase):

	def setUp(self):
		self.dojo = Dojo()
		
	def test_rejects_invalid_room_type(self):
		self.assertEqual((self.dojo.create_room("Spooky", "Scary")), "\n 'Scary'"
			" is an invalid room type\nRoom not added\n")
	
	def test_new_room_is_instance_of_room(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.create_room("Bush", "LivingSpace")
		self.assertIsInstance(self.dojo.rooms[0], Office)
		self.assertIsInstance(self.dojo.rooms[1], LivingSpace)

	def test_rejects_invalid_name(self):
		self.dojo.create_room("Scary34", "Office")
		self.assertTrue("Scary34" not in [room.name for room in self.dojo.rooms])

	def test_create_office_room_successfully(self):
		self.dojo.create_room("Japan", "Office")
		self.assertTrue("Japan" in [room.name for room in self.dojo.rooms])

	def test_create_living_space_successfully(self):
		self.dojo.create_room("Hopewell", "livingspace")
		self.assertTrue("Hopewell" in [room.name for room in self.dojo.rooms])

	def test_rejects_duplicate_name(self):
		self.dojo.create_room("Jamaica", "Office")
		self.dojo.create_room("Jamaica", "livingspace")
		self.assertTrue("Jamaica" in [room.name for room in self.dojo.rooms if room.category == "Office"])
		self.assertFalse("Jamaica" in [room.name for room in self.dojo.rooms if room.category == "Living Space"])


class TestAddPerson(unittest.TestCase):
	
	def setUp(self):
		self.dojo = Dojo()
	def test_new_person_is_instance_of_person(self):
		self.dojo.add_person("fellow", "John", "Ngravo", "Y")
		self.dojo.add_person("staff", "johny", "mdogo")
		self.assertIsInstance(self.dojo.persons[0], Fellow)
		self.assertIsInstance(self.dojo.persons[1], Staff)

	def test_rejects_invalid_person_name(self):
		self.dojo.add_person("fellow", "John3", "Spike")
		self.assertTrue("John3 Spike" not in [person.name for person in self.dojo.persons])

	def test_rejects_invalid_person_name_non_strings(self):
		self.assertEqual(self.dojo.add_person("fellow", 125, 58888), "\n 125 58888"
		 " contains non-alphabets\nPerson not added\n")
	
	def test_adds_fellow_succesfully(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.add_person("fellow", "johny", "bravo")
		self.assertTrue("Johny Bravo" in [person.name for person in self.dojo.persons])

	def test_adds_fellow_succesfully_with_accomadation(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.create_room("Hunteress", "livingspace")
		self.dojo.add_person("fellow", "John", "Ngravo", "Y")
		self.assertTrue("John Ngravo" in [person.name for person in self.dojo.persons])

	def test_adds_fellow_and_has_received_accomodation(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.create_room("Hunteress", "livingspace")
		self.dojo.add_person("fellow", "John", "Ngravo", "Y")
		self.assertTrue(self.dojo.persons[0].accomodation.name == "Hunteress")

	def test_adds_fellow_and_staff_received_offices(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.add_person("fellow", "johny", "bravo")
		self.dojo.add_person("staff", "John", "Ngravo")
		self.assertTrue(self.dojo.persons[0].office.name == "Hunter")
		self.assertTrue(self.dojo.persons[1].office.name == "Hunter")

	def test_adds_staff_succesfully(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.add_person("staff", "John", "Ngravo")
		self.assertTrue("John Ngravo" in [person.name for person in self.dojo.persons])
		
	def test_raise_error_on_duplicate_persons(self):
		self.dojo.create_room("Hunter", "Office")
		self.dojo.add_person("staff", "John", "Ngravo")
		self.assertEqual(self.dojo.add_person("staff", "John", "Ngravo"),
		 "\n John Ngravo already exists\nPerson not added\n")


class TestPrintFunctions(unittest.TestCase):
	"""A class to test the print functionalities and the ability
	of the functions to output optional txt files. 

	The test_print functions test whether the functions will actually 
	print the required content on the screen. We first create a room, 
	and then add persons. Before running the print function, 
	we reassign sys.stdout to string_with_print_content. 
	The system will print everything here which we shall later 
	capture with the getvalue() method. We compare this value with 
	the expected output and assert whether it's true."""

	def setUp(self):
		self.dojo = Dojo()

	def test_print_names_of_people_in_room(self):
		#setup mock data
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("fellow", "ernest", "achesa", "N")
		self.dojo.add_person("staff", "george", "wanjala")
		#string_with_print_content will hold the output being printed
		stored_standard_output = sys.stdout
		string_with_print_content = StringIO()
		sys.stdout = string_with_print_content
		#call the function which will print to string_with_print_content...
		#...instead of printing on the screen
		self.dojo.print_room("Nairobi")
		#end the function and revert to the original state of sys.stdout
		sys.stdout = stored_standard_output
		output = string_with_print_content.getvalue()
		#escaped characters such as x1b[33m refer to the color
		heading = "\x1b[33m\nROOM NAME: NAIROBI\tROLE\n"
		expected_output = heading + "\x1b[0m\nErnest Achesa \t\tFELLOW\nGeorge Wanjala \t\tSTAFF\n"
		self.assertEqual(output, expected_output)

	def test_print_allocations_on_screen(self):
		#setup mock data		
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.create_room("Chetambe", "livingspace")
		self.dojo.add_person("staff", "george", "wanjala", "Y")
		#string_with_print_content will hold the output being printed
		stored_standard_output = sys.stdout
		string_with_print_content = StringIO()
		sys.stdout = string_with_print_content
		#call the function which will print to string_with_print_content...
		#...instead of printing on the screen
		self.dojo.print_allocations()
		#end the function and revert to the original state of sys.stdout
		sys.stdout = stored_standard_output
		output = string_with_print_content.getvalue()
		#escaped characters such as x1b[33m refer to the color
		heading_1 = "\x1b[34m\nALLOCATIONS - OFFICES\x1b[0m\n"
		heading_2 = "\x1b[33m\nROOM NAME: NAIROBI\tROLE\t\tACCOMODATION\n"
		Office_occupants = "\x1b[0m\nGeorge Wanjala \t\tSTAFF\t\t\n\n"
		heading_3 = "\x1b[34m\nALLOCATIONS - LIVING SPACES\x1b[0m\n"
		expected_output = heading_1 + heading_2 + Office_occupants + heading_3
		self.assertEqual(output, expected_output)

	def  test_print_allocations_with_output_file(self):
		self.dojo.create_room("Chetambe", "livingspace")
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("staff", "george", "wanjala", "Y")
		self.dojo.print_allocations("test_allocations.txt")
		self.assertTrue(os.path.isfile("test_allocations.txt"))
		with open("test_allocations.txt") as outputfile:
			lines = [line.rstrip('\n') for line in outputfile]
			self.assertTrue("ROOM NAME: NAIROBI\tROLE\t\tACCOMODATION" in lines)
			self.assertTrue("George Wanjala \t\tSTAFF\t\t" in lines)
		os.remove("test_allocations.txt")

	def test_print_unallocated_on_screen(self):
		#setup mock data
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("fellow", "george", "wanjala", "Y")
		#string_with_print_content will hold the output being printed
		stored_standard_output = sys.stdout
		string_with_print_content = StringIO()
		sys.stdout = string_with_print_content
		#call the function which will print to string_with_print_content...
		#...instead of printing on the screen
		self.dojo.print_unallocated()
		#end the function and revert to the original state of sys.stdout
		sys.stdout = stored_standard_output
		output = string_with_print_content.getvalue()
		#escaped characters such as x1b[33m refer to the color
		heading_1 = "\x1b[34m\nUNALLOCATED - OFFICES\x1b[0m\n"
		heading_2 = "\x1b[33m\nPERSON NAME\t\tROLE\n\x1b[0m\n\n"
		heading_3 = "\x1b[34m\nUNALLOCATED - LIVING SPACES\x1b[0m\n"
		heading_4 = "\x1b[33m\nPERSON NAME\t\tROLE\n\x1b[0m\n"
		unallocated_persons = "George Wanjala\t\tFELLOW\n"
		expected_output = heading_1 + heading_2 + heading_3 + heading_4 + unallocated_persons
		self.assertEqual(output, expected_output)

	def  test_print_uanllocated_with_output_file(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("fellow", "george", "wanjala", "Y")
		self.dojo.print_unallocated("test_unallocated.txt")
		self.assertTrue(os.path.isfile("test_unallocated.txt"))
		with open("test_unallocated.txt", "r") as outputfile:
			lines = [line.rstrip() for line in outputfile]
			self.assertTrue("PERSON NAME\t\tROLE" in lines)
			self.assertTrue("George Wanjala\t\tFELLOW" in lines)
		os.remove("test_unallocated.txt")

class TestRellocatePerson(unittest.TestCase):
	def setUp(self):
		self.dojo = Dojo()

	def test_rejects_inavalid_id(self):
		rellocate_a = self.dojo.rellocate_person("a", "Nairobi")
		self.assertEqual(rellocate_a, "Invalid Person ID")

	def test_rejects_non_existent_id(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("fellow", "bob", "james")
		self.dojo.create_room("Red", "Office")
		rellocate_bob = self.dojo.rellocate_person(3, "Red")
		self.assertEqual(rellocate_bob, "Invalid Person ID")
	
	def test_rejects_non_existent_room(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("fellow", "bob", "james")
		rellocate_bob = self.dojo.rellocate_person(1, "Purple")
		self.assertEqual(rellocate_bob, "No such room exists")

	def test_rellocates_a_person_succesfully_office(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("fellow", "bob", "james")
		self.dojo.create_room("Kisii", "Office")
		self.dojo.rellocate_person(1, "Kisii")
		self.assertTrue(self.dojo.rooms[1].occupants)
		self.assertFalse(self.dojo.rooms[0].occupants)

	def test_rellocates_a_person_succesfully_livingspace(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.create_room("Kisii", "livingspace")
		self.dojo.add_person("fellow", "bob", "james", "Y")
		self.dojo.create_room("Kenya", "livingspace")
		self.dojo.rellocate_person(1, "Kenya")
		self.assertTrue(self.dojo.rooms[0].occupants)
		self.assertFalse(self.dojo.rooms[1].occupants)
		self.assertTrue(self.dojo.rooms[2].occupants)

	def test_reject_reallocation_of_staff_to_livingspace(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("staff", "bob", "james")
		self.dojo.create_room("Kisii", "Livingspace")
		self.dojo.rellocate_person(1, "Kisii")
		self.assertFalse(self.dojo.rooms[1].occupants)
		self.assertTrue(self.dojo.rooms[0].occupants)

	def test_rejects_reallocation_to_full_room(self):
		self.dojo.create_room("Nairobi", "Office")
		self.dojo.add_person("staff", "baba", "james")
		self.dojo.add_person("staff", "bebe", "james")
		self.dojo.add_person("staff", "bibi", "james")
		self.dojo.add_person("staff", "bobo", "james")
		self.dojo.add_person("staff", "bubu", "james")
		self.dojo.add_person("staff", "babu", "james")
		self.dojo.create_room("Kisii", "Office")
		self.dojo.add_person("staff", "babe", "james")
		relocate_babe = self.dojo.rellocate_person(7, "Nairobi")
		msg ="The requested room is full. Try another room"
		self.assertEqual(relocate_babe, msg)
		self.assertTrue(self.dojo.rooms[0].occupants)

class LoadPeople(unittest.TestCase):
	#Test cases for the LoadPeople function
	def setUp(self):
		self.dojo = Dojo()

	def test_raises_error_on_non_existing_file(self):
		test_load = self.dojo.load_people("load.txt")
		self.assertEqual(test_load, "No such file exists")

	def test_raises_error_on_an_empty_file(self):
		with open("load.txt", "w"):
			test_load = self.dojo.load_people("load.txt")
			self.assertEqual(test_load, "load.txt is empty!")
		os.remove("load.txt")

	def test_loads_people_succesfully(self):
		with open("load2.txt", "w") as inputfile:
			inputfile.write("OLUWAFEMI SULE FELLOW Y\n")
			inputfile.write("DOMINIC WALTERS STAFF\n")
			inputfile.write("SIMON PATTERSON FELLOW Y\n")
		self.dojo.load_people("load2.txt")
		self.assertEqual(len(self.dojo.persons), 3)
		self.assertTrue(self.dojo.persons[2].name == "Simon Patterson")
		os.remove("load2.txt")	

if __name__ == "__main__":
	unittest.main()
