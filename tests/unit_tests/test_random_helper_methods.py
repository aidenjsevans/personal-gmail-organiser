from unittest import TestCase

import string

from utilities.random_helper import RandomHelper

class TestRandomHelperMethods(TestCase):

    def test_create_random_alphabetic_code(self):

        random_alphabetic_code: str = RandomHelper.create_random_alphabetic_code(
            number_of_chars = 3,
            suppress_print = False)

        self.assertTrue(len(random_alphabetic_code) == 3)

        for char in random_alphabetic_code:

            self.assertIn(char, string.ascii_lowercase)