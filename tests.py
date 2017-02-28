import unittest
from models import Office, LivingSpace, Fellow, Staff

class TestRooms(unittest.TestCase):

    def test_create_office_room_successfully(self):
        office = Office("Office", "Spooky")
        initial_room_count = len(office.all_rooms())
        office.create_room()
        new_room_count = len(office.all_rooms())
        self.assertTrue("Spooky" in office.all_rooms() and new_room_count - initial_room_count == 1 )

    def test_create_living_space_room_successfully(self):
        living_space = LivingSpace("LivingSpace", "Righty")
        initial_room_count = len(living_space.all_rooms())
        living_space.create_room()
        new_room_count = len(living_space.all_rooms())
        self.assertTrue("Righty" in living_space.all_rooms() and new_room_count - initial_room_count == 1 )

    def test_raise_error_on_duplicate_room(self):
    	with self.assertRaises(ValueError):
    		office_2 = Office("Office", "Speedy")
    		office_2.create_room()

class TestPersons(unittest.TestCase):

    def test_add_new_fellow_successfully(self):
        fellow = Fellow("Fellow", "George Bush")
        initial_members_count = len(fellow.all_members())
        fellow.add_new_member()
        new_members_count = len(fellow.all_members())
        self.assertTrue("George Bush" in fellow.all_members() and new_members_count - initial_members_count == 1 )

    def test_add_new_staff_successfully(self):
        staff = Staff("Staff", "Tony Blair")
        initial_members_count = len(staff.all_members())
        staff.add_new_member()
        new_members_count = len(staff.all_members())
        self.assertTrue("Tony Blair" in staff.all_members() and new_members_count - initial_members_count == 1 )

    def test_raise_error_on_duplicate_persons(self):
    	with self.assertRaises(ValueError):
    		fellow_2 = Fellow("Fellow", "Jonathan Swift")
    		fellow_2.add_new_member()

    def test_no_staff_can_receive_living_space(self):
        with self.assertRaises(ValueError):
            staff_2 = Staff("Staff", "Bob Marley", "Y")
            staff_2.add_new_member()

if __name__ == "__main__":
    unittest.main()
