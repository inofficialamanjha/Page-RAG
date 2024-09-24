import json
from typing import Optional

from common.constants import DataSourceType
from models.data.interface import BaseData
from models.data.text.text import TextData
from models.page.page_data.factory import PageDataFactory


class PageMetadata(dict):
    SOURCE_KEY = 'source'
    PATH_KEY = 'path'
    PAGE_NUMBER_KEY = 'number'

    def __init__(self, source_type: DataSourceType, number: int, path: Optional[str] = None):
        super().__init__()
        self[self.SOURCE_KEY] = source_type.value
        self[self.PATH_KEY] = path
        self[self.PAGE_NUMBER_KEY] = number


class Page(dict):
    METADATA_KEY = 'metadata'
    DATA_KEY = 'data'

    def __init__(self, metadata: PageMetadata):
        super().__init__()
        self[self.METADATA_KEY] = metadata
        self[self.DATA_KEY] = []

    def add_data(self, data: BaseData):
        data = PageDataFactory.get_page_data(data)
        self[self.DATA_KEY].append(data)


def _module_testing():
    page = Page(PageMetadata(source_type=DataSourceType.PDF, number=0, path='path/to/file'))
    page.add_data(TextData(body='This is a test data'))
    page_json_dump = json.dumps(page)
    print(f'Serialized page: {page_json_dump}')
    print(f'Deserialized page: {json.loads(page_json_dump)}')


if __name__ == '__main__':
    _module_testing()
