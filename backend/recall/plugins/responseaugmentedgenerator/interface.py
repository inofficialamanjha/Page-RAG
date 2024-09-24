from abc import ABC
from typing import List, Generator

from models.data.interface import BaseData


class BaseResponseAugmentedGenerator(ABC):
    """
    Interface for response augmented generator
    """
    def generate(self, user_query: str, datas: List[BaseData]) -> Generator[str, None, None]:
        """
        Generate the response
        """
        pass
