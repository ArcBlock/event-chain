import logging

from forge_sdk import did as forge_did, utils as forge_utils

from forge_symposia.server import utils
from forge_symposia.server.app import forge
from forge_symposia.server.endpoints.lib import auth_component


def get_handler(**args):
    tx = forge_utils.build_poke_tx(
            chain_id=forge.config.chain_id,
            address=args.get('user_did').lstrip(forge_did.PREFIX),
            pk=forge_utils.multibase_b58decode(args.get('user_pk')))
    logging.debug(tx)
    return {
        'request_type': 'signature',
        'workflow': 'poke',
        'tx': tx,
        'description': 'Get 25 TBA',
    }


def post_handler(**args):
    wallet_res = args.get('wallet_res')
    token = args.get('token')

    tx = wallet_res.get_origin_tx()
    logging.debug(f'nonce: {tx.nonce}')
    tx.signature = wallet_res.get_signature()

    res = forge.rpc.send_tx(tx)
    if res.hash:
        utils.mark_token_status(token, 'succeed')
        logging.debug(f'hash: {res.hash}')
        return {'status': 0,
                'hash': res.hash,
                'tx': forge_utils.multibase_b58encode(
                        tx.SerializeToString())}
    else:
        utils.mark_token_status(token, 'error')
        logging.error(res)
        return {'error': f"Oops, something is wrong :("}


checkin = auth_component.create('checkin',
                                get_handler=get_handler,
                                post_handler=post_handler)
