from abc import ABC, abstractmethod


class Error_abstr(ABC):
    @abstractmethod
    def local_error(self):
        pass
