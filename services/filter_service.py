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
            filter_id: str):
        
        filter_dict: dict = self.gmail_service.service.users().settings().filters().get(
            userId="me",
            id=filter_id
            ).execute()
        
        return Filter.from_gmail_api_dict(filter_dict)

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
        
        print(f"\nFilter saved: {filepath}\n")
        print(f"{self.__str__()}")

    def delete_filter(
            self,
            filter_id: str,
            suppress_print: bool) -> Filter:

        try:

            filter_dict: dict = self.gmail_service.service.users().settings().filters().get(
                userId="me",
                id=filter_id
                ).execute()
            
            filter = Filter.from_gmail_api_dict(filter_dict)

            self.gmail_service.service.users().settings().filters().delete(
                userId="me",
                id=filter_id
                ).execute()
            
            if suppress_print:
                return filter
            
            print(f"\nFilter deleted:")
            print(f"\n{filter.__str__()}")

            #   TODO need to delete the local saved json file as well. Should implement a file that stores the filter name and ids as key value pairs

            return filter

        except HttpError as error:

            match error.resp.status:

                case 404:
                
                    print(f"\nFilter ID : {filter_id} does not exist")

    def print_all_filters(self) -> None:

        results = self.gmail_service.service.users().settings().filters().list(userId="me").execute()
        filters = results.get("filter",[])

        if not filters:
            print("\nNo filters found")
            return
        
        print("\nFilters:")

        for filter_dict in filters:
            
            filter = Filter.from_gmail_api_dict(filter_dict=filter_dict)
            
            print(f"\n{filter.__str__()}")