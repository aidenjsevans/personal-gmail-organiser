
class MainWindowMixin:

    def set_main_window(self, main_window):
        
        if not hasattr(self, "main_window"):
            raise AttributeError(f"'{self.__class__.__name__}' must define a 'main_window' attribute")

        self.main_window = main_window