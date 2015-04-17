class MyException(Exception):
    """Base class exceptions for other exceptions"""
    pass

class SourceDestinationSameError(MyException):
    """Raised when source and destination are same"""
    pass

class KeyMissingError(MyException):
    """Raised when key missing in input"""
    pass

class ValueMissingError(MyException):
    """Raised when value missing in input"""
    pass
