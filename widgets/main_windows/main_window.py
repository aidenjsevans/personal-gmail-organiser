from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QLabel, 
    QVBoxLayout, QPushButton, QGridLayout, 
    QWidget, QStackedWidget, QMenuBar)

from PySide6.QtGui import QAction, QIcon

from widgets.views.home_view import HomeView

class MainWindow(QMainWindow):
    
    def __init__(
            self,
            title: str,
            width_px: float,
            heigh_px: float,
            tool_bar: QToolBar,
            menu_bar: QMenuBar):
        
        super().__init__()

        self.setWindowTitle(title)
        self.resize(width_px, heigh_px)

        tool_bar = tool_bar(parent = self)
        self.addToolBar(tool_bar)

        menu_bar = menu_bar(parent = self)
        self.setMenuBar(menu_bar)

        self.home_view = HomeView()
        
        self.stack = QStackedWidget()
        self.stack.addWidget(self.home_view)
        self.stack.setCurrentIndex(0)

        main_window_layout = QGridLayout()
        self.stack.setLayout(main_window_layout)
        
        self.setCentralWidget(self.stack)

        
        
