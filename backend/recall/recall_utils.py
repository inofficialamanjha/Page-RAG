import json
import os.path
from typing import Dict, List, Union, Any, Optional
import requests
from requests import Response

from openai import Stream
from openai.lib.azure import AzureOpenAI
from openai.types.chat import ChatCompletion

from common.configurations import Configurations

DEPENDENCIES_DIR = os.path.join('backend', 'recall', 'dependencies')
LLM_GENERATOR_RETRY_COUNT = 3


def add_traceback_to_request_prompt(request_prompt: List[Dict[str, str]], completion: str, exception: Exception) -> \
        List[Dict[str, str]]:
    """
    Add traceback to the request prompt
    """
    return request_prompt + [{'role': 'assistant', 'content': f'{completion}'},
                             {'role': 'user',
                              'content': f'Regenerate the json response again.\n'
                                         f'Got the following error and traceback while parsing the response:\n'
                                         f'Exception: {exception}'}]


def get_azure_open_ai_client(configurations: Configurations) -> AzureOpenAI:
    azure_open_ai_services_config = \
        configurations[Configurations.BACKEND_KEY][Configurations.Backend.RECALL_KEY][
            Configurations.Backend.Recall.AZURE_OPEN_AI_SERVICES_KEY]
    return AzureOpenAI(
        api_version=azure_open_ai_services_config[Configurations.Backend.Recall.AzureOpenAiService.API_VERSION],
        azure_endpoint=azure_open_ai_services_config[
            Configurations.Backend.Recall.AzureOpenAiService.ENDPOINT_KEY],
        api_key=azure_open_ai_services_config[Configurations.Backend.Recall.AzureOpenAiService.KEY],
    )


class AzureOpenAIChatObject:
    """
    Azure OpenAI Chat Object

    Loads json configurations for prompting LLM's on Azure Ai Studio
    """

    def __init__(self, setup_json: str, stream: bool = False):
        with open(setup_json, 'r', encoding='utf-8') as file:
            setup_dict = json.load(file)
        self.contextual_prompt = get_contextual_prompt(setup_dict)
        chat_parameters = setup_dict['chatParameters']
        self.deployment_name = chat_parameters['deploymentName']
        self.temperature = chat_parameters['temperature']
        self.max_tokens = chat_parameters['maxResponseLength']
        self.top_p = chat_parameters['topProbablities']
        self.frequency_penalty = chat_parameters['frequencyPenalty']
        self.presence_penalty = chat_parameters['presencePenalty']
        self.stop = chat_parameters['stopSequences']
        self.stream = stream

    def get_completion(self, azure_open_ai_client: AzureOpenAI, request_prompt: List[Dict[str, str]]) \
            -> Union[ChatCompletion, Stream[ChatCompletion]]:
        """
        Get the completion from Azure OpenAI

        Args:
            azure_open_ai_client: AzureOpenAI Client
            request_prompt: List of dictionaries containing the request prompt

        Returns:
            The completion (message) from Azure OpenAI LLM
        """
        return azure_open_ai_client.chat.completions.create(
            model=self.deployment_name,
            messages=request_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            stop=self.stop,
            stream=self.stream
        )


class Phi3Med128KInstructAzureAiStudioClient:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key

    def get_completion(self, data: Dict[str, Any]) -> Response:
        stream = data[Phi3Med128KInstructAzureAiStudioChatObject.STREAM_KEY]

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'text/event-stream' if stream else 'application/json'
        }

        response = requests.post(
            url=self.url,
            headers=headers,
            json=data
        )

        response.raise_for_status()
        return response


class Phi3Med128KInstructAzureAiStudioChatObject:
    STREAM_KEY = 'stream'

    def __init__(self, setup_json: str, stream: bool = False):
        with open(setup_json, 'r', encoding='utf-8') as file:
            setup_dict = json.load(file)
            self.contextual_prompt = get_contextual_prompt(setup_dict)
            self.max_token = 1024
            self.temperature = 0.7
            self.top_p = 1
            self.stream = stream

    def invoke_deployment(self, client: Phi3Med128KInstructAzureAiStudioClient,
                          request_prompt: List[Dict[str, str]]) -> Response:
        data = {
            'messages': request_prompt,
            'max_tokens': self.max_token,
            'temperature': self.temperature,
            'top_p': self.top_p,
            self.STREAM_KEY: self.stream
        }

        return client.get_completion(data)


def get_contextual_prompt(setup_dict: Dict) -> List[Dict[str, str]]:
    contextual_prompt: List[Dict[str, str]] = []

    # Fetch the system prompt
    if 'systemPrompt' in setup_dict:
        contextual_prompt.append({'role': 'system', 'content': f'{setup_dict["systemPrompt"]}'})

    # Load the fewShotExamples
    if 'fewShotExamples' in setup_dict:
        for few_shot_example in setup_dict['fewShotExamples']:
            if 'userInput' in few_shot_example:
                contextual_prompt.append({'role': 'user', 'content': f'{few_shot_example["userInput"]}'})
            if 'chatbotResponse' in few_shot_example:
                contextual_prompt.append({'role': 'assistant', 'content': f'{few_shot_example["chatbotResponse"]}'})

    return contextual_prompt


def _module_testing(test: Optional[str] = None):
    sample_chat_setup = os.path.join(DEPENDENCIES_DIR, 'SampleChatSetup.json')

    if test == 'azure':
        azure_client = AzureOpenAI(
            api_key='<azure-openai-service-key>',
            api_version='2024-02-15-preview',
            azure_endpoint='<azure-openai-endpoint>'
        )
        azure_chat_object = AzureOpenAIChatObject(sample_chat_setup)
        request_prompt = azure_chat_object.contextual_prompt
        print(request_prompt)
        request_prompt = request_prompt + [{'role': 'user', 'content': 'Tell me a joke'}]
        completion = azure_chat_object.get_completion(azure_client, request_prompt).choices[0].message.content
        print(completion)
        request_prompt = request_prompt + [
            {'role': 'user', 'content': 'Can you tell me something about London. How can I travel there?'}]
        completion = azure_chat_object.get_completion(azure_client, request_prompt).choices[0].message.content
        print(completion)

    elif test == 'phi3':
        phi3_med_128k_instruct_azure_ai_studio_client = Phi3Med128KInstructAzureAiStudioClient(
            url='<azure-phi3-completions-url>',
            api_key='<phi3-med-instruct-key>'
        )
        phi3_med_128k_instruct_azure_ai_studio_chat_object = Phi3Med128KInstructAzureAiStudioChatObject(
            sample_chat_setup,
        )
        request_prompt = phi3_med_128k_instruct_azure_ai_studio_chat_object.contextual_prompt
        print(request_prompt)
        request_prompt = request_prompt + [{'role': 'user', 'content': 'Tell me a joke'}]
        completion = phi3_med_128k_instruct_azure_ai_studio_chat_object.invoke_deployment(
            phi3_med_128k_instruct_azure_ai_studio_client, request_prompt
        )
        if phi3_med_128k_instruct_azure_ai_studio_chat_object.stream:
            for item in completion.iter_lines():
                print(item)
        else:
            print(completion.json())


if __name__ == '__main__':
    _module_testing('phi3')
