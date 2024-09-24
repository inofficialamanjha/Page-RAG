from enum import Enum
from typing import Optional


class Environment(Enum):
    DEV = 1
    PROD = 2

    @staticmethod
    def from_value(value: int) -> Optional['Environment']:
        for env in Environment:
            if env.value == value:
                return env
        raise None


class DataSourceType(Enum):
    PDF = 1


class DataType(Enum):
    TEXT = 1

    @staticmethod
    def from_value(value: int) -> Optional['DataType']:
        for dt in DataType:
            if dt.value == value:
                return dt
        raise None


class GeneratorType(Enum):
    CHATGPT4 = 1
    PHI3MED128KINS = 2
    CPU_PROCESSING = 3
    CHATGPT35TURBO = 4

    @staticmethod
    def from_value(value: int) -> Optional['GeneratorType']:
        for gt in GeneratorType:
            if gt.value == value:
                return gt
        raise None
