import os

from constants.filters.filters_path import FiltersPath

class TestFiltersPath:

    def __init__(self):
        self.__tests_dir = "tests"
        self.__data_dir = "data"
        self.__filters_data_dir = "filters"

    @property
    def tests_dir(self) -> str:
        return self.__tests_dir

    @property
    def data_dir(self) -> str:
        return self.__data_dir
    
    @property
    def filters_data_dir(self) -> str:
        return self.__filters_data_dir
    
    @property
    def dir_path(self) -> str:
        return os.path.join(self.tests_dir, self.data_dir, self.filters_data_dir)

    