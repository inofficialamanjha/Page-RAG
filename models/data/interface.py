from abc import ABC, abstractmethod
from typing import List

from common.constants import DataType


class BaseData(ABC):
    """
    Interface for data types
    """

    @property
    @abstractmethod
    def get_data_type(self) -> DataType:
        """
        Get the data type
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        String representation of the data type
        """
        pass

    @abstractmethod
    def chunk(self) -> List['BaseData']:
        pass

    @abstractmethod
    def preprocess(self) -> 'BaseData':
        pass

    @abstractmethod
    def get_embedding_tokens(self) -> str:
        pass
