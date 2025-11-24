import os

import time

from program_objects.program import Program
from program_objects.program_initialiser import ProgramInitialiser

from constants.user_interface.user_interface_constants import UserInterfaceConstants
from constants.filters.filter_constants import FilterConstants
from constants.labels.label_constants import LabelConstants

class ProgramRunner:
        
        def __init__(
            self,
            scopes: list[str],
            service_version: str,
            user_interface_constants: UserInterfaceConstants,
            filter_constants: FilterConstants,
            label_constants: LabelConstants):

            self.scopes = scopes
            self.service_version = service_version
            
            self.user_interface_constants = user_interface_constants
            self.filter_constants = filter_constants
            self.label_constants = label_constants

        def run(self):
            
            #   Clear the console
            os.system('cls')

            program = Program(
                scopes = self.scopes,
                service_version = self.service_version,
                user_interface_constants = self.user_interface_constants,
                filter_constants = self.filter_constants,
                label_constants = self.label_constants
                )
            
            program_initialiser = ProgramInitialiser(program)
            program_initialiser.initialise_program()

            time.sleep(1)
            
            print("\nGMAIL ORGANISER")

            finished_choosing_gmail_service: bool = False

            while not finished_choosing_gmail_service:

                finished_choosing_gmail_service = program.user_choosing_gmail_service()
