from PySide6.QtWidgets import QMenuBar, QWidget, QMenu

from widgets.main_windows.main_window import MainWindow
from widgets.menus.menu import Menu

from utilities.mixins.main_window_mixin import MainWindowMixin

class MenuBar(QMenuBar, MainWindowMixin):

    def __init__(
            self,
            menus: list[Menu],
            main_window: MainWindow | None = None):
        
        super().__init__()
        
        self.menus = menus
        self.main_window = main_window

    def initialise_menus(self):

        for menu in self.menus:
            
            menu.set_main_window(self.main_window)
            menu.initialise_menu_actions()
            
            self.addMenu(menu)
