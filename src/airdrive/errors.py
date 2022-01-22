class AirDriveException(Exception):
    """
    The base class for all AirDrive exceptions.
    """
    pass


class AccountNotFound(AirDriveException):
    def __init__(self, message):
        super().__init__(message)


class InvalidCredentials(AirDriveException):
    def __init__(self, message):
        super().__init__(message)


class InvalidToken(AirDriveException):
    def __init__(self, message):
        super().__init__(message)


class InvalidURL(AirDriveException):
    def __init__(self, message):
        super().__init__(message)


class InvalidFile(AirDriveException):
    def __init__(self, message):
        super().__init__(message)


class FileNotFound(AirDriveException):
    def __init__(self, message):
        super().__init__(message)


class InvalidParameter(AirDriveException):
    def __init__(self, message):
        super().__init__(message)
