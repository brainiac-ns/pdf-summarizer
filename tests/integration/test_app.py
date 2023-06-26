import unittest
import os
import fitz
import shutil
from utils import extract_text, write_list_to_pdf


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data_dir = "test_data"
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        os.mkdir(self.test_data_dir)

    def test_integration(self) -> None:
        extracted = extract_text("integration/test_data/input.pdf")
        extracted_text = extracted[0]
        expected_text = "The dominant sequence tran"
        self.assertIn(expected_text, extracted_text)
        strings = [extracted_text]

        output_pdf_path = os.path.join(self.test_data_dir, "integration_test.pdf")
        write_list_to_pdf(strings, output_pdf_path)
        self.assertTrue(os.path.exists(output_pdf_path))
        self.assertGreater(os.path.getsize(output_pdf_path), 0)
        doc = fitz.open(output_pdf_path)
        extracting_text = []
        for page in doc:
            extracting_text.append(page.get_text().replace('\n', ''))
        doc.close()
        print(strings[0].replace('\n', ''))
        print(extracting_text[0])
        self.assertEqual(strings[0].replace('\n', '').split()[0], extracting_text[0].split()[0])

    def tearDown(self) -> None:
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
