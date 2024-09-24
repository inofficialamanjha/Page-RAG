import logging

LOGGING_DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOGGING_DEFAULT_FORMAT, force=True)
