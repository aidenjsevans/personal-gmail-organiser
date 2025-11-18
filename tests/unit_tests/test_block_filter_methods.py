from doctest import Example
from unittest import TestCase

from models.filters.block_filter import BlockFilter

class TestBlockFilterMethods(TestCase):
    
    def setUp(self):
        
        self.name: str = "block_filter"
        self.email_1: str = "example1@gmail.com"
        self.email_2: str = "example2@gmail.com"
        self.invalid_email: str = "example3gmail.com"

    def test_check_instance_validity_with_invalid_criteria_with_more_than_one_element(self):

        invalid_criteria: dict = {
            "from": self.email_1,
            "to": self.email_2
            }

        with self.assertRaises(Exception) as context:
            
            block_filter = BlockFilter(
                name = self.name,
                criteria=invalid_criteria
                )

        self.assertEqual(str(context.exception), "A block filters criteria must only contain 1 element")

    def test_check_instance_validity_with_invalid_criteria_without_from_element(self):

        invalid_criteria: dict = {
            "to": self.email_1
            }
        
        with self.assertRaises(Exception) as context:

            block_filter = BlockFilter(
                name = self.name,
                criteria=invalid_criteria
                )
        
        self.assertEqual(str(context.exception), "A block filters criteria must only contain a 'from' element")

    def test_to_json_dict(self):

        block_filter = BlockFilter(
            name = self.name,
            criteria = {"from": self.email_1},
            filter_id = "filter_id",
            blocked_email_addresses = set([self.email_1])
        )

        expected_dict: dict = {
            "block_filter": {
                "criteria": {"from": self.email_1},
                "action": {
                    "removeLabelIds": ["INBOX"],
                    "addLabelIds": ["TRASH"]
                    },
                "id": "filter_id",
                "blocked_email_addresses": [self.email_1]
            }
        }

        json_dict: dict = block_filter.to_json_dict()

        self.assertEqual(expected_dict, json_dict, f"\n\nExpected: {expected_dict}, \n\n\nResult: {json_dict}")