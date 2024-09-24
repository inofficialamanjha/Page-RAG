from dataclasses import dataclass
from typing import List


@dataclass
class UserQueryResponse:
    response: str

    RESPONSE_KEY = 'response'

    def to_dict(self):
        return {
            self.RESPONSE_KEY: self.response
        }


@dataclass
class FileUploadResponse:
    uploaded: bool

    IS_UPLOADED_KEY = 'isUploaded'

    def to_dict(self):
        return {
            self.IS_UPLOADED_KEY: self.uploaded
        }


@dataclass
class SearchQueryResponse:
    response: List[str]

    RESPONSE_KEY = 'response'

    def to_dict(self):
        return {
            self.RESPONSE_KEY: self.response
        }


@dataclass
class ErrorResponse:
    error: str

    ERROR_KEY = 'error'

    def to_dict(self):
        return {
            self.ERROR_KEY: self.error
        }
