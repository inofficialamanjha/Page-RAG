from abc import ABC
from typing import List


class BaseSearchQueryGenerator(ABC):
    """
    Interface for search query generator
    """

    def generate(self, user_query: str) -> List[str]:
        """
        Generate the search query
        """
        pass
