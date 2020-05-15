# A little workshop on raising and handling exceptions. The following function reg_entries_checker
# takes in a txt file with lines of registrations entries. An entry consist of name, email and age.
# The function checks out whether a line doesn't have a name with numbers (only alphabetic characters),
# or line's email missing characters "@" and "." or the age integer in line goes out of the range between 10 and 100.
# After analyzing the function write out 2 log files, one for bad entries, the other for good.

import pathlib


class CustomError(Exception):
    pass


class NotNameError(CustomError):
    pass


class NotEmailError(CustomError):
    pass


def reg_entries_checker(file_in):
    with open(file_in, "r", encoding="utf8") as file, \
         open("registrations_bad.log", "w", encoding="utf8") as bads, \
         open("registrations_good.log", "w", encoding="utf8") as goods:
        for line in file:
            try:
                reg_line = line.strip().split(" ")
                if len(reg_line) < 3:
                    raise ValueError("В записе не три элемента.")
                elif not reg_line[0].isalpha():
                    raise NotNameError("В имени есть цифры.")
                elif "@" not in reg_line[1] or "." not in reg_line[1]:
                    raise NotEmailError("В эмейле не хватает символов.")
                elif int(reg_line[2]) not in range(10, 100):
                    raise ValueError("Возраст не в диапазоне.")
                else:
                    goods.write(f"{reg_line}\n")
            except ValueError as exc1:
                print("Битая запись...")
                bads.write(f"{reg_line} - {ValueError.__name__} - {exc1.args}\n")
                continue
            except CustomError as exc2:
                print("Битая запись...")
                bads.write(f"{reg_line} - {CustomError.__name__} - {exc2.args}\n")
                continue


file_name = "registrations.txt"
file_path = pathlib.Path.cwd() / "registrations.txt"

reg_entries_checker(file_name)