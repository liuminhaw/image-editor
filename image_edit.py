#!/usr/bin/python

"""
# Program:
#    Make simple image modification
# Author
#    haw
# Exit Code:
#    1 - Program usage syntax error
#    15 - Fail _file_exist_check
#    17 - Fail _file_format_check (FileFormatError)
#    19 - Fail _directory_exist_check
#    21 - Fail _quality_check
#    23 - Fail _proportion_check
#    25 - Fail _compress_image (CompressionError)
#    27 - Fail _resize_image (ResizeError)
#    29 - Fail _file_verify (FileCorruptError)
#    31 - Fail _convert_image (ConversionError)
"""

import sys, os
from PIL import Image

from image_editor_pkg import logging_class
from image_editor_pkg import block_class as blkcl
from image_editor_pkg import exceptions as editor_err


VERSION = 'Version 0.2.0'

FILETYPE = ('.jpg', '.jpeg', '.png')

logger = logging_class.PersonalLog('image_editor')


def main():
    message = \
    """
    USAGE:
        image_edit.py convert INPUTFILE OUTPUTFILE
        image_edit.py compress INPUTFILE OUTPUTFILE [QUALITY]
        image_edit.py resize INPUTFILE OUTPUTFILE [PROPORTION]
        image_edit.py dir-convert INPUTDIR OUTPUTDIR
        image_edit.py dir-compress INPUTDIR OUTPUTDIR [QUALITY]
        image_edit.py dir-resize INPUTDIR OUTPUTDIR [PROPORTION]
        image_edit.py version
    """
    if len(sys.argv) == 1:
        print(message)
        sys.exit(1)
    elif sys.argv[1] == 'convert':
        image_convert()
    elif sys.argv[1] == 'compress':
        image_compress()
    elif sys.argv[1] == 'resize':
        image_resize()
    elif sys.argv[1] == 'dir-convert':
        image_dir_convert()
    elif sys.argv[1] == 'dir-compress':
        image_dir_compress()
    elif sys.argv[1] == 'dir-resize':
        image_dir_resize()
    elif sys.argv[1] == 'version':
        version()
    else:
        print(message)


def image_convert():
    message = \
    """
    USAGE:
        image_edit.py convert INPUTFILE OUTPUTFILE
    """

    # Input validation
    input_file, output_file = _input_check(message, file=True)

    # Test if input file exist
    _file_exist_check(input_file)

    # Verify image file availability
    try:
        _file_verify(input_file)
    except editor_err.FileCorruptError as err:
        logger.info(err)
        sys.exit(29)

    # Test output directory
    _directory_exist_check(output_file)

    # Convert image
    try:
        _convert_image_jpg(input_file, output_file)
    except editor.ConversionError as err:
        logger.info(err)
        sys.exit(31)



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
    try:
        _file_format_check(input_file, FILETYPE)
    except editor_err.FileFormatError as err:
        logger.info(err)
        sys.exit(17)

    # Verify image file not corrupted
    try:
        _file_verify(input_file)
    except editor_err.FileCorruptError as err:
        logger.info(err)
        sys.exit(29)

    # Test if output directory exist
    _directory_exist_check(output_file)

    # Test quality value
    compress_quality = _quality_check()

    # Compress image
    try:
        _compress_image(input_file, output_file, compress_quality)
    except editor_err.CompressionError as err:
        logger.info(err)
        sys.exit(25)



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
    try:
        _file_format_check(input_file, FILETYPE)
    except editor_err.FileFormatError as err:
        logger.info(err)
        sys.exit(17)

    # Verify image file not corrupted
    try:
        _file_verify(input_file)
    except editor_err.FileCorruptError as err:
        logger.info(err)
        sys.exit(29)

    # Test output directory
    _directory_exist_check(output_file)

    # Test proportion
    proportion = _proportion_check()

    # Resize image
    try:
        _resize_image(input_file, output_file, proportion)
    except editor_err.ResizeError as err:
        logger.info(err)
        sys.exit(27)


def image_dir_convert():
    message = \
    """
    USAGE:
        image_edit.py dir-convert INPUTDIR OUTPUTDIR
    """
    # Input validation
    input_dir, output_dir = _input_check(message, file=False)

    # Test directory existence
    _directory_exist_check(input_dir)
    os.makedirs(output_dir.dir, exist_ok=True)

    # Iterate through files
    for file_object in input_dir.iterate_files():
        # Define output file
        new_filename = file_object.file_name + '-Converted.jpeg'
        output_file = blkcl.File(os.path.join(output_dir.dir, new_filename))

        # Check output_file existence
        if output_file.file_exist():
            logger.info('Skip file {} that already exist'.format(output_file.abs))
            continue

        # Convert
        try:
            _convert_image_jpg(file_object, output_file)
        except editor_err.ConversionError as err:
            logger.info(err)
            continue


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
        try:
            _file_format_check(file_object, FILETYPE)
        except editor_err.FileFormatError as err:
            logger.info(err)
            continue

        # Define output file
        new_filename = file_object.file_name + '-Compressed' + file_object.file_extension
        output_file = blkcl.File(os.path.join(output_dir.dir, new_filename))

        # Check output_file existence
        if output_file.file_exist():
            logger.info('Skip file {} that already exist.'.format(output_file.abs))
            continue

        # Verify image file not corrupted
        try:
            _file_verify(file_object)
        except editor_err.FileCorruptError as err:
            logger.info(err)
            continue

        # Compress
        try:
            _compress_image(file_object, output_file, compress_quality)
        except editor_err.CompressionError as err:
            logger.info(err)
            continue


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
        try:
            _file_format_check(file_object, FILETYPE)
        except editor_err.FileFormatError as err:
            logger.info(err)
            continue

        # Define output file
        new_filename = file_object.file_name + '-Resized' + file_object.file_extension
        output_file = blkcl.File(os.path.join(output_dir.dir, new_filename))

        # Check output_file existence
        if output_file.file_exist():
            logger.info('Skip file {} that already exist.'.format(output_file.abs))
            continue

        # Verify image file not corrupted
        try:
            _file_verify(file_object)
        except editor_err.FileCorruptError as err:
            logger.info(err)
            continue

        # Resize
        try:
            _resize_image(file_object, output_file, proportion)
        except editor_err.ResizeError as err:
            logger.info(err)
            continue


def version():
    """
    Show current using version of the program
    """
    print('Current version: {}'.format(VERSION))


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
        sys.exit(1)

    return (input, output)


def _file_exist_check(file):
    """
    Check input file existence

    Input:
        file - File class object
    """

    if not file.file_exist():
        # raise editor_err.FileNotExistError('File {} not exist'.format(file.abs))
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

    Error:
        FileFormatError - Invalid file format
    """
    if not file.format_check(formats):
        raise editor_err.FileFormatError('{} not expected file format - {}'.format(file.abs, ' '.join(formats)))
        # logger.warning('Source file format not in {}.'.format(' '.join(formats)))
        # sys.exit(17)


def _file_verify(file):
    """
    Check input file image not corrupted

    Input:
        file - File class object

    Error:
        FileCorruptError - Invalid file
    """
    try:
        with Image.open(file.abs) as image_file:
            image_file.verify()
    except:
        raise editor_err.FileCorruptError('File {} invalid'.format(file.abs))
        # logger.warning('Image {} corrupted.'.format(file.abs))
        # sys.exit(29)


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

    Error:
        CompressionError - Failed to compress image
    """

    try:
        with Image.open(input_file.abs) as image_file:
            image_file.save(output_file.abs, quality=quality)
        logger.info('Compress image {} success.'.format(input_file.abs))
    except Exception as err:
        logger.warning('Error: {}'.format(err))
        raise editor_err.CompressionError('Failed to compress image {}'.format(input_file.abs))
        # logger.warning('Failed to compress image {}.'.format(intput_file.abs))
        # sys.exit(25)


def _resize_image(input_file, output_file, proportion):
    """
    Resize input_file width and height divide by proportion

    Input:
        input_file - File class object
        output_file - File class object
        proportion - Integer

    Error:
        ResizeError - Failed to resize image
    """

    try:
        with Image.open(input_file.abs) as image_file:
            width, height = image_file.size
            new_image_file = image_file.resize((width // proportion, height // proportion))
            new_image_file.save(output_file.abs, quality=100)
            logger.info('Resize image {} success.'.format(input_file.abs))
    except Exception as err:
        logger.warning('Error: {}'.format(err))
        raise editor_err.ResizeError('Failed to resize image {}'.format(input_file.abs))
        # logger.warning('Failed to resize image {}.'.format(input_file.abs))
        # sys.exit(27)


def _convert_image_jpg(input_file, output_file):
    """
    Convert input_file image to jpeg format

    Input:
        input_file - File class object
        output_file - File class object

    Error:
        ConversionError - Failed to convert image
    """

    try:
        with Image.open(input_file.abs) as image_file:
            # Image with transparency should be converted to RGBA
            image_file = image_file.convert('RGBA')

            image_file.load()
            img = Image.new('RGB', image_file.size, (255,255,255))
            img.paste(image_file, mask=image_file.split()[3])
            img.convert('RGB').save(output_file.abs, 'JPEG')

            logger.info('Convert image {} success.'.format(input_file.abs))
    except Exception as err:
        logger.warning('Error: {}'.format(err))
        raise editor_err.ConversionError('Failed to convert image {}'.format(input_file.abs))
        # logger.info('Error: {}'.format(err))
        # logger.warning('Failed to convert image {}.'.format(input_file.abs))
        # sys.exit(31)

if __name__ == '__main__':
    main()
