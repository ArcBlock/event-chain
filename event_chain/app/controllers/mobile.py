import logging
from datetime import datetime

from event_chain.app import db
from event_chain.app import models
from event_chain.app import utils
from event_chain.config import config

from forge_sdk import rpc as forge_rpc
from forge_sdk import utils as forge_utils
from forge_sdk import protos as forge_protos

logger = logging.getLogger('controller-mobile')


def buy_ticket_mobile(tx, signature):

    acquire_asset_tx = forge_utils.parse_to_proto(tx.itx.value,
                                                  forge_protos.AcquireAssetTx)

    tx.signature = signature

    ticket_address = acquire_asset_tx.specs[0].address
    res = forge_rpc.send(tx)
    if forge_utils.is_response_ok(res):
        return ticket_address, hash
    else:
        return None, None


def consume_ticket_mobile(ticket, consume_tx, address, signature, user_pk):
    res = ticket.consume_mobile(consume_tx, address, signature, user_pk)

    if res.code != 0 or res.hash is None:
        logger.error(res)
        logger.error(
            'Fail to consume ticket by mobile {}'.format(ticket.address),
        )
    else:
        logger.info("Mobile ConsumeTx has been sent by tx: {}!".format(
            res.hash,
        ))
    return res.hash


def gen_poke_tx(address, pk):
    poke_itx = forge_protos.PokeTx(
        date=str(
            datetime.now().date()),
        address='zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',
    )
    itx = forge_utils.encode_to_any('fg:t:poke', poke_itx)
    params = {
        'from': address,
        'chain_id': config.chain_id,
        'nonce': 0,
        'pk': pk,
        'itx': itx
    }
    return forge_protos.Transaction(**params)


def send_poke_tx(poke_tx, signature):
    complete_tx = utils.update_tx_signature(poke_tx, signature)
    res = forge_rpc.send_tx(complete_tx)
    if res.code != 0:
        logger.error('Fail to send poke tx.')
        logger.error(res)
    else:
        return res.hash
