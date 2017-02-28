import unittest
from models import Room

class TestCreateRoom(unittest.TestCase):

    def test_create_room_successfully(self):
        room = Room("Office", "Spooky")
        initial_room_count = len(room.all_rooms())
        room.create_room()
        new_room_count = len(room.all_rooms())
        self.assertTrue("Spooky" in room.all_rooms() and new_room_count - initial_room_count == 1 )

    def test_raise_eeror_on_duplicate_room(self):
    	with self.assertRaises(ValueError):
    		room_2 = Room("Office", "Spooky")
    		room_2.create_room()





if __name__ == "__main__":
    unittest.main()
