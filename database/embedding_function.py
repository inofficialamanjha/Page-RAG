import numpy as np
from chromadb import EmbeddingFunction, Documents, Embeddings

from common.configurations import Configurations


class DummyEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        configurations = Configurations.instance()
        self.max_length = configurations[configurations.BACKEND_KEY][configurations.Backend.TOKENIZER_KEY][
            configurations.Backend.Tokenizer.MAX_LENGTH_KEY]
        self.dummy_np_array = np.zeros((self.max_length,))

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for _ in input:
            embeddings.append(self.dummy_np_array.tolist())
        return embeddings


def _module_testing():
    embedding_function = DummyEmbeddingFunction()
    dummy_embeddings = embedding_function.__call__(["Hello World!"])
    for dummy_embedding in dummy_embeddings:
        print(dummy_embedding)


if __name__ == '__main__':
    _module_testing()
