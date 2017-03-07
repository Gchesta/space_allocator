import sys
from io import StringIO
import unittest
from dojo import Dojo

class Case(unittest.TestCase):

    def setUp(self):
        self.dojo = Dojo()
    
    def test_print_names_of_people_in_room(self):
        self.dojo.create_room("Nairobi", "Office")
        self.dojo.add_person("fellow", "ernest", "achesa", "N")
        self.dojo.add_person("staff", "george", "wanjala")
        old_stdout = sys.stdout
        temp = StringIO()
        sys.stdout = temp
        #call functions
        self.dojo.print_room("Nairobi")
        #end functions
        sys.stdout = old_stdout
        output = temp.getvalue()
        expected_output = "Ernest Achesa\nGeorge Wanjala\n"
        self.assertEqual(output, expected_output)

    """def test_print_allocations_on_screen(self):
        self.dojo.create_room("Nairobi", "Office")
        self.dojo.create_room("Chetambe", "livingspace")
        self.dojo.add_person("fellow", "ernest", "achesa", "Y")
        self.dojo.add_person("staff", "george", "wanjala")
        old_stdout = sys.stdout
        temp = StringIO()
        sys.stdout = temp
        #call functions
        self.dojo.print_allocations()
        #end functions
        sys.stdout = old_stdout
        output = temp.getvalue()
        expected_output = "\nName\t\t\tAllocated Office\tAllocated Living Space\nErnest Achesa\t\tNairobi\t\t\tChetambe\nGeorge Wanjala\t\tNairobi\n"
        self.assertEqual(output, expected_output)"""

if __name__ == "__main__":
    unittest.main()
