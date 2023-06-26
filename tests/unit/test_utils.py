import unittest
import os
import fitz

from utils import (
    check_if_short_text,
    check_if_table,
    starts_with_figure_number,
    starts_with_table_number,
    extract_text,
    write_list_to_pdf
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

    def test_write_list_to_pdf(self):
        strings = ["Hello, World! This is a test. Writing to PDF.", "Tomica testing"]
        path_to_pdf = os.path.join(self.test_data_dir, "test_output.pdf")

        write_list_to_pdf(strings, path_to_pdf)
        self.assertTrue(os.path.exists(path_to_pdf))

        self.assertGreater(os.path.getsize(path_to_pdf), 0)

        doc = fitz.open(path_to_pdf)
        extracted_text = []
        for page in doc:
            extracted_text.append(page.get_text())
        for string in strings:
            self.assertIn(string, " ".join(extracted_text))

        doc.close()

    def test_extract_text(self):
        extracted = extract_text("uploads/input.pdf")
        print("Extracted:", extracted[0])
        self.assertIn("The dominant sequence tran", extracted[0])

        


if __name__ == "__main__":
    unittest.main()
