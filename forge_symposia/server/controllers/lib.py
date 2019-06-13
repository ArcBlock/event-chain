import logging

from forge_symposia.server import models
from forge_symposia.server.forge import forge

logger = logging.getLogger('server-controllers')


def get_event_state(address):
    state = forge.rpc.get_single_asset_state(address)
    if state:
        logger.error(f'Fail to get asset state for event {address}')
        return models.EventState(state)


def get_response_event(address):
    event_state = get_event_state(address)
    if event_state:
        return models.ResponseEvent(event_state)
