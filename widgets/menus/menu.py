from PySide6.QtWidgets import QMenu, QWidget
from PySide6.QtGui import QAction

from widgets.main_windows.main_window import MainWindow
from widgets.actions.action import Action

from utilities.mixins.main_window_mixin import MainWindowMixin

from typing import Callable

class Menu(QMenu, MainWindowMixin):

    def __init__(
            self,
            title: str,
            actions: list[Action],
            methods: list[Callable],
            main_window: MainWindow | None = None):
        
        self.actions_list = actions
        self.methods = methods
        self.main_window = main_window
        
        super().__init__(
            title = title
            )
    
    def initialise_menu_actions(self):

        if not self.main_window:
            print(f"ERROR: Main window not initialised ({self.__class__.__name__})")
            return
        
        if len(self.methods) != len(self.actions_list):
            print(f"ERROR: Each action must have a method entry")
            return

        for index, action in enumerate(self.actions_list):

            action.set_main_window(self.main_window)
            method: Callable = self.methods[index]
            action.connect_method(method)
            self.addAction(action)