from constants.filters.filters_path import FiltersPath

class MainBlockFiltersPath(FiltersPath):

    def __init__(self):
        self.__data_dir = "data"
        self.__filters_data_dir = "filters"
        self.__specific_filters_data_dir = "block_filters"

    @property
    def data_dir(self) -> str:
        return self.__data_dir
    
    @property
    def filters_data_dir(self) -> str:
        return self.__filters_data_dir
    
    @property
    def specific_filters_data_dir(self) -> str | None:
        return self.__specific_filters_data_dir