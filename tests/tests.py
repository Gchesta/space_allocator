import unittest
from app.dojo import  Dojo

class TestRooms(unittest.TestCase):

    def test_create_office_room_successfully(self):
        test_office = Dojo()
        test_office.create_room("Office", ["Spooky"])
        self.assertTrue("Spooky" in test_office.offices)

    def test_multiple_office_room_successfully(self):
        test_office = Dojo()
        test_office.create_room("Office", ["Spider", "Spongy", "Sweety"])
        self.assertTrue("Spider" in test_office.offices)
        self.assertTrue("Spongy" in test_office.offices)
        self.assertTrue("Sweety" in test_office.offices)
        self.assertFalse("Joginder" in test_office.offices)

    def test_create_living_space_successfully(self):
        test_living_space = Dojo()
        test_living_space.create_room("Living-space", ["Stingy"])
        self.assertTrue("Stingy" in test_living_space.living_spaces)

    def test_create_multiple_living_space_successfully(self):
        test_living_space = Dojo()
        test_living_space.create_room("Living-space", ["Greenie", "Japan", "Carlifonia"])
        self.assertTrue("Greenie" in test_living_space.living_spaces)
        self.assertTrue("Japan" in test_living_space.living_spaces)
        self.assertTrue("Carlifonia" in test_living_space.living_spaces)
        self.assertFalse("Joginder" in test_living_space.living_spaces)

    def test_raise_error_on_duplicate_room(self):
        with self.assertRaises(ValueError):
            test_office = Dojo()
            test_office.create_room("Office", "Spooky")

class TestPersons(unittest.TestCase):

    def test_add_new_fellow_successfully(self):
        test_fellow = Dojo()
        test_fellow.add_new_member("Fellow", "Brian Mukopi")
        self.assertTrue("Brian Mukopi" in test_fellow.fellows)
        self.assertFalse("Maraiah Wairimu" in test_fellow.fellows)

    def test_add_new_staff_successfully(self):
        test_staff = Dojo()
        test_staff.add_new_member("Staff", "Janathan Wanjala")
        self.assertTrue("Janathan Wanjala" in test_staff.staff)
        self.assertFalse("Maraiah Wairimu" in test_staff.staff)

    
    def test_raise_error_on_duplicate_persons(self):
        with self.assertRaises(ValueError):
            test_fellow = Dojo()
            test_fellow.add_new_member("Fellow", "Jonathan Swift")
    
                    

if __name__ == "__main__":
    unittest.main()
