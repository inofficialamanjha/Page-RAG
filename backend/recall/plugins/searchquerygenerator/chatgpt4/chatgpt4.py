import json
import os
from typing import List, Dict

from openai.lib.azure import AzureOpenAI

from backend.recall.plugins.searchquerygenerator.interface import BaseSearchQueryGenerator
from backend.recall.plugins.searchquerygenerator.utils import CHAT_SETUP_JSON_PATH, parse_completion, get_request
from backend.recall.recall_utils import AzureOpenAIChatObject, DEPENDENCIES_DIR, LLM_GENERATOR_RETRY_COUNT, \
    add_traceback_to_request_prompt


class ChatGpt4SearchQueryGenerator(BaseSearchQueryGenerator):
    def __init__(self, az_openai_client: AzureOpenAI):
        self.client = az_openai_client
        self.chat_object = AzureOpenAIChatObject(CHAT_SETUP_JSON_PATH)

    def generate(self, user_query: str) -> List[str]:
        request = json.dumps(get_request(user_query))
        request_prompt = self.chat_object.contextual_prompt + [{'role': 'user', 'content': request}]

        for _ in range(LLM_GENERATOR_RETRY_COUNT):
            completion = self.chat_object.get_completion(self.client, request_prompt).choices[0].message.content
            try:
                return parse_completion(completion)
            except Exception as exception:
                request_prompt = add_traceback_to_request_prompt(request_prompt, completion, exception)

        raise Exception('Internal server error: Unable to generate search queries')


def _module_testing():
    azure_client = AzureOpenAI(
        api_key='<azure-openai-service-key>',
        api_version='2024-02-15-preview',
        azure_endpoint='<azure-openai-endpoint>'
    )
    search_query_generator = ChatGpt4SearchQueryGenerator(azure_client)
    print(search_query_generator.generate('Who is the president of America?'))


if __name__ == '__main__':
    _module_testing()
