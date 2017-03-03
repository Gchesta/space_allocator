import unittest
from app import Dojo

class TestRoomPersons(unittest.TestCase):
    def setUp(self):
        self.test_object = Dojo()
        self.test_accomodated = Dojo()


    def test_rejects_invalid_room_type(self):
        self.assertEqual((self.test_object.create_room({"<type_of_room>":"Spooky", "<room_name>": ["Scary"]})), "The Dojo doesn't have that room type")

    def test_rejects_invalid_room_name(self):
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Scary34"]})
        self.assertTrue("Scary34" not in [room.room_name for room in self.test_object.offices])

    def test_create_office_room_successfully(self):
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Japan"]})
        self.assertTrue("Japan" in [room.room_name for room in self.test_object.offices])

    def test_create_multiple_office_rooms_successfully(self):
        objects_before = len(self.test_object.offices)
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Zambia", "Zaire", "Pretoria"]})
        objects_after = len(self.test_object.offices)
        self.assertTrue(objects_after - objects_before == 3)

    def test_create_living_space_successfully(self):
        self.test_object.create_room({"<type_of_room>":"Livingspace", "<room_name>": ["Hopewell"]})
        self.assertTrue("Hopewell" in [room.room_name for room in self.test_object.livingspaces])

    def test_create_multiple_living_rooms_successfully(self):
        objects_before = len(self.test_object.livingspaces)
        self.test_object.create_room({"<type_of_room>":"Livingspace", "<room_name>": ["Washington", "Nairobi", "Kampala"]})
        objects_after = len(self.test_object.livingspaces)
        self.assertTrue(objects_after - objects_before == 3)

    def test_rejects_duplicate_room_name(self):
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Hunter"]})
        self.test_object.create_room({"<type_of_room>":"Livingspace", "<room_name>": ["Hunter"]})
        self.assertTrue("Hunter" in [room.room_name for room in self.test_object.offices])
        self.assertFalse("Hunter" in [room.room_name for room in self.test_object.livingspaces])

    def test_rejects_invalid_person_name(self):
        self.test_object.add_person({'<first_name>': 'Spider2', '<surname>': 'dee', 'fellow': True, 'staff': False, "<wants_accomodation>": "Y"})
        self.assertTrue("Spider2 Dee" not in [person.full_name for person in self.test_object.fellows])

    def test_rejects_invalid_person_name_non_strings(self):
        self.assertEqual(self.test_object.add_person({'<first_name>': 125, '<surname>': 1, 'fellow': True, 'staff': False, "<wants_accomodation>": "Y"}), "Name contains non-alphabetic characters")

    def test_adds_if_fellow_succesfully(self):
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Honter", "Buggy", "Spooky"]})
        self.test_object.create_room({"<type_of_room>":"Livingspace", "<room_name>": ["Alto", "Base", "Zimma"]})
        self.test_object.add_person({'<first_name>': "Johny", '<surname>': "bravo", 'fellow': True, 'staff': False, "<wants_accomodation>": "N"})
        self.assertTrue("Johny Bravo" in [person.full_name for person in self.test_object.fellows])

    def test_adds_fellow_succesfully_with_accomadation(self):
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Honter", "Buggy", "Spooky"]})
        self.test_object.create_room({"<type_of_room>":"Livingspace", "<room_name>": ["Alto", "Base", "Zimma"]})
        self.test_object.add_person({'<first_name>': "janE", '<surname>': "ngRavo", 'fellow': True, 'staff': False, "<wants_accomodation>": "Y"})
        self.assertTrue("Jane Ngravo" in [person.full_name for person in self.test_object.fellows])

    def test_adds_fellow_and_has_received_accomodation(self):
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Honter", "Buggy", "Spooky"]})
        self.test_object.create_room({"<type_of_room>":"Livingspace", "<room_name>": ["Alto", "Base", "Zimma"]})
        self.test_object.add_person({'<first_name>': "janE", '<surname>': "ngRavo", 'fellow': True, 'staff': False, "<wants_accomodation>": "Y"})
        self.assertTrue(self.test_object.fellows[0].livingspace)

    def test_adds_fellow_and_staff_received_offices(self):
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Honter", "Buggy", "Spooky"]})
        self.test_object.create_room({"<type_of_room>":"Livingspace", "<room_name>": ["Alto", "Base", "Zimma"]})
        self.test_object.add_person({'<first_name>': "janE", '<surname>': "ngRavo", 'fellow': True, 'staff': False, "<wants_accomodation>": "Y"})
        self.test_object.add_person({'<first_name>': "Danie", '<surname>': "simBa", 'staff': True, 'fellow': False})
        self.assertTrue(self.test_object.fellows[0].office)
        self.assertTrue(self.test_object.staff[0].office)

    def test_adds_staff_succesfully(self):
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Honter", "Buggy", "Spooky"]})
        self.test_object.create_room({"<type_of_room>":"Livingspace", "<room_name>": ["Alto", "Base", "Zimma"]})
        self.test_object.add_person({'<first_name>': "Johny", '<surname>': "bravo", 'staff': True, 'fellow': False})
        self.assertTrue("Johny Bravo" in [person.full_name for person in self.test_object.staff])
        
    def test_raise_error_on_duplicate_persons(self):
        self.test_object.create_room({"<type_of_room>":"Office", "<room_name>": ["Honter", "Buggy", "Spooky"]})
        self.test_object.create_room({"<type_of_room>":"Livingspace", "<room_name>": ["Alto", "Base", "Zimma"]})
        self.test_object.add_person({'<first_name>': "Johny", '<surname>': "bravo", 'fellow': True, 'staff': False, "<wants_accomodation>": "N"})
        self.assertEqual(self.test_object.add_person({'<first_name>': "Johny", '<surname>': "bravo", 'fellow': True, 'staff': False, "<wants_accomodation>": "N"}), "There is already a person with that name")
             

if __name__ == "__main__":
    unittest.main()
