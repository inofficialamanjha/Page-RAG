import json
from typing import List

from backend.recall.plugins.searchquerygenerator.interface import BaseSearchQueryGenerator
from backend.recall.plugins.searchquerygenerator.utils import CHAT_SETUP_JSON_PATH, get_request, parse_completion
from backend.recall.recall_utils import Phi3Med128KInstructAzureAiStudioClient, \
    Phi3Med128KInstructAzureAiStudioChatObject, LLM_GENERATOR_RETRY_COUNT, add_traceback_to_request_prompt


class Phi3Med128KInstruct(BaseSearchQueryGenerator):
    def __init__(self, phi3_client: Phi3Med128KInstructAzureAiStudioClient):
        self.client = phi3_client
        self.chat_object = Phi3Med128KInstructAzureAiStudioChatObject(CHAT_SETUP_JSON_PATH)

    def generate(self, user_query: str) -> List[str]:
        request = json.dumps(get_request(user_query))
        request_prompt = self.chat_object.contextual_prompt + [{'role': 'user', 'content': request}]

        for _ in range(LLM_GENERATOR_RETRY_COUNT):
            response_json = self.chat_object.invoke_deployment(self.client, request_prompt).json()
            completion = response_json['choices'][0]['message']['content']

            try:
                return parse_completion(completion)
            except Exception as exception:
                request_prompt = add_traceback_to_request_prompt(request_prompt, completion, exception)

        raise Exception('Internal server error: Unable to generate search queries')


def _module_testing():
    phi3_med_128k_instruct_azure_ai_studio_client = Phi3Med128KInstructAzureAiStudioClient(
        url='<azure-phi3-completion-url>',
        api_key='<phi3-med-instruct-key>'
    )
    phi3_med_129k_instruct = Phi3Med128KInstruct(phi3_med_128k_instruct_azure_ai_studio_client)
    print(phi3_med_129k_instruct.generate('Who is the president of America?'))


if __name__ == '__main__':
    _module_testing()
