import unittest
from models import Dojo, Room, Office, LivingSpace, Person, Fellow

class TestRooms(unittest.TestCase):

    def test_create_room_successfully(self):
        office = Office("Office", "Spooky")
        initial_room_count = len(office.all_rooms())
        office.create_room()
        new_room_count = len(office.all_rooms())
        self.assertTrue("Spooky" in office.all_rooms() and new_room_count - initial_room_count == 1 )

    def test_raise_eeror_on_duplicate_room(self):
    	with self.assertRaises(ValueError):
    		office_2 = Office("Office", "Speedy")
    		office_2.create_room()

class TestPersons(unittest.TestCase):

    def test_add_new_member_successfully(self):
        fellow = Fellow("Fellow", "George Bush")
        initial_members_count = len(fellow.all_members())
        fellow.add_new_member()
        new_members_count = len(fellow.all_members())
        self.assertTrue("George Bush" in fellow.all_members() and new_members_count - initial_members_count == 1 )

    def test_raise_eeror_on_duplicate_persons(self):
    	with self.assertRaises(ValueError):
    		fellow_2 = Fellow("Fellow", "Jonathan Swift")
    		fellow_2.add_new_member()

if __name__ == "__main__":
    unittest.main()
