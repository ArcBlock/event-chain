import logging

from forge_sdk import did as forge_did, rpc as forge_rpc
from forge_sdk import utils as forge_utils

from event_chain import protos
from event_chain.app import models

logger = logging.getLogger('controller-ticket')


def buy_tickets_general(event_address, num, wallet, token=None):
    spec_datas = []
    for i in range(0, num):
        spec_datas.append({'id': forge_did.AbtDid(role_type='asset').new()})

    res, tickets = forge_rpc.acquire_asset(to=event_address,
                                           spec_datas=spec_datas,
                                           type_url='ec:s:general_ticket',
                                           proto_lib=protos, wallet=wallet,
                                           token=token)
    if forge_utils.is_response_ok(res):
        return tickets
    else:
        logger.error(f"Fail to buy tickets for event {event_address}")


def buy_ticket(event_address, user):
    logger.debug(f'user wallet: {user.get_wallet()}')
    ticket_address = buy_tickets_general(event_address, 1,
                                         user.get_wallet(), user.token)
    logger.debug(f"Buy ticket process is completed. ticket {ticket_address}")
    return ticket_address


def consume(ticket_address, user):
    logger.debug("Consuming ticket {}".format(ticket_address))
    ticket = models.get_ticket_state(ticket_address)
    logger.debug("Event is  {}".format(ticket.ticket_info.event_address))
    consume_tx = models.get_event_state(
            ticket.ticket_info.event_address,
    ).event_info.consume_tx
    if not consume_tx:
        return None

    logger.debug("consume tx: {}".format(consume_tx))

    res = ticket.consume(consume_tx, user.get_wallet(), user.token)

    if res.code != 0 or res.hash is None:
        logger.error(res)
        logger.error('Fail to consume ticket {}'.format(ticket_address))
    else:
        logger.info(
                "ConsumeTx has been sent by tx: {}!".format(res.hash),
        )
    return res.hash


def verify_ticket_address(ticket_address):
    try:
        state = models.get_ticket_state(ticket_address)
    except Exception:
        logger.error('Error in checking ticket')
        raise TypeError("{} is not an ticket address.".format(ticket_address))

    if not state:
        logger.error(u'Ticket {} does not exist.'.format(ticket_address))
        raise ValueError('Ticket {} does not exist'.format(ticket_address))


def list_user_tickets(user_address):
    assets = models.sql.AssetState.query.filter_by(owner=user_address).all()
    tickets = []
    for asset in assets:
        asset_state = forge_rpc.get_single_asset_state(asset.address)
        if asset_state and asset_state.data.type_url == 'ec:s:general_ticket':
            tickets.append(asset_state)
    return tickets
