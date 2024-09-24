"""
This file contains the implementation of the Pipeline class which is used to process the data and index it
"""
import datetime
from typing import List, Any

from tqdm import tqdm

from backend.data_parsers.pdf.pdf_parser import PdfParser
from backend.search.search import Search
from models.page.page import Page
from models.page.page_data.factory import PageDataFactory
from common.utils import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


class Pipeline:
    _instance: Any = None

    def __init__(self):
        self.search = Search.instance()

    @staticmethod
    def instance():
        if Pipeline._instance is None:
            Pipeline._instance = Pipeline()
        return Pipeline._instance

    def process(self, file_path: str):
        start_time = datetime.datetime.now()
        pages = Pipeline._get_pages(file_path)
        for page in tqdm(pages, desc=f'Processing pages in {file_path}'):
            page_datas = page[page.DATA_KEY]
            for page_data in page_datas:
                data = PageDataFactory.from_page_data(page_data)
                chunks = data.chunk()
                for chunk in chunks:
                    preprocessed_chunk = chunk.preprocess()
                    db_id = self.search.insert(preprocessed_chunk.get_embedding_tokens(), page)
                    if db_id is None:
                        _logger.error(f'Failed to insert chunk into database: {preprocessed_chunk}')
        _logger.info('Total processing time for file %s: %s', file_path, datetime.datetime.now() - start_time)

    @staticmethod
    def _get_pages(file_path: str) -> List[Page]:
        if file_path.endswith('.pdf'):
            return PdfParser(file_path).parse()
        return []

    def __del__(self):
        if Pipeline._instance == self:
            Pipeline._instance = None


def _module_testing():
    pipeline = Pipeline()
    pipeline.process('test/ms_balaji_infratech.pdf')


if __name__ == '__main__':
    _module_testing()
