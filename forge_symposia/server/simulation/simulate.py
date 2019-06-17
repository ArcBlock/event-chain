import json
import logging
import os
import uuid

from forge_symposia.server import controllers
from forge_symposia.server.app import forge

logger = logging.getLogger('ec-simulator')

DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_data.json")

with open(DATA_PATH, "r") as read_file:
    data = json.load(read_file)


def simulate():

    events = data.get('events')

    test_user = forge.rpc.create_wallet(moniker='alice', passphrase='abcd1234')

    logger.info("Creating Events...")
    for event in events:
        event['description'] = event['description'] + str(uuid.uuid4())
        controllers.create_event_general(wallet=test_user.wallet,
                                         token=test_user.token,
                                         **event)
    logger.info("All simulated events are created.")


if __name__ == '__main__':
    simulate()
    logger.info("Data has been simulated.")
