from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QStyle, QApplication, QWidget

from widgets.main_windows.main_window import MainWindow
from widgets.actions.action import Action

from typing import Callable

class ViewHomeViewAction(Action):

    def __init__(
            self,
            app: QApplication,
            home_view: QWidget,
            main_window: MainWindow | None = None
            ):
        
        self.app = app
        self.home_view = home_view
        
        home_icon: QIcon = self.app.style().standardIcon(
            QStyle.StandardPixmap.SP_DirHomeIcon
            )

        super().__init__(
            main_window = main_window,
            icon = home_icon
            )
        
    def connect_method(self):

        if not self.main_window:
            print(f"ERROR: Main window not initialised ({self.__class__.__name__()})")
            return
        
        method: Callable = self.main_window.set_view(self.home_view)
        super().connect_method(method)

