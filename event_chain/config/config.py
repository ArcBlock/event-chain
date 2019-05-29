import logging
import os
import os.path as path

from forge_sdk import rpc
from forge_sdk.config import config as forge_config


logger = logging.getLogger('ec-config')

app_config_path = path.join(path.dirname(__file__), "forge.toml")

# APP_SK = 'zyQBXZ7NijYQQRzLUryjkd1Mj4qSpofcnsgEh8a8ZrtbgM1jSKHrC85V' \
#          'edZsQ5N3x5M298zpridcq2bKBZtmqroT'
# APP_PK = "zExrfT2pXtVqdAqgZwjvdMBo5RpqSqn1fa43Wp93peuSR"
# APP_ADDR = "z1UT9an1Z4W1gnmzASneER2J5eqtx5jfwgx"

APP_SK = b'0\243\016\303\017\r\305\026#~\301\227\033;\274\303pl\243 \004,' \
         b'\224c\003\261\2629&G\345\020\317w\007P\234\211g\246Q\264P\325\346' \
         b'/}E\020\304\365\216\242\033o\302\206v\203\303+\206n\212'

APP_PK = b'\317w\007P\234\211g\246Q\264P\325\346/}E\020\304\365\216\242\033o' \
         b'\302\206v\203\303+\206n\212'
APP_ADDR = "z1UT9an1Z4W1gnmzASneER2J5eqtx5jfwgx"

ARC = 'https://abtwallet.io/i/'

app_path = forge_config.get_app_path()

forge_path = forge_config.get_forge_path()

app_host = forge_config.get_app_host()

forge_port = forge_config.get_forge_port()

db_path = path.join(forge_path, "index", "index.sqlite3")

googlemaps_key = os.environ.get('GOOGLEMAPS_KEY')

chain_info = rpc.get_chain_info().info
chain_id = chain_info.network

SERVER_ADDRESS = "http://" + app_host + ":5000"

if not os.path.exists(app_path):
    os.system('mkdir -p {}'.format(app_path))
    logger.info("{} created.".format(app_path))
