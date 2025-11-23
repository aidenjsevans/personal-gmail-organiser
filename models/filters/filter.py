import os

from constants.filters.filters_path import FiltersPath

from utilities.io_helper import IOHelper

class Filter:
    
    def __init__(
            self,
            name: str | None,
            criteria: dict,
            action: dict,
            filter_id: str | None = None):
        
        self.name = name
        self.criteria = criteria
        self.action = action
        self.filter_id = filter_id
    
    @classmethod
    def from_gmail_api_dict(
        cls, 
        filter_dict: dict):

        keys: list[str] = set(filter_dict.keys())

        if "id" in keys:
            filter_id: str = filter_dict["id"]
        else:
            raise Exception("The input dictionary must contain an 'id' key")
        
        if "criteria" in keys:
            filter_criteria: dict = filter_dict["criteria"]
        else:
            filter_criteria: dict = None
        
        if "action" in keys:
            filter_action: dict = filter_dict["action"]
        else:
            filter_action: dict = None

        return cls(
            name = None,
            filter_id = filter_id,
            criteria = filter_criteria,
            action = filter_action
            )
    
    @classmethod
    def from_dict(
        cls,
        filter_dict: dict):

        keys: list[str] = list(filter_dict.keys())
        
        filter_name: str = keys[0]

        filter_criteria: dict = filter_dict[filter_name]["criteria"]
        filter_action: dict = filter_dict[filter_name]["action"]
        filter_id: str = filter_dict[filter_name]["id"]

        return cls(
            name = filter_name,
            filter_id = filter_id,
            criteria = filter_criteria,
            action = filter_action
            )

    @property
    def config(self) -> dict:

        filter_config = {
            "criteria": self.criteria,
            "action": self.action
            }

        return filter_config

    def to_json_dict(self):
        return {
            #   Criteria and action must be list for valid json format
            self.name.lower(): {
                "criteria": self.criteria,
                "action": self.action,
                "id": self.filter_id,
            }
        }
    
    def __str__(self):
        
        values: list[str] = []

        values.append(f"\tName: {self.name}")
        values.append(f"\tID: {self.filter_id}")
        values.append(f"\tCriteria: ")

        for key, value in self.criteria.items():
            values.append(f"\t\t{key}: {value}")
        
        values.append(f"\tAction: ")

        for key, value in self.action.items():
            values.append(f"\t\t{key}: {value}")
    
        return f"\n".join(values)



    

        