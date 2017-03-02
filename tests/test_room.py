"""This is a module that will test for the integrity of the "room" module
specifically the LivingSpace and the Office Classes 
"""
import unittest
from room import  LivingSpace, Office

class TestRooms(unittest.TestCase):
    """ This class has got two methods that have got a similar 
    approach but test different features. The test_living_space
    method tests whether an item created by instatiating the 
    LivingSpace will be an instance of of the LivingSpace class.
    It also asserts that the item created is NOT an object of 
    the Office class. The test_office_inheritance method applies 
    the same logic but to the Office class.
    """

    def test_livingspace_inheritance(self):
        test_living_space = LivingSpace("Restplace")
        self.assertTrue(isinstance(test_living_space, LivingSpace))
        self.assertTrue(test_living_space.date_created)
        self.assertFalse(isinstance(test_living_space, Office))

    def test_office_inheritance(self):
        test_office = Office("Workplace")
        self.assertTrue(isinstance(test_office, Office))
        self.assertEqual(test_office.occupants, [])
        self.assertFalse(isinstance(test_office, LivingSpace))
          
if __name__ == "__main__":
    unittest.main()
