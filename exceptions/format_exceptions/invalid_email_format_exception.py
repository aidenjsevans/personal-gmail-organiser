from exceptions.custom_exception import CustomException
from enums.format_error_codes import FormatErrorCodes

class InvalidEmailFormatException(CustomException):

    def __init__(
            self, 
            email_address: str):
        
        self.__error = FormatErrorCodes.invalid_email_format_exception.name
        self.__error_code = FormatErrorCodes.invalid_email_format_exception.value
        self.__email_address = email_address

    @property
    def error(self):
        return self.__error

    @property
    def error_code(self):
        return self.__error_code

    @property
    def message(self):
        message: str = f"'{self.email_address}' is not a valid email address format"
        return message
