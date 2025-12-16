from widgets.main_windows.main_window import MainWindow
from widgets.toolbars.tool_bar import ToolBar
from widgets.actions.action import Action

from typing import Callable

from PySide6.QtGui import QIcon

class MainToolbar(ToolBar):

    def __init__(
            self,
            main_window: MainWindow | None = None):
        
        super().__init__(
            main_window = main_window  
            )
    
    def connect_tool_bar_actions(self):

        self.actions_list = [
            Action(
                main_window = self.main_window,
                text = "Action 1"
            ),
            Action(
                main_window = self.main_window,
                text = "Action 2"
            )
        ]

        action1_method: Callable = lambda: print("Action 1")
        action2_method: Callable = lambda: print("Action 2")

        self.methods = [
            action1_method,
            action2_method
            ]
        
        super().connect_tool_bar_actions()
    
        


