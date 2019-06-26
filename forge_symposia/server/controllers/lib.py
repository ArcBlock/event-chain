import logging

from forge_sdk import protos as forge_protos, utils as forge_utils

from forge_symposia.server import models
from forge_symposia.server.forge import forge

logger = logging.getLogger('server-controllers')


def get_event_state(address):
    state = forge.rpc.get_single_asset_state(address)
    if state:
        return models.EventState(state)
    else:
        logger.error(f'Fail to get asset state for event {address}')


def get_response_event(address):
    event_state = get_event_state(address)
    if event_state:
        return models.ResponseEvent(event_state)


def get_ticket_state(address):
    ticket_state = forge.rpc.get_single_asset_state(address)
    if ticket_state:
        event_state = get_event_state(ticket_state.parent)
        return models.TicketState(ticket_state, event_state)
    else:
        logger.error(f'Fail to get asset state for event {address}')


def gen_consume_tx(wallet, token=None):
    consume_itx = forge_protos.ConsumeAssetTx(issuer=wallet.address)
    logger.debug(str(forge.rpc))
    tx = forge.rpc.build_signed_tx(itx=forge_utils.encode_to_any(
            'fg:t:consume_asset', consume_itx), wallet=wallet, token=token)
    return tx.SerializeToString()
