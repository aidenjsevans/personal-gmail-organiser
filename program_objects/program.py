from constants.user_interface.user_interface_constants import UserInterfaceConstants
from constants.filters.filter_constants import FilterConstants
from constants.labels.label_constants import LabelConstants

from services.gmail_service import GmailService
from services.block_filter_service import BlockFilterService
from services.filter_service import FilterService
from services.label_service import LabelService
from services.message_service import MessageService

from utilities.user_interface_helper import UserInterfaceHelper
from utilities.filter_helper import FilterHelper
from utilities.gmail_helper import GmailHelper

from models.label import Label
from models.filters.filter import Filter

class Program:
    
    def __init__(
            self,
            scopes: list[str],
            service_version: str,
            user_interface_constants: UserInterfaceConstants,
            filter_constants: FilterConstants,
            label_constants: LabelConstants) -> None:
        
        self.scopes = scopes
        self.service_version = service_version
        
        self.user_interface_constants = user_interface_constants
        self.filter_constants = filter_constants
        self.label_constants = label_constants

        self.authentication_data_dir: str | None = None
        self.filter_data_dir: str | None = None
        self.block_filter_data_dir: str | None = None
        
        self.filter_id_name_pairs_filepath: str | None = None
        self.dir_paths_filepath: str | None = None

        self.gmail_service: GmailService | None = None
        self.filter_service: FilterService | None = None
        self.block_filter_service: BlockFilterService | None = None
        self.label_service: LabelService | None = None
        self.message_service: MessageService | None =  None

    def user_choosing_gmail_service(self) -> bool:

        gmail_service_options: dict = UserInterfaceHelper.get_service_options(
            user_interface_constants = self.user_interface_constants,
            attribute_name = "gmail_service_options",
            service_name = "Gmail"
            )

        index_choice: str = input("\nSelect a Gmail service: ")

        has_user_finished_choosing_gmail_service = False

        if not index_choice.isdigit():
            
            print(f"ERROR: '{index_choice}' is not an integer")

            return has_user_finished_choosing_gmail_service
        
        try:

            if gmail_service_options[int(index_choice)] == 'exit':
                
                has_user_finished_choosing_gmail_service = True
                
                return has_user_finished_choosing_gmail_service

            if gmail_service_options[int(index_choice)] == 'gmail filters':

                has_user_finished_choosing_filter_service = False

                while not has_user_finished_choosing_filter_service:

                    has_user_finished_choosing_filter_service = self.user_choosing_filter_service()

        except KeyError:

            print(f"ERROR: '{index_choice}' is not a valid input")

            return has_user_finished_choosing_gmail_service

    def user_choosing_filter_service(self) -> bool:

        filter_service_options: dict = UserInterfaceHelper.get_service_options(
            user_interface_constants = self.user_interface_constants,
            attribute_name = "filter_service_options",
            service_name = "Filter"
            )

        index_choice: str = input("\nSelect a filter service: ")
        
        has_user_finished_choosing_filter_service = False

        if not index_choice.isdigit():
            
            print(f"ERROR: '{index_choice}' is not an integer")
            
            return has_user_finished_choosing_filter_service

        try:

            if filter_service_options[int(index_choice)] == 'exit':
                
                has_user_finished_choosing_filter_service = True
                
            if filter_service_options[int(index_choice)] == 'print all filters':

                self.filter_service.print_all_filters()
            
            if filter_service_options[int(index_choice)] == 'delete filter':

                has_user_finished_choosing_delete_service_option: bool = False

                while not has_user_finished_choosing_delete_service_option:
                    
                    has_user_finished_choosing_delete_service_option = self.user_choosing_delete_filter_service()

            if filter_service_options[int(index_choice)] == "create filter":

                has_user_finished_choosing_create_service_option: bool = False

                while not has_user_finished_choosing_create_service_option:
                    
                    has_user_finished_choosing_create_service_option = self.user_choosing_create_filter_service()

            return has_user_finished_choosing_filter_service
        
        except KeyError:
            
            print(f"ERROR: '{index_choice}' is not a valid input")

            return has_user_finished_choosing_filter_service

    def user_choosing_delete_filter_service(self) -> bool:
            
            filter_delete_service_options: dict = UserInterfaceHelper.get_service_options(
                user_interface_constants = self.user_interface_constants,
                attribute_name = "filter_delete_service_options",
                service_name = "Filter delete"
                )

            index_choice: str = input("\nSelect a filter delete service: ")

            has_user_finished_choosing_delete_service = False

            if not index_choice.isdigit():

                print(f"ERROR: '{index_choice}' is not an integer")

                return has_user_finished_choosing_delete_service

            try:

                if filter_delete_service_options[int(index_choice)] == 'exit':
            
                    has_user_finished_choosing_delete_service = True

                    return has_user_finished_choosing_delete_service
            
                if filter_delete_service_options[int(index_choice)] == 'delete by id':

                    filter_id_input: str = input("\nFilter ID: ")

                    self.filter_service.delete_cloud_filter_by_id(
                        filter_id = filter_id_input, 
                        suppress_print = False
                        )

                    return has_user_finished_choosing_delete_service

            except KeyError:

                print(f"ERROR: '{index_choice}' is not a valid input")

                return has_user_finished_choosing_delete_service

    def user_choosing_create_filter_service(self) -> bool:

        filter_create_service_options: dict = UserInterfaceHelper.get_service_options(
            user_interface_constants = self.user_interface_constants,
            attribute_name = "filter_create_service_options",
            service_name = "Filter create"
            )
        
        index_choice: str = input("\nSelect a filter create service: ")

        has_user_finished_choosing_create_service = False

        if not index_choice.isdigit():

            print(f"ERROR: '{index_choice}' is not an integer")

            return has_user_finished_choosing_create_service

        try:

            if filter_create_service_options[int(index_choice)] == 'exit':
        
                has_user_finished_choosing_create_service = True

                return has_user_finished_choosing_create_service
        
            if filter_create_service_options[int(index_choice)] == 'create filter':

                has_user_finished_creating_filter: bool = False

                while not has_user_finished_creating_filter:
                    
                    has_user_finished_creating_filter = self.user_creating_filter()
                
                return has_user_finished_choosing_create_service

        except KeyError:

            print(f"ERROR: '{index_choice}' is not a valid input")

            return has_user_finished_choosing_create_service

    #   TODO break down into smaller sub methods
    def user_creating_filter(self) -> bool:

        has_user_finished_creating_filter = False

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

            return has_user_finished_creating_filter

        try:

            if filter_criteria_options[int(criteria_index_choice)] == 'exit':

                has_user_finished_creating_filter = True

                return has_user_finished_creating_filter
            
            if filter_criteria_options[int(criteria_index_choice)] == 'from':
                
                #   TODO validate email format
                sender_email_input: str = input("Sender email: ")
                filter_criteria['from'] = sender_email_input

        except KeyError:

            print(f"ERROR: '{criteria_index_choice}' is not a valid input")

            return has_user_finished_creating_filter
        
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

            return has_user_finished_creating_filter
        
        try:

            if filter_action_options[int(action_index_choice)] == 'exit':

                has_user_finished_creating_filter = True

                return has_user_finished_creating_filter
            
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

                    return has_user_finished_creating_filter
                
                try:

                    label_choice: Label = label_options[int(label_index_choice)]
                    label_id: str = label_choice.label_id

                    add_label_ids.append(label_id)

                    filter_action['addLabelIds'] = add_label_ids
                
                except KeyError:

                    print(f"ERROR: '{label_index_choice}' is not a valid input")

                    return has_user_finished_creating_filter
        
        except KeyError:

            print(f"ERROR: '{action_index_choice}' is not a valid input")

            return has_user_finished_creating_filter
        
        created_filter: Filter = Filter(
            name = filter_name,
            criteria = filter_criteria,
            action = filter_action
        )

        created_filter_with_id: Filter = self.filter_service.save_filter_to_cloud(created_filter)
        self.filter_service.save_filter_to_local_json_file(created_filter_with_id)

        has_user_finished = True

        return has_user_finished
    
    def user_choosing_filter_criteria(self):

        #   TODO allow user to add multiple actions and criteria
        filter_criteria_options: dict = FilterHelper.get_filter_options(
            filter_constants = self.filter_constants,
            attribute_name = "filter_criteria_options",
            option_name = "Criteria"
            )
        
        criteria_index_choice: str = input("\nSelect a filter criteria option: ")
        
        filter_criteria: dict = {}

        has_user_finished_choosing_criteria_option = False

        if not criteria_index_choice.isdigit():

            print(f"ERROR: '{criteria_index_choice}' is not an integer")

            return has_user_finished_choosing_criteria_option

        try:
            #   TODO consider adding a 'continue' option instead of just exit
            if filter_criteria_options[int(criteria_index_choice)] == 'exit':

                has_user_finished_choosing_criteria_option = True

                return has_user_finished_choosing_criteria_option
            
            if filter_criteria_options[int(criteria_index_choice)] == 'from':
                
                sender_email_input: str = input("Sender email: ")

                if not GmailHelper.is_valid_email_address(sender_email_input):
                    
                    print(f"ERROR: '{sender_email_input}' is not a valid email address")

                    return has_user_finished_choosing_criteria_option

                from_criteria: str | None = filter_criteria_options.get("from")

                if from_criteria == None:

                    filter_criteria['from'] = sender_email_input
                
                else:

                    sender_emails: set[str] = GmailHelper.create_email_address_set_from_email_address_string(from_criteria)

                    sender_emails.add(sender_email_input)

                    from_criteria = GmailHelper.create_email_address_string_from_email_address_set(sender_emails)

                    filter_criteria['from'] = sender_email_input


        except KeyError:

            print(f"ERROR: '{criteria_index_choice}' is not a valid input")

            return has_user_finished_choosing_criteria_option


                

  