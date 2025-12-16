from PySide6.QtWidgets import (
    QMainWindow, QGridLayout, 
    QWidget, QStackedWidget, QMenuBar)

from widgets.toolbars.tool_bar import ToolBar

class MainWindow(QMainWindow):
    
    def __init__(
            self,
            title: str,
            width_px: float,
            height_px: float,
            tool_bar_class: ToolBar,
            menu_bar: QMenuBar,
            home_view: QWidget,
            filter_service_view: QWidget):
        
        super().__init__()

        self.setWindowTitle(title)
        self.resize(width_px, height_px)

        tool_bar = tool_bar_class(
            main_window = self
            )
        tool_bar.connect_tool_bar_actions()
        self.addToolBar(tool_bar)

        menu_bar.set_main_window(self)
        menu_bar.initialise_menus()
        self.setMenuBar(menu_bar)

        self.home_view = home_view
        self.filter_service_view = filter_service_view
        
        self.stack = QStackedWidget()

        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.filter_service_view)

        self.stack.setCurrentIndex(0)

        main_window_layout = QGridLayout()
        self.stack.setLayout(main_window_layout)

        self.setCentralWidget(self.stack)
    
    #   Add validation
    def set_view_by_index(self, index: int):
        self.stack.setCurrentIndex(index)
    
    #   Add validation
    def set_view(self, view: QWidget):
        self.stack.setCurrentWidget(view)



        
        
