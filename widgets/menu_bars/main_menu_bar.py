from PySide6.QtWidgets import QMenuBar, QWidget, QMenu

from widgets.menus.gmail_services_menu import GmailServicesMenu

from constants.user_interface.main_user_interface_constants import MainUserInterfaceConstants

from widgets.main_windows.main_window import MainWindow
from widgets.menu_bars.menu_bar import MenuBar
from widgets.menus.menu import Menu

class MainMenuBar(MenuBar):

    def __init__(
            self,
            menus: list[Menu],
            main_window: MainWindow | None = None):
        
        super().__init__(
            menus = menus,
            main_window = main_window
        )
        
    def initialise_menus(self):

        if not self.main_window:
            print(f"ERROR: Main window not initialised ({self.__class__.__name__})")
            return

        for menu in self.menus:
            
            menu.set_main_window(self.main_window)
            menu.initialise_menu_actions()
            self.addMenu(menu)

