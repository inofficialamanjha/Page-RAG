from typing import List

from langchain_text_splitters import CharacterTextSplitter

from common.configurations import Configurations
from common.constants import DataType
from models.data.interface import BaseData
from backend.preprocessors.text import TextPreProcessors


class TextData(BaseData):
    def __init__(self, body: str):
        self.body = body
        self.configurations = Configurations.instance()

    def __str__(self):
        return self.body

    @property
    def get_data_type(self) -> DataType:
        return DataType.TEXT

    def chunk(self) -> List['TextData']:
        chunk_size = self.configurations[Configurations.MODEL_KEY][Configurations.Model.DATA_KEY][
            Configurations.Model.Data.TEXT_KEY][Configurations.Model.Data.Text.CHUNK_SIZE_KEY]
        overlap = self.configurations[Configurations.MODEL_KEY][Configurations.Model.DATA_KEY][
            Configurations.Model.Data.TEXT_KEY][Configurations.Model.Data.Text.OVERLAP_KEY]
        text_splitter = CharacterTextSplitter(
            separator=' ',
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len,
            is_separator_regex=False
        )
        return [TextData(chunk) for chunk in text_splitter.split_text(self.body)]

    def preprocess(self) -> 'TextData':
        pre_processor = TextPreProcessors()
        text = self.body
        text = pre_processor.case_folding(text)
        text = pre_processor.transform_emoji_into_characters(text)
        text = pre_processor.remove_extra_spaces(text)
        text = pre_processor.remove_hyperlinks(text)
        text = pre_processor.remove_tags(text)
        text = pre_processor.remove_non_alpha_numeric_characters(text)
        return TextData(text)

    def get_embedding_tokens(self) -> str:
        return self.body


def _module_testing():
    text_data = TextData(
        'for additional information to on Balaji infratech the details provided above and let us provide you with '
        'excellent service, “Development of Indian highway you can be trust on us. . .\nContact us \nConclusion '
        'Service you can trust. . . \n \n Balaji infratech ANNEXURE-A – BANKING DETAILS ANNEXURE-B- GST Registration '
        'Bank : YES BANK Branch : MAHAVIR ENCLAVE Branch IFSC Code : YESB0000978 Account Number : 097863300000898 '
        'Account Name :M/s Balaji Infratech Account Type : Current Account Branch Contact No.: GST Registration no: '
        '07APCPD9380B1Z6 Pan card no : APCPD9380B Thanks for your attention We hope that soon we will offer you our '
        'best services.')
    print(text_data)
    print(text_data.get_data_type)
    for text_data_chunk in text_data.chunk():
        print(text_data_chunk.preprocess())


if __name__ == '__main__':
    _module_testing()
