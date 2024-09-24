"""
This file contains the implementation of the PdfParser class which is used to parse PDF files
"""
from typing import List

from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter

from backend.data_parsers.interface import BaseFileDataParser
from common.configurations import Configurations
from common.constants import DataSourceType
from common.utils import logging
from models.data.text.text import TextData
from models.page.page import Page, PageMetadata

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


class PdfParser(BaseFileDataParser):
    def parse(self) -> List[Page]:
        text = self._read_file()
        chunks = self._chunk(text)
        pages: List[Page] = []
        for count, chunk in enumerate(chunks):
            page = Page(metadata=PageMetadata(source_type=DataSourceType.PDF, number=count + 1, path=self.file_path))
            text_data = TextData(body=chunk)
            page.add_data(text_data)
            pages.append(page)
        return pages

    def _read_file(self) -> str:
        reader = PdfReader(self.file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

    @staticmethod
    def _chunk(text: str) -> List[str]:
        configurations = Configurations.instance()
        chunk_size = configurations[configurations.BACKEND_KEY][configurations.Backend.DATA_PARSERS_KEY][
            configurations.Backend.DataParsers.PDF_PARSER_KEY][
            configurations.Backend.DataParsers.PdfParser.CHUNK_SIZE_KEY]
        overlap = configurations[configurations.BACKEND_KEY][configurations.Backend.DATA_PARSERS_KEY][
            configurations.Backend.DataParsers.PDF_PARSER_KEY][
            configurations.Backend.DataParsers.PdfParser.OVERLAP_KEY]

        if not chunk_size:
            return [text]

        text_splitter = CharacterTextSplitter(
            separator=' ',
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len,
            is_separator_regex=False
        )
        _logger.info('Splitting text into chunks of size: %d with overlap: %d', chunk_size, overlap)
        return text_splitter.split_text(text)


def _module_testing():
    pdf_parser = PdfParser('test/ms_balaji_infratech.pdf')
    for page in pdf_parser.parse():
        print(page)


if __name__ == '__main__':
    _module_testing()
