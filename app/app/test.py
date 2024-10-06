from django.urls import reverse 
from django.test import SimpleTestCase
from app import calc

class CalcTest(SimpleTestCase):
    """_summary_
    Test the calc module.
    """
    def test_add_numbers(self):
        res = calc.add(5,2)
        self.assertEqual(res, 7)
        
        
        
    def test_subtract_numbers(self):
        """
           Subtract numbers
        """
        res = calc.subtract(5,2)
        self.assertEqual(res, 3)