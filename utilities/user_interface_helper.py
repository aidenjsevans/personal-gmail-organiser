from threading import Thread

import itertools

import time

from constants.user_interface.user_interface_constants import UserInterfaceConstants

class UserInterfaceHelper:

    @staticmethod
    def get_service_options(
        user_interface_constants: UserInterfaceConstants,
        attribute_name: str,
        service_name: str,
        default = None) -> dict:

        '''
        Gets the options for a specific service defined within a UserInterfaceConstants object.
        The service options are returned in a dictionary with the keys being numeric values starting from 1, and 
        the values are the names of the options. The method also adds an exit option at the end of the dictionary.

        Args:
            user_interface_constants (UserInterfaceConstants: The UserInterfaceConstants object from which to retrieve values from.
            attribute_name (str): The name of the attribute to retrieve.
            service_name (str): The name of the service
            default: The default return value if the attribute cannot be found
        
        Returns:
            dict: A dictionary containing the service options as values and numeric keys starting from 1. The return dictionary
            also contains and additional 'exit' option
        
        Raises:
            Exception: If the attribute cannot be found within the UserInterfaceConstants object

        '''

        service_options_list: list | None = getattr(user_interface_constants, attribute_name, default)

        if service_options_list == None:
            raise Exception(f"The attribute {attribute_name} does not exist within the UserInterfaceConstants object")
        
        service_options: dict = {}

        for index, option in enumerate(service_options_list):
            service_options[index + 1] = option
        
        service_options[len(service_options_list) + 1] = "exit"

        print(f"\n{service_name} service options: \n")

        for index, option in service_options.items():
            print(f"\t{index}. {option}")

        return service_options

#   TODO create method to call another method with the progress indicator
class ProgressIndicator:

    def __init__(
            self,
            message: str):

        self.has_finished = False
        self.message = message

    def start(self):

        #   Setting daemon to True means that the program can still exit if the daemon thread
        #   is still running
        Thread(
            target = self.print_indicator,
            daemon = True).start()
    
    def print_indicator(self):

        spinner = itertools.cycle(['|', '/', '-', '\\'])
        
        while not self.has_finished:
            
            char = next(spinner)
            
            print(f"\r{self.message}... {char}", end="", flush=True)
            
            time.sleep(0.1)
        
        print(
            f"\r{self.message}... \u2714",
            end = "",
            flush = True)
    
    def stop(self):

        self.has_finished = True





    

