from abc import ABC, abstractmethod

class CustomException(Exception, ABC):

    @property
    @abstractmethod
    def error():
        pass

    @property
    @abstractmethod
    def error_code():
        pass

    @property
    @abstractmethod
    def message():
        pass

    def __str__(self):

        values: list[str] = []

        values.append(f"Error: {self.error}")
        values.append(f"Error code: {self.error_code}")
        values.append(f"Message: {self.message}")

        return f"\n".join(values)
