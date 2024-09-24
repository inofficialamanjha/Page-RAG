import datetime
from typing import List, Generator

from openai.lib.azure import AzureOpenAI

from backend.recall.plugins.responseaugmentedgenerator.factory import ResponseAugmentedGeneratorFactory
from backend.recall.plugins.searchquerygenerator.chatgpt4.chatgpt4 import ChatGpt4SearchQueryGenerator
from backend.recall.plugins.searchquerygenerator.factory import SearchQueryGeneratorFactory
from backend.search.search import Search
from common.configurations import Configurations
from models.data.interface import BaseData
from models.data.text.text import TextData
from models.page.page import Page, PageMetadata
from models.page.page_data.factory import PageDataFactory
from common.utils import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

_INTERNAL_ERROR_RESPONSE_MESSAGE = 'Sorry, I am unable to process your query at the moment. Please try again later.'


class Recall:
    _instance = None

    def __init__(self):
        self.search = Search.instance()

        search_query_generator_factory = SearchQueryGeneratorFactory.instance()
        self.search_query_generator_plugin = search_query_generator_factory.get_search_query_generator()

        response_augmented_generator_factory = ResponseAugmentedGeneratorFactory.instance()
        self.response_augmented_generator_plugin = (response_augmented_generator_factory
                                                    .get_response_augmented_generator())

    @staticmethod
    def instance():
        if Recall._instance is None:
            Recall._instance = Recall()
        return Recall._instance

    def query(self, user_query: str) -> Generator[str, None, None]:
        try:
            search_queries = self.get_search_query(user_query)
        except Exception:
            _logger.error('Failed to generate search queries for user query: %s', user_query)
            yield _INTERNAL_ERROR_RESPONSE_MESSAGE
            return

        search_query_chunks: List[str] = []
        for search_query in search_queries:
            text_data = TextData(body=search_query)
            chunks = text_data.chunk()
            for chunk in chunks:
                preprocessed_chunk = chunk.preprocess()
                search_query_chunks.append(preprocessed_chunk.get_embedding_tokens())
        final_search_results = self.get_final_search_results(search_query_chunks)

        try:
            for word in self._get_response(user_query, final_search_results):
                yield word
        except Exception:
            _logger.error('Failed to generate response for user query: %s', user_query)
            yield _INTERNAL_ERROR_RESPONSE_MESSAGE

    def get_search_query(self, user_query: str) -> List[str]:
        start_time = datetime.datetime.now()
        search_query = self.search_query_generator_plugin.generate(user_query)
        _logger.info('Time taken to generate search query: %s', datetime.datetime.now() - start_time)
        return search_query

    def get_final_search_results(self, search_queries: List[str]) -> List[Page]:
        search_results = self.search.query(search_queries)
        unique_pages = set()
        final_search_results: List[Page] = []
        for page in search_results:
            page_metadata = page[Page.METADATA_KEY]
            path = page_metadata[PageMetadata.PATH_KEY]
            page_number = page_metadata[PageMetadata.PAGE_NUMBER_KEY]

            page_id = (path, page_number)
            if page_id not in unique_pages:
                unique_pages.add(page_id)
                final_search_results.append(page)
        return final_search_results

    def _get_response(self, user_query: str, page_results: List[Page]) -> Generator[str, None, None]:
        datas: List[BaseData] = []
        for page in page_results:
            page_datas = page[Page.DATA_KEY]
            for data_dict in page_datas:
                data = PageDataFactory.from_page_data(data_dict)
                if data:
                    datas.append(data)
        return self.response_augmented_generator_plugin.generate(user_query, datas)

    def __del__(self):
        if Recall._instance is not None:
            Recall._instance = None


def _module_testing():
    recall = Recall.instance()
    for response_word in recall.query('what is the capital of india'):
        print(response_word, end=' ', flush=True)
    print()


if __name__ == '__main__':
    _module_testing()
