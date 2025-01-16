import unittest
from .date_util import parse_dates, parse_date
from datetime import date


class TestDateUtil(unittest.TestCase):
    def test_parse_dates(self):
        """
        Test the parse_dates function.
        :return:
        """
        # Test with valid dates
        dates = {
            "bill_date": "2021-01-01",
            "bill_period_to": "2021-01-31",
            "date_of_last_payment": "2021-01-31",
            "bill_period_from": "2021-01-01",
        }

        # Test with valid dates
        self.assertEqual(
            parse_dates(dates),
            {
                "bill_date": date(2021, 1, 1),
                "bill_period_to": date(2021, 1, 31),
                "date_of_last_payment": date(2021, 1, 31),
                "bill_period_from": date(2021, 1, 1),
            }
        )

        # Test with invalid dates
        dates = {
            "bill_date": "01-01-2021",
            "bill_period_to": "2021-01-31",
            "date_of_last_payment": "2021-01-31",
            "bill_period_from": "2021-01-01",
        }

        with self.assertRaises(ValueError):
            parse_dates(dates)

    def test_parse_date(self):
        """
        Test the parse_date function.
        :return:
        """
        # Test with valid date
        date_string = "2021-01-01"
        self.assertEqual(parse_date(date_string), date(2021, 1, 1))

        # Test with invalid date
        date_string = "01-01-2021"
        with self.assertRaises(ValueError):
            parse_date(date_string)
