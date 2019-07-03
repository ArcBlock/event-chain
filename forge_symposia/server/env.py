import base64
import logging
import os

from dotenv import find_dotenv, load_dotenv

from forge_symposia.server.forge import forge

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('server-env')


# dotenv_path = join(dirname(dirname(__file__)), '.env')
# logger.debug(f'env path: {dotenv_path}')


SERVER_HOST = os.getenv('SERVER_HOST')
CHAIN_HOST = os.getenv('REACT_APP_CHAIN_HOST')
APP_PK = base64.b16decode(os.getenv('REACT_APP_APP_PK'))
APP_SK = base64.b16decode(os.getenv('REACT_APP_APP_SK'))
APP_ADDR = os.getenv('REACT_APP_APP_ID')

INDEX_DB = os.path.join(forge.config.path, "index", "index.sqlite3")
logger.debug(f'index db: {INDEX_DB}')
