from constants.user_interface.user_interface_constants import UserInterfaceConstants

class TestUserInterfaceConstants(UserInterfaceConstants):

    def __init__(self):
        
        self.__gmail_service_options: list = [
            "option_1"
        ]

        self.__filter_service_options: list = [
            "option_2",
            "option_3",
            "option_4",
            "option_5",
            "option_6"
        ]

        self.__filter_delete_service_options: list = [
            "option_7",
            "option_8"
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
    
    @property
    def filter_create_service_options(self) -> str:
        pass