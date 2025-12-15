from PySide6.QtWidgets import QMenu, QWidget
from PySide6.QtGui import QAction

from constants.user_interface.user_interface_constants import UserInterfaceConstants

class GmailServicesMenu(QMenu):

    def __init__(
            self,
            parent: QWidget,
            user_interface_constants: UserInterfaceConstants):
        
        super().__init__(
            title = "Gmail Services",
            parent = parent)

        gmail_service_options: list[str] = user_interface_constants.gmail_service_options

        for service_option in gmail_service_options:

            action = QAction(
                text = service_option,
                parent = self
            )

            action.triggered.connect(lambda: print(f"{service_option}"))

            self.addAction(action)
