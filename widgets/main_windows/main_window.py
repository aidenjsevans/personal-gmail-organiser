from PySide6.QtWidgets import QMainWindow, QToolBar, QLabel, QVBoxLayout, QPushButton, QGridLayout
from PySide6.QtGui import QAction, QIcon

from widgets.toolbars.toolbar import Toolbar
from widgets.actions.action import Action

class MainWindow(QMainWindow):
    
    def __init__(
            self,
            title: str,
            width_px: float,
            heigh_px: float):
        
        super().__init__()
        
        layout = QGridLayout()

        self.setWindowTitle(title)
        self.resize(width_px, heigh_px)

        self.setLayout(layout)

        action1 = Action(
            icon = QIcon(),
            text = "Action 1",
            trigger_function = self.action1_triggered,
            parent = self
            )
        
        action2 = Action(
            icon = QIcon(),
            text = "Action 2",
            trigger_function = self.action2_triggered,
            parent = self
            )
    
        toolbar = Toolbar(
            actions = [
               action1,
               action2 
            ]
        )

        self.addToolBar(toolbar)

    def on_button_click(self):
        self.label.setText("Button clicked!")

    def action1_triggered(self):
        print("Action 1 clicked!")

    def action2_triggered(self):
        print("Action 2 clicked!")