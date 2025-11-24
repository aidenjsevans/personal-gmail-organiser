import os

from services.gmail_service_user import GmailServiceUser

from constants.filters.filters_path import FiltersPath

from models.filters.filter import Filter

from utilities.io_helper import IOHelper

from googleapiclient.errors import HttpError

class FilterService(GmailServiceUser):

    def __init__(
            self, 
            gmail_service,
            filter_data_dir: str):
        
        super().__init__(gmail_service)
        self.filter_data_dir = filter_data_dir

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
    def print_all_filters(self) -> None:

        filters: list[Filter] | None = self.get_all_cloud_filters()

        if not filters:
            print("\nNo filters found")
            return
        
        print("\nFilters:")

        for filter in filters:
            print(f"\n{filter.__str__()}")