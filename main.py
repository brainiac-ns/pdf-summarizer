import re
import fitz

doc = fitz.open("data/input.pdf")


def whole_row_is_not_number(string):
    counter = 0
    for word in string.split("\n"):
        try:
            float(word)
            counter += 1
        except Exception:
            continue
    return counter > 1


def starts_with_figure_number(string):
    pattern = r"^Figure \d+"
    match1 = re.match(pattern, string.split("\n")[0])
    return match1 is None


def starts_with_table_number(string):
    pattern = r"^Table \d+:"
    match1 = re.match(pattern, string)
    return match1 is None


def check_if_not_text(text):
    total = 0
    for lines in text.split("\n"):
        if len(lines) < 10:
            total += 1

    return total < 3


def f():
    for page in doc:
        output = page.get_text("blocks")
        for block in output:
            a = [i for i in block[4].split("\n") if i != ""]
            if len(a) == 1:
                continue

            if "References" in block[4] or "Acknowledgements" in block[4]:
                return
            elif (
                len(block[4]) > 100
                and "∗" not in block[4]
                and check_if_not_text(block[4])
                and starts_with_figure_number(block[4])
                and starts_with_table_number(block[4])
            ):
                print(block[4])
                print("-" * 10)
            else:
                try:
                    if whole_row_is_not_number(block[4]):
                        continue
                    int(block[4][0])
                    print(block[4])
                    print("-" * 20)
                except Exception:
                    continue


f()
