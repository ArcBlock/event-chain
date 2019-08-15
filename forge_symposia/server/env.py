import base64
import logging
import os
import pathlib

from forge_symposia.server.forge import forge

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('server-env')

SERVER_HOST = os.getenv('SERVER_HOST')
CHAIN_HOST = os.getenv('REACT_APP_CHAIN_HOST')
APP_PK = base64.b16decode(os.getenv('REACT_APP_APP_PK'))
APP_SK = base64.b16decode(os.getenv('REACT_APP_APP_SK'))
APP_ADDR = os.getenv('REACT_APP_APP_ID')

INDEX_DB = os.path.join(forge.config.path, "index", "index.sqlite3")
APP_DB = os.path.join(os.path.dirname(forge.config.path), "ec_app/app.db")
FORGE_SWAP_API = f'{os.getenv("FORGE_SWAP")}/api/swap'

pathlib.Path(APP_DB).parent.mkdir(parents=True, exist_ok=True)

logger.debug(f'index db: {INDEX_DB}')
logger.debug(f'app db: {os.path.dirname(APP_DB)}')
