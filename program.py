import os

from models.filters.filter import Filter
from models.label import Label

from services.gmail_service import GmailService
from services.block_filter_service import BlockFilterService
from services.filter_service import FilterService
from services.label_service import LabelService
from services.message_service import MessageService

from constants.authentication.main_authentication_path import MainAuthenticationPath
from constants.user_interface.user_interface_constants import UserInterfaceConstants
from constants.user_interface.main_user_interface_constants import MainUserInterfaceConstants
from constants.filters.filter_constants import FilterConstants
from constants.filters.main_filter_constants import MainFilterConstants
from constants.labels.label_constants import LabelConstants
from constants.labels.main_label_constants import MainLabelConstants

from utilities.io_helper import IOHelper
from utilities.user_interface_helper import UserInterfaceHelper
from utilities.random_helper import RandomHelper
from utilities.filter_helper import FilterHelper

SCOPES = ["https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.settings.basic"]

class Program:
    
    def __init__(
            self,
            scopes: list[str],
            service_version: str,
            user_interface_constants: UserInterfaceConstants,
            filter_constants: FilterConstants,
            label_constants: LabelConstants,
            number_of_random_chars: int = 5,
            name_collision_count_limit: int = 10) -> None:
        
        self.scopes = scopes
        self.service_version = service_version
        self.user_interface_constants = user_interface_constants
        self.filter_constants = filter_constants
        self.label_constants = label_constants

        self.authentication_data_dir: str | None = None
        self.filter_data_dir: str | None = None
        self.block_filter_data_dir: str | None = None
        self.filter_id_name_pairs_filepath: str | None = None

        self.gmail_service: GmailService | None = None
        self.filter_service: FilterService | None = None
        self.block_filter_service: BlockFilterService | None = None
        self.label_service: LabelService | None = None
        self.message_service: MessageService | None =  None

        self.number_of_random_chars = number_of_random_chars
        self.name_collision_count_limit = name_collision_count_limit

        self.has_initialised_dir_paths: bool = False
        self.has_initialised_filepaths: bool = False
        self.has_initialised_services: bool = False

    def run(self) -> None:

        os.system('cls')

        self.initialise()
        
        print("\nGMAIL ORGANISER\n")

        finished_choosing_gmail_service: bool = False

        while not finished_choosing_gmail_service:

            finished_choosing_gmail_service = self.user_choosing_gmail_service()

    def user_choosing_gmail_service(self) -> bool:

        gmail_service_options: dict = UserInterfaceHelper.get_service_options(
            user_interface_constants = self.user_interface_constants,
            attribute_name = "gmail_service_options",
            service_name = "Gmail"
            )

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

        filter_service_options: dict = UserInterfaceHelper.get_service_options(
            user_interface_constants = self.user_interface_constants,
            attribute_name = "filter_service_options",
            service_name = "Filter"
            )

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

            if filter_service_options[int(index_choice)] == "create filter":

                finished_choosing_create_service_option: bool = False

                while not finished_choosing_create_service_option:
                    finished_choosing_create_service_option = self.user_choosing_create_filter_service()

            return has_user_finished
        
        except KeyError:
            
            print(f"ERROR: '{index_choice}' is not a valid input")

            return has_user_finished

    def user_choosing_delete_filter_service(self) -> bool:
            
            filter_delete_service_options: dict = UserInterfaceHelper.get_service_options(
            user_interface_constants = self.user_interface_constants,
            attribute_name = "filter_delete_service_options",
            service_name = "Filter delete"
            )

            index_choice: str = input("\nSelect a filter delete service: ")

            has_user_finished = False

            if not index_choice.isdigit():

                print(f"ERROR: '{index_choice}' is not an integer")

                return has_user_finished

            try:

                if filter_delete_service_options[int(index_choice)] == 'exit':
            
                    has_user_finished = True

                    return has_user_finished
            
                if filter_delete_service_options[int(index_choice)] == 'delete by id':

                    filter_id_input: str = input("\nFilter ID: ")

                    self.filter_service.delete_cloud_filter_by_id(
                        filter_id = filter_id_input, 
                        suppress_print = False
                        )

                    return has_user_finished

            except KeyError:

                print(f"ERROR: '{index_choice}' is not a valid input")

                return has_user_finished

    def user_choosing_create_filter_service(self) -> bool:

        filter_create_service_options: dict = UserInterfaceHelper.get_service_options(
            user_interface_constants = self.user_interface_constants,
            attribute_name = "filter_create_service_options",
            service_name = "Filter create"
            )
        
        index_choice: str = input("\nSelect a filter create service: ")

        has_user_finished = False

        if not index_choice.isdigit():

            print(f"ERROR: '{index_choice}' is not an integer")

            return has_user_finished

        try:

            if filter_create_service_options[int(index_choice)] == 'exit':
        
                has_user_finished = True

                return has_user_finished
        
            if filter_create_service_options[int(index_choice)] == 'create filter':

                finished_creating_filter: bool = False

                while not finished_creating_filter:
                    finished_creating_filter = self.user_creating_filter()
                
                return has_user_finished

        except KeyError:

            print(f"ERROR: '{index_choice}' is not a valid input")

            return has_user_finished

    #   TODO break down into smaller sub methods
    def user_creating_filter(self) -> bool:

        has_user_finished = False

        #   TODO validate the filter name
        filter_name: str = input("Filter name: ")

        #   TODO allow user to add multiple actions and criteria
        filter_criteria_options: dict = FilterHelper.get_filter_options(
            filter_constants = self.filter_constants,
            attribute_name = "filter_criteria_options",
            option_name = "Criteria"
            )
        
        criteria_index_choice: str = input("\nSelect a filter criteria option: ")
        filter_criteria: dict = {}

        if not criteria_index_choice.isdigit():

            print(f"ERROR: '{criteria_index_choice}' is not an integer")

            return has_user_finished

        try:

            if filter_criteria_options[int(criteria_index_choice)] == 'exit':

                has_user_finished = True

                return has_user_finished
            
            if filter_criteria_options[int(criteria_index_choice)] == 'from':
                
                #   TODO validate email format
                sender_email_input: str = input("Sender email: ")
                filter_criteria['from'] = sender_email_input

        except KeyError:

            print(f"ERROR: '{criteria_index_choice}' is not a valid input")

            return has_user_finished
        
        #   TODO allow user to add multiple actions and criteria
        filter_action_options: dict = FilterHelper.get_filter_options(
            filter_constants = self.filter_constants,
            attribute_name = "filter_action_options",
            option_name = "Action"
            )
        
        action_index_choice: str = input("\nSelect a filter action option: ")
        filter_action: dict = {}

        #   TODO encapsulate this check into a function to reduce repetition
        if not action_index_choice.isdigit():

            print(f"ERROR: '{action_index_choice}' is not an integer")

            return has_user_finished
        
        try:

            if filter_action_options[int(action_index_choice)] == 'exit':

                has_user_finished = True

                return has_user_finished
            
            #   TODO allow user to add multiple label ids
            if filter_action_options[int(action_index_choice)] == 'addLabelIds':

                label_options: dict = self.label_service.get_label_options()
                add_label_ids: list[str] = []

                print("\nLabels: \n")

                for index, label in label_options.items():

                    if isinstance(label, Label):

                        print(f"\t{index}. {label.name}")
                    
                    else:
                        print(f"\t{index}. {label}")
                
                label_index_choice: str = input("\nSelect a label: ")

                #   TODO encapsulate this check into a function to reduce repetition
                if not label_index_choice.isdigit():

                    print(f"ERROR: '{label_index_choice}' is not an integer")

                    return has_user_finished
                
                try:

                    label_choice: Label = label_options[int(label_index_choice)]
                    label_id: str = label_choice.label_id

                    add_label_ids.append(label_id)

                    filter_action['addLabelIds'] = add_label_ids
                
                except KeyError:

                    print(f"ERROR: '{label_index_choice}' is not a valid input")

                    return has_user_finished
        
        except KeyError:

            print(f"ERROR: '{action_index_choice}' is not a valid input")

            return has_user_finished
        
        created_filter: Filter = Filter(
            name = filter_name,
            criteria = filter_criteria,
            action = filter_action
        )

        created_filter_with_id: Filter = self.filter_service.save_filter_to_cloud(created_filter)
        self.filter_service.save_filter_to_local_json_file(created_filter_with_id)

        has_user_finished = True

        return has_user_finished
                
    def initialise(self):

        self.initialise_dir_paths()
        self.initialise_services()

        has_successfully_initialised: bool = True

        if not self.has_initialised_filepaths:
            has_successfully_initialised = False

        if not self.has_initialised_dir_paths:
            has_successfully_initialised = False
        
        if not self.has_initialised_services:
            has_successfully_initialised = False

        for value in self.__dict__.values():

            if value == None:
                has_successfully_initialised = False
                break
        
        if not has_successfully_initialised:
            raise Exception("Program failed to initialise")
    
    #   TODO need to add a feature to ensure that the services are initialised after the dir paths. Could use some sort of bool
    def initialise_services(self):

        if not self.has_initialised_filepaths or not self.has_initialised_dir_paths:
            raise Exception("Program failed to initialise")

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
        
        label_service = LabelService(
            gmail_service = gmail_service,
            label_constants = self.label_constants
            )
        
        message_service =  MessageService(gmail_service)

        self.gmail_service = gmail_service
        self.filter_service = filter_service
        self.block_filter_service = block_filter_service
        self.label_service = label_service
        self.message_service = message_service

        self.has_initialised_services = True

    def initialise_filepaths(self):

        self.filter_id_name_pairs_filepath: str = os.path.join("data", "id_name_pairs.json")

        if not os.path.exists(self.filter_id_name_pairs_filepath):

            IOHelper.write_dict_to_json_file(
                data = {}, 
                filepath = self.filter_id_name_pairs_filepath
                )
            
        print(f"\nWritten filepath: {self.filter_id_name_pairs_filepath}")
        
        self.has_initialised_filepaths = True

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
        
        self.has_initialised_dir_paths = True
    
    def cloud_sync_filters(self):

        filter_id_name_pairs_filepath: str = os.path.join("data", "id_name_pairs.json")

        if not os.path.exists(filter_id_name_pairs_filepath):

            IOHelper.write_dict_to_json_file(
                data = {}, 
                filepath = filter_id_name_pairs_filepath
                )
        
        filters: list[Filter] | None = self.filter_service.get_all_cloud_filters()

        if filters == None:
            return
        
        #   TODO need a way to determine if a filter is a block filter

        id_name_pairs_dict: dict = IOHelper.read_dict_from_local_json_file(filter_id_name_pairs_filepath)

        #   TODO come back to this (this should not happen)
        if id_name_pairs_dict == None:
            raise Exception()

        for filter in filters:

            if filter.filter_id in id_name_pairs_dict:
                continue

            if filter.name == None:

                name_collision_count: int = 0
                
                while True:
                    
                    #   TODO consider how to deal with this outcome
                    if name_collision_count > self.name_collision_count_limit:
                        raise Exception(f"Name collision count of {self.name_collision_count_limit} exceeded")

                    random_alphabetic_code: str = RandomHelper.create_random_alphabetic_code(
                        number_of_chars = self.number_of_random_chars
                        )
                    
                    random_filter_name: str = f"filter_{random_alphabetic_code}"

                    filepath: str = os.path.join(self.filter_data_dir, random_filter_name)

                    if os.path.exists(filepath):
                        name_collision_count += 1
                        continue
                    
                    filter.name = random_filter_name
                    break
            
            filter_name: str = filter.name
            filter_id: str = filter.filter_id

            id_name_pairs_dict[filter_id] = filter_name
            
            self.filter_service.save_filter_to_local_json_file(filter)

        IOHelper.write_dict_to_json_file(
            data = filter_id_name_pairs_filepath,
            filepath = filter_id_name_pairs_filepath)
            
if __name__ == "__main__":
    
    main_user_interface_constants = MainUserInterfaceConstants()
    main_filter_constants = MainFilterConstants()
    main_label_constants = MainLabelConstants()

    program: Program = Program(
        scopes = SCOPES,
        service_version = "v1",
        user_interface_constants = main_user_interface_constants,
        filter_constants = main_filter_constants,
        label_constants = main_label_constants 
        )
    
    program.run()
 
    """
    gmail_service = GmailService(
            scopes = SCOPES,
            authentication_data_dir = os.path.join("data", "authentication"),
            service_version = "v1"
            )
    
    label_service = LabelService(gmail_service)

    for label in label_service.get_all_labels():
        print(f"\n{label.__str__()}")
    """
    

