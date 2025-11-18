from abc import ABC, abstractmethod

import os

class AuthenticationPath(ABC):
    
    @property
    @abstractmethod
    def token_filename(self) -> str:
        pass
    
    @property
    @abstractmethod
    def credentials_filename(self) -> str:
        pass
    
    @property
    @abstractmethod
    def data_dir(self) -> str:
        pass
    
    @property
    @abstractmethod
    def authentication_data_dir(self) -> str:
        pass

    @property
    def token_filepath(self) -> str:
        return os.path.join(self.data_dir, self.authentication_data_dir, self.token_filename)

    @property
    def credentials_filepath(self) -> str:
        return os.path.join(self.data_dir, self.authentication_data_dir, self.credentials_filename)







