import json
import os.path
from typing import List, Dict, Any, Optional

import chromadb
from chromadb import QueryResult
from chromadb.api.models import Collection

from backend.tokenizer.tokenizer import BertTokenizer
from common.constants import DataSourceType
from database.embedding_function import DummyEmbeddingFunction
from models.data.text.text import TextData
from models.page.page import PageMetadata, Page


class ChromaDatabase:
    _instance = None

    _COLLECTION_PATH = os.path.join('database', '.chroma.db')
    _COLLECTION_NAME = 'collection'

    def __init__(self):
        self.client = chromadb.PersistentClient(path=self._COLLECTION_PATH)
        self.collection = self.create()

    @staticmethod
    def instance():
        if ChromaDatabase._instance is None:
            ChromaDatabase._instance = ChromaDatabase()
        return ChromaDatabase._instance

    def create(self) -> Collection:
        return self.client.get_or_create_collection(name=self._COLLECTION_NAME,
                                                    metadata={"hnsw:space": "cosine"},
                                                    embedding_function=DummyEmbeddingFunction())

    def add(self, embeddings: List[Any], metadatas: List[Dict], ids: List[str]):
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(self, query_embeddings: List[Any], n_results: int = 10) -> Optional[QueryResult]:
        if query_embeddings:
            return self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results
            )
        return None

    def delete(self):
        self.client.delete_collection(self._COLLECTION_NAME)
        self.collection = self.create()

    def count(self) -> int:
        return self.collection.count()

    def peek(self):
        return self.collection.peek()

    def __del__(self):
        if ChromaDatabase._instance == self:
            ChromaDatabase._instance = None


def _module_testing():
    database = ChromaDatabase.instance()
    tokenizer = BertTokenizer.instance()
    page = Page(PageMetadata(
        source_type=DataSourceType.PDF,
        number=0,
        path='path/to/file'
    ))
    text_data = TextData(body='Lets go for a movie tonight')
    page.add_data(text_data)
    print(page)
    database.add(
        embeddings=[tokenizer.tokenize(text_data.body).tolist()],
        metadatas=[{'page': json.dumps(page)}],
        ids=['1']
    )
    print(database.peek())
    query = 'movie tonight'
    query_embedding = tokenizer.tokenize(query)
    result = database.query([query_embedding.tolist()])
    print(result)
    database.delete()


if __name__ == '__main__':
    _module_testing()
