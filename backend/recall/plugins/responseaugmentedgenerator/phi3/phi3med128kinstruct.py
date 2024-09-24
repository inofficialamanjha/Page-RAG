import json
from typing import List, Generator

from backend.recall.plugins.responseaugmentedgenerator.interface import BaseResponseAugmentedGenerator
from backend.recall.plugins.responseaugmentedgenerator.utils import CHAT_SETUP_JSON_PATH, get_request, DELIMITERS
from backend.recall.recall_utils import Phi3Med128KInstructAzureAiStudioChatObject, \
    Phi3Med128KInstructAzureAiStudioClient
from models.data.interface import BaseData
from models.data.text.text import TextData


class Phi3Med128kInstruct(BaseResponseAugmentedGenerator):
    def __init__(self, phi3_client: Phi3Med128KInstructAzureAiStudioClient):
        self.client = phi3_client
        self.chat_object = Phi3Med128KInstructAzureAiStudioChatObject(CHAT_SETUP_JSON_PATH, stream=True)

    def generate(self, user_query: str, datas: List[BaseData]) -> Generator[str, None, None]:
        request = json.dumps(get_request(user_query, datas))
        request_prompt = self.chat_object.contextual_prompt + [{'role': 'user', 'content': request}]

        buffer = ""

        response = self.chat_object.invoke_deployment(self.client, request_prompt)
        for item in response.iter_lines():
            if item:
                item_str = item.decode('utf-8').strip()

                if item_str == 'data: [DONE]':
                    break

                try:
                    if item_str.startswith('data:'):
                        item_str = item_str[len('data: '):]
                    completion_chunk = json.loads(item_str)

                    if 'choices' in completion_chunk and len(completion_chunk['choices']) > 0:
                        chunk_message = completion_chunk['choices'][0].get('delta', {}).get('content', '')
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

                except json.JSONDecodeError:
                    continue

        if buffer:
            yield buffer.strip()


def _module_testing():
    phi3_med_128k_instruct_azure_ai_studio_client = Phi3Med128KInstructAzureAiStudioClient(
        url='<azure-phi3-completion-url>',
        api_key='<phi3-med-instruct-key>'
    )
    response_augmented_generator = Phi3Med128kInstruct(phi3_med_128k_instruct_azure_ai_studio_client)
    user_query = 'What is the service offered by the Balaji Infratech?'
    data = [
        TextData(
            'Balaji Infratech provides a range of automation services such as traffic counting,'
            ' parking management, and toll collection.'),
        TextData('Xero Technologies is a marketing agency that provides Ai marketing services.')
    ]
    for message in response_augmented_generator.generate(user_query, data):
        print(message, end=' ', flush=True)
    print()


if __name__ == '__main__':
    _module_testing()
