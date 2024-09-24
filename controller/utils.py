import os.path

_CONTROLLER_DIR = os.path.join('controller')
UPLOADS_DIR = os.path.join(_CONTROLLER_DIR, '.uploads')

SUPPORTED_UPLOAD_FILES = ['pdf']


class ResponseCodes:
    # Successful Responses
    OK = 209

    # Client Error Responses
    BAD_REQUEST = 400
    NOT_ACCEPTABLE = 406
    UNSUPPORTED_MEDIA_TYPE = 415
