import json
import os
from typing import List, Dict

from backend.recall.recall_utils import DEPENDENCIES_DIR

CHAT_SETUP_JSON_PATH = os.path.join(DEPENDENCIES_DIR, 'SearchQueryChatSetup.json')


def get_request(user_query: str) -> Dict:
    return {
        'userQuery': user_query
    }


def parse_completion(completion_to_parse: str) -> List[str]:
    completion_dict = json.loads(completion_to_parse)
    if completion_dict['code'] == 400:
        return []
    elif completion_dict['code'] == 200:
        search_queries = completion_dict['response']['searchQueries']
        for _ in search_queries:
            if not isinstance(_, str):
                raise ValueError('Invalid response: field "searchQueries" is not a list of strings')
        return search_queries
    else:
        raise ValueError('Invalid response: field "code" is not a valid value')
