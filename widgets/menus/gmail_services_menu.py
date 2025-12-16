from PySide6.QtWidgets import QMenu, QWidget
from PySide6.QtGui import QAction

from constants.user_interface.user_interface_constants import UserInterfaceConstants

from widgets.views.filter_service_view import FilterServiceView
from widgets.main_windows.main_window import MainWindow

class GmailServicesMenu(QMenu):

    def __init__(
            self,
            filter_service_view: QWidget,
            main_window: MainWindow | None = None):
        
        super().__init__()

        self.setTitle("Services")

        self.filter_service_view = filter_service_view
        self.main_window = main_window

    def set_main_window(self, main_window: MainWindow):
        self.main_window = main_window
    
    def initialise_menu_actions(self):

        if not self.main_window:
            print("ERROR: Main window not initialised")
            return
        
        filter_service_action = QAction(
            text = "Filter Service",
            parent = self
            )

        filter_service_action.triggered.connect(lambda: self.main_window.set_view(self.filter_service_view))

        self.addAction(filter_service_action)


