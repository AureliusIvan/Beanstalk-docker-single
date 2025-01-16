import unittest
from .month_util import int_to_month_name


class TestBillingCalculations(unittest.TestCase):
    """
    Test the month utility functions.
    """

    def test_int_to_month_name(self):
        """
        Test the int_to_month_name function.
        :return:
        """
        self.assertEqual(int_to_month_name(1), "January")
        self.assertEqual(int_to_month_name(2), "February")
        self.assertEqual(int_to_month_name(3), "March")
        self.assertEqual(int_to_month_name(4), "April")
        self.assertEqual(int_to_month_name(5), "May")
        self.assertEqual(int_to_month_name(6), "June")
        self.assertEqual(int_to_month_name(7), "July")
        self.assertEqual(int_to_month_name(8), "August")
        self.assertEqual(int_to_month_name(9), "September")
        self.assertEqual(int_to_month_name(10), "October")
        self.assertEqual(int_to_month_name(11), "November")
        self.assertEqual(int_to_month_name(12), "December")
