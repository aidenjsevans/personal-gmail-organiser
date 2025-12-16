from PySide6.QtWidgets import QWidget, QGridLayout, QLabel

class FilterServiceView(QWidget):

    def __init__(self):

        super().__init__()

        filter_view_layout = QGridLayout(parent = self)

        header_label = QLabel(
            text = "Filter Services"
            )
        
        filter_view_layout.addWidget(header_label, 0, 0)