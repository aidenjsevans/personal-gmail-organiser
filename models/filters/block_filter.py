import os

from models.filters.filter import Filter

from utilities.io_helper import IOHelper
from utilities.gmail_helper import GmailHelper

from exceptions.format_exceptions.invalid_email_format_exception import InvalidEmailFormatException

from constants.filters.main_block_filters_path import MainBlockFiltersPath
from constants.filters.filters_path import FiltersPath

class BlockFilter(Filter):
    
    def __init__(
            self,
            name: str,
            criteria: dict | None,
            
            action: dict | None = {
                "removeLabelIds": ["INBOX"],
                "addLabelIds": ["TRASH"]
                },
            
            filters_path: FiltersPath = MainBlockFiltersPath(),
            filter_id: str | None = None,
            blocked_email_addresses: set[str] | None = None):
        
        super().__init__(
            name=name,
            criteria=criteria, 
            action=action,
            filters_path=filters_path,
            filter_id=filter_id)
        
        self.blocked_email_addresses = blocked_email_addresses

        self.check_instance_validity()
    
    @classmethod
    def from_local_json_file_by_name(
        cls, 
        name: str,
        filters_path: FiltersPath):

        dir_path: str = filters_path.dir_path
        filename: str = f"{name.lower()}.json"
        filepath: str = os.path.join(dir_path, filename)

        data: dict = IOHelper.read_dict_from_local_json_file(filepath=filepath)

        criteria: dict = data[name.lower()]["criteria"]
        action: dict = data[name.lower()]["action"]
        filter_id: str | None = data[name.lower()]["id"]
        #   Need to convert list to set to account for valid json format
        blocked_email_addresses: set[str] | None = set(data[name.lower()]["blocked_email_addresses"])

        block_filter = BlockFilter(
            name=name,
            criteria=criteria,
            action=action,
            filters_path=filters_path,
            filter_id=filter_id,
            blocked_email_addresses=blocked_email_addresses
            )
        
        print(f"\nBlock filter loaded from: {filepath}\n")
        print(f"{block_filter.__str__()}")
        
        return block_filter
    
    def save_to_local_json_file(self):
        
        dir_path: str = self.filters_path.dir_path
        filename: str = f"{self.name.lower()}.json"
        filepath: str = os.path.join(dir_path, filename)

        filter_dict: dict = self.to_json_dict()

        IOHelper.write_dict_to_json_file(
            data=filter_dict,
            filepath=filepath
        )

        print(f"\nBlock filter saved to: {filepath}\n")
        print(f"\t{self.__str__()}")

    def to_json_dict(self):

        json_dict: dict = super().to_json_dict()
        #   Need to convert set to list for valid json format
        json_dict[self.name.lower()]["blocked_email_addresses"] = list(self.blocked_email_addresses)

        return json_dict
        
    def check_instance_validity(self):
        
        keys: list[str] = list(self.criteria.keys())

        if len(keys) > 1:
            raise Exception("A block filters criteria must only contain 1 element")
        
        if keys[0] != "from":
            raise Exception("A block filters criteria must only contain a 'from' element")
        
        for email_address in self.blocked_email_addresses:
            if not GmailHelper.is_valid_email_address(email_address):
                raise InvalidEmailFormatException(email_address)
    
    def __str__(self):

        values: list[str] = []
        
        values.append(f"\tName: {self.name}")
        values.append("\tBlocked emails: ")

        for email_address in self.blocked_email_addresses:
            values.append(f"\t\t{email_address}")

        values.append(super().__str__())

        return f"\n".join(values)
    
            

        
