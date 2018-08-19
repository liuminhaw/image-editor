"""
Program:
    Class of file and directory
Author:
    haw
Version:
    0.1.0
"""


import os


class BlockType():

    def __init__(self,path):
        self.abs = os.path.abspath(path)
        self.dir = os.path.abspath(path)

    def dir_exist(self):
        return os.path.isdir(self.dir)


class Directory(BlockType):

    def __init__(self, path):
        BlockType.__init__(self, path)

        self.base = os.path.basename(self.abs)

    def iterate_files(self):
        """
        Iterates through files in the directory

        Return:
            A File class object
        """
        for file in os.listdir(self.dir):
            filepath = os.path.join(self.dir, file)
            yield File(filepath)


class File(BlockType):

    def __init__(self, path):
        BlockType.__init__(self, path)

        self.dir = os.path.dirname(self.abs)
        self.base = os.path.basename(self.abs)
        self.file_name = os.path.splitext(self.base)[0]
        self.file_extension = os.path.splitext(self.base)[1]

    def file_exist(self):
        return os.path.isfile(self.abs)

    def format_check(self, formats):
        """
        Compare file format to formats

        Input:
            formats - tuple of file formats
        """
        return self.file_extension.lower() in formats
