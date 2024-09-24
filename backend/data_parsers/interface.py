"""
This file contains the implementation of the FileDataParser Interface which is used to parse data from files
"""
import os.path
from abc import ABC, abstractmethod
from typing import Optional, List

from models.page.page import Page


class BaseFileDataParser(ABC):
    def __init__(self, file_path: Optional[str]):
        if file_path and not os.path.exists(file_path):
            raise FileNotFoundError(f'{file_path} not found')
        # Get the absolute path of the file
        self.file_path = os.path.abspath(file_path)

    @abstractmethod
    def parse(self) -> List[Page]:
        pass
