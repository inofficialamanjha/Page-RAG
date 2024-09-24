import datetime

import numpy
from FlagEmbedding import BGEM3FlagModel

from common.configurations import Configurations
from common.utils import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


class BertTokenizer:
    _instance = None

    def __init__(self):
        configurations = Configurations.instance()

        self.embedding_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

        self.batch_size = configurations[configurations.BACKEND_KEY][configurations.Backend.TOKENIZER_KEY][
            configurations.Backend.Tokenizer.BATCH_SIZE_KEY]
        self.max_length = configurations[configurations.BACKEND_KEY][configurations.Backend.TOKENIZER_KEY][
            configurations.Backend.Tokenizer.MAX_LENGTH_KEY]

    @staticmethod
    def instance():
        if BertTokenizer._instance is None:
            BertTokenizer._instance = BertTokenizer()
        return BertTokenizer._instance

    def tokenize(self, text: str) -> numpy.ndarray:
        start_time = datetime.datetime.now()
        embedding = self.embedding_model.encode(text,
                                                batch_size=self.batch_size,
                                                max_length=self.max_length)['dense_vecs']
        _logger.info('Time taken to tokenize text: %s', datetime.datetime.now() - start_time)
        return embedding

    def __del__(self):
        if BertTokenizer._instance == self:
            BertTokenizer._instance = None


def _module_testing():
    tokenizer = BertTokenizer.instance()
    embedding = tokenizer.tokenize("Hello World!")
    print(embedding.shape)


if __name__ == '__main__':
    _module_testing()
