from typing import Any

from backend.recall.plugins.searchquerygenerator.chatgpt35turbo.chatgpt35turbo import ChatGpt35Turbo
from backend.recall.plugins.searchquerygenerator.chatgpt4.chatgpt4 import ChatGpt4SearchQueryGenerator
from backend.recall.plugins.searchquerygenerator.interface import BaseSearchQueryGenerator
from backend.recall.plugins.searchquerygenerator.self.cpuprocessing import Cpu
from backend.recall.recall_utils import get_azure_open_ai_client
from common.configurations import Configurations
from common.constants import GeneratorType


class SearchQueryGeneratorFactory:
    _instance: Any = None

    def __init__(self):
        self.configurations = Configurations.instance()

    @staticmethod
    def instance() -> Any:
        if SearchQueryGeneratorFactory._instance is None:
            SearchQueryGeneratorFactory._instance = SearchQueryGeneratorFactory()
        return SearchQueryGeneratorFactory._instance

    def get_search_query_generator(self) -> BaseSearchQueryGenerator:
        search_query_generator = self.configurations[Configurations.BACKEND_KEY][Configurations.Backend.RECALL_KEY][
            Configurations.Backend.Recall.SEARCH_QUERY_GENERATOR_KEY]
        value = GeneratorType.from_value(search_query_generator)
        if value == GeneratorType.CHATGPT4:
            return ChatGpt4SearchQueryGenerator(get_azure_open_ai_client(self.configurations))
        elif value == GeneratorType.CPU_PROCESSING:
            return Cpu()
        elif value == GeneratorType.CHATGPT35TURBO:
            return self._get_chatgpt35turbo_generator()
        raise ValueError('Invalid search query generator type')

    def _get_chatgpt35turbo_generator(self) -> BaseSearchQueryGenerator:
        deployment_name = self.configurations[Configurations.BACKEND_KEY][Configurations.Backend.RECALL_KEY][
            Configurations.Backend.Recall.CHAT_GPT_35_TURBO_KEY][
            Configurations.Backend.Recall.ChatGpt35Turbo.DEPLOYMENT_KEY]
        return ChatGpt35Turbo(deployment_name, get_azure_open_ai_client(self.configurations))


def _module_testing():
    search_query_generator_factory = SearchQueryGeneratorFactory()
    search_query_generator = search_query_generator_factory.get_search_query_generator()
    print(search_query_generator)


if __name__ == '__main__':
    _module_testing()
