import os

from services.gmail_service import GmailService
from services.block_filter_service import BlockFilterService
from services.filter_service import FilterService
from services.label_service import LabelService
from services.message_service import MessageService

from constants.authentication.main_authentication_path import MainAuthenticationPath
from constants.user_interface.user_interface_constants import UserInterfaceConstants
from constants.user_interface.main_user_interface_constants import MainUserInterfaceConstants

from utilities.io_helper import IOHelper

SCOPES = ["https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.settings.basic"]

class Program:
    
    def __init__(
            self,
            scopes: list[str],
            service_version: str,
            user_interface_constants: UserInterfaceConstants) -> None:
        
        self.scopes = scopes
        self.service_version = service_version
        self.user_interface_constants = user_interface_constants

        self.authentication_data_dir: str | None = None
        self.filter_data_dir: str | None = None
        self.block_filter_data_dir: str | None = None

        self.gmail_service: GmailService | None = None
        self.filter_service: FilterService | None = None
        self.block_filter_service: BlockFilterService | None = None
        self.label_service: LabelService | None = None
        self.message_service: MessageService | None =  None

    def run(self) -> None:

        os.system('cls')

        self.initialise()
        
        print("\nGMAIL ORGANISER\n")

        finished_choosing_gmail_service: bool = False

        while not finished_choosing_gmail_service:

            finished_choosing_gmail_service = self.user_choosing_gmail_service()


    def user_choosing_gmail_service(self) -> bool:

        gmail_service_options_list: list = self.user_interface_constants.gmail_service_options
        gmail_service_options: dict = {}

        for index, option in enumerate(gmail_service_options_list):
            gmail_service_options[index + 1] = option

        gmail_service_options[len(gmail_service_options) + 1] = "exit"

        print("Gmail service options: \n")

        for index, option in gmail_service_options.items():
            print(f"\t{index}. {option}")

        index_choice: str = input("\nSelect a Gmail service: ")

        has_user_finished = False

        if not index_choice.isdigit():
            
            print(f"ERROR: '{index_choice}' is not an integer")

            return has_user_finished

        if gmail_service_options[int(index_choice)] == 'exit':
            
            has_user_finished = True
            
            return has_user_finished

        if gmail_service_options[int(index_choice)] == 'gmail filters':

            finished_choosing_filter_service = False

            while not finished_choosing_filter_service:

                finished_choosing_filter_service = self.user_choosing_filter_service()

    def user_choosing_filter_service(self) -> bool:

        filter_service_options_list: list = self.user_interface_constants.filter_service_options
        
        filter_service_options: dict = {}

        for index, option in enumerate(filter_service_options_list):
            filter_service_options[index + 1] = option

        filter_service_options[len(filter_service_options_list) + 1] = "exit"

        print("\nFilter service options: \n")

        for index, option in filter_service_options.items():
            print(f"\t{index}. {option}")
        
        index_choice: str = input("\nSelect a filter service: ")
        
        has_user_finished = False

        if not index_choice.isdigit():
            
            print(f"ERROR: '{index_choice}' is not an integer")
            
            return has_user_finished

        try:

            if filter_service_options[int(index_choice)] == 'exit':
                
                has_user_finished = True
                
            if filter_service_options[int(index_choice)] == 'print all filters':

                self.filter_service.print_all_filters()
            
            if filter_service_options[int(index_choice)] == 'delete filter':

                finished_choosing_delete_service_option: bool = False

                while not finished_choosing_delete_service_option:

                    finished_choosing_delete_service_option = self.user_choosing_delete_filter_service()

            return has_user_finished
        
        except KeyError:
            
            print(f"ERROR: '{index_choice}' is not a valid input")

            return has_user_finished

    def user_choosing_delete_filter_service(self) -> bool:
            
            filter_delete_service_options_list: list = self.user_interface_constants.filter_delete_service_options
            filter_delete_service_options: dict = {}

            for index, option in enumerate(filter_delete_service_options_list):
                filter_delete_service_options[index + 1] = option

            filter_delete_service_options[len(filter_delete_service_options_list) + 1] = "exit"

            print("\nFilter delete service options: \n")

            for index, option in filter_delete_service_options.items():
                print(f"\t{index}. {option}")

            index_choice: str = input("\nSelect a filter delete service: ")

            has_user_finished = False

            if not index_choice.isdigit():

                print(f"ERROR: '{index_choice}' is not an integer")

                return has_user_finished

            try:

                if filter_delete_service_options[int(index_choice)] == 'exit':
            
                    has_user_finished = True

                return has_user_finished
                  
            except KeyError:

                print(f"ERROR: '{index_choice}' is not a valid input")

                return has_user_finished

    def initialise(self):

        self.initialise_dir_paths()
        self.initialise_services()

        has_successfully_initialised: bool = True

        for value in self.__dict__.values():

            if value == None:

                has_successfully_initialised = False
                break
        
        if not has_successfully_initialised:
            raise Exception("Program failed to initialise")
        
    def initialise_services(self):

        gmail_service = GmailService(
            scopes = self.scopes,
            authentication_data_dir = self.authentication_data_dir,
            service_version = self.service_version
            )
        
        filter_service = FilterService(
            gmail_service = gmail_service,
            filter_data_dir = self.filter_data_dir
            )
        
        block_filter_service = BlockFilterService(gmail_service)
        label_service = LabelService(gmail_service)
        message_service =  MessageService(gmail_service)

        self.gmail_service = gmail_service
        self.filter_service = filter_service
        self.block_filter_service = block_filter_service
        self.label_service = label_service
        self.message_service = message_service

    def initialise_dir_paths(self):

        dir_paths_filepath: str = os.path.join("data", "dir_paths.csv")

        if not os.path.exists(dir_paths_filepath):

            default_paths: list = []

            default_authentication_dir_path_list: list = [
                "DEFAULT_AUTHENTICATION_DIR", 
                "data", 
                "authentication"]

            default_filter_dir_path_list: list = [
                "DEFAULT_FILTER_DIR", 
                "data", 
                "filters"]
            
            default_block_filter_dir_path_list: list = [
                "DEFAULT_BLOCK_FILTER_DIR", 
                "data", 
                "filters",
                "block_filters"]

            default_paths.append(default_authentication_dir_path_list)
            default_paths.append(default_filter_dir_path_list)
            default_paths.append(default_block_filter_dir_path_list)

            IOHelper.write_lists_to_csv_file(
                filepath=dir_paths_filepath,
                lists_arg=default_paths,
                )
            
            self.authentication_data_dir = os.path.join(*default_authentication_dir_path_list[1:])
            self.filter_data_dir = os.path.join(*default_filter_dir_path_list[1:])
            self.block_filter_data_dir = os.path.join(*default_block_filter_dir_path_list[1:])

            print(f"\nWritten directory paths: {dir_paths_filepath}")
        
        else:

            default_path_lists: list[list] = IOHelper.read_csv_file_to_lists(dir_paths_filepath)

            while default_path_lists:

                default_path_list: list = default_path_lists.pop()
                path_name: str = default_path_list[0]

                match path_name:
                    case "DEFAULT_AUTHENTICATION_DIR":
                        self.authentication_data_dir = os.path.join(*default_path_list[1:])
                    case "DEFAULT_FILTER_DIR":
                        self.filter_data_dir = os.path.join(*default_path_list[1:])
                    case "DEFAULT_BLOCK_FILTER_DIR":
                        self.block_filter_data_dir = os.path.join(*default_path_list[1:])
                    case _:
                        raise Exception(f"Path name '{path_name}' is not recognised")
            
            print(f"\nRead directory paths: {dir_paths_filepath}")
            
if __name__ == "__main__":
    
    main_user_interface_constants = MainUserInterfaceConstants()

    program: Program = Program(
        scopes=SCOPES,
        service_version="v1",
        user_interface_constants=main_user_interface_constants
        )
    
    program.run()
