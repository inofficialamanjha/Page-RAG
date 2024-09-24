from abc import ABC, abstractmethod

from models.data.interface import BaseData


class PageDataInterface(ABC):
    @abstractmethod
    def to_data(self, data: BaseData) -> dict:
        return {}

    @abstractmethod
    def from_data(self, data: dict) -> BaseData:
        pass
