from PySide6.QtWidgets import QToolBar

from widgets.actions.action import Action

from utilities.mixins.main_window_mixin import MainWindowMixin

from typing import Callable

class ToolBar(QToolBar, MainWindowMixin):

    def __init__(
            self,
            actions: list[Action] | None = None,
            methods: list[Callable] | None = None,
            main_window = None):
        
        self.actions_list = actions
        self.methods = methods
        self.main_window = main_window
    
        super().__init__()
    
    def connect_tool_bar_actions(self):

        if not self.main_window:
            print(f"ERROR: Main window not initialised ({self.__class__.__name__()})")
            return
        
        if not self.actions_list:
            print(f"ERROR: Actions not initialised ({self.__class__.__name__()})")
            return
        
        if not self.methods:
            print(f"ERROR: Action methods not initialised ({self.__class__.__name__()})")
            return
        
        if len(self.methods) != len(self.actions_list):
            print(f"ERROR: Each action must have a method entry")
            return

        for index, action in enumerate(self.actions_list):

            method: Callable = self.methods[index]
            action.connect_method(method)
            self.addAction(action)
        
