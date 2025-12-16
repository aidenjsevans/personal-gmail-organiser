from PySide6.QtGui import QAction, QIcon

from utilities.mixins.main_window_mixin import MainWindowMixin

from typing import Callable

class Action(QAction, MainWindowMixin):

    def __init__(
            self,
            main_window = None,
            icon: QIcon | None = QIcon(),
            text: str | None = None
            ):
        
        self.main_window = main_window
        self.method: Callable | None = None
        
        super().__init__(
            text = text,
            icon = icon
            )
        
        if self.method:
            self.triggered.connect(self.method)
        
    def connect_method(self, method: Callable):
        self.method = method
        self.triggered.connect(self.method)
