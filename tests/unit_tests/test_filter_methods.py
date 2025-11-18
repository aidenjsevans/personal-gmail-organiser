import os

from unittest import TestCase

from models.filters.filter import Filter

from constants.filters.test_filters_path import TestFiltersPath

class TestFilterMethods(TestCase):

    @classmethod
    def setUpClass(cls):
        
        test_data_dir: str = TestFiltersPath().data_dir

        for entry in os.listdir(test_data_dir):

            filepath: str = os.path.join(test_data_dir, entry)
            
            if os.path.isfile(filepath):
                os.remove(filepath)
    
    def setUp(self):

        self.email_1: str = "example1@gmail.com"
        
        self.filter = Filter(
           name = "filter",
            criteria = {"from": self.email_1},
            
            action = {
                "removeLabelIds": ["INBOX"],
                "addLabelIds": ["TRASH"]
                },

            filters_path = TestFiltersPath(),
            filter_id = "filter_id" 
        )

    def test_to_json_dict(self):

        expected_dict: dict = {
            "filter": {
                "criteria": {"from": self.email_1},
                "action": {
                    "removeLabelIds": ["INBOX"],
                    "addLabelIds": ["TRASH"]
                    },
                "id": "filter_id"
            }
        }

        json_dict: dict = self.filter.to_json_dict()

        self.assertEqual(expected_dict, json_dict, f"\n\nExpected: {expected_dict}, \n\n\nResult: {json_dict}")

    def test_save_local_json_file(self):

        filter = Filter(
            name = "filter",
            criteria = {"from": self.email_1},

            action = {
                "removeLabelIds": ["INBOX"],
                "addLabelIds": ["TRASH"]
                },

            filters_path = TestFiltersPath(),
            filter_id = "filter_id"
        )

        filter.save_to_local_json_file()

        expected_filepath: str = os.path.join("tests","data","filters","filter_name.json")

        self.assertTrue(os.path.exists(expected_filepath))

    
