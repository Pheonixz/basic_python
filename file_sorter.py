# Another simple program written in object oriented style. It purpose to take in a dir
# or a dir of dirs a zip full of some files, arrange the files by years and months and
# then write out arranged files to newly created dirs.


import os
import pathlib
import shutil
import time
import zipfile
from datetime import datetime


class Sorter:

    def __init__(self, in_dir, out_dir):
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.file_paths = []
        self.files = {}

    def to_get_the_file_timestamp(self):
        self.to_get_the_file_path()
        for file in self.file_paths:
            file_struct_time = time.gmtime(os.path.getmtime(file))
            file_timestamp = time.strftime("%Y %m", file_struct_time)
            self.files[file] = file_timestamp

    def to_get_the_file_path(self):
        for path_name, dir_name, file_list in os.walk(self.in_dir):
            for file in file_list:
                file_path = os.path.join(path_name, file)
                self.file_paths.append(file_path)

    def to_sort_photos(self):
        for key, value in self.files.items():
            file_and_path = self.to_create_file_paths(key, value[:4], value[5:7])
            shutil.move(file_and_path[0], file_and_path[1])

    def to_create_file_paths(self, element, path_piece1, path_piece2):
        dir_path = os.path.normpath(os.path.join(self.out_dir, path_piece1, path_piece2))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return [element, dir_path]

    def to_execute_a_sorter(self):
        self.to_get_the_file_timestamp()
        self.to_sort_photos()


class SorterV2(Sorter):

    def __init__(self, in_dir, out_dir):
        super().__init__(in_dir, out_dir)
        self.filename = None
        self.file_to_extract = None

    def to_sort_out_a_zipped_file(self, zfile):
        for member in zfile.namelist():
            self.file_to_extract = zfile.getinfo(member)

            if not self.file_to_extract.is_dir():
                file_to_move = self.to_move_a_file(member, zfile)
                self.to_return_original_timestamp(file_to_move[0], file_to_move[1])

    def to_move_a_file(self, member, zfile):
        file_timestamp = self.to_set_file_properties(member, self.file_to_extract)
        dir_path = self.to_create_file_paths(None, self.file_to_extract[0], self.file_to_extract[1])[1]

        self.file_to_extract = zfile.open(member)
        out_dir_path = open(os.path.join(dir_path, self.filename), "wb")

        with self.file_to_extract as source, out_dir_path as target:
            shutil.copyfileobj(source, target)

        return dir_path, file_timestamp

    def to_set_file_properties(self, for_name, for_time):
        self.filename = os.path.basename(for_name)
        file_timestamp = datetime(
            year=for_time.date_time[0], month=for_time.date_time[1], day=for_time.date_time[2],
            hour=for_time.date_time[3], minute=for_time.date_time[4], second=for_time.date_time[5]
        )

        return file_timestamp

    def to_return_original_timestamp(self, dir_path, file_timestamp):
        file_path = os.path.join(dir_path, self.filename)
        new_file_timestamp = time.mktime(file_timestamp.timetuple())
        os.utime(file_path, (new_file_timestamp, new_file_timestamp))

    def to_execute_a_sorter(self):
        if str(self.in_dir).endswith("zip"):
            with zipfile.ZipFile(input_zip, "r") as zfile:
                self.to_sort_out_a_zipped_file(zfile)
        else:
            super().to_execute_a_sorter()


input_zip = pathlib.Path.cwd() / ...
input_dir = pathlib.Path.cwd() / ...
output_dir = pathlib.Path.cwd() / ...

new_sorter = SorterV2(input_dir, output_dir)
new_sorter.to_execute_a_sorter()
