from abc import ABC, abstractmethod

class FilterConstants(ABC):
    
    @property
    @abstractmethod
    def filter_criteria_options(self) -> set[str]:
        pass
    
    @property
    @abstractmethod
    def filter_action_options(self) -> set[str]:
        pass