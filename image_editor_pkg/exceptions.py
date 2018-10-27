"""
Exceptions definition of python image-editor program

Author:
    haw
"""


class editorError(Exception):
    """
    Base class for other user-defined exceptions
    """
    pass


class FileCorruptError(editorError):
    """
    Raise if file not found
    """
    pass


class FileFormatError(editorError):
    """
    Raise if file format not expected
    """
    pass



class ConversionError(editorError):
    """
    Raise image conversion failed
    """
    pass


class CompressionError(editorError):
    """
    Raise if image compression failed
    """
    pass


class ResizeError(editorError):
    """
    Raise if image resize failed
    """
    pass
