from PySide6.QtWidgets import QToolBar

from widgets.actions.action import Action

class Toolbar(QToolBar):

    def __init__(
            self,
            actions: list[Action]):

        super().__init__()

        for action in actions:
            self.addAction(action)



