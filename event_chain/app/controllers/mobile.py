import logging
from datetime import datetime

from forge_sdk import did as forge_did
from forge_sdk import protos as forge_protos
from forge_sdk import rpc as forge_rpc
from forge_sdk import utils as forge_utils

from event_chain.app import utils
from event_chain.config import config

logger = logging.getLogger('controller-mobile')


def buy_ticket_mobile(tx, signature):
    acquire_asset_tx = forge_utils.parse_to_proto(tx.itx.value,
                                                  forge_protos.AcquireAssetTx)

    tx.signature = signature

    ticket_address = acquire_asset_tx.specs[0].address
    res = forge_rpc.send_tx(tx)
    if forge_utils.is_response_ok(res):
        return ticket_address, res.hash
    else:
        return None, None


def consume_ticket_mobile(origin_tx, signature, ticket_address):
    new_tx = build_cosnume_ticket_mobile_tx(origin_tx, signature, )
    res = forge_rpc.send_tx(new_tx)

    if res.code != 0 or res.hash is None:
        logger.error(res)
        logger.error(f'Fail to consume ticket by mobile {ticket_address}')
    else:
        logger.info(f"Mobile ConsumeTx has been sent by tx: {res.hash}!")
    return res.hash


def build_cosnume_ticket_mobile_tx(origin_tx, signature, ):
    old_multisig = origin_tx.signatures[0]
    new_multisig = forge_protos.Multisig(
            signer=old_multisig.signer,
            pk=old_multisig.pk,
            signature=signature,
            data=old_multisig.data
    )
    new_tx = origin_tx.__deepcopy__()
    forge_rpc.add_multisigs(new_tx, [new_multisig])
    return new_tx


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


APP_CREDENTIALS = {
    'APP_SK': config.APP_SK,
    'APP_PK': config.APP_PK,
    'APP_ADDR': config.APP_ADDR
}


def require_sig_buy_ticket(did, tx, url):
    params = {
        'user_did': did,
        'tx': tx,
        'url': config.SERVER_ADDRESS + url,
        'description': 'Confirm the purchase below.',
        'action': 'responseAuth',
        'workflow': 'buy-ticket',
    }
    response = forge_did.require_sig(**params, **APP_CREDENTIALS)
    logger.debug('did auth response: {}'.format(response))
    return response


def require_sig_poke(did, tx, url):
    params = {
        'user_did': did,
        'tx': tx,
        'url': config.SERVER_ADDRESS + url,
        'description': 'Get some lucky money!',
        'action': 'responseAuth',
        'workflow': 'poke',
    }
    response = forge_did.require_sig(**params, **APP_CREDENTIALS)
    logger.debug('did auth response: {}'.format(response))
    return response


def require_sig_consume(did, tx, url):
    params = {
        'user_did': did,
        'tx': tx,
        'url': config.SERVER_ADDRESS + url,
        'description': 'Confirm to use the ticket.',
        'action': 'responseAuth',
        'workflow': 'use-ticket',
    }
    response = forge_did.require_sig(**params, **APP_CREDENTIALS)
    logger.debug('did auth response: {}'.format(response))
    return response


def require_asset_consume(url, target):
    params = {
        'url': config.SERVER_ADDRESS + url,
        'description': 'Please select a ticket for event.',
        'action': 'responseAuth',
        'workflow': 'use-ticket',
        'target': target,
    }
    return forge_did.require_asset(**params, **APP_CREDENTIALS)
