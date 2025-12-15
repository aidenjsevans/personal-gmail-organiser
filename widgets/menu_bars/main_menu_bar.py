from PySide6.QtWidgets import QMenuBar, QWidget

from widgets.menus.gmail_services_menu import GmailServicesMenu

from constants.user_interface.main_user_interface_constants import MainUserInterfaceConstants

class MainMenuBar(QMenuBar):

    def __init__(
            self,
            parent: QWidget):
        
        super().__init__(parent = parent)

        gmail_service_menu = GmailServicesMenu(
            parent = self,
            user_interface_constants = MainUserInterfaceConstants() 
            )
        
        self.addMenu(gmail_service_menu)
