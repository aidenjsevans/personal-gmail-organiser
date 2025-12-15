from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QWidget, QToolBar

class MainToolbar(QToolBar):

    def __init__(
            self,
            parent: QWidget | None = None):
        
        super().__init__(parent = parent)

        action_1 = QAction(
            text = "Action 1",
            parent = self
            )
        
        action_1.setIcon(QIcon())
        action_1.triggered.connect(lambda: print("Action 1"))

        action_2 = QAction(
            text = "Action 2",
            parent = self
            )
        
        action_2.setIcon(QIcon())
        action_2.triggered.connect(lambda: print("Action 2"))

        self.addAction(action_1)
        self.addAction(action_2)
        

