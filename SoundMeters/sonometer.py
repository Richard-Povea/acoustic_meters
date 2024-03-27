from abc import ABC, abstractmethod
from pandas import DataFrame

class Sonometer(ABC):
    def __init__(self, path:str):
        self.path = path
        self.data = self.__import_data__()

    @abstractmethod
    def __import_data__(self)->DataFrame:
        raise NotImplementedError("This method is not implemented.")
