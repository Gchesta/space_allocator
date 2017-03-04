"""This is a module that will test for the integrity of the "person" 
module specifically the Fellow and the Staff Classes 
"""
import unittest
from person import  Fellow, Staff

class TestPersons(unittest.TestCase):
    """ This class has got two methods that have got a similar 
    approach but test different features. The test_fellow_iheritannce
    method tests whether an item created by instatiating the 
    Fellow will be an instance of the Fellow class.
    It also asserts that the item created is NOT an object of 
    the Staff class. The test_staff_inheritance method applies 
    the same logic but to the Staff class.
    """

    def test_fellow_inheritance(self):
        """Test inheritance on class Fellow"""

        test_fellow = Fellow("Bush Nyongesa", "Workplace", "Restplace")
        self.assertTrue(isinstance(test_fellow, Fellow))
        self.assertEqual(test_fellow.full_name, "Bush Nyongesa")
        self.assertFalse(isinstance(test_fellow, Staff))

    def test_staff_inheritance(self):
         """Test inheritance on class Staff"""

         test_staff = Staff("Jerome Steel", "Workhorse")
         self.assertTrue(isinstance(test_staff, Staff))
         self.assertEqual(test_staff.office, "Workhorse")
         self.assertFalse(isinstance(test_staff, Fellow))
          
if __name__ == "__main__":
    unittest.main()
