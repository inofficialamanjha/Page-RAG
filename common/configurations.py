from dataclasses import dataclass
import json
from typing import Any

_DEFAULT_CONFIGURATIONS_FILE_PATH = 'AppSettings.json'


class Configurations(dict):
    BACKEND_KEY = 'backend'
    MODEL_KEY = 'model'
    ENVIRONMENT_KEY = 'environment'

    _instance: Any = None

    @dataclass
    class Backend:
        DATA_PARSERS_KEY = 'dataParsers'
        TOKENIZER_KEY = 'tokenizer'
        SEARCH_KEY = 'search'
        RECALL_KEY = 'recall'

        @dataclass
        class DataParsers:
            PDF_PARSER_KEY = 'pdf'

            @dataclass
            class PdfParser:
                CHUNK_SIZE_KEY = 'chunkSize'
                OVERLAP_KEY = 'overlap'

        @dataclass
        class Tokenizer:
            BATCH_SIZE_KEY = 'batchSize'
            MAX_LENGTH_KEY = 'maxLength'

        @dataclass
        class Search:
            N_RESULTS_KEY = 'nResults'
            THRESHOLD_KEY = 'threshold'

        @dataclass
        class Recall:
            AZURE_OPEN_AI_SERVICES_KEY = 'azureOpenAiService'
            PHI3_MED128K_INSTRUCT_KEY = 'phi3Med128KInstructService'
            CHAT_GPT_35_TURBO_KEY = 'chatGpt35Turbo'
            RESPONSE_AUGMENTED_GENERATOR_KEY = 'responseAugmentedGenerator'
            SEARCH_QUERY_GENERATOR_KEY = 'searchQueryGenerator'

            @dataclass
            class AzureOpenAiService:
                ENDPOINT_KEY = 'endpoint'
                KEY = 'key'
                API_VERSION = 'apiVersion'

            @dataclass
            class Phi3Med128KInstructService:
                ENDPOINT_KEY = 'endpoint'
                KEY = 'key'

            @dataclass
            class ChatGpt35Turbo:
                DEPLOYMENT_KEY = 'deploymentName'

    @dataclass
    class Model:
        DATA_KEY = 'data'

        @dataclass
        class Data:
            TEXT_KEY = 'text'

            @dataclass
            class Text:
                CHUNK_SIZE_KEY = 'chunkSize'
                OVERLAP_KEY = 'overlap'

    def __init__(self, file_path: str = _DEFAULT_CONFIGURATIONS_FILE_PATH):
        super().__init__()
        with open(file_path, 'r') as file:
            self.update(json.load(file))
        self._validate()

    @staticmethod
    def instance() -> Any:
        if Configurations._instance is None:
            Configurations._instance = Configurations()
        return Configurations._instance

    def _validate(self):
        if self[self.MODEL_KEY][self.Model.DATA_KEY][self.Model.Data.TEXT_KEY][self.Model.Data.Text.CHUNK_SIZE_KEY] > \
                self[self.BACKEND_KEY][self.Backend.TOKENIZER_KEY][self.Backend.Tokenizer.MAX_LENGTH_KEY]:
            raise ValueError('Chunk size should be less than or equal to max length')

    def __del__(self):
        if Configurations._instance == self:
            Configurations._instance = None


def _module_testing():
    configurations = Configurations.instance()
    print(configurations)


if __name__ == '__main__':
    _module_testing()
