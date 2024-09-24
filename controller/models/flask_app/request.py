import os
from dataclasses import dataclass

from werkzeug.local import LocalProxy
from flask import request as Request
from werkzeug.utils import secure_filename

from controller.utils import UPLOADS_DIR


@dataclass
class UserQueryRequest:
    query: str
    stream: bool

    USER_QUERY_KEY = 'user_query'
    TO_STREAM_KEY = 'stream'

    @staticmethod
    def from_request(request: LocalProxy) -> 'UserQueryRequest':
        assert isinstance(request, LocalProxy)
        stream = request.args.get(UserQueryRequest.TO_STREAM_KEY, default='false', type=str).lower()
        return UserQueryRequest(
            query=request.args.get(UserQueryRequest.USER_QUERY_KEY, default='', type=str),
            stream=(stream == 'true')
        )


@dataclass
class FileUploadRequest:
    file_path: str = ''

    FILE_KEY = 'file'

    @staticmethod
    def from_request(request: LocalProxy) -> 'FileUploadRequest':
        assert isinstance(request, LocalProxy)
        if FileUploadRequest.FILE_KEY in request.files:
            file = request.files[FileUploadRequest.FILE_KEY]
            file_path = os.path.join(UPLOADS_DIR, secure_filename(file.filename))

            # Create the uploads directory if it does not exist
            os.makedirs(UPLOADS_DIR, exist_ok=True)

            file.save(file_path)
            return FileUploadRequest(file_path)

        return FileUploadRequest('')


@dataclass
class SearchQueryRequest:
    search_query: str
    simplify: bool

    SEARCH_QUERY_KEY = 'search_query'
    TO_SIMPLIFY = 'simplify'

    @staticmethod
    def from_request(request: LocalProxy) -> 'SearchQueryRequest':
        assert isinstance(request, LocalProxy)
        simplify = request.args.get(SearchQueryRequest.TO_SIMPLIFY, default='false', type=str).lower()
        return SearchQueryRequest(
            search_query=request.args.get(SearchQueryRequest.SEARCH_QUERY_KEY, default='', type=str),
            simplify=(simplify == 'true')
        )
