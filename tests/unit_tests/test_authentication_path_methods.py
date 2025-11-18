from unittest import TestCase

import os

from constants.authentication.main_authentication_path import MainAuthenticationPath

class TestAuthenticationPathMethods(TestCase):

    def test_token_filepath(self):

        main_authentication_path = MainAuthenticationPath()
        token_filepath: str = main_authentication_path.token_filepath
        self.assertEqual(token_filepath, os.path.join("data", "authentication", "token.json"))

    def test_credentials_filepath(self):
        
        main_authentication_path = MainAuthenticationPath()
        credentials_filepath: str = main_authentication_path.credentials_filepath
        self.assertEqual(credentials_filepath, os.path.join("data", "authentication", "credentials.json"))
        
