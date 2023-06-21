import unittest

from utils import (
    check_if_short_text,
    check_if_table,
    starts_with_figure_number,
    starts_with_table_number,
)


class TestUtils(unittest.TestCase):
    def test_check_if_table(self):
        # Test case 1: Valid table with more than 1 row of numbers
        table1 = "1\n2\n3\n"
        self.assertTrue(check_if_table(table1))

        # Test case 2: Invalid table with only 1 row of numbers
        table2 = "1\n"
        self.assertFalse(check_if_table(table2))

        # Test case 3: Invalid table with no numbers
        table3 = "abc\ndef\n"
        self.assertFalse(check_if_table(table3))

        # Test case 4: Valid table with numbers and other characters
        table4 = "1\n2\n3\nabc\n"
        self.assertTrue(check_if_table(table4))

    def test_starts_with_figure_number(self):
        # Test case 1: String starts with "Figure :"
        string1 = "Figure 1: This is a figure description."
        self.assertFalse(starts_with_figure_number(string1))

        # Test case 2: String does not start with "Figure :"
        string2 = "This is not a figure description."
        self.assertTrue(starts_with_figure_number(string2))

        # Test case 3: Empty string
        string3 = ""
        self.assertTrue(starts_with_figure_number(string3))

    def test_starts_with_table_number(self):
        # Test case 1: String starts with "Table :"
        string1 = "Table 1: This is a table description."
        self.assertFalse(starts_with_table_number(string1))

        # Test case 2: String does not start with "Table :"
        string2 = "This is not a table description."
        self.assertTrue(starts_with_table_number(string2))

        # Test case 3: Empty string
        string3 = ""
        self.assertTrue(starts_with_table_number(string3))

    def test_check_if_short_text(self):
        # Test case 1: Text with less than 2 short lines
        text1 = "This is a short line.\nAnother short line.\n"
        self.assertTrue(check_if_short_text(text1))

        # Test case 2: Text with 1 short line
        text2 = "This is a short line. Another short line.Yet another short.\n"
        self.assertTrue(check_if_short_text(text2))

        # Test case 3: Text with more than 3 short lines
        text3 = "The.\nAnoe.\nYet t \
            line.\nAnd another short line.\n"
        self.assertFalse(check_if_short_text(text3))

        # Test case 4: Empty text
        text4 = ""
        self.assertTrue(check_if_short_text(text4))


if __name__ == "__main__":
    unittest.main()