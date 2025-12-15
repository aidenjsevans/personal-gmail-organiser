
class GridWidget:

    def __init__(self, *, row = 0, column = 0, **kwargs):
        
        self.row = row
        self.column = column
        super().__init__(**kwargs)
        
