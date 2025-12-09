import os

from services.gmail_service_user import GmailServiceUser

from constants.filters.filters_path import FiltersPath

from models.filters.filter import Filter

from utilities.io_helper import IOHelper
from utilities.user_interface_helper import ProgressIndicator
from utilities.random_helper import RandomHelper

from googleapiclient.errors import HttpError

class FilterService(GmailServiceUser):

    def __init__(
            self, 
            gmail_service,
            filter_data_dir: str,
            filter_name_collision_count_limit: int,
            number_of_filter_name_random_chars: int):
        
        super().__init__(gmail_service)
        self.filter_data_dir = filter_data_dir
        self.name_collision_count_limit = filter_name_collision_count_limit
        self.number_of_filter_name_random_chars = number_of_filter_name_random_chars

    def get_local_filter_by_name(
            self,
            name: str) -> Filter | None:
        
        json_filepath: str = os.path.join(self.filter_data_dir, f"{name}.json")

        data: dict | None = IOHelper.read_dict_from_local_json_file(json_filepath)

        if data != None:

            criteria: dict = data[name.lower()]["criteria"]
            action: dict = data[name.lower()]["action"]
            filter_id: str | None = data[name.lower()]["id"]

            filter = Filter(
                name=name.lower(),
                criteria=criteria,
                action=action,
                filter_id=filter_id
                )
        
            print(f"\nFilter loaded: {json_filepath}\n")
            print(f"{filter.__str__()}")
        
            return filter
        
        else:

            print(f"\nFilter not found: {json_filepath}")

            return None

    def get_cloud_filter_by_id(
            self,
            filter_id: str) -> Filter | None:
        
        try:

            filter_dict: dict = self.gmail_service.service.users().settings().filters().get(
                userId = "me",
                id = filter_id
                ).execute()
        
            return Filter.from_gmail_api_dict(filter_dict)

        except HttpError as error:

            match error.resp.status:

                case 404:
                
                    print(f"\nWARNING: filter {filter_id} does not exist in the cloud")

                    return None

    #   TODO test this function
    def get_all_cloud_filters(self) -> list[Filter] | list:

        results = self.gmail_service.service.users().settings().filters().list(userId="me").execute()
        
        filter_dicts = results.get("filter",[])

        filters: list[Filter] = []

        if not filter_dicts:
            
            return filters
        
        for filter_dict in filter_dicts:
            
            filter = Filter.from_gmail_api_dict(filter_dict=filter_dict)
            
            filters.append(filter)
        
        return filters
    
    #   TODO save changes to the id name pairs json
    def get_all_local_filters(self) -> list[Filter] | list:

        filters: list[Filter] = []

        with os.scandir(self.filter_data_dir) as entries:

            for entry in entries:

                if not entry.is_file():
                    continue

                if not entry.name.endswith(".json"):
                    continue

                filter_dict: dict = IOHelper.read_dict_from_local_json_file(entry.path)
                filter = Filter.from_dict(filter_dict)

                filters.append(filter)
        
        return filters

    def save_filter_to_local_json_file(
            self,
            filter: Filter):
        
        json_dict: dict = filter.to_json_dict()
        filter_name: str = filter.name

        filepath: str = os.path.join(self.filter_data_dir, f"{filter_name}.json")

        IOHelper.write_dict_to_json_file(
            data = json_dict,
            filepath = filepath
            )
        
        print(f"\nFilter saved to local file: {filepath}\n")
        print(f"{filter.__str__()}")

    #   TODO validate filter input
    def save_filter_to_cloud(
            self, 
            filter: Filter) -> Filter:

        filter_config: dict = filter.config

        created_filter_dict: dict = self.gmail_service.service.users().settings().filters().create(
            userId = "me",
            body = filter_config
            ).execute()
        
        created_filter_id = created_filter_dict["id"]
        filter.filter_id = created_filter_id

        print(f"\nFilter uploaded to cloud:\n")
        print(f"{filter.__str__()}")

        return filter
        
    def delete_cloud_filter_by_id(
            self,
            filter_id: str,
            suppress_print: bool) -> Filter | None:

            filter = self.get_cloud_filter_by_id(filter_id)

            if filter == None:
                return None

            self.gmail_service.service.users().settings().filters().delete(
                userId="me",
                id=filter_id
                ).execute()
            
            if suppress_print:
                return filter
            
            print(f"\nFilter deleted from cloud:")
            print(f"\n{filter.__str__()}")

            #   TODO need to delete the local saved json file as well. Should implement a file that stores the filter name and ids as key value pairs

            return filter

    def delete_local_filter_by_name(
            self,
            name: str,
            suppress_print: bool) -> None:
        
        filepath: str = os.path.join(self.filter_data_dir, f"{name}.json")

        filter_dict: Filter | None = IOHelper.read_dict_from_local_json_file(filepath)

        if filter_dict == None:

            return

        filter = Filter.from_dict(filter_dict)

        IOHelper.delete_local_file(filepath)

        if suppress_print:
            return
        
        print(f"\nFilter deleted from: {filepath}")
        print(f"\n{filter.__str__()}")

    #   TODO test this function
    def print_all_local_filters(self) -> None:

        filters: list[Filter] | None = self.get_all_local_filters()

        if not filters:
            print("\nNo filters found")
            return
        
        print("\nFilters:")

        for filter in filters:
            print(f"\n{filter.__str__()}")
    
    def sync_cloud_filters(
            self,
            with_progress_indicator: bool = True) -> bool:

        if with_progress_indicator:
            sync_cloud_filters_progress_indicator = ProgressIndicator("Filter cloud sync")
            sync_cloud_filters_progress_indicator.start()

        local_filters: list[Filter] = self.get_all_local_filters()
        local_filters_filter_id_set: set = set()

        for local_filter in local_filters:
            local_filters_filter_id_set.add(local_filter.filter_id)

        cloud_filters: list[Filter] = self.get_all_cloud_filters()
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
                        number_of_chars = self.number_of_filter_name_random_chars
                        )
                    
                    random_filter_name: str = f"filter_{random_alphabetic_code}"

                    filepath: str = os.path.join(self.filter_data_dir, random_filter_name)

                    if os.path.exists(filepath):
                        name_collision_count += 1
                        continue
                    
                    cloud_filter.name = random_filter_name
                    
                    break
                
                local_filters.append(cloud_filter)
                local_filters_filter_id_set.add(cloud_filter.filter_id)

                self.save_filter_to_local_json_file(cloud_filter)
        
        #   Check if local filters are missing from cloud storage. If so, delete the filter from local storage
        for local_filter in local_filters:

            if local_filter.filter_id not in cloud_filters_filter_id_set:

                self.delete_local_filter_by_name(
                    name = local_filter.name,
                    suppress_print = False
                    )
        
        if with_progress_indicator:
            sync_cloud_filters_progress_indicator.stop()
        
        return True
