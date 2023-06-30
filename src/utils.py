import re
import textwrap
from typing import Dict, List

import fitz
from reportlab.pdfgen import canvas


def check_if_table(string: str) -> bool:
    """
    Checks if the paragraph is a table
    (if it contains more than 1 row with just numbers)

    Args:
        string (str): Input paragraphs

    Returns:
        bool: True if paragraph is a table, False otherwise
    """
    counter = 0
    for word in string.split("\n"):
        try:
            float(word)
            counter += 1
        except Exception:
            continue
    return counter > 1


def starts_with_figure_number(string: str) -> bool:
    """
    Checks if string starts with Figure :

    Args:
        string (str): Input string

    Returns:
        bool: True if string starts with Figure :, False otherwise
    """
    pattern = r"^Figure \d+:"
    match1 = re.match(pattern, string)
    return match1 is None


def starts_with_table_number(string: str) -> bool:
    """
    Checks if string starts with table:

    Args:
        string (str): Input string

    Returns:
        bool: True if string starts with Table :, False otherwise
    """
    pattern = r"^Table \d+:"
    match1 = re.match(pattern, string)
    return match1 is None


def check_if_short_text(text: str) -> bool:
    """
    Checks if text is short

    Args:
        text (str): Input text

    Returns:
        bool: True if text is short, False otherwise
    """
    total = 0
    for lines in text.split("\n"):
        if len(lines) < 10:
            total += 1
    return total < 3


def write_list_to_pdf(strings: Dict[str, str], path_to_pdf: str = "uploads/output.pdf"):
    """
    Renders text to pdf
    Args:
        strings (str): List of paragraphs
        path_to_pdf (str, optional): Path to pdf.
    """

    c = canvas.Canvas(path_to_pdf)
    c.setFontSize(10)
    y = 800
    items_num = 0
    max_line_length = 120
    for string in strings:
        string = string.replace("\n", " ")
        if len(string) > max_line_length:
            wrapped_lines = textwrap.wrap(string, width=max_line_length)
            for wrapped_line in wrapped_lines:
                c.drawString(20, y, wrapped_line)
                y -= 20
                items_num += 1
                if items_num == 40:
                    c.showPage()
                    c.setFontSize(10)
                    y = 800
                    items_num = 0
        else:
            c.drawString(20, y, wrapped_line)
            y -= 20
            items_num += 1
            if items_num == 40:
                c.showPage()
                c.setFontSize(10)
                y = 800
                items_num = 0

    c.save()


def extract_text(path_to_pdf: str = "data/input.pdf") -> List[str]:
    """
    Extracts text from pdf

    Args:
        path_to_pdf (str, optional): Path to pdf. Defaults to "data/input.pdf".

    Returns:
        List[str]: List of paragraphs
    """
    extracted_text = []
    doc = fitz.open(path_to_pdf)
    for page in doc:
        output = page.get_text("blocks")
        for block in output:
            a = [i for i in block[4].split("\n") if i != ""]
            if len(a) == 1:
                continue

            if (
                "References" in block[4]
                or "Acknowledgements" in block[4]
                or "Conclusion" in block[4]
            ):
                return extracted_text
            elif (
                len(block[4]) > 100
                and "∗" not in block[4]
                and check_if_short_text(block[4])
                and starts_with_figure_number(block[4])
                and starts_with_table_number(block[4])
            ):
                extracted_text.append(block[4])
            else:
                try:
                    if check_if_table(block[4]):
                        continue
                    int(block[4][0])
                    extracted_text.append(block[4])
                except Exception:
                    continue

    return extracted_text
