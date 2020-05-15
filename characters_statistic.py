# A programme which takes in a zipped txt file, unzips it and then
# collect statistic of appearance for each alphabetic character in the text.
# The results are printed out to the console.

import collections
import pathlib
from operator import itemgetter
from pprint import pprint
from zipfile import ZipFile

zipped_file = pathlib.Path.cwd() / "char_stat_voyna-i-mir.txt.zip"


class Statistics:
    sort_key = itemgetter(1)
    reverse_key = True

    def __init__(self, work_file):
        self.total = 0
        self.work_file = work_file
        self.stats_dict = collections.defaultdict(int)
        self.stats_list = []

    def to_unzip_a_file(self, new_file):
        open_zip_file = ZipFile(new_file, "r")
        for file_to_extract in open_zip_file.namelist():
            open_zip_file.extract(file_to_extract)
            self.work_file = file_to_extract

    def to_collect_stats(self):
        with open(self.work_file, "r", encoding="cp1251") as work_file:
            for line in work_file:
                self.char_adding(line)

    def char_adding(self, line):
        for char in line:
            if char.isalpha():
                self.stats_dict[char] += 1

    def to_extract_stats_from_dict(self):
        for key, value in self.stats_dict.items():
            self.stats_list.append([key, value])

    def to_sort_the_results(self):
        self.stats_list = sorted(self.stats_list, key=self.sort_key, reverse=self.reverse_key)

    def to_print_the_results(self):
        txt1 = "буква"
        txt2 = "частота"
        txt3 = "итого"
        print(
            "+" + 9 * "-" + "+" + 10 * "-" + "+" + "\n" +
            f"|{txt1:^9}" + "|" + f"{txt2:^10}|" + "\n" +
            "+" + 9 * "-" + "+" + 10 * "-" + "+"
        )
        for element in self.stats_list:
            print(f"|{element[0]:^9}" + "|" + f"{element[1]:^10}|")
            self.total += element[1]
        print(
            "+" + 9 * "-" + "+" + 10 * "-" + "+" + "\n" +
            f"|{txt3:^9}" + "|" + f"{self.total:^10}|" + "\n" +
            "+" + 9 * "-" + "+" + 10 * "-" + "+" + "\n"
        )


class StatisticsFrequencyAscending(Statistics):
    reverse_key = False


class StatisticsAlphabeticDescending(Statistics):
    sort_key = itemgetter(0)


class StatisticsAlphabeticAscending(Statistics):
    sort_key = itemgetter(0)
    reverse_key = False


def to_execute_statics_collector(file):
    options = {
        "1": Statistics,
        "2": StatisticsFrequencyAscending,
        "3": StatisticsAlphabeticDescending,
        "4": StatisticsAlphabeticAscending
    }

    pprint(options)

    while True:
        user_input = input("Выберите класс, введите цифру: ")
        if user_input in options:
            break

    collector = options[user_input](file)
    collector.to_unzip_a_file(collector.work_file)
    collector.to_collect_stats()
    collector.to_extract_stats_from_dict()
    collector.to_sort_the_results()
    collector.to_print_the_results()


to_execute_statics_collector(zipped_file)
