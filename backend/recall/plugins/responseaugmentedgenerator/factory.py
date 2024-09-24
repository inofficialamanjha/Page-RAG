from typing import Any

from backend.recall.plugins.responseaugmentedgenerator.chatgpt35turbo.chatgpt35turbo import ChatGpt35Turbo
from backend.recall.plugins.responseaugmentedgenerator.chatgpt4.chatgpt4 import ChatGpt4ResponseAugmentedGenerator
from backend.recall.plugins.responseaugmentedgenerator.interface import BaseResponseAugmentedGenerator
from backend.recall.plugins.responseaugmentedgenerator.phi3.phi3med128kinstruct import Phi3Med128kInstruct
from backend.recall.recall_utils import Phi3Med128KInstructAzureAiStudioClient, get_azure_open_ai_client
from common.configurations import Configurations
from common.constants import GeneratorType


class ResponseAugmentedGeneratorFactory:
    _instance: Any = None

    def __init__(self):
        self.configurations = Configurations.instance()

    @staticmethod
    def instance() -> Any:
        if ResponseAugmentedGeneratorFactory._instance is None:
            ResponseAugmentedGeneratorFactory._instance = ResponseAugmentedGeneratorFactory()
        return ResponseAugmentedGeneratorFactory._instance

    def get_response_augmented_generator(self) -> BaseResponseAugmentedGenerator:
        search_query_generator = self.configurations[Configurations.BACKEND_KEY][Configurations.Backend.RECALL_KEY][
            Configurations.Backend.Recall.RESPONSE_AUGMENTED_GENERATOR_KEY]
        value = GeneratorType.from_value(search_query_generator)
        if value == GeneratorType.CHATGPT4:
            return ChatGpt4ResponseAugmentedGenerator(get_azure_open_ai_client(self.configurations))
        if value == GeneratorType.PHI3MED128KINS:
            return self._get_phi3med128kins_generator()
        elif value == GeneratorType.CHATGPT35TURBO:
            return self._get_chatgpt35turbo_generator()
        raise ValueError('Invalid response augmented generator type')

    def _get_phi3med128kins_generator(self) -> BaseResponseAugmentedGenerator:
        phi3_med_128k_instruct_config = self.configurations[Configurations.BACKEND_KEY][
            Configurations.Backend.RECALL_KEY][Configurations.Backend.Recall.PHI3_MED128K_INSTRUCT_KEY]
        phi3_med_128k_instruct_azure_ai_studio_client = Phi3Med128KInstructAzureAiStudioClient(
            url=phi3_med_128k_instruct_config[Configurations.Backend.Recall.Phi3Med128KInstructService.ENDPOINT_KEY],
            api_key=phi3_med_128k_instruct_config[Configurations.Backend.Recall.Phi3Med128KInstructService.KEY]
        )
        return Phi3Med128kInstruct(phi3_med_128k_instruct_azure_ai_studio_client)

    def _get_chatgpt35turbo_generator(self) -> BaseResponseAugmentedGenerator:
        deployment_name = self.configurations[Configurations.BACKEND_KEY][Configurations.Backend.RECALL_KEY][
            Configurations.Backend.Recall.CHAT_GPT_35_TURBO_KEY][
            Configurations.Backend.Recall.ChatGpt35Turbo.DEPLOYMENT_KEY]
        return ChatGpt35Turbo(deployment_name, get_azure_open_ai_client(self.configurations))


def _module_testing():
    response_augmented_generator_factory = ResponseAugmentedGeneratorFactory()
    response_augmented_generator = response_augmented_generator_factory.get_response_augmented_generator()
    print(response_augmented_generator)


if __name__ == '__main__':
    _module_testing()
