from typing import Optional

from common.constants import DataType
from models.data.interface import BaseData
from models.data.text.text import TextData
from models.page.page_data.text.text import PageTextData
from models.page.page_data.constants import PageDataConstants


class PageDataFactory:
    TYPE_KEY = 'type'

    @staticmethod
    def get_page_data(data: BaseData) -> dict:
        if data.get_data_type == DataType.TEXT:
            assert isinstance(data, TextData)
            return PageTextData().to_data(data)
        return {}

    @staticmethod
    def from_page_data(page_data: dict) -> Optional[BaseData]:
        if DataType.from_value(page_data.get(PageDataConstants.TYPE_KEY, -1)) == DataType.TEXT:
            return PageTextData().from_data(page_data)
        return None


def _module_testing():
    page_data_factory = PageDataFactory()
    text_data = TextData(body='Hello World')
    print(text_data.get_data_type)
    print(page_data_factory.get_page_data(text_data))


if __name__ == '__main__':
    _module_testing()
