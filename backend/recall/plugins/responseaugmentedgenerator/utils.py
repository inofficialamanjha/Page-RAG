import json
import os
from typing import List, Dict, Optional

from backend.recall.recall_utils import DEPENDENCIES_DIR
from common.constants import DataType
from models.data.interface import BaseData
from models.data.text.text import TextData

CHAT_SETUP_JSON_PATH = os.path.join(DEPENDENCIES_DIR, 'ResponseAugmentedGeneratorChatSetup.json')
DELIMITERS = {' '}


def get_request(user_query: str, datas: List[BaseData]) -> Dict:
    request_dict = {
        'userQuery': user_query,
        'recalledData': []
    }
    for data in datas:
        data_request_dict = _get_base_data_request(data)
        if data_request_dict:
            request_dict['recalledData'].append(data_request_dict)
    return request_dict


def _get_base_data_request(data: BaseData) -> Optional[Dict]:
    if data.get_data_type == DataType.TEXT:
        assert isinstance(data, TextData)
        return {
            'type': 'text',
            'content': data.body
        }
    return None
