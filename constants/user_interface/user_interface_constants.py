from abc import ABC, abstractmethod

class UserInterfaceConstants(ABC):
    
    @property
    @abstractmethod
    def gmail_service_options(self) -> str:
        pass

    @property
    @abstractmethod
    def filter_service_options(self) -> str:
        pass

    @property
    @abstractmethod
    def filter_delete_service_options(self) -> str:
        pass

    @property
    @abstractmethod
    def filter_create_service_options(self) -> str:
        pass
    
