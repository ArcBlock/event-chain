from forge_sdk import did as forge_did, utils as forge_utils

from forge_symposia.server import env
from forge_symposia.server import utils
from forge_symposia.server.app import forge
from forge_symposia.server.endpoints.lib import auth_component


def get_handler(**args):
    address = args.get('user_did').lstrip(forge_did.PREFIX)
    pk = forge_utils.multibase_b58decode(args.get('user_pk'))
    tx = forge_utils.build_transfer_tx(chain_id=forge.config.chain_id,
                                       to=env.APP_ADDR,
                                       value=2,
                                       address=address,
                                       pk=pk)

    return {
        'request_type': 'signature',
        'workflow': 'payment',
        'tx': tx,
        'description': 'Pay 2 TBA',
    }


def post_handler(**args):
    wallet_res = args.get('wallet_res')
    token = args.get('token')
    tx = wallet_res.get_origin_tx()
    tx.signature = wallet_res.get_signature()

    res = forge.rpc.send_tx(tx)
    if res.hash:
        utils.mark_token_status(token, 'succeed')
        return {'status': 0,
                'hash': res.hash,
                'tx': forge_utils.multibase_b58encode(
                        tx.SerializeToString())}
    else:
        utils.mark_token_status(token, 'error')
        return {'error': f"Oops, error code: {res.code}"}


payment = auth_component.create('payment',
                                get_handler,
                                post_handler)
