from program_objects.program_runner import ProgramRunner

from constants.user_interface.main_user_interface_constants import MainUserInterfaceConstants
from constants.filters.main_filter_constants import MainFilterConstants
from constants.labels.main_label_constants import MainLabelConstants

from widgets.main_windows.main_window import MainWindow
from widgets.toolbars.main_toolbar import MainToolbar
from widgets.menu_bars.main_menu_bar import MainMenuBar

from widgets.menus.gmail_services_menu import GmailServicesMenu

from widgets.views.home_view import HomeView
from widgets.views.filter_service_view import FilterServiceView

from PySide6.QtWidgets import QApplication

if __name__ == "__main__":

    SCOPES: list[str] = [
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.settings.basic"]

    SERVICE_VERSION: str = "v1"
    MAIN_USER_INTERFACE_CONSTANTS = MainUserInterfaceConstants()
    MAIN_FILTER_CONSTANTS = MainFilterConstants()
    MAIN_LABEL_CONSTANTS = MainLabelConstants()

    '''
    program_runner = ProgramRunner(
        scopes = SCOPES,
        service_version = SERVICE_VERSION,
        user_interface_constants = MAIN_USER_INTERFACE_CONSTANTS,
        filter_constants = MAIN_FILTER_CONSTANTS,
        label_constants = MAIN_LABEL_CONSTANTS
        )

    program_runner.run()
    '''

    app = QApplication([])

    HOME_VIEW = HomeView()
    FILTER_SERVICE_VIEW = FilterServiceView()

    GMAIL_SERVICE_MENU = GmailServicesMenu(
        filter_service_view = FILTER_SERVICE_VIEW
        )

    MAIN_MENU_BAR = MainMenuBar(
        menus = [
            GMAIL_SERVICE_MENU
            ] 
        )
    
    window = MainWindow(
        title = "Gmail Organiser",
        width_px = 500,
        height_px = 500,
        tool_bar_class = MainToolbar,
        menu_bar = MAIN_MENU_BAR,
        home_view = HOME_VIEW,
        filter_service_view = FILTER_SERVICE_VIEW
        )

    window.show()
    app.exec()




