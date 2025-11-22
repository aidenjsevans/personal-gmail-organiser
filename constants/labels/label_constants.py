from abc import ABC, abstractmethod

class LabelConstants(ABC):
    
    @property
    @abstractmethod
    def banned_filter_label_ids(self) -> set[str]:
        pass