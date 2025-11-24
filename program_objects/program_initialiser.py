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
            number_of_random_chars: int = 5,
            name_collision_count_limit: int = 10):
        
        self.program = program
        self.number_of_random_chars = number_of_random_chars
        self.name_collision_count_limit = name_collision_count_limit

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
        
        self.sync_cloud_filters()

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

        gmail_service = GmailService(
            scopes = self.program.scopes,
            authentication_data_dir = self.program.authentication_data_dir,
            service_version = self.program.service_version
            )
        
        filter_service = FilterService(
            gmail_service = gmail_service,
            filter_data_dir = self.program.filter_data_dir,
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
    
    def sync_cloud_filters(self):

        if not self.has_initialised_dir_paths:
            raise Exception("\nERROR: failed to initialise filepaths")
        
        sync_cloud_filters_progress_indicator = ProgressIndicator("Filter cloud sync")
        sync_cloud_filters_progress_indicator.start()

        #   TODO remove
        time.sleep(2)

        local_filters: list[Filter] = self.program.filter_service.get_all_local_filters()
        local_filters_filter_id_set: set = set()

        for local_filter in local_filters:

            local_filters_filter_id_set.add(local_filter.filter_id)

        cloud_filters: list[Filter] = self.program.filter_service.get_all_cloud_filters()
        cloud_filters_filter_id_set: set = set()

        for cloud_filter in cloud_filters:

            cloud_filters_filter_id_set.add(cloud_filter.filter_id)

        #   Check if cloud filters are missing from local storage. If so, generate a name and add the filter to data/filters
        for cloud_filter in cloud_filters:

            if cloud_filter.filter_id not in local_filters_filter_id_set:

                name_collision_count: int = 0
                
                while True:
                    
                    #   TODO consider how to deal with this outcome
                    if name_collision_count > self.name_collision_count_limit:
                        raise Exception(f"Name collision count of {self.name_collision_count_limit} exceeded")

                    random_alphabetic_code: str = RandomHelper.create_random_alphabetic_code(
                        number_of_chars = self.number_of_random_chars
                        )
                    
                    random_filter_name: str = f"filter_{random_alphabetic_code}"

                    filepath: str = os.path.join(self.program.filter_data_dir, random_filter_name)

                    if os.path.exists(filepath):
                        name_collision_count += 1
                        continue
                    
                    cloud_filter.name = random_filter_name
                    
                    break
                
                local_filters.append(cloud_filter)
                local_filters_filter_id_set.add(cloud_filter.filter_id)

                self.program.filter_service.save_filter_to_local_json_file(cloud_filter)

                #   TODO add entry to filter id name pairs json
        
        
        #   Check if local filters are missing from cloud storage. If so, delete the filter from local storage
        for local_filter in local_filters:

            if local_filter.filter_id not in cloud_filters_filter_id_set:

                self.program.filter_service.delete_local_filter_by_name(
                    name = local_filter.name,
                    suppress_print = False
                    )
        
        sync_cloud_filters_progress_indicator.stop()

        self.has_synced_cloud_filters = True
