from unittest import TestCase

from constants.user_interface.test_user_interface_constants import TestUserInterfaceConstants

from utilities.user_interface_helper import UserInterfaceHelper

class TestUserInterfaceHelperMethods(TestCase):

    def setUp(self):

        self.user_interface_constants = TestUserInterfaceConstants()
    
    def test_get_service_options(self):

        expected_service_options: dict = {
            1: "option_2",
            2: "option_3",
            3: "option_4",
            4: "option_5",
            5: "option_6",
            6: "exit"
        }

        service_options = UserInterfaceHelper.get_service_options(
            user_interface_constants = self.user_interface_constants,
            attribute_name = "filter_service_options",
            service_name = "Filter"
        )

        self.assertEqual(expected_service_options, service_options, f"\n\nExpected: {expected_service_options}, \n\n\nResult: {service_options}")

