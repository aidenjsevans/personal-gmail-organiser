import os

import time

from program_objects.program import Program

from utilities.io_helper import IOHelper
from utilities.random_helper import RandomHelper
from utilities.user_interface_helper import ProgressIndicator

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
            number_of_filter_name_random_chars: int = 5,
            filter_name_collision_count_limit: int = 10):
        
        self.program = program
        self.number_of_filter_name_random_chars = number_of_filter_name_random_chars
        self.filter_name_collision_count_limit = filter_name_collision_count_limit

        self.has_initialised_dir_paths = False
        self.has_initialised_services = False
        self.has_synced_cloud_filters = False
    
    def initialise_program(self) -> Program:

        self.initialise_dir_paths()

        if not self.has_initialised_dir_paths:
            raise Exception("\nERROR: failed to initialise dir paths")

        self.initialise_services()

        if not self.has_initialised_services:
            raise Exception("\nERROR: failed to initialise services")
        
        self.has_synced_cloud_filters = self.filter_service.sync_cloud_filters()

        if not self.has_synced_cloud_filters:
            raise Exception("\nERROR: failed to sync cloud filters")

        for attribute, value in self.__dict__.items():

            if value == None:
                raise Exception(f"\nERROR: failed to initialise {attribute}")
        
        return self.program

    
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
        
        if not self.has_initialised_dir_paths:
            raise Exception("Program failed to initialise")

        self.gmail_service = GmailService(
            scopes = self.program.scopes,
            authentication_data_dir = self.program.authentication_data_dir,
            service_version = self.program.service_version
            )
        
        self.filter_service = FilterService(
            gmail_service = self.gmail_service,
            filter_data_dir = self.program.filter_data_dir,
            filter_name_collision_count_limit = self.filter_name_collision_count_limit,
            number_of_filter_name_random_chars = self.number_of_filter_name_random_chars
            )
        
        self.block_filter_service = BlockFilterService(self.gmail_service)
        
        self.label_service = LabelService(
            gmail_service = self.gmail_service,
            label_constants = self.program.label_constants
            )
        
        self.message_service =  MessageService(self.gmail_service)

        self.program.gmail_service = self.gmail_service
        self.program.filter_service = self.filter_service
        self.program.block_filter_service = self.block_filter_service
        self.program.label_service = self.label_service
        self.program.message_service = self.message_service

        self.has_initialised_services = True