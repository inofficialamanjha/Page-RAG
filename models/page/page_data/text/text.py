from typing import Dict

from models.data.text.text import TextData
from models.page.page_data.interface import PageDataInterface
from models.page.page_data.constants import PageDataConstants


class PageTextData(PageDataInterface):
    def from_data(self, data: dict) -> TextData:
        return TextData(body=data[PageDataConstants.BODY_KEY])

    def to_data(self, data: TextData) -> Dict:
        return {
            PageDataConstants.BODY_KEY: data.body,
            PageDataConstants.TYPE_KEY: data.get_data_type.value
        }


def _module_testing():
    page_text_data = PageTextData()
    text_data = TextData(body='Hello World')
    to_page_data = page_text_data.to_data(text_data)
    print(to_page_data)
    from_page_data = page_text_data.from_data(to_page_data)
    assert isinstance(from_page_data, TextData)
    print(from_page_data.body)


if __name__ == '__main__':
    _module_testing()
