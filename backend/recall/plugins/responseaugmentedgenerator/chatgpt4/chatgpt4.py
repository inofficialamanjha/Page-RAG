import json
import os.path
from typing import List, Dict, Optional, Generator

from openai.lib.azure import AzureOpenAI

from backend.recall.plugins.responseaugmentedgenerator.interface import BaseResponseAugmentedGenerator
from backend.recall.plugins.responseaugmentedgenerator.utils import get_request, DELIMITERS, CHAT_SETUP_JSON_PATH
from backend.recall.recall_utils import AzureOpenAIChatObject, DEPENDENCIES_DIR
from common.constants import DataType
from models.data.interface import BaseData
from models.data.text.text import TextData


class ChatGpt4ResponseAugmentedGenerator(BaseResponseAugmentedGenerator):
    def __init__(self, az_openai_client: AzureOpenAI):
        self.client = az_openai_client
        self.chat_object = AzureOpenAIChatObject(CHAT_SETUP_JSON_PATH, stream=True)

    def generate(self, user_query: str, datas: List[BaseData]) -> Generator[str, None, None]:
        request = json.dumps(get_request(user_query, datas))
        request_prompt = self.chat_object.contextual_prompt + [{'role': 'user', 'content': request}]

        buffer = ""

        for chunk in self.chat_object.get_completion(self.client, request_prompt):
            if len(chunk.choices) > 0:
                chunk_message = chunk.choices[0].delta.content
                if chunk_message:
                    buffer += chunk_message

                while True:
                    for i, char in enumerate(buffer):
                        if char in DELIMITERS:
                            word = buffer[:i + 1].strip()
                            buffer = buffer[i + 1:].lstrip()
                            if word:
                                yield word
                            break
                    else:
                        break

        # Yield any remaining text in the buffer as the last word
        if buffer:
            yield buffer.strip()


def _module_testing():
    azure_client = AzureOpenAI(
        api_key='<azure-openai-service-key>',
        api_version='2024-02-15-preview',
        azure_endpoint='<azure-openai-endpoint>'
    )
    response_augmented_generator = ChatGpt4ResponseAugmentedGenerator(azure_client)
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
