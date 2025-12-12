from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget

from typing import Callable

class Action(QAction):

    def __init__(
            self,
            icon: QIcon,
            text: str,
            trigger_function: Callable,
            parent: QWidget):

        super().__init__(parent = parent)

        if icon:
            self.setIcon(icon)
        
        if text:
            self.setText(text)

        if trigger_function:
            self.triggered.connect(trigger_function)

