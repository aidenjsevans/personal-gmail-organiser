import os

from program_objects.program import Program

from utilities.io_helper import IOHelper
from utilities.random_helper import RandomHelper

from services.gmail_service import GmailService
from services.filter_service import FilterService
from services.block_filter_service import BlockFilterService
from services.label_service import LabelService
from services.message_service import MessageService

from models.filters.filter import Filter

class ProgramInitialiser():

    def __init__(
            self, 
            program: Program,
            number_of_random_chars: int = 5,
            name_collision_count_limit: int = 10):
        
        self.program = program
        self.number_of_random_chars = number_of_random_chars
        self.name_collision_count_limit = name_collision_count_limit

        self.has_initialised_filepaths = False
        self.has_initialised_dir_paths = False
        self.has_initialised_services = False
    
    def initialise_program(self) -> Program:

        self.initialise_filepaths()

        if not self.has_initialised_filepaths:
            raise Exception("\nERROR: failed to initialise filepaths")
        
        self.initialise_dir_paths()

        if not self.has_initialised_dir_paths:
            raise Exception("\nERROR: failed to initialise dir paths")

        self.initialise_services()

        if not self.has_initialised_services:
            raise Exception("\nERROR: failed to initialise services")

        for attribute, value in self.__dict__.items():

            if value == None:
                raise Exception(f"\nERROR: failed to initialise {attribute}")
        
        return self.program

    def initialise_filepaths(self):

        self.program.filter_id_name_pairs_filepath = os.path.join("data", "filter_id_name_pairs.json")

        if not os.path.exists(self.program.filter_id_name_pairs_filepath):

            IOHelper.write_dict_to_json_file(
                data = {}, 
                filepath = self.program.filter_id_name_pairs_filepath
                )
            
            print(f"\nWritten filepath: {self.program.filter_id_name_pairs_filepath}")
        
        self.has_initialised_filepaths = True
    
    def initialise_dir_paths(self):

        self.program.dir_paths_filepath = os.path.join("data", "dir_paths.csv")

        if not os.path.exists(self.program.dir_paths_filepath):

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
                filepath = self.program.dir_paths_filepath,
                lists_arg = default_paths,
                )
            
            self.program.authentication_data_dir = os.path.join(*default_authentication_dir_path_list[1:])
            self.program.filter_data_dir = os.path.join(*default_filter_dir_path_list[1:])
            self.program.block_filter_data_dir = os.path.join(*default_block_filter_dir_path_list[1:])

            print(f"\nWritten directory paths: {self.program.dir_paths_filepath}")
        
        else:

            default_path_lists: list[list] = IOHelper.read_csv_file_to_lists(self.program.dir_paths_filepath)

            while default_path_lists:

                default_path_list: list = default_path_lists.pop()
                path_name: str = default_path_list[0]

                match path_name:

                    case "DEFAULT_AUTHENTICATION_DIR":
                        
                        self.program.authentication_data_dir = os.path.join(*default_path_list[1:])
                    
                    case "DEFAULT_FILTER_DIR":

                        self.program.filter_data_dir = os.path.join(*default_path_list[1:])
                    
                    case "DEFAULT_BLOCK_FILTER_DIR":

                        self.program.block_filter_data_dir = os.path.join(*default_path_list[1:])

                    case _:
                        
                        raise Exception(f"Path name '{path_name}' is not recognised")
            
            print(f"\nRead directory paths: {self.program.dir_paths_filepath}")
        
        self.has_initialised_dir_paths = True
    
    def initialise_services(self):
        
        if not self.has_initialised_filepaths or not self.has_initialised_dir_paths:
            raise Exception("Program failed to initialise")

        gmail_service = GmailService(
            scopes = self.program.scopes,
            authentication_data_dir = self.program.authentication_data_dir,
            service_version = self.program.service_version
            )
        
        filter_service = FilterService(
            gmail_service = gmail_service,
            filter_data_dir = self.program.filter_data_dir
            )
        
        block_filter_service = BlockFilterService(gmail_service)
        
        label_service = LabelService(
            gmail_service = gmail_service,
            label_constants = self.program.label_constants
            )
        
        message_service =  MessageService(gmail_service)

        self.program.gmail_service = gmail_service
        self.program.filter_service = filter_service
        self.program.block_filter_service = block_filter_service
        self.program.label_service = label_service
        self.program.message_service = message_service

        self.has_initialised_services = True
    
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
