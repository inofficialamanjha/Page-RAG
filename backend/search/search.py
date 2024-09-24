import datetime
import json
import math
import uuid
from typing import Optional, List

from backend.tokenizer.tokenizer import BertTokenizer
from common.configurations import Configurations
from common.constants import DataSourceType
from database.chromadatabase import ChromaDatabase
from models.data.text.text import TextData
from models.page.page import Page, PageMetadata
from common.utils import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


class Search:
    _instance = None
    _PAGE_DATA_KEY = 'pageData'

    def __init__(self):
        self.database = ChromaDatabase.instance()
        self.tokenizer = BertTokenizer.instance()
        configurations = Configurations.instance()
        self.n_results = configurations[configurations.BACKEND_KEY][configurations.Backend.SEARCH_KEY][
            configurations.Backend.Search.N_RESULTS_KEY]
        self.threshold = configurations[configurations.BACKEND_KEY][configurations.Backend.SEARCH_KEY][
            configurations.Backend.Search.THRESHOLD_KEY]

    @staticmethod
    def instance():
        if Search._instance is None:
            Search._instance = Search()
        return Search._instance

    def insert(self, token: str, page: Page) -> Optional[uuid.UUID]:
        start_time = datetime.datetime.now()
        db_id = uuid.uuid4()
        try:
            embedding = self.tokenizer.tokenize(token)
            self.database.add(
                embeddings=[embedding.tolist()],
                metadatas=[{self._PAGE_DATA_KEY: json.dumps(page)}],
                ids=[str(db_id)]
            )
            _logger.info('Time taken to insert token: %s', datetime.datetime.now() - start_time)
            return db_id
        except Exception as e:
            _logger.error('Failed to insert token into database: %s', e)
            return None

    def query(self, query_texts: List[str]) -> List[Page]:
        start_time = datetime.datetime.now()
        query_embeddings = [self.tokenizer.tokenize(query_text).tolist() for query_text in query_texts]
        query_results = self.database.query(query_embeddings, n_results=self.n_results)

        pages: List[Page] = []

        if query_results:
            distances_list = query_results['distances']
            metadatas_list = query_results['metadatas']
            assert len(distances_list) == len(metadatas_list)

            for indexes, distances in enumerate(distances_list):
                assert len(distances) == len(metadatas_list[indexes])
                for index, distance in enumerate(distances):
                    cosine_similarity = self._convert_cosine_distance_to_similarity_index(distance)
                    if cosine_similarity > self.threshold:
                        pages.append(json.loads(metadatas_list[indexes][index][self._PAGE_DATA_KEY]))

        _logger.info('Time taken to query: %s', datetime.datetime.now() - start_time)
        return pages

    @staticmethod
    def _convert_cosine_distance_to_similarity_index(distance: float) -> float:
        cosine_distance = math.cos(distance)
        return (cosine_distance + 1) / 2

    def __del__(self):
        if Search._instance == self:
            Search._instance = None


def _module_testing():
    search = Search.instance()
    database = ChromaDatabase.instance()
    token = 'Lets go out for a movie. What about Batman Begins at 8PM?'
    page = Page(PageMetadata(
        source_type=DataSourceType.PDF,
        number=0,
        path='path/to/file'
    ))
    page.add_data(TextData(body=token))
    print(page)
    db_id = search.insert(token, page)
    print(db_id)
    print(database.count())
    print(database.peek())
    query = 'go out for a movie'
    result = search.query([query])
    print(f'Query Results: {result}')


if __name__ == '__main__':
    _module_testing()
