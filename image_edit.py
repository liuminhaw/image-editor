#!/usr/bin/python

"""
# Program:
#    Make simple image modification
# Author
#    haw
# Exit Code:
#    13 - Fail _input_check
#    15 - Fail _file_exist_check
#    17 - Fail _file_format_check
#    19 - Fail _directory_exist_check
#    21 - Fail _quality_check
#    23 - Fail _proportion_check
#    25 - Fail _compress_image
#    27 - Fail _resize_image
"""

import sys, os
from PIL import Image

import logging_class


FILETYPE = ('.jpg', '.jpeg', '.png')

logger = logging_class.PersonalLog('image_modify')


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



def main():
    message = \
    """
    USAGE:
        image_modify compress INPUTFILE OUTPUTFILE [QUALITY]
        image_modify resize INPUTFILE OUTPUTFILE [PROPORTION]
        image_modify dir-compress INPUTDIR OUTPUTDIR [QUALITY]
        image_modify dir-resize INPUTDIR OUTPUTDIR [PROPORTION]
    """
    if len(sys.argv) == 1:
        print(message)
        sys.exit(1)
    elif sys.argv[1] == 'compress':
        image_compress()
    elif sys.argv[1] == 'resize':
        image_resize()
    elif sys.argv[1] == 'dir-compress':
        image_dir_compress()
    elif sys.argv[1] == 'dir-resize':
        image_dir_resize()
    else:
        print(message)


def image_compress():
    message = \
    """
    USAGE:
        image_modify compress INPUTFILE OUTPUTFILE [QUALITY]
    NOTE:
        QUALITY should be between 1 to 95
        Default value is 75 if not specified
    """
    FILETYPE = ('.jpg', '.jpeg')

    # Input validation
    input_file, output_file = _input_check(message, file=True)

    # Test if input file exist
    _file_exist_check(input_file)

    # Test if image is jpg file
    _file_format_check(input_file, FILETYPE)

    # Test if output directory exist
    _directory_exist_check(output_file)

    # Test quality value
    compress_quality = _quality_check()

    # Compress image
    _compress_image(input_file, output_file, compress_quality)



def image_resize():
    message = \
    """
    USAGE:
        image_modify resize INPUTFILE OUTPUTFILE [PROPORTION]
    NOTE:
        PROPORTION will devide the origin image width and height by the value
        Default value for PROPORTION is 2 if not specified
    """

    # Input validation
    input_file, output_file = _input_check(message)

    # Test input file
    _file_exist_check(input_file)

    # Test file format
    _file_format_check(input_file, FILETYPE)

    # Test output directory
    _directory_exist_check(output_file)

    # Test proportion
    proportion = _proportion_check()

    # Resize image
    _resize_image(input_file, output_file, proportion)


def image_dir_compress():
    message = \
    """
    USAGE:
        image_modify dir-compress INPUTDIR OUTPUTDIR [QUALITY]
    NOTE:
        QUALITY should be between 1 to 95
        Default value of QUALITY is 75 if not specified
    """
    FILETYPE = ('.jpg', '.jpeg')

    # Input validation (commandline argument)
    input_dir, output_dir = _input_check(message, file=False)

    # Test if input directory exist
    _directory_exist_check(input_dir)

    # Create output directory if not already exist
    os.makedirs(output_dir.dir, exist_ok=True)

    # Test quality value
    compress_quality = _quality_check()

    # Iterate through files in directory
    for file_object in input_dir.iterate_files():
        # Check file format
        if not file_object.format_check(FILETYPE):
            logger.info('Skipped file {}.'.format(file_object.base))
            continue

        # Define output file
        new_filename = file_object.file_name + '-Compressed' + file_object.file_extension
        output_file = File(os.path.join(output_dir.dir, new_filename))

        # Check output_file existence
        if output_file.file_exist():
            logger.info('Skip file {} that already exist.'.format(output_file.abs))
            continue

        # Compress
        _compress_image(file_object, output_file, compress_quality)


def image_dir_resize():
    message = \
    """
    USAGE:
        image_modify dir-resize INPUTDIR OUTPUTDIR [PROPORTION]
    NOTE:
        PROPORTION will divide the origin image width and height by the value
        Default value for PROPORTION is 2 if not specified
    """

    # Input validation (Commandline arguments)
    input_dir, output_dir = _input_check(message, file=False)

    # Test if input directory exist
    _directory_exist_check(input_dir)

    # Create output directory if not already exist
    os.makedirs(output_dir.dir, exist_ok=True)

    # Test Proportion value
    proportion = _proportion_check()

    # Iterate through files in directory
    for file_object in input_dir.iterate_files():
        # Check file format
        if not file_object.format_check(FILETYPE):
            logger.info('Skipped file {}.'.format(file_object.base))
            continue

        # Define output file
        new_filename = file_object.file_name + '-Resized' + file_object.file_extension
        output_file = File(os.path.join(output_dir.dir, new_filename))

        # Check output_file existence
        if output_file.file_exist():
            logger.info('Skip file {} that already exist.'.format(output_file.abs))
            continue

        # Resize
        _resize_image(file_object, output_file, proportion)


def _input_check(message, file=True):
    """
    Check program input arguments

    Input:
        message - String
        file - Boolean (True if file, False if directory)
    """

    try:
        if file:
            input = File(sys.argv[2])
            output = File(sys.argv[3])
        else:
            input = Directory(sys.argv[2])
            output = Directory(sys.argv[3])
    except IndexError:
        print(message)
        sys.exit(13)

    return (input, output)


def _file_exist_check(file):
    """
    Check input file existence

    Input:
        file - File class object
    """

    if not file.file_exist():
        logger.warning('Source file {} does not exist.'.format(file.abs))
        sys.exit(15)


def _directory_exist_check(file_dir):
    """
    Check output directory existence

    Input:
        dir - File class object or Directory class object
    """

    if not file_dir.dir_exist():
        logger.warning('Directory {} does not exist.'.format(file_dir.dir))
        sys.exit(19)


def _file_format_check(file, formats):
    """
    Check input file format

    Input:
        file - File class object
        formats - tuple of file formats
    """

    if not file.format_check(formats):
        logger.warning('Source file format not in {}.'.format(' '.join(formats)))
        sys.exit(17)


def _quality_check():
    """
    Get input quality value

    Return:
        quality - Integer
    """
    try:
        quality = int(sys.argv[4])
        if quality < 1 or quality > 95:
            raise Warning
    except ValueError:
        logger.info('QUALITY should be numeric value.')
        sys.exit(21)
    except Warning:
        logger.info('QUALITY value should be betweeb 1 to 95.')
        sys.exit(21)
    except:
        quality = 75

    return quality


def _proportion_check():
    """
    Get input proportion value

    Return:
        proportion - Integer
    """

    try:
        proportion = int(sys.argv[4])
        if proportion <= 0:
            raise Warning
    except ValueError:
        logger.info('PROPORTION should be numeric value.')
        sys.exit(23)
    except Warning:
        logger.info('PROPORTION should be positive integer.')
        sys.exit(23)
    except:
        proportion = 2

    return proportion


def _compress_image(input_file, output_file, quality):
    """
    Compress input_file and save to output_file

    Input:
        input_file - File class object
        output_file - File class object
        quality - Integer
    """

    try:
        with Image.open(input_file.abs) as image_file:
            image_file.save(output_file.abs, quality=quality)
        logger.info('Compress image {} success.'.format(input_file.abs))
    except:
        logger.warning('Failed to compress image {}.'.format(intput_file.abs))
        sys.exit(25)


def _resize_image(input_file, output_file, proportion):
    """
    Resize input_file width and height divide by proportion

    Input:
        input_file - File class object
        output_file - File class object
        proportion - Integer
    """

    try:
        with Image.open(input_file.abs) as image_file:
            width, height = image_file.size
            new_image_file = image_file.resize((width // proportion, height // proportion))
            new_image_file.save(output_file.abs, quality=100)
            logger.info('Resize image {} success.'.format(input_file.abs))
    except:
        logger.warning('Failed to resize image {}.'.format(input_file.abs))
        sys.exit(27)


if __name__ == '__main__':
    main()
