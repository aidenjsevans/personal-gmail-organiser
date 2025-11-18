from unittest import TestCase

from utilities.gmail_helper import GmailHelper

class TestGmailHelperMethods(TestCase):

    def test_is_valid_email_address_with_valid_email_address(self):

        valid_email_address = "example@gmail.com"
        result: bool = GmailHelper.is_valid_email_address(valid_email_address)

        self.assertEqual(result, True)
    
    def test_is_valid_email_address_with_invalid_email_address(self):

        invalid_email_address = "examplegmail.com"
        result: bool = GmailHelper.is_valid_email_address(invalid_email_address)

        self.assertEqual(result, False)

    def test_create_email_address_set_from_email_address_string_with_empty_string(self):

        empty_string = ""
    
        with self.assertRaises(Exception) as context:

            result: set = GmailHelper.create_email_address_set_from_email_address_string(empty_string)
            self.assertEqual(str(context.exception), "At least 1 argument must be given")

    def test_create_email_address_set_from_email_address_string(self):

        email_address_string: str = "(example1@gmail.com OR example2@gmail.com OR example3@gmail.com)"
        email_address_set: set = GmailHelper.create_email_address_set_from_email_address_string(email_address_string)

        self.assertEqual(email_address_set, set([
            "example1@gmail.com", 
            "example2@gmail.com", 
            "example3@gmail.com"
            ]))
    
    def test_create_email_address_string_from_email_address_set_with_empty_set(self):

        empty_email_address_set = set()

        with self.assertRaises(Exception) as context:

            result: str = GmailHelper.create_email_address_string_from_email_address_set(empty_email_address_set)
            self.assertEqual(str(context.exception), "At least 1 argument must be given")
    
    def test_create_email_address_string_from_email_address_set(self):

        email_address_set_1 = set(["example1@gmail.com"])
        email_address_set_2 = set(["example2@gmail.com", "example3@gmail.com"])

        result_1 = GmailHelper.create_email_address_string_from_email_address_set(email_address_set_1)

        self.assertEqual(result_1, "(example1@gmail.com)")

        result_2 = GmailHelper.create_email_address_string_from_email_address_set(email_address_set_2)

        self.assertEqual(result_2, "(example3@gmail.com OR example2@gmail.com)")

