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
#    29 - Fail _file_verify
"""

import sys, os
from PIL import Image

from image_editor_pkg import logging_class
from image_editor_pkg import block_class as blkcl


FILETYPE = ('.jpg', '.jpeg', '.png')

logger = logging_class.PersonalLog('image_editor')


def main():
    message = \
    """
    USAGE:
        image_edit.py compress INPUTFILE OUTPUTFILE [QUALITY]
        image_edit.py resize INPUTFILE OUTPUTFILE [PROPORTION]
        image_edit.py dir-compress INPUTDIR OUTPUTDIR [QUALITY]
        image_edit.py dir-resize INPUTDIR OUTPUTDIR [PROPORTION]
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
        image_edit.py compress INPUTFILE OUTPUTFILE [QUALITY]
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

    # Verify image file not corrupted
    _file_verify(input_file)

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
        image_edit.py resize INPUTFILE OUTPUTFILE [PROPORTION]
    NOTE:
        PROPORTION will devide the origin image width and height by the value
        Default value for PROPORTION is 2 if not specified
    """

    # Input validation
    input_file, output_file = _input_check(message, file=True)

    # Test input file
    _file_exist_check(input_file)

    # Test file format
    _file_format_check(input_file, FILETYPE)

    # Verify image file not corrupted
    _file_verify(input_file)

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
        image_edit.py dir-compress INPUTDIR OUTPUTDIR [QUALITY]
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
        output_file = blkcl.File(os.path.join(output_dir.dir, new_filename))

        # Check output_file existence
        if output_file.file_exist():
            logger.info('Skip file {} that already exist.'.format(output_file.abs))
            continue

        # Verify image file not corrupted
        _file_verify(file_object)

        # Compress
        _compress_image(file_object, output_file, compress_quality)


def image_dir_resize():
    message = \
    """
    USAGE:
        image_edit.py dir-resize INPUTDIR OUTPUTDIR [PROPORTION]
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
        output_file = blkcl.File(os.path.join(output_dir.dir, new_filename))

        # Check output_file existence
        if output_file.file_exist():
            logger.info('Skip file {} that already exist.'.format(output_file.abs))
            continue

        # Verify image file not corrupted
        _file_verify(file_object)

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
            input = blkcl.File(sys.argv[2])
            output = blkcl.File(sys.argv[3])
        else:
            input = blkcl.Directory(sys.argv[2])
            output = blkcl.Directory(sys.argv[3])
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


def _file_verify(file):
    """
    Check input file image not corrupted

    Input:
        file - File class object
    """

    try:
        with Image.open(file.abs) as image_file:
            image_file.verify()
    except:
        logger.warning('Image {} corrupted.'.format(file.abs))
        sys.exit(29)


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
