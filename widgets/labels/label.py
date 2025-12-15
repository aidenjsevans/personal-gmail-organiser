from PySide6.QtWidgets import QLabel
from widgets.grid_widget import GridWidget

class Label(QLabel, GridWidget):

    def __init__(
            self,
            text: str,
            row: int,
            column: int):
        
        super().__init__(
            row = row,
            column = column
            )
        
        if text:
            self.setText(text)