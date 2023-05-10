from abc import ABC, abstractmethod


class DataLoader(ABC):
    @abstractmethod
    def read(self):
        """
        Base method for loading data.
        """
        raise NotImplementedError()

    @abstractmethod
    def write(self):
        """
        Base method for writing data.
        """
        raise NotImplementedError()
