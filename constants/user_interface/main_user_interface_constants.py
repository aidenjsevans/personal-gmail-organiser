from constants.user_interface.user_interface_constants import UserInterfaceConstants

class MainUserInterfaceConstants(UserInterfaceConstants):

    def __init__(self):
        
        self.__gmail_service_options: list = [
            "gmail filters"
        ]

        self.__filter_service_options: list = [
            "create filter",
            "delete filter",
            "create block filter",
            "print all filters",
            "add email to block filter"
        ]

        self.__filter_delete_service_options: list = [
            "delete by name",
            "delete by id"
        ]

    @property
    def gmail_service_options(self) -> str:
        return self.__gmail_service_options
    
    @property
    def filter_service_options(self) -> str:
        return self.__filter_service_options

    @property
    def filter_delete_service_options(self) -> str:
        return self.__filter_delete_service_options