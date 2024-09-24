import argparse
import datetime
import sys
from typing import List, Optional

import waitress

from backend.pipeline.pipeline import Pipeline
from backend.recall.recall import Recall
from common.configurations import Configurations
from common.constants import Environment
from controller.flask_app import app
from database.chromadatabase import ChromaDatabase
from common.utils import logging

_MIN_PYTHON_VERSION = (3, 11)
if sys.version_info < _MIN_PYTHON_VERSION:
    sys.exit(f'Python version {".".join(map(str, _MIN_PYTHON_VERSION))} or higher is required to run this script')

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f'Startup script for calling agent')

    parser.add_argument('--files', type=str, default=[], nargs='+', help='Files to be processed')

    group_database = parser.add_argument_group('Database')
    group_database.add_argument('--save', default=False, action='store_true',
                                help='Save the data to database')
    group_database.add_argument('--reset', default=False, action='store_true',
                                help='Clear previous existing database')

    group_runtime = parser.add_argument_group('Runtime')
    group_runtime.add_argument('--host', default=False, action='store_true',
                               help='Host the application as a flask server')

    return parser.parse_args()


def _start(opt: argparse.Namespace, environment: Optional[Environment]):
    pipeline = Pipeline.instance()
    chroma_database = ChromaDatabase.instance()

    if opt.reset:
        chroma_database.delete()

    for file in opt.files:
        pipeline.process(file)

    if opt.host:
        _start_server(environment)
    else:
        _start_console()

    if not opt.save:
        chroma_database.delete()


def _start_server(environment: Optional[Environment]):
    try:
        if environment == Environment.PROD:
            _logger.info('Starting the server in production environment')
            waitress_logger = logging.getLogger('waitress')
            waitress_logger.setLevel(logging.INFO)
            waitress.serve(app, host='0.0.0.0', port=5000)
        else:
            _logger.info('Starting the server in development environment')
            app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception:
        _logger.info('Exiting the server')


def _start_console():
    recall = Recall.instance()

    print('Hey human, I am your assistant. Ask me anything. Type "exit" to exit.')
    while True:
        query = input('Enter your query: ')
        if 'exit' in query.split()[0].lower():
            break
        start_time = datetime.datetime.now()
        response_chunk_times: List[datetime.datetime] = []
        for response_word in recall.query(query):
            if response_word and response_word != '':
                print(response_word, end=' ', flush=True)
                response_chunk_times.append(datetime.datetime.now())
        _logger.info('Total time taken to generate response to the query %s: %s', query,
                     datetime.datetime.now() - start_time)
        _logger.info('Time taken to generate response chunks: %s',
                     [response_chunk_time - start_time for response_chunk_time in response_chunk_times])
        print()


def process_args(opt: argparse.Namespace):
    if not opt.files:
        opt.save = True
        opt.reset = False

    if opt.host:
        opt.save = True


if __name__ == '__main__':
    configurations = Configurations.instance()
    args = parse_args()
    process_args(args)
    _start(args, Environment.from_value(configurations[Configurations.ENVIRONMENT_KEY]))
