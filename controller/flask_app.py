import datetime
import os
from typing import List, Tuple, Any

from werkzeug.utils import secure_filename

from backend.pipeline.pipeline import Pipeline
from backend.recall.recall import Recall
from flask import request, jsonify, Response, Flask, make_response

from common.constants import DataType
from controller.models.flask_app.request import UserQueryRequest, FileUploadRequest, SearchQueryRequest
from controller.utils import ResponseCodes, SUPPORTED_UPLOAD_FILES
from controller.models.flask_app.response import UserQueryResponse, FileUploadResponse, ErrorResponse, \
    SearchQueryResponse
from common.utils import logging
from models.page.page import Page
from models.page.page_data.factory import PageDataFactory

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

recall = Recall.instance()
pipeline = Pipeline.instance()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1 GB


@app.get('/')
def home():
    return '<p>Welcome to PageRAG Flask Application Server</p>'


@app.post('/upload_files/')
def upload_files() -> Tuple[Response, Any]:
    """
    Make sure to set the `enctype="multipart/form-data"` in the form otherwise the browser will not upload the file
    """
    file_upload_request = FileUploadRequest.from_request(request)
    if not file_upload_request.file_path:
        return jsonify(ErrorResponse('Invalid file upload request').to_dict()), ResponseCodes.BAD_REQUEST

    if any(file_upload_request.file_path.endswith(file_type) for file_type in SUPPORTED_UPLOAD_FILES):
        pipeline.process(file_upload_request.file_path)
        os.remove(file_upload_request.file_path)
        return jsonify(FileUploadResponse(uploaded=True).to_dict()), ResponseCodes.OK

    os.remove(file_upload_request.file_path)
    return jsonify(ErrorResponse('Unsupported file type').to_dict()), ResponseCodes.UNSUPPORTED_MEDIA_TYPE


@app.get('/query/')
def query() -> Tuple[Response, Any]:
    user_query_request = UserQueryRequest.from_request(request)
    if not user_query_request.query:
        return jsonify(ErrorResponse('Invalid user query').to_dict()), ResponseCodes.BAD_REQUEST

    start_time = datetime.datetime.now()
    if user_query_request.stream:
        def _generate_response():
            for response_word in recall.query(user_query_request.query):
                if response_word and response_word != '':
                    yield response_word + ' '
            _logger.info('Total processing time for query %s: %s', user_query_request.query,
                         datetime.datetime.now() - start_time)

        return Response(_generate_response(), content_type='text/plain'), ResponseCodes.OK
    else:
        collected_response: List[str] = []
        for response_word in recall.query(user_query_request.query):
            if response_word and response_word != '':
                collected_response.append(response_word)
        response = ' '.join(collected_response)
        _logger.info('Total processing time for query %s: %s', user_query_request.query,
                     datetime.datetime.now() - start_time)
        return jsonify(UserQueryResponse(response).to_dict()), ResponseCodes.OK


@app.get('/search/')
def search() -> Tuple[Response, Any]:
    search_query_request = SearchQueryRequest.from_request(request)
    if not search_query_request.search_query:
        return jsonify(ErrorResponse('Invalid search query').to_dict()), ResponseCodes.BAD_REQUEST

    start_time = datetime.datetime.now()
    if search_query_request.simplify:
        search_queries = recall.get_search_query(search_query_request.search_query)
    else:
        search_queries = [search_query_request.search_query]

    final_search_results = recall.get_final_search_results(search_queries)
    text_response: List[str] = []

    for page in final_search_results:
        page_datas = page[Page.DATA_KEY]
        for page_data in page_datas:
            data = PageDataFactory.from_page_data(page_data)
            if data:
                if data.get_data_type == DataType.TEXT:
                    text_response.append(data.__str__())

    _logger.info('Total processing time for search query %s: %s', search_query_request.search_query,
                 datetime.datetime.now() - start_time)
    return jsonify(SearchQueryResponse(text_response).to_dict()), ResponseCodes.OK


@app.errorhandler(413)
def too_large(e):
    return make_response(jsonify(message="File is too large"), 413)


def _module_testing():
    # URL Testing session
    app.run()


if __name__ == '__main__':
    _module_testing()
