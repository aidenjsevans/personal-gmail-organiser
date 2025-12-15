from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

class HomeView(QWidget):

    def __init__(self):

        super().__init__()

        home_view_layout = QGridLayout(parent = self)

        header_label = QLabel(
            text = "Gmail Organiser"
            )
        
        home_view_layout.addWidget(header_label, 0, 0)
