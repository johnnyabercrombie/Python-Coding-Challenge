"""
LH Ventures Python Coding Challenge Unit Tests
"""

from contextlib import redirect_stdout
from datetime import datetime
import io
import unittest
from unittest import TestCase

from main import _clean_filter_values, display_table


class TestMain(TestCase):

    def test_clean_filter_values_no_input(self):
        with self.assertRaises(ValueError):
            _clean_filter_values("")

    def test_clean_filter_values_with_invalid_price_min(self):
        with self.assertRaises(ValueError):
            _clean_filter_values("i * * *")

    def test_clean_filter_values_with_invalid_price_max(self):
        with self.assertRaises(ValueError):
            _clean_filter_values("* i * *")

    def test_clean_filter_values_with_invalid_expires_start(self):
        with self.assertRaises(ValueError):
            _clean_filter_values("* * i *")

    def test_clean_filter_values_with_invalid_expires_end(self):
        with self.assertRaises(ValueError):
            _clean_filter_values("* * * i")

    def test_clean_filter_values_with_invalid_values(self):
        with self.assertRaises(ValueError):
            _clean_filter_values("i i i i")

    def test_clean_filter_values_with_missing_values(self):
        with self.assertRaises(ValueError):
            _clean_filter_values("* *")

    def test_clean_filter_values_with_too_many_values(self):
        with self.assertRaises(ValueError):
            _clean_filter_values("* * * * * *")

    def test_clean_filter_values_with_valid_price_min(self):
        price_min, price_max, exp_start, exp_stop = _clean_filter_values("3.0 * * *")
        self.assertEqual(3.0, price_min)
        self.assertEqual('*', price_max)
        self.assertEqual('*', exp_start)
        self.assertEqual('*', exp_stop)

    def test_clean_filter_values_with_valid_price_max(self):
        price_min, price_max, exp_start, exp_stop = _clean_filter_values("* 3.0 * *")
        self.assertEqual('*', price_min)
        self.assertEqual(3.0, price_max)
        self.assertEqual('*', exp_start)
        self.assertEqual('*', exp_stop)

    def test_clean_filter_values_with_valid_expires_start(self):
        price_min, price_max, exp_start, exp_stop = _clean_filter_values("* * JUL-01-2019 *")
        self.assertEqual('*', price_min)
        self.assertEqual('*', price_max)
        self.assertEqual(datetime(2019, 7, 1), exp_start)
        self.assertEqual('*', exp_stop)

    def test_clean_filter_values_with_valid_expires_end(self):
        price_min, price_max, exp_start, exp_stop = _clean_filter_values("* * * JUL-01-2019")
        self.assertEqual('*', price_min)
        self.assertEqual('*', price_max)
        self.assertEqual('*', exp_start)
        self.assertEqual(datetime(2019, 7, 1), exp_stop)

    def test_clean_filter_values_with_valid_values(self):
        price_min, price_max, exp_start, exp_stop = _clean_filter_values("2.0 3.0 JUN-01-2019 JUL-01-2019")
        self.assertEqual(2.0, price_min)
        self.assertEqual(3.0, price_max)
        self.assertEqual(datetime(2019, 6, 1), exp_start)
        self.assertEqual(datetime(2019, 7, 1), exp_stop)

    def test_display_table_with_valid_values(self):
        std_output = io.StringIO()
        with redirect_stdout(std_output):
            display_table("2.0 3.0 JUN-01-2019 JUL-01-2019")

        std_output_string = std_output.getvalue()
        self.assertIn('Curry Powder', std_output_string)
        self.assertIn('2.47', std_output_string)
        self.assertIn('06/13/2019', std_output_string)

        self.assertIn('Halibut - Steaks', std_output_string)
        self.assertIn('2.67', std_output_string)
        self.assertIn('06/14/2019', std_output_string)

        self.assertNotIn('Bread Crumbs - Panko', std_output_string)
        self.assertNotIn('1.71', std_output_string)
        self.assertNotIn('04/16/2019', std_output_string)

        self.assertNotIn('Chicken - Ground', std_output_string)
        self.assertNotIn('1.39', std_output_string)
        self.assertNotIn('10/26/2019', std_output_string)

    def test_display_table_with_valid_values_and_wildcards(self):
        std_output = io.StringIO()
        with redirect_stdout(std_output):
            display_table("4.0 * * JUL-01-2019")

        std_output_string = std_output.getvalue()
        self.assertIn('Wasabi Powder', std_output_string)
        self.assertIn('4.95', std_output_string)
        self.assertIn('03/08/2019', std_output_string)

        self.assertIn('Beans - Soya Bean', std_output_string)
        self.assertIn('4.39', std_output_string)
        self.assertIn('02/18/2019', std_output_string)

        self.assertNotIn('Truffle Cups - Brown', std_output_string)
        self.assertNotIn('1.04', std_output_string)
        self.assertNotIn('12/22/2019', std_output_string)

        self.assertNotIn('Mackerel Whole Fresh', std_output_string)
        self.assertNotIn('3.98', std_output_string)
        self.assertNotIn('07/25/2019', std_output_string)


if __name__ == '__main__':
    unittest.main()
