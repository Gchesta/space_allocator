import unittest
from dojo import Dojo

class TestRoomPersons(unittest.TestCase):
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
             

if __name__ == "__main__":
    unittest.main()
