from typing import List

from openai.lib.azure import AzureOpenAI

from backend.recall.plugins.searchquerygenerator.chatgpt4.chatgpt4 import ChatGpt4SearchQueryGenerator
from backend.recall.plugins.searchquerygenerator.interface import BaseSearchQueryGenerator


class ChatGpt35Turbo(BaseSearchQueryGenerator):
    def __init__(self, deployment_name: str, az_openai_client: AzureOpenAI):
        chat_gpt4_search_query_generator = ChatGpt4SearchQueryGenerator(az_openai_client)
        chat_gpt4_search_query_generator.chat_object.deployment_name = deployment_name
        self.generator = chat_gpt4_search_query_generator

    def generate(self, user_query: str) -> List[str]:
        return self.generator.generate(user_query)


def _module_testing():
    azure_client = AzureOpenAI(
        api_key='<azure-openai-service-key>',
        api_version='2024-02-15-preview',
        azure_endpoint='<azure-openai-endpoint>'
    )
    search_query_generator = ChatGpt35Turbo('gpt-35-turbo', azure_client)
    print(search_query_generator.generate('Who is the president of America?'))


if __name__ == '__main__':
    _module_testing()
