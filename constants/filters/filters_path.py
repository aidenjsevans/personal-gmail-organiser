from abc import ABC, abstractmethod

import os

class FiltersPath(ABC):
    
    @property
    @abstractmethod
    def data_dir(self) -> str:
        pass
    
    @property
    @abstractmethod
    def filters_data_dir(self) -> str:
        pass
    
    @property
    @abstractmethod
    def specific_filters_data_dir(self) -> str | None:
        pass

    @property
    def dir_path(self) -> str:
        
        if self.specific_filters_data_dir == None:
            return os.path.join(self.data_dir, self.filters_data_dir)
        else:
            return os.path.join(self.data_dir, self.filters_data_dir, self.specific_filters_data_dir)
    

