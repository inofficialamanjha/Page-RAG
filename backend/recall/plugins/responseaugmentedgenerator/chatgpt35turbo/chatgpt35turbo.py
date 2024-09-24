from typing import List, Generator

from openai.lib.azure import AzureOpenAI

from backend.recall.plugins.responseaugmentedgenerator.chatgpt4.chatgpt4 import ChatGpt4ResponseAugmentedGenerator
from backend.recall.plugins.responseaugmentedgenerator.interface import BaseResponseAugmentedGenerator
from models.data.interface import BaseData
from models.data.text.text import TextData


class ChatGpt35Turbo(BaseResponseAugmentedGenerator):
    def __init__(self, deployment_name: str, az_openai_client: AzureOpenAI):
        chat_gpt4_response_augmented_generator = ChatGpt4ResponseAugmentedGenerator(az_openai_client)
        chat_gpt4_response_augmented_generator.chat_object.deployment_name = deployment_name
        self.generator = chat_gpt4_response_augmented_generator

    def generate(self, user_query: str, datas: List[BaseData]) -> Generator[str, None, None]:
        return self.generator.generate(user_query, datas)


def _module_testing():
    azure_client = AzureOpenAI(
        api_key='<azure-openai-service-key>',
        api_version='2024-02-15-preview',
        azure_endpoint='<azure-openai-endpoint>'
    )
    response_augmented_generator = ChatGpt35Turbo('gpt-35-turbo', azure_client)
    user_query = 'What is the service offered by the Balaji Infratech?'
    data = [
        TextData(
            'Balaji Infratech provided a range of automation services such as traffic counting,'
            ' parking management, and toll collection.'),
        TextData('Xero Technologies is a marketing agency that provides Ai marketing services.')
    ]
    for message in response_augmented_generator.generate(user_query, data):
        print(message, end=' ', flush=True)
    print()


if __name__ == '__main__':
    _module_testing()
