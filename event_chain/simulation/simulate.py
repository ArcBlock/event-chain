import json
import logging
import os
import uuid

from event_chain.application import controllers

logger = logging.getLogger('ec-simulator')

DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_data.json")

with open(DATA_PATH, "r") as read_file:
    data = json.load(read_file)


def simulate():
    users = data.get('users')
    events = data.get('events')

    test_user = None

    logger.info("Creating Users...")
    for user in users:
        test_user = controllers.register_user(
            user.get('moniker'),
            user.get('passphrase')
        )

    logger.info("Users are created.")

    logger.info("Creating Events...")
    for event in events:
        event['description'] = event['description'] + str(uuid.uuid4())
        controllers.create_event_general(test_user.get_wallet(), **event)
    logger.info("All simulated events are created.")


if __name__ == '__main__':
    simulate()
    logger.info("Data has been simulated.")
