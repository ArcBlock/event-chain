import logging

from forge_sdk import did, rpc, utils as forge_utils

from event_chain import protos

logger = logging.getLogger('ec-controller')


def buy_tickets_general(event_address, num, wallet, token=None):
    spec_datas = []
    for i in range(0, num):
        spec_datas.append({'id': did.AbtDid(role_type='asset').new()})

    res, tickets = rpc.acquire_asset(event_address, spec_datas,
                                     'ec:s:general_ticket', protos, wallet,
                                     token)
    if forge_utils.is_response_ok(res):
        return tickets
    else:
        logger.error(f"Fail to buy tickets for event {event_address}")
